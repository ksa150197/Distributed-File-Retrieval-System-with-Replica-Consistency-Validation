import socket
import json
import struct
import base64
import sys
import os

SERVER1_HOST = "127.0.0.1"
SERVER1_PORT = 5001

DOWNLOAD_DIR = "client"


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
# Save File
# ----------------------------
def save_file(filename, encoded_data):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    filepath = os.path.join(DOWNLOAD_DIR, filename)

    data = base64.b64decode(encoded_data)

    with open(filepath, "wb") as f:
        f.write(data)

    print(f"[CLIENT] File saved as {filepath}")


# ----------------------------
# Main Client Logic
# ----------------------------
def main():

    if len(sys.argv) != 2:
        print("Usage: python3 client.py <filename>")
        return

    filename = sys.argv[1]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.connect((SERVER1_HOST, SERVER1_PORT))

        request = {
            "type": "FILE_REQUEST",
            "pathname": filename
        }

        send_message(sock, request)

        response = receive_message(sock)

        if response["type"] == "FILE_CONTENT":

            print("[CLIENT] File received from SERVER1")

            save_file(response["filename"], response["content"])


        elif response["type"] == "FILE_CONFLICT":

            print("[CLIENT] Replica mismatch detected")

            save_file("server1_copy_" + filename,
                      response["server1_copy"])


        elif response["type"] == "ERROR":

            print("[CLIENT ERROR]:", response["message"])


        elif response["type"] == "INFO":

            print("[CLIENT INFO]:", response["message"])


        else:

            print("[CLIENT] Unknown response")


if __name__ == "__main__":
    main()