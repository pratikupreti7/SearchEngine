
# webcrawler.py
import requests
from bs4 import BeautifulSoup

def crawl_url(url):
    try:

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        text_content = soup.get_text()
        headings = [tag.text.strip() for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

        return text_content, headings
    except Exception as e:
        print(f"Error: Could not retrieve page content for {url}")
        return None, None

