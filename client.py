import socket
import json

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(("127.0.0.1", 6881))
    request = {
        "action": "register",
        "file_name": "abc.txt",
        "peer_address": "127.0.0.1:6882"
    }
    client.send(json.dumps(request).encode())
    response = client.recv(1024).decode()
    print("Response from tracker:", response)