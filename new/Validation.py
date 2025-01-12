import hashlib

def calculate_file_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    hash_func = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):  # Read the file in 8 KB chunks
                hash_func.update(chunk)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    return hash_func.hexdigest()

def validate_files(original_file, reconstructed_file):
    """Validates if the original file and reconstructed file are identical."""
    print("Calculating hash for the original file...")
    original_hash = calculate_file_hash(original_file)

    print("Calculating hash for the reconstructed file...")
    reconstructed_hash = calculate_file_hash(reconstructed_file)

    if original_hash is None or reconstructed_hash is None:
        print("Validation failed: One or both files could not be read.")
        return False

    if original_hash == reconstructed_hash:
        print("Validation successful: The files are identical.")
        return True
    else:
        print("Validation failed: The files are different.")
        return False

if __name__ == "__main__":
    # Specify the paths to the original and reconstructed files
    original_file = r"F:\acnn\P2P_Bittorrent\new\CS1 S11.txt"  # Path to the original file
    reconstructed_file = r"F:\acnn\P2P_Bittorrent\new\reconstructed_file.txt"  # Path to the reconstructed file

    # Perform validation
    validate_files(original_file, reconstructed_file)
