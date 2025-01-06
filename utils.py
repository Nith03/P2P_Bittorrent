import hashlib

def chunk_file(file_path, chunk_size=256 * 1024):
    """Splits a file into fixed-size chunks."""
    chunks = []
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            chunks.append(chunk)
    return chunks

def generate_hashes(chunks):
    """Generates a SHA-256 hash for each chunk."""
    return [hashlib.sha256(chunk).hexdigest() for chunk in chunks]

# Test the function
file_path = r"C:\Users\Admin\Desktop\chunkeyy.txt"  # Replace with your file path
chunks = chunk_file(file_path)
chunk_hashes = generate_hashes(chunks)

print("File split into chunks and hashes generated.")