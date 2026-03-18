# Distributed File Retrieval System with Replica Consistency Validation

## Overview
This project implements a **distributed file retrieval system** using a client–server architecture with **replicated file servers**. The system ensures that the client receives consistent data by validating file replicas using **SHA-256 hashing** before returning the file.

The architecture includes:

- **Client** – initiates file requests  
- **Server1 (Coordinator)** – handles client requests and verifies replica consistency  
- **Server2 (Replica)** – maintains replicated file storage

Communication between nodes is implemented using **TCP sockets and JSON-based message passing**.


## Installation Steps

Clone the repository:

```bash
git clone https://github.com/yourusername/distributed-file-system.git
cd distributed-file-system
```
Make sure Python 3 is installed.

## Running the System

Open three terminals.

Start Server2 (Replica)

```bash
python3 server2.py
```

Start Server1 (Coordinator)
```bash
python3 server1.py
```

Run Client
```bash
python3 client.py filename.txt
```

## Example Output

Client terminal:
```bash
[CLIENT] File received from SERVER1
[CLIENT] File saved as client/filename.txt
```

Replica mismatch case:
```bash
[CLIENT] Replica mismatch detected
```

Error case:
```bash
[CLIENT ERROR]: File not found on both servers
```

