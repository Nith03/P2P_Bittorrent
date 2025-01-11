import socket
import threading

class TrackerServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.files = {}  # {file_name: {peer_address, ...}}
    
    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            command, *args = data.split('|')

            if command == 'REGISTER':
                file_name, peer_address = args
                if file_name not in self.files:
                    self.files[file_name] = set()
                self.files[file_name].add(peer_address)
                client_socket.sendall(b"ACK_REGISTER")

            elif command == 'DISCOVER':
                file_name = args[0]
                peers = list(self.files.get(file_name, []))
                client_socket.sendall('|'.join(peers).encode())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen()
            print(f"Tracker server running on {self.host}:{self.port}")
            
            while True:
                client_socket, _ = server.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    TrackerServer().start()
