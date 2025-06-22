# nmap_scan.py

import subprocess

def run_nmap_scan(ip):
    try:
        print(f"Running Nmap scan on {ip}...")
        result = subprocess.check_output(['nmap', '-T4', '-F', ip], stderr=subprocess.STDOUT, text=True)
        print("Nmap scan completed.")
        return result
    except subprocess.CalledProcessError as e:
        print("Nmap command failed:", e.output)
        return f"Nmap command failed:\n{e.output}"
    except Exception as e:
        print("Unexpected error during Nmap scan:", str(e))
        return f"Unexpected error during Nmap scan:\n{str(e)}"
