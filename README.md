# Distributed File Retrieval System with Replica Consistency Validation

## Overview
This project implements a **distributed file retrieval system** using a client–server architecture with **replicated file servers**. The system ensures that the client receives consistent data by validating file replicas using **SHA-256 hashing** before returning the file.

The architecture includes:

- **Client** – initiates file requests  
- **Server1 (Coordinator)** – handles client requests and verifies replica consistency  
- **Server2 (Replica)** – maintains replicated file storage

Communication between nodes is implemented using **TCP sockets and JSON-based message passing**.


---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/distributed-file-system.git
cd distributed-file-system
```

zsdv
