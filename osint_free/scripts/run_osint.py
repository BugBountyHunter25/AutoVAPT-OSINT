from osint_free.core.whois_dns import whois_dns
from osint_free.core.subdomains import get_subdomains_crtsh
from osint_free.core.breach_free import pwned_password_sha1
from osint_free.core.robots_sitemap import fetch_robots_sitemap
from osint_free.core.nmap_scan import run_nmap_scan
from osint_free.core.ip_location import get_ip_location
from osint_free.core.homepage_scraper import scrape_homepage
from osint_free.core.shodan_scraper import shodan_scan
from osint_free.scripts.report_osint import report_osint
import socket


def run_osint_stage(target, test_password=None , phone_number=None):
    out = {'domain': target}
    out.update(whois_dns(target))
    out['subdomains'] = get_subdomains_crtsh(target)

    
    # Run Nmap
    try:
        ip = socket.gethostbyname(target)
        out['resolved_ip'] = ip
        out['nmap_scan'] = run_nmap_scan(ip)
        out['ip_location'] = get_ip_location(ip)
    except Exception as e:
        out['nmap_scan'] = f"Nmap error: {str(e)}"

        if phone_number:
            from osint_free.core.phone_lookup import lookup_phone_info
            out['phone_info'] = lookup_phone_info(phone_number)

        out.update(fetch_robots_sitemap(target))
        out['homepage_scrape'] = scrape_homepage(target)

    # Shodan scan
    SHODAN_API_KEY = " i4NodjgP3sdorKOlffWb0fzKNAPfgKIx "
    try:
        out['shodan_data'] = shodan_scan(ip, SHODAN_API_KEY)
    except Exception as e:
        out['shodan_data'] = f"Shodan scan error: {str(e)}"
   
    if test_password:
        out['password_pwned'] = pwned_password_sha1(test_password)
    
    report_osint(out)
    return out

if __name__ == "__main__":
    domain = input("Enter domain: ")
    test_password = input("Enter password to check (optional): ") or None
    phone = input("Enter phone number (optional): ").strip() or None
    result = run_osint_stage(domain if domain else None, test_password, phone)
    print("OSINT Report generated: osint_report.json")