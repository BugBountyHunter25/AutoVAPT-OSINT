import requests
from bs4 import BeautifulSoup

def scrape_homepage(domain):
    result = {}

    try:
        url = f"https://{domain}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            result['error'] = f"Status code {response.status_code}"
            return result

        soup = BeautifulSoup(response.text, 'html.parser')

        result['title'] = soup.title.string.strip() if soup.title else "No Title Found"

        # Meta description and keywords
        meta_desc = soup.find("meta", attrs={"name": "description"})
        result['meta_description'] = meta_desc["content"] if meta_desc else "Not Found"

        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        result['meta_keywords'] = meta_keywords["content"] if meta_keywords else "Not Found"

        # All H1 tags
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]
        result['h1_headers'] = h1_tags

    except Exception as e:
        result['error'] = f"Scraping error: {str(e)}"

    return result
