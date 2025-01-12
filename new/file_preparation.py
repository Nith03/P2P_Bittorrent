import os
import hashlib

# File Chunking and Hashing
def split_file(file_path, chunk_size=256 * 1024):
    """Splits the file into chunks and generates their SHA-256 hashes."""
    chunks = []
    hashes = []

    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            chunks.append(chunk)
            hashes.append(hashlib.sha256(chunk).hexdigest())

    return chunks, hashes

def save_chunks(chunks, output_dir="chunks"):
    """Saves chunks to a directory."""
    os.makedirs(output_dir, exist_ok=True)
    for i, chunk in enumerate(chunks):
        with open(os.path.join(output_dir, f"chunk_{i}"), 'wb') as f:
            f.write(chunk)

def save_hashes(hashes, output_file="hashes.txt"):
    """Saves the chunk hashes to a file."""
    with open(output_file, "w") as file:
        for hash_value in hashes:
            file.write(hash_value + "\n")

if __name__ == "__main__":
    file_path = r"F:\acnn\P2P_Bittorrent\new\CS1 S11.txt"  # Replace with your file path

    # Step 1: Split the file into chunks and compute hashes
    chunks, hashes = split_file(file_path)

    # Step 2: Save chunks to a directory
    save_chunks(chunks)

    # Step 3: Save hashes to a file
    save_hashes(hashes)

    # Step 4: Output hashes for integrity verification
    print("File chunks created and hashes are:")
    for i, h in enumerate(hashes):
        print(f"Chunk {i}: {h}")
