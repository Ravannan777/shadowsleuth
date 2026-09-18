#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tool Name : ShadowSleuth - Advanced OSINT & Reconnaissance Utility
Author    : Sreenand K
Platform  : Windows, Linux, Termux (Android)
"""

import socket
import sys
import platform
import json
import urllib.request
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def banner():
    print("=" * 65)
    print("      [+] SHADOWSLEUTH - ADVANCED OSINT TOOL [+]")
    print(f"      [i] Developer : Sreenand K")
    print(f"      [i] Platform  : Windows, Linux, Termux (Android)")
    print(f"      [i] Version   : 1.5.0 (Professional Edition)")
    print("=" * 65)

def phone_osint():
    print("\n--- [ 1. Phone Number Intelligence & Social Check ] ---")
    number_str = input("Enter phone number (e.g., 8289804072 or +918289804072): ")
    
    if not number_str.startswith("+"):
        number_str = "+91" + number_str

    try:
        parsed_number = phonenumbers.parse(number_str)
        if phonenumbers.is_valid_number(parsed_number):
            formatted_num = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            print("\n[+] Valid Phone Number Found!")
            print(f"    -> Full Number      : {formatted_num}")
            print(f"    -> Country/Location : {geocoder.description_for_number(parsed_number, 'en')}")
            print(f"    -> Service Provider : {carrier.name_for_number(parsed_number, 'en')}")
            print(f"    -> Timezone         : {timezone.time_zones_for_number(parsed_number)}")
            
            print("\n[*] Meta & Social Platform Intelligence:")
            print(f"    -> WhatsApp Link    : https://wa.me/{formatted_num.replace('+', '')}")
            print(f"    -> Facebook Lookup  : https://www.facebook.com/search/people/?q={formatted_num}")
            print(f"    -> Instagram Profile: Check via Username/Recovery (Direct phone scraping blocked by Meta API)")
        else:
            print("[-] Invalid phone number or formatting.")
    except Exception as e:
        print(f"[-] Error: {e}")

def username_osint():
    print("\n--- [ 2. Username Recon / Social Media Check ] ---")
    username = input("Enter username to search: ").strip()
    
    platforms = {
        "GitHub": {"url": f"https://github.com/{username}", "error_text": "Not Found"},
        "Instagram": {"url": f"https://www.instagram.com/{username}/", "error_text": "Page Couldn't Be Loaded"},
        "Twitter (X)": {"url": f"https://twitter.com/{username}", "error_text": "this page doesn't exist"},
        "Facebook": {"url": f"https://www.facebook.com/{username}", "error_text": "this page isn't available"},
        "WhatsApp": {"url": f"https://wa.me/{username}", "error_text": "phone number shared via url is invalid"},
        "Pinterest": {"url": f"https://www.pinterest.com/{username}/", "error_text": "profile not found"},
        "Reddit": {"url": f"https://www.reddit.com/user/{username}", "error_text": "sorry, nobody on reddit goes by that name"},
        "TikTok": {"url": f"https://www.tiktok.com/@{username}", "error_text": "Couldn't find this account"},
        "Steam": {"url": f"https://steamcommunity.com/id/{username}", "error_text": "The specified profile could not be found"}
    }

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    print(f"\n[*] Searching accurately for username '{username}' across platforms...\n")
    
    for platform_name, data in platforms.items():
        url = data["url"]
        error_msg = data["error_text"].lower()
        try:
            response = requests.get(url, headers=headers, timeout=6)
            if response.status_code == 200:
                if error_msg in response.text.lower():
                    print(f"[-] [{platform_name}] Not Found")
                else:
                    print(f"[+] [{platform_name}] Found -> {url}")
            elif response.status_code == 404:
                print(f"[-] [{platform_name}] Not Found")
            else:
                print(f"[?] [{platform_name}] Status: {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"[!] [{platform_name}] Connection Error / Blocked")

def email_osint():
    print("\n--- [ 3. Email OSINT & Disposable Mail Check ] ---")
    email = input("Enter email address to analyze: ").strip()
    
    if "@" not in email:
        print("[-] Invalid email format.")
        return

    username, domain = email.split("@", 1)
    
    disposable_domains = [
        "mailinator.com", "10minutemail.com", "tempmail.com", "guerrillamail.com",
        "trashmail.com", "yopmail.com", "sharklasers.com", "getnada.com",
        "dispostable.com", "temp-mail.org", "fakemailgenerator.com"
    ]

    print(f"\n[*] Analyzing Email: {email}")
    print(f"    -> Username : {username}")
    print(f"    -> Domain   : {domain}")

    if domain.lower() in disposable_domains:
        print("    -> Status   : [!] WARNING: This is a Temporary / Disposable (Fake) Email!")
    else:
        print("    -> Status   : [+] Standard / Legitimate Email Domain")

    print("\n[*] Checking common platforms for email association...")
    email_platforms = {
        "Gravatar": f"https://en.gravatar.com/{username}.json",
        "GitHub (API check)": f"https://api.github.com/search/users?q={email}",
        "Facebook Recovery Link": f"https://www.facebook.com/login/identify/?ctx=recover&email={email}"
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    for p_name, p_url in email_platforms.items():
        try:
            res = requests.get(p_url, headers=headers, timeout=5)
            if res.status_code == 200:
                print(f"[+] [{p_name}] Associated endpoint active!")
            else:
                print(f"[-] [{p_name}] Restricted or Not found")
        except:
            print(f"[!] [{p_name}] Connection error")

def ip_geolocation():
    print("\n--- [ 4. IP / Geo-Location Lookup ] ---")
    ip_input = input("Enter IP address or leave blank for your IP: ").strip()
    url = f"http://ip-api.com/json/{ip_input}" if ip_input else "http://ip-api.com/json/"
    
    try:
        print("\n[*] Fetching location data...")
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        
        if data['status'] == 'success':
            print("\n[+] Target IP Details Found:")
            print(f"    -> Query IP     : {data.get('query')}")
            print(f"    -> Country      : {data.get('country')} ({data.get('countryCode')})")
            print(f"    -> Region/State : {data.get('regionName')} ({data.get('region')})")
            print(f"    -> City         : {data.get('city')}")
            print(f"    -> ZIP Code     : {data.get('zip')}")
            print(f"    -> ISP          : {data.get('isp')}")
            print(f"    -> Organization : {data.get('org')}")
            print(f"    -> Timezone     : {data.get('timezone')}")
            print(f"    -> Coordinates  : Lat: {data.get('lat')}, Lon: {data.get('lon')}")
        else:
            print("[-] Failed to retrieve IP information.")
    except Exception as e:
        print(f"[-] Error: {e}")

def port_scanner():
    print("\n--- [ 5. Advanced Quick Port Scanner ] ---")
    target = input("Enter target IP or Domain (e.g., scanme.nmap.org): ").strip()
    
    try:
        target_ip = socket.gethostbyname(target)
        print(f"\n[*] Resolved Target: {target} -> {target_ip}")
        print("[*] Scanning common ports... Please wait.\n")
        
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
            445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy"
        }
        
        for port, service in common_ports.items():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                print(f"[+] Port {port} ({service}) IS OPEN")
            else:
                print(f"[-] Port {port} ({service}) is closed")
            s.close()
    except socket.gaierror:
        print("[-] Hostname could not be resolved.")
    except Exception as e:
        print(f"[-] Error: {e}")

def domain_recon():
    print("\n--- [ 6. Domain & DNS Information ] ---")
    domain = input("Enter Domain Name (e.g., google.com): ").strip()
    
    try:
        print(f"\n[*] Gathering information for {domain}...")
        ip_addr = socket.gethostbyname(domain)
        print(f"[+] IP Address : {ip_addr}")
        
        host_info = socket.gethostbyaddr(ip_addr)
        print(f"[+] Hostname   : {host_info[0]}")
        if host_info[1]:
            print(f"[+] Aliases    : {', '.join(host_info[1])}")
    except socket.gaierror:
        print("[-] Could not resolve domain name.")
    except Exception as e:
        print(f"[-] Error: {e}")

def mac_lookup():
    print("\n--- [ 7. MAC Address Vendor Lookup ] ---")
    mac = input("Enter MAC address (e.g., 00:11:22:33:44:55): ").strip()
    url = f"https://api.macvendors.com/{mac}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        print(f"\n[*] Looking up vendor for MAC: {mac}...")
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"[+] MAC Vendor Found: {response.text}")
        elif response.status_code == 404:
            print("[-] MAC address vendor not found or invalid format.")
        else:
            print(f"[?] Error status code: {response.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    while True:
        banner()
        print(" 1. Phone Number Intelligence & Social Check")
        print(" 2. Username OSINT (Social Media Search)")
        print(" 3. Email OSINT & Disposable Mail Check")
        print(" 4. IP / Geo-Location Lookup")
        print(" 5. Advanced Quick Port Scanner")
        print(" 6. Domain & DNS Information")
        print(" 7. MAC Address Vendor Lookup")
        print(" 8. Exit")
        
        choice = input("\nShadowSleuth > Select an option: ")
        
        if choice == '1':
            phone_osint()
            input("\nPress Enter to return to the main menu...")
        elif choice == '2':
            username_osint()
            input("\nPress Enter to return to the main menu...")
        elif choice == '3':
            email_osint()
            input("\nPress Enter to return to the main menu...")
        elif choice == '4':
            ip_geolocation()
            input("\nPress Enter to return to the main menu...")
        elif choice == '5':
            port_scanner()
            input("\nPress Enter to return to the main menu...")
        elif choice == '6':
            domain_recon()
            input("\nPress Enter to return to the main menu...")
        elif choice == '7':
            mac_lookup()
            input("\nPress Enter to return to the main menu...")
        elif choice == '8':
            print("\nExiting ShadowSleuth. Stay safe!")
            sys.exit(0)
        else:
            print("\n[-] Invalid option! Please select a valid number.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()