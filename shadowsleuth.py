import streamlit as st
import socket
import json
import urllib.request
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

# Page Configuration
st.set_page_config(
    page_title="ShadowSleuth | Military-Grade OSINT", 
    page_icon="🕵️‍♂️", 
    layout="wide"
)

# ---------------------------------------------------------
# CYBERPUNK / MILITARY-GRADE TACTICAL CSS STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;600&display=swap');

    .stApp {
        background-color: #05050a;
        color: #00ff66;
        font-family: 'Share Tech Mono', monospace;
    }

    [data-testid="stSidebar"] {
        background-color: #080c14;
        border-right: 1px solid #1f293d;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #00f0ff !important;
        font-weight: bold;
    }

    h1, h2, h3 {
        font-family: 'Share Tech Mono', monospace;
        color: #00f0ff !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }

    .stTextInput input {
        background-color: #0d111a !important;
        color: #00ff66 !important;
        border: 1px solid #1f3a2e !important;
        border-radius: 4px;
        font-family: 'Share Tech Mono', monospace;
    }
    .stTextInput input:focus {
        border-color: #00ff66 !important;
        box-shadow: 0 0 8px rgba(0, 255, 102, 0.4);
    }

    .stButton button {
        background: linear-gradient(135deg, #0b1f14 0%, #0d2b1d 100%);
        color: #00ff66;
        border: 1px solid #00ff66;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: #00ff66;
        color: #05050a;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.6);
    }

    .stSuccess {
        background-color: rgba(0, 255, 102, 0.1) !important;
        border: 1px solid #00ff66 !important;
        color: #00ff66 !important;
    }
    .stError {
        background-color: rgba(255, 0, 85, 0.1) !important;
        border: 1px solid #ff0055 !important;
        color: #ff0055 !important;
    }
    .stWarning {
        background-color: rgba(255, 170, 0, 0.1) !important;
        border: 1px solid #ffaa00 !important;
        color: #ffaa00 !important;
    }

    hr {
        border-color: #1f293d;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1>[+] SHADOWSLEUTH // TACTICAL OSINT ENGINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00f0ff; letter-spacing: 2px;'>DEVELOPER: SREENAND K | STATUS: SECURE / ACTIVE | EDITION: v1.5.0 PRO</p>", unsafe_allow_html=True)
st.divider()

# Sidebar Navigation
menu = st.sidebar.selectbox("⚡ SELECT RECON MODULE", [
    "Phone Intelligence",
    "Username Recon",
    "Email OSINT",
    "IP / Geo-Location",
    "Port Scanner",
    "Domain & DNS",
    "MAC Vendor Lookup"
])

# 1. Phone Intelligence
if menu == "Phone Intelligence":
    st.subheader("📱 Phone Number Intelligence & Social Vector")
    number_str = st.text_input("Enter target phone number (e.g., +918289804072):", "+91")
    
    if st.button("EXECUTE PHONE SCAN"):
        if number_str:
            if not number_str.startswith("+"):
                number_str = "+91" + number_str
            try:
                parsed_number = phonenumbers.parse(number_str)
                if phonenumbers.is_valid_number(parsed_number):
                    formatted_num = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
                    st.success("[+] Target Verified: Valid Phone Number")
                    st.code(f"""
[+] Full Number      : {formatted_num}
[+] Country/Location : {geocoder.description_for_number(parsed_number, 'en')}
[+] Service Provider : {carrier.name_for_number(parsed_number, 'en')}
[+] Timezone         : {timezone.time_zones_for_number(parsed_number)}
                    """)
                    st.markdown("### Tactical Endpoints")
                    st.markdown(f"- [WhatsApp Direct Link](https://wa.me/{formatted_num.replace('+', '')})")
                    st.markdown(f"- [Facebook Entity Lookup](https://www.facebook.com/search/people/?q={formatted_num})")
                else:
                    st.error("[-] Invalid phone footprint or formatting.")
            except Exception as e:
                st.error(f"[-] Execution Error: {e}")

# 2. Username Recon
elif menu == "Username Recon":
    st.subheader("👤 Username Recon / Cross-Platform Matrix")
    username = st.text_input("Enter target username:").strip()
    
    if st.button("EXECUTE USERNAME SCAN"):
        if username:
            platforms = {
                "GitHub": f"https://github.com/{username}",
                "Instagram": f"https://www.instagram.com/{username}/",
                "Twitter (X)": f"https://twitter.com/{username}",
                "Facebook": f"https://www.facebook.com/{username}",
                "Pinterest": f"https://www.pinterest.com/{username}/",
                "Reddit": f"https://www.reddit.com/user/{username}",
                "TikTok": f"https://www.tiktok.com/@{username}",
                "Steam": f"https://steamcommunity.com/id/{username}"
            }
            headers = {"User-Agent": "Mozilla/5.0"}
            
            with st.spinner("Scanning global networks..."):
                for p_name, url in platforms.items():
                    try:
                        res = requests.get(url, headers=headers, timeout=5)
                        if res.status_code == 200:
                            st.success(f"[+] [{p_name}] TARGET FOUND -> {url}")
                        else:
                            st.warning(f"[-] [{p_name}] Not Found / Restricted")
                    except:
                        st.error(f"[!] [{p_name}] Connection Timeout")

# 3. Email OSINT
elif menu == "Email OSINT":
    st.subheader("📧 Email Intelligence & Disposable Mail Vector")
    email = st.text_input("Enter target email address:").strip()
    
    if st.button("EXECUTE EMAIL ANALYSIS"):
        if "@" in email:
            uname, domain = email.split("@", 1)
            disposable_domains = ["mailinator.com", "10minutemail.com", "tempmail.com", "yopmail.com", "sharklasers.com"]
            
            st.code(f"""
[i] Email Entity : {email}
[i] Username     : {uname}
[i] Domain Host  : {domain}
            """)
            
            if domain.lower() in disposable_domains:
                st.error("⚠️ THREAT DETECTED: Temporary / Disposable (Burner) Mail Provider!")
            else:
                st.success("[+] Status: Standard / Legitimate Domain Entity")
        else:
            st.error("[-] Invalid email structure.")

# 4. IP Geolocation
elif menu == "IP / Geo-Location":
    st.subheader("🌍 IP Network & Geo-Intelligence Lookup")
    ip_input = st.text_input("Enter target IP (leave blank for local host):").strip()
    
    if st.button("EXECUTE IP TRACE"):
        url = f"http://ip-api.com/json/{ip_input}" if ip_input else "http://ip-api.com/json/"
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode())
            if data['status'] == 'success':
                st.json(data)
            else:
                st.error("[-] Target telemetry retrieval failed.")
        except Exception as e:
            st.error(f"[-] Error: {e}")

# 5. Port Scanner
elif menu == "Port Scanner":
    st.subheader("🔌 Advanced Tactical Port Scanner")
    target = st.text_input("Enter target host/IP (e.g., scanme.nmap.org):").strip()
    
    if st.button("INITIATE PORT PROBE"):
        if target:
            try:
                target_ip = socket.gethostbyname(target)
                st.info(f"[*] Target Resolved: {target} -> {target_ip}")
                common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
                
                for port, service in common_ports.items():
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1.0)
                    if s.connect_ex((target_ip, port)) == 0:
                        st.success(f"[OPEN] Port {port} ({service})")
                    else:
                        st.warning(f"[CLOSED] Port {port} ({service})")
                    s.close()
            except Exception as e:
                st.error(f"[-] Socket Error: {e}")

# 6. Domain & DNS Info
elif menu == "Domain & DNS":
    st.subheader("🌐 Domain Recon & DNS Resolution")
    domain = st.text_input("Enter target domain name:").strip()
    
    if st.button("RESOLVE DNS RECORDS"):
        if domain:
            try:
                ip_addr = socket.gethostbyname(domain)
                st.success(f"[+] Resolved IP: {ip_addr}")
                host_info = socket.gethostbyaddr(ip_addr)
                st.code(f"[+] Hostname Entity: {host_info[0]}")
            except Exception as e:
                st.error(f"[-] Resolution Failed: {e}")

# 7. MAC Vendor Lookup
elif menu == "MAC Vendor Lookup":
    st.subheader("💻 MAC Hardware Vendor Identification")
    mac = st.text_input("Enter MAC address (e.g., 00:11:22:33:44:55):").strip()
    
    if st.button("QUERY HARDWARE VENDOR"):
        if mac:
            try:
                res = requests.get(f"https://api.macvendors.com/{mac}", timeout=5)
                if res.status_code == 200:
                    st.success(f"[+] Hardware Vendor Identified: {res.text}")
                else:
                    st.warning("[-] Vendor signature not found.")
            except Exception as e:
                st.error(f"[-] API Error: {e}")