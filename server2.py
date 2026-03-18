import socket
import json
import struct
import os
import hashlib
import base64

SERVER2_PORT = 5002
STORAGE_DIR = "server2/storage"


# ----------------------------
# Send JSON Message
# ----------------------------
def send_message(sock, message_dict):
    data = json.dumps(message_dict).encode('utf-8')
    length = struct.pack('!I', len(data))
    sock.sendall(length + data)


# ----------------------------
# Receive JSON Message
# ----------------------------
def receive_message(sock):
    raw_length = sock.recv(4)
    if not raw_length:
        return None
    message_length = struct.unpack('!I', raw_length)[0]
    data = b''
    while len(data) < message_length:
        chunk = sock.recv(message_length - len(data))
        if not chunk:
            break
        data += chunk
    return json.loads(data.decode('utf-8'))


# ----------------------------
# Compute SHA256 Hash
# ----------------------------
def compute_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()


# ----------------------------
# Handle Incoming Request
# ----------------------------
def handle_request(conn):
    request = receive_message(conn)

    if not request:
        return

    if request["type"] == "FILE_METADATA_REQUEST":
        pathname = request["pathname"]
        file_path = os.path.join(STORAGE_DIR, pathname)

        if os.path.exists(file_path):
            file_hash = compute_hash(file_path)
            file_size = os.path.getsize(file_path)

            response = {
                "type": "FILE_METADATA_RESPONSE",
                "exists": True,
                "hash": file_hash,
                "size": file_size
            }
        else:
            response = {
                "type": "FILE_METADATA_RESPONSE",
                "exists": False
            }

        send_message(conn, response)

    elif request["type"] == "FILE_CONTENT_REQUEST":
        pathname = request["pathname"]
        file_path = os.path.join(STORAGE_DIR, pathname)

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')

            response = {
                "type": "FILE_CONTENT",
                "filename": pathname,
                "content": encoded
            }
        else:
            response = {
                "type": "ERROR",
                "message": "File not found"
            }

        send_message(conn, response)


# ----------------------------
# Main Server Loop
# ----------------------------
def main():
    os.makedirs(STORAGE_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", SERVER2_PORT))
        server.listen()

        print(f"[SERVER2] Listening on port {SERVER2_PORT}")

        while True:
            conn, addr = server.accept()
            print("[SERVER2] Connected by", addr)
            handle_request(conn)
            conn.close()


if __name__ == "__main__":
    main()