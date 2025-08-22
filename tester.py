import requests
from bs4 import BeautifulSoup

url = "https://singmalls.app/en/malls"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Find all mall links
mall_links = soup.select("a[href*='/directory']")
mall_urls = ["https://singmalls.app" + a['href'] for a in mall_links]

for u in mall_urls:
    print(u)
