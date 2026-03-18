# Distributed File Retrieval System with Replica Consistency Validation

## Overview
This project implements a **distributed file retrieval system** using a client–server architecture with **replicated file servers**. The system ensures that the client receives consistent data by validating file replicas using **SHA-256 hashing** before returning the file.

The architecture includes:

- **Client** – initiates file requests  
- **Server1 (Coordinator)** – handles client requests and verifies replica consistency  
- **Server2 (Replica)** – maintains replicated file storage

Communication between nodes is implemented using **TCP sockets and JSON-based message passing**.

---

## System Architecture

![Architecture Diagram](distributed_system_architecture.png)

### Communication Flow

1. Client sends a file request to Server1.
2. Server1 checks its local storage.
3. Server1 requests metadata from Server2.
4. Server2 returns file metadata including SHA-256 hash.
5. Server1 compares hashes to verify replica consistency.
6. Server1 sends the appropriate response to the client.

---

## Key Features

- Distributed client-server architecture
- Replica-based file storage
- SHA-256 hash-based consistency validation
- TCP socket communication
- JSON-based structured messaging
- Failure detection using timeouts

---

## Technologies Used

| Technology | Purpose |
|-----------|--------|
| Python | Implementation language |
| TCP Sockets | Network communication |
| JSON | Structured message exchange |
| SHA-256 (hashlib) | Replica consistency validation |
| Base64 | Binary file transmission |

---

## Project Structure
