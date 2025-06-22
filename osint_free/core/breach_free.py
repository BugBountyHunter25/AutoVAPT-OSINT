import requests
import hashlib

def pwned_password_sha1(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    resp = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}', timeout=10)
    return any(line.split(':')[0] == suffix for line in resp.text.splitlines())