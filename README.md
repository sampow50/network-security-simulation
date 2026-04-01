# Network Vulnerability & Exploit Simulation 🔐

This project is an educational cybersecurity simulation that demonstrates how attackers identify vulnerable systems and exploit weak credentials across a network.

## 🚀 Features
- Scans IP addresses for open SSH (port 22) and Telnet (port 23) services
- Tests common username/password combinations against detected services
- Identifies weak or compromised accounts
- Simulates propagation behavior in a controlled environment

## 🛠️ Technologies Used
- Python
- socket (network scanning)
- paramiko (SSH connections)
- telnetlib (Telnet connections)

## ⚙️ How It Works
1. The program scans a range of IP addresses for open ports
2. It attempts login using a list of common credentials
3. Successful logins are recorded for analysis
4. The simulation demonstrates how vulnerabilities can be exploited

## 📚 What I Learned
- How network services like SSH and Telnet operate
- Common vulnerabilities in weak authentication systems
- How attackers automate credential-based attacks
- Importance of secure password practices and system hardening

## ⚠️ Disclaimer
This project was developed for educational purposes in a controlled environment. It is intended to demonstrate cybersecurity concepts and should not be used on unauthorized systems.
