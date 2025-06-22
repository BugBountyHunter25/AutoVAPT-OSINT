import requests

def get_subdomains_crtsh(domain):
    url = f'https://crt.sh/?q=%25.{domain}&output=json'
    try:
        names = {r['name_value'] for r in requests.get(url, timeout=10).json()}
        return sorted(names)
    except:
        return []