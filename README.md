# System Sentinel v1.0

A lightweight system monitoring security tool written in Python. It audits running processes for high CPU usage and monitors network interfaces for suspicious listening ports.

##  Features
- **Integrity Shield (SHA-256)**: Upon startup, the tool calculates a cryptographic baseline hash of its own source code. It continuously monitors itself to detect any unauthorized modifications in real-time.**
- **Process Monitoring**: Scans all active processes and alerts if a process exceeds a defined CPU threshold.
- **Network Auditing**: Lists all active listening ports (IPv4/IPv6) and identifies potentially malicious activity (e.g., port 4444).
- **Triple-Logger System**: Separates process logs, network logs and security logs into independent files (`processes.log`, `network.log`, `security.log`) for better data organization and auditing.
- **Graceful Shutdown**: Handles user interruptions (Ctrl+C) clean and safely.

##  Tech Stack
- **Language**: Python 3.x
- **Library**: `psutil` (for cross-platform system information), `hashlib` (Cryptography)

##  Installation & Usage
1. **Clone the repository**
2. **Install psutil (pip install psutil)**
3. **Run (python sentinel.py)**
