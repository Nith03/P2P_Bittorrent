import socket
import threading
import json
import hashlib
import os

CHUNK_SIZE = 512 * 1024  # 512 KB

def generate_chunks(file_path):
    """Generate chunks from a file."""
    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            yield chunk

def compute_sha1(chunk):
    """Compute SHA-1 hash of a chunk."""
    return hashlib.sha1(chunk).hexdigest()

def register_with_tracker(tracker_address, file_name, peer_address):
    """Register the peer with the tracker."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tracker_socket:
        tracker_socket.connect(tracker_address)
        request = {
            "action": "register",
            "file_name": file_name,
            "peer_address": peer_address,
        }
        tracker_socket.send(json.dumps(request).encode())
        response = tracker_socket.recv(1024).decode()
        return json.loads(response)

def handle_peer_connection(peer_socket, file_chunks):
    """Handle incoming requests from other peers."""
    try:
        data = peer_socket.recv(1024).decode()
        request = json.loads(data)
        action = request.get('action')
        chunk_index = request.get('chunk_index')

        if action == "request_chunk" and 0 <= chunk_index < len(file_chunks):
            response = {"chunk_data": file_chunks[chunk_index].decode('latin1')}
            peer_socket.send(json.dumps(response).encode())
    except Exception as e:
        print(f"Error handling peer connection: {e}")
    finally:
        peer_socket.close()

def peer_server(file_chunks, port):
    """Start the peer server to share file chunks."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Peer is listening on port {port}...")

    while True:
        peer_socket, addr = server.accept()
        threading.Thread(target=handle_peer_connection, args=(peer_socket, file_chunks)).start()

if __name__ == "__main__":
    # File information
    file_path = r"C:\Users\Admin\Desktop\chunkeyy.txt"  # Replace with the actual file path
    file_name = os.path.basename(file_path)
    chunks = list(generate_chunks(file_path))

    # Tracker and Peer settings
    tracker_address = ("127.0.0.1", 6881)  # Tracker's address
    peer_port = 6882  # Port on which this peer will run
    peer_address = f"127.0.0.1:{peer_port}"

    # Register with Tracker
    tracker_response = register_with_tracker(tracker_address, file_name, peer_address)
    print(f"Registered with tracker. Active peers: {tracker_response.get('peers', [])}")

    # Start Peer Server
    threading.Thread(target=peer_server, args=(chunks, peer_port)).start()