# System Sentinel v1.0

A lightweight system monitoring security tool written in Python. It audits running processes for high CPU usage and monitors network interfaces for suspicious listening ports.

##  Features
- **Process Monitoring**: Scans all active processes and alerts if a process exceeds a defined CPU threshold.
- **Network Auditing**: Lists all active listening ports (IPv4/IPv6) and identifies potentially malicious activity (e.g., port 4444).
- **Dual-Logger System**: Separates process logs and network logs into independent files (`processes.log` and `network.log`) for better data organization and auditing.
- **Graceful Shutdown**: Handles user interruptions (Ctrl+C) clean and safely.

##  Tech Stack
- **Language**: Python 3.x
- **Library**: `psutil` (for cross-platform system information)

##  Installation & Usage
1. **Clone the repository**
2. **Install psutil (pip install psutil)**
3. **Run (python sentinel.py)**
