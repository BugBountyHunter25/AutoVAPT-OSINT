import requests
from urllib.parse import urljoin

def fetch_robots_sitemap(domain):
    result = {}

    # Force HTTPS, you can fallback to HTTP if you want
    base_url = f"https://{domain}/"

    try:
        robots_url = urljoin(base_url, "robots.txt")
        robots_response = requests.get(robots_url, timeout=5)
        if robots_response.status_code == 200:
            result['robots.txt'] = robots_response.text
        else:
            result['robots.txt'] = f"robots.txt not found or returned status {robots_response.status_code}"
    except Exception as e:
        result['robots.txt'] = f"Error fetching robots.txt: {str(e)}"

    try:
        sitemap_url = urljoin(base_url, "sitemap.xml")
        sitemap_response = requests.get(sitemap_url, timeout=5)
        if sitemap_response.status_code == 200:
            result['sitemap.xml'] = sitemap_response.text
        else:
            result['sitemap.xml'] = f"sitemap.xml not found or returned status {sitemap_response.status_code}"
    except Exception as e:
        result['sitemap.xml'] = f"Error fetching sitemap.xml: {str(e)}"

    return result
