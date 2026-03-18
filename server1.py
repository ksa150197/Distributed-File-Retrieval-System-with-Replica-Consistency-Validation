import socket
import json
import struct
import os
import hashlib
import base64

SERVER1_PORT = 5001
SERVER2_PORT = 5002
SERVER2_HOST = "127.0.0.1"
STORAGE_DIR = "server1/storage"
TIMEOUT = 5


# ----------------------------
# Utility: Send JSON message
# ----------------------------
def send_message(sock, message_dict):
    data = json.dumps(message_dict).encode('utf-8')
    length = struct.pack('!I', len(data))
    sock.sendall(length + data)


# ----------------------------
# Utility: Receive JSON message
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
# Query SERVER2 for metadata
# ----------------------------
def query_server2(pathname):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            sock.connect((SERVER2_HOST, SERVER2_PORT))

            send_message(sock, {
                "type": "FILE_METADATA_REQUEST",
                "pathname": pathname
            })

            response = receive_message(sock)
            return response

    except socket.timeout:
        print("[SERVER1] SERVER2 Timeout.")
        return {"type": "TIMEOUT"}

    except Exception as e:
        print("[SERVER1] SERVER2 Error:", e)
        return {"type": "ERROR"}


# ----------------------------
# Handle Client Request
# ----------------------------
def handle_client(conn):
    request = receive_message(conn)
    if request["type"] != "FILE_REQUEST":
        return

    pathname = request["pathname"]
    local_path = os.path.join(STORAGE_DIR, pathname)

    s1_exists = os.path.exists(local_path)
    s1_hash = None

    if s1_exists:
        s1_hash = compute_hash(local_path)

    # Query SERVER2
    s2_response = query_server2(pathname)

    # ---------------- Decision Logic ----------------
    if s2_response["type"] == "TIMEOUT":
        if s1_exists:
            send_file(conn, pathname, local_path)
        else:
            send_error(conn, "File not found and SERVER2 unreachable.")
        return

    if s2_response.get("exists") == True:
        s2_hash = s2_response["hash"]

        if s1_exists:
            if s1_hash == s2_hash:
                send_file(conn, pathname, local_path)
            else:
                send_conflict(conn, pathname, local_path)
        else:
            # Fetch file from SERVER2
            send_message(conn, {
                "type": "INFO",
                "message": "File exists only on SERVER2"
            })

    else:
        if s1_exists:
            send_file(conn, pathname, local_path)
        else:
            send_error(conn, "File not found on both servers.")


# ----------------------------
# Send File
# ----------------------------
def send_file(conn, filename, filepath):
    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')

    send_message(conn, {
        "type": "FILE_CONTENT",
        "filename": filename,
        "content": encoded
    })


# ----------------------------
# Send Conflict
# ----------------------------
def send_conflict(conn, filename, filepath):
    with open(filepath, "rb") as f:
        file1 = base64.b64encode(f.read()).decode('utf-8')

    send_message(conn, {
        "type": "FILE_CONFLICT",
        "filename": filename,
        "server1_file": file1,
        "message": "Replica mismatch detected."
    })


# ----------------------------
# Send Error
# ----------------------------
def send_error(conn, message):
    send_message(conn, {
        "type": "ERROR",
        "message": message
    })


# ----------------------------
# Main Server Loop
# ----------------------------
def main():
    os.makedirs(STORAGE_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", SERVER1_PORT))
        server.listen()

        print(f"[SERVER1] Listening on port {SERVER1_PORT}")

        while True:
            conn, addr = server.accept()
            print("[SERVER1] Connected by", addr)
            handle_client(conn)
            conn.close()


if __name__ == "__main__":
    main()