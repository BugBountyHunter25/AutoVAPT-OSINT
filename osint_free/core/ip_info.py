import requests

def get_ip_info(ip):
    try:
        res = requests.get(f'https://ipinfo.io/{ip}/json', timeout=10)
        return res.json()
    except:
        return {"error": "IP info fetch failed"}
