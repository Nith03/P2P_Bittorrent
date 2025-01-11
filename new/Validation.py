import hashlib

def calculate_file_hash(file_path):
    hash_obj = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

original_hash = calculate_file_hash("file.txt")
reconstructed_hash = calculate_file_hash("reconstructed_file.txt")

if original_hash == reconstructed_hash:
    print("File integrity verified: The files match!")
else:
    print("File integrity failed: The files do not match.")
