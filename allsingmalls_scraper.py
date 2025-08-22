import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_mall_tenants(mall_url):
    """Scrape tenants from a given mall directory URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(mall_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    tenant_links = soup.find_all("a", href=True)

    tenants = []
    for a in tenant_links:
        text = a.get_text(strip=True)
        # Skip empty texts and nav links like "Home" or "Malls"
        if text and text.lower() not in ["home", "malls"]:
            tenants.append(text)

    # Extract mall name from URL
    mall_name = mall_url.split("/")[-2].replace("-", " ").title()
    return mall_name, tenants

def save_to_csv(all_data):
    """Save the collected tenant data to CSV."""
    df = pd.DataFrame(all_data)
    df.to_csv("malls_tenants.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} rows to malls_tenants.csv")

url = "https://singmalls.app/en/malls"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

if __name__ == "__main__":
    # Manually input the list of mall directory URLs here
    mall_links = soup.select("a[href*='/directory']")
    mall_urls = ["https://singmalls.app" + a['href'] for a in mall_links]
    all_data = []
    for url in mall_urls:
        print(f"Scraping {url} ...")
        mall_name, tenants = scrape_mall_tenants(url)
        for tenant in tenants:
            all_data.append({"Mall Name": mall_name, "Tenant": tenant})
        time.sleep(1)  # politeness delay

    save_to_csv(all_data)
