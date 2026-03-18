# Distributed-File-Retrieval-System-with-Replica-Consistency-Validation
A Python distributed file retrieval system with two replicated servers. The coordinator server verifies replica consistency using SHA-256 hashing before sending files to the client via TCP socket communication.

Installation

Clone the repository:
git clone https://github.com/yourusername/distributed-file-system.git
cd distributed-file-system

Make sure Python 3 is installed.

Running the System

Open three terminals.

Start Server2 (Replica)
python3 server2.py

Start Server1 (Coordinator)
python3 server1.py

Run Client
python3 client.py filename.txt

Example Output

Client terminal:
[CLIENT] File received from SERVER1
[CLIENT] File saved as client/filename.txt

Replica mismatch case:
[CLIENT] Replica mismatch detected

Error case:
[CLIENT ERROR]: File not found on both servers

Concepts Demonstrated
-Client–Server architecture
-Coordinator-based distributed systems
-Replica validation
-Message passing communication
-Failure detection through timeouts

Author - Kumar Shubham Anand

License - This project is for educational purposes.


