# 🔍 NmapScan Pro | Automated Nmap Scanner

[![Python 3.x](https://img.shields.io/badge/Python-3.x-%233776AB?logo=python)](https://python.org)
[![Nmap Required](https://img.shields.io/badge/Nmap-Required-%23FF6600?logo=gnu)](https://nmap.org)
[![License MIT](https://img.shields.io/badge/License-MIT-%23green)](LICENSE)
[![Version 1.0](https://img.shields.io/badge/Version-1.0-%23blueviolet)](CHANGELOG.md)

**Automate your network scanning** with this powerful Nmap wrapper that simplifies complex scans into single commands.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| ⚡ **One-Click Scans** | Predefined profiles for quick/full/udp scans |
| 🎯 **Smart Targeting** | Supports IPs, ranges, and hostnames |
| 📂 **Organized Output** | Auto-saves in multiple formats (XML/JSON/TXT) |
| ⏱ **Time-Saving** | Parallel scanning for multiple targets |
| 🔐 **Security Focused** | Clean output sanitization |

---

## 🛠 Installation

```bash
# Clone repository
git clone https://github.com/Endenss/NmapScan-Pro.git && cd NmapScan-Pro

# Install dependencies
pip install -r requirements.txt

# Verify Nmap is installed
nmap --version
🖥 Usage Examples
Basic Scan
bash
Copy
python nmapscan.py 192.168.1.1 --quick
Full Network Audit
bash
Copy
python nmapscan.py 10.0.0.0/24 --full --output network_audit
Custom Scan
bash
Copy
python nmapscan.py example.com -c "-sS -T4 --top-ports 100"
📂 Output Structure
text
Copy
results/
├── scans/
│   ├── 2023-11-20_14-30_192.168.1.1_quick.nmap
│   ├── 2023-11-20_14-30_192.168.1.1_quick.json
│   └── 2023-11-20_14-30_192.168.1.1_quick.xml
└── logs/
    └── scan_history.log
⚙️ Configuration
Edit config/profiles.json to customize scan profiles:

json
Copy
{
  "quick": "-T4 -F --max-retries 1",
  "full": "-A -T4 -v -Pn -p-",
  "udp": "-sU -T4 --top-ports 50"
}
📜 License
MIT License © 2023 Endenss

💡 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/AmazingFeature)

Open Pull Request

Open in GitHub
