# multi_scraper.py
import requests
from bs4 import BeautifulSoup

def get_links(base_url):
    html = requests.get(base_url).text
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/wiki') and ':' not in a['href']:
            full_url = "https://en.wikipedia.org" + a['href']
            links.append(full_url)
    return list(set(links))[:10]  # First 10 links for safety

def get_text_from_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()
