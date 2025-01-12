import os
import socket
import hashlib
import threading

def calculate_hash(data):
    """Calculates the SHA-256 hash of the given data."""
    return hashlib.sha256(data).hexdigest()

def send_chunk(peer_address, chunk_id, chunk_dir="chunks"):
    """Handles sending a chunk to a requesting peer."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(peer_address)
            chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_id}")

            if not os.path.exists(chunk_path):
                sock.sendall(b"ERROR|Chunk not found")
                return

            with open(chunk_path, 'rb') as chunk_file:
                data = chunk_file.read()
                sock.sendall(b"CHUNK|" + data)
    except Exception as e:
        print(f"Error sending chunk: {e}")

def handle_peer_connection(client_socket, chunk_dir="chunks"):
    """Handles incoming requests from other peers."""
    try:
        data = client_socket.recv(1024).decode()
        command, *args = data.split('|')

        if command == "REQUEST":
            chunk_id = args[0]
            chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_id}")
            print(f"Peer received request for chunk: {chunk_id}")

            if os.path.exists(chunk_path):
                with open(chunk_path, 'rb') as chunk_file:
                    chunk_data = chunk_file.read()
                    client_socket.sendall(chunk_data)
            else:
                print(f"Chunk not found: {chunk_path}")
                client_socket.sendall(b"ERROR|Chunk not found")
    except Exception as e:
        print(f"Error handling peer connection: {e}")
    finally:
        client_socket.close()


def peer_server(host="0.0.0.0", port=6000, chunk_dir="chunks"):
    """Starts a server to listen for incoming peer requests."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"Peer server running on {host}:{port}")

        while True:
            client_socket, _ = server.accept()
            threading.Thread(target=handle_peer_connection, args=(client_socket, chunk_dir)).start()

def request_chunk(peer_address, chunk_id):
    """Requests a chunk from another peer."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(peer_address)
            sock.sendall(f"REQUEST|{chunk_id}".encode())
            data = sock.recv(1024 * 256)  # Adjust buffer size as needed
            return data
    except Exception as e:
        print(f"Error requesting chunk: {e}")
        return None

def download_file(tracker_address, file_name, output_file, chunk_count, expected_hashes):
    """Handles downloading the file by requesting chunks from peers."""
    try:
        # Step 1: Discover peers
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(tracker_address)
            sock.sendall(f"DISCOVER|{file_name}".encode())
            response = sock.recv(1024).decode()
            peers = response.split('|')

        if not peers or peers == ['']:
            print("No peers available for the requested file.")
            return

        # Step 2: Download chunks
        chunks = [None] * chunk_count
        for chunk_id in range(chunk_count):
            for peer in peers:
                peer_ip, peer_port = peer.split(':')
                peer_address = (peer_ip, int(peer_port))
                chunk_data = request_chunk(peer_address, chunk_id)

                # Verify the hash of the downloaded chunk
                if chunk_data and hashlib.sha256(chunk_data).hexdigest() == expected_hashes[chunk_id]:
                    chunks[chunk_id] = chunk_data
                    break
                else:
                    print(f"Chunk {chunk_id} failed hash verification.")
            else:
                print(f"Chunk {chunk_id} could not be downloaded.")

        # Step 3: Reconstruct the file
        if None in chunks:
            print("File reconstruction failed: Missing or corrupted chunks.")
            return

        with open(output_file, 'wb') as file:
            for chunk in chunks:
                file.write(chunk)

        print(f"File {output_file} successfully reconstructed.")
    except Exception as e:
        print(f"Error downloading file: {e}")


def load_hashes(hash_file):
    """Load the expected chunk hashes from a file."""
    try:
        with open(hash_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Hash file not found: {hash_file}")
        return None

if __name__ == "__main__":
    # Start peer server
    threading.Thread(target=peer_server, args=("0.0.0.0", 6000)).start()

    # Register the file with the tracker
    tracker_address = ("127.0.0.1", 5000)
    file_name = "file.txt"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(tracker_address)
            sock.sendall(f"REGISTER|{file_name}|127.0.0.1:6000".encode())
            response = sock.recv(1024).decode()
            print(response)  # Expect "ACK_REGISTER"
        except Exception as e:
            print(f"Error registering with tracker: {e}")

    # Load expected hashes
    expected_hashes = load_hashes("hashes.txt")
    if not expected_hashes:
        print("Failed to load hashes. Exiting.")
        exit(1)

    # Attempt to download the file
    chunk_count = len(expected_hashes)
    download_file(tracker_address, file_name, "reconstructed_file.txt", chunk_count, expected_hashes)

