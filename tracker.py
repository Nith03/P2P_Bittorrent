import socket
import threading
import json

peers = {}  # Dictionary to store peers for each file

def handle_tracker_connection(conn):
    try:
        # Receive data from the peer
        data = conn.recv(1024).decode()
        request = json.loads(data)

        # Log the received request
        print(f"Received request: {request}")

        action = request["action"]
        file_name = request["file_name"]

        if action == "register":
            peer_address = request["peer_address"]
            if file_name not in peers:
                peers[file_name] = []
            if peer_address not in peers[file_name]:
                peers[file_name].append(peer_address)
            response = {"peers": peers[file_name]}
        elif action == "get_peers":
            response = {"peers": peers.get(file_name, [])}
        else:
            response = {"error": "Unknown action"}

        # Send the response back to the peer
        conn.send(json.dumps(response).encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def tracker_server(host="127.0.0.1", port=6881):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Tracker is running on {host}:{port}...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_tracker_connection, args=(conn,)).start()

if __name__ == "__main__":
    tracker_server()
