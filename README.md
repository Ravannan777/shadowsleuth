# ShadowSleuth 🕵️‍♂️

**ShadowSleuth** is a powerful, cross-platform OSINT (Open Source Intelligence) and Reconnaissance utility written in Python. It is designed for security researchers and penetration testers to gather digital footprints, check usernames, analyze phone numbers and emails, and perform network reconnaissance efficiently.

---

## 🚀 Features

* **Phone Number Intelligence:** Extracts country, region, service provider, and timezone details.
* **Username Recon:** Checks popular social media platforms (GitHub, Instagram, Twitter/X, Reddit, TikTok, etc.) for target accounts securely.
* **Email OSINT & Disposable Mail Check:** Analyzes email addresses and detects temporary/fake email domains.
* **IP & Geo-Location Lookup:** Fetches detailed network information, ISP, and geographical coordinates of an IP address.
* **Advanced Quick Port Scanner:** Scans common network ports (FTP, SSH, HTTP, HTTPS, MySQL, etc.) on a target IP or domain.
* **Domain & DNS Information:** Resolves IP addresses and retrieves hostname/alias records.
* **MAC Address Vendor Lookup:** Identifies the manufacturer/vendor of a given MAC address.

---

## 🛠️ Platforms Supported

* **Windows** (10 / 11)
* **Linux** (Ubuntu, Kali Linux, etc.)
* **Termux** (Android)

---

## 📥 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ravannan777/shadowsleuth.git

    cd ShadowSleuth
2. Install Required Python Libraries:
Make sure you have Python installed, then run:
   ```bash
   
   pip install -r requirements.txt

3. Run the Tool:

* Windows / Linux / Termux:
   ```bash
   python shadowsleuth.py

# 📖 Usage Guide*
When you run the script, an interactive menu will appear with the following options:

* Phone Number Intelligence & Social Check - Input a phone number with or without a country code to view its provider and location.

* Username OSINT - Enter a username to find active social media profiles.

* Email OSINT - Verify if an email is legitimate or a temporary/disposable fake mail.

* IP / Geo-Location Lookup - Analyze public or local IP details.

* Advanced Quick Port Scanner - Check open ports on target hosts.

* Domain & DNS Information - Gather DNS records and hostnames.

* MAC Address Vendor Lookup - Find the hardware manufacturer using a MAC address.

**👨‍💻 Developer:**

* Developer: Sreenand K

* Project Type: Cybersecurity Learning & Reconnaissance Utility




# ⚠️ Disclaimer
This tool is developed for educational purposes and authorized security auditing only. The author is not responsible for any misuse or illegal activities conducted using this software.

```text 
========================================================================================
                          SHADOWSLEUTH v1.5.0 - DETAILED FLOWCHART
========================================================================================

 [ User / Security Researcher ]
        │
        ▼
 ┌────────────────────────────────────────────────────────────────────────────────────┐
 │                                 shadowsleuth.py                                    │
 │                       (Cross-Platform OSINT & Recon Engine)                        │
 └────────────────────────────────────────────────────────────────────────────────────┘
        │
        ├─► [1] Phone Intelligence ──► Parse Number ──► Get Country / Carrier / Timezone
        │
        ├─► [2] Username Recon ────► Target Username ──► Bypass Soft 404 ──► Social Profiles
        │                                                                   ├─ GitHub
        │                                                                   ├─ Instagram
        │                                                                   ├─ Twitter (X)
        │                                                                   └─ ... (Others)
        │
        ├─► [3] Email OSINT ───────► Split Email ──► Check Fake Domain (Disposable Check)
        │                                          └─ Verify Public Endpoints (Gravatar)
        │
        ├─► [4] IP Geo-Location ───► Target IP/Input ──► Query API ──► ISP / City / Coords
        │
        ├─► [5] Port Scanner ──────► Resolve Domain ──► TCP Socket ──► Open/Closed Ports
        │                                                                   ├─ 21 (FTP)
        │                                                                   ├─ 22 (SSH)
        │                                                                   ├─ 80 (HTTP)
        │                                                                   └─ 443 (HTTPS)
        │
        ├─► [6] Domain Recon ──────► Target Domain ──► Socket DNS ──► IP & Host Resolution
        │
        └─► [7] MAC Address Lookup ─► MAC Input ─────► Vendor API ──► Hardware Manufacturer

========================================================================================
