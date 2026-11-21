# 🛡️ CyberTools

**Python-Based Cybersecurity & Network Analysis Toolkit**

## About

CyberTools is a personal cybersecurity project developed in Python, focused on network analysis, device discovery, and IP address management.

The main goal is to improve my programming, networking, Linux, and cybersecurity skills through practical projects and hands-on experimentation.

This project is primarily developed and tested on **Kali Linux**.

## Features

Installation & Usage

1. Requirements

Python 3.x

Linux (Kali Linux recommended)

Git (optional)

No external Python packages are required.

2. Clone the Repository

Open a Linux terminal and run:

git clone https://github.com/sebas/CyberTools.git
cd CyberTools

Alternatively, download the repository as a ZIP file and extract it.

3. Run the IP Manager

Navigate to the directory containing the IP Manager and run:

python3 (file you want to run)

5. Example — IP Manager

Choose an option: 1
Enter the IP address to add: 192.168.1.222
Enter the device name: Lenovo

IP 192.168.1.122 added successfully.

Choose an option: 3

Registered IP addresses:
Device: Lenovo | IP: 192.168.1.222

### IP Manager
- Add IP addresses with custom device names.
- Remove saved IP addresses.
- List registered devices.
- Search for devices by name.
- Validate IPv4 addresses.
- Prevent duplicate IP entries.
- Save information locally in a text file.

### Network Discovery
- Identify the local IPv4 network.
- Discover devices responding to ICMP ping requests.
- Compare discovered IPs with saved entries.
- Display device connectivity status.

###  TCP Port Scanner
- Scan TCP ports.
- Identify open ports.
- Display associated service information when available.
- Track scanning progress.

## Technologies

- **Language:** Python 3
- **Operating System:** Kali Linux
- **Modules:** `os`, `ipaddress`, `subprocess`, `socket`
- **Tools:** Linux terminal, Git and GitHub

## Project Structure

The project includes tools for IP management, network discovery, and TCP port analysis. Its structure may change as development continues.

## Project Goals

- Strengthen Python programming skills.
- Understand TCP/IP networking.
- Learn network analysis techniques.
- Develop practical cybersecurity tools.
- Improve Linux and command-line skills.
- Build a technical portfolio.

## Development Status

**Work in Progress**

CyberTools is an educational project under active development. New features, improvements, and code restructuring are planned.

## Disclaimer

CyberTools is intended for educational purposes and authorized network testing only.

Use these tools exclusively on networks and systems you own or have explicit permission to test.

## Author

Developed as a personal learning project focused on programming, networking, and cybersecurity.
