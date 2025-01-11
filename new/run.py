import subprocess
import threading

def start_tracker():
    subprocess.run(["python", "tracker_server.py"])

def start_peer():
    subprocess.run(["python", "peer_node.py"])

if __name__ == "__main__":
    # Start Tracker
    threading.Thread(target=start_tracker).start()

    # Start Peer
    threading.Thread(target=start_peer).start()
