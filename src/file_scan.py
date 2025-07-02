import json
import os

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


def scan_files(root_dir):
    file_data = []
    # Directories to exclude to avoid permission issues
    exclude_dirs = [".venv", "__pycache__", ".git"]
    
    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Check if file is readable
                if os.access(file_path, os.R_OK):
                    file_info = {
                        "name": file,
                        "path": file_path,
                        "size": os.path.getsize(file_path),
                        "extension": os.path.splitext(file)[1].lower(),
                        "last_modified": os.path.getmtime(file_path)
                    }
                    file_data.append(file_info)
                else:
                    print(f"Skipping {file_path}: File not readable")
            except (PermissionError, FileNotFoundError, OSError) as e:
                print(f"Error accessing {file_path}: {e}")
                continue
    return file_data

def create_vector_index(file_data, index_path="file_index.faiss", metadata_path="file_metadata.json"):
    # Load embedding model
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Create text for embedding (combine name and path for better search)
    texts = [f"{f['name']} {f['path']}" for f in file_data]
    embeddings = embedder.encode(texts, show_progress_bar=True)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, index_path)
    
    # Save metadata
    with open(metadata_path, "w") as f:
        json.dump(file_data, f)
    
    print(f"Vector index created at {index_path}, metadata saved at {metadata_path}")

def query_file_path(query, top_k=5, index_path="file_index.faiss", metadata_path="file_metadata.json"):
    # Load embedding model and FAISS index
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(index_path)
    with open(metadata_path, "r") as f:
        file_metadata = json.load(f)
    
    # Encode query and search
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    
    # Return matching files
    results = [file_metadata[i] for i in indices[0]]
    return results

if __name__ == "__main__":
    """# Set root directory (using raw string to avoid escape issues)
    root_directory = r"E:\Projects"
    
    # Step 1: Scan files
    files = scan_files(root_directory)
    
    # Step 2: Create vector index
    create_vector_index(files)
    
    # Step 3: Save metadata to CSV (optional, for reference)
    df = pd.DataFrame(files)
    df.to_csv("file_index.csv", index=False)
    print("File index CSV created at file_index.csv")
    """
    # Step 4: Example query
    query = "path for gh archive file"
    results = query_file_path(query, top_k=1)
    for result in results:
        print(f"File: {result['name']}, Path: {result['path']}")