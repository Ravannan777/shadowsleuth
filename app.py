from flask import Flask, render_template, request, jsonify
import socket
import json
import urllib.request
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_phone', methods=['POST'])
def check_phone():
    data = request.json
    number_str = data.get('number', '').strip()
    if not number_str.startswith("+"):
        number_str = "+91" + number_str
    try:
        parsed_number = phonenumbers.parse(number_str)
        if phonenumbers.is_valid_number(parsed_number):
            formatted_num = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return jsonify({
                'status': 'success',
                'full_number': formatted_num,
                'location': geocoder.description_for_number(parsed_number, 'en'),
                'provider': carrier.name_for_number(parsed_number, 'en'),
                'timezone': str(timezone.time_zones_for_number(parsed_number)),
                'whatsapp': f"https://wa.me/{formatted_num.replace('+', '')}",
                'facebook': f"https://www.facebook.com/search/people/?q={formatted_num}"
            })
        else:
            return jsonify({'status': 'error', 'message': 'Invalid phone number format.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.json
    username = data.get('username', '').strip()
    platforms = {
        "GitHub": {"url": f"https://github.com/{username}", "icon": "🐙"},
        "Instagram": {"url": f"https://www.instagram.com/{username}/", "icon": "📸"},
        "Twitter (X)": {"url": f"https://twitter.com/{username}", "icon": "🐦"},
        "Facebook": {"url": f"https://www.facebook.com/{username}", "icon": "👥"},
        "Pinterest": {"url": f"https://www.pinterest.com/{username}/", "icon": "📌"},
        "Reddit": {"url": f"https://www.reddit.com/user/{username}", "icon": "🤖"},
        "TikTok": {"url": f"https://www.tiktok.com/@{username}", "icon": "🎵"},
        "Steam": {"url": f"https://steamcommunity.com/id/{username}", "icon": "🎮"}
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    
    for p_name, info in platforms.items():
        try:
            res = requests.get(info['url'], headers=headers, timeout=4)
            if res.status_code == 200:
                results.append({"name": p_name, "icon": info['icon'], "url": info['url'], "status": "FOUND"})
            else:
                results.append({"name": p_name, "icon": info['icon'], "url": info['url'], "status": "NOT FOUND"})
        except:
            results.append({"name": p_name, "icon": info['icon'], "url": info['url'], "status": "TIMEOUT"})
            
    return jsonify({'status': 'success', 'results': results})

@app.route('/check_ip', methods=['POST'])
def check_ip():
    data = request.json
    ip_input = data.get('ip', '').strip()
    url = f"http://ip-api.com/json/{ip_input}" if ip_input else "http://ip-api.com/json/"
    try:
        response = urllib.request.urlopen(url)
        ip_data = json.loads(response.read().decode())
        if ip_data.get('status') == 'success':
            return jsonify({'status': 'success', 'data': ip_data})
        else:
            return jsonify({'status': 'error', 'message': 'IP lookup failed.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/check_domain', methods=['POST'])
def check_domain():
    data = request.json
    domain = data.get('domain', '').strip()
    try:
        ip_addr = socket.gethostbyname(domain)
        host_info = socket.gethostbyaddr(ip_addr)
        return jsonify({
            'status': 'success',
            'ip': ip_addr,
            'hostname': host_info[0]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/check_mac', methods=['POST'])
def check_mac():
    data = request.json
    mac = data.get('mac', '').strip()
    url = f"https://api.macvendors.com/{mac}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'success', 'vendor': response.text})
        else:
            return jsonify({'status': 'error', 'message': 'Vendor not found.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)