import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_100am_tenants():
    url = "https://singmalls.app/en/malls/100-am/directory"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Each tenant link is inside <a>
    tenant_links = soup.find_all("a", href=True)

    tenants = []
    for a in tenant_links:
        text = a.get_text(strip=True)
        # Skip empty texts and nav links like "Home" or "Malls"
        if text and text.lower() not in ["home", "malls"]:
            tenants.append(text)

    return tenants

def save_to_csv(tenants):
    # Each tenant gets its own row
    df = pd.DataFrame([{"Mall Name": "100 AM", "Tenant": t} for t in tenants])
    df.to_csv("100AM_tenants.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(tenants)} tenants to 100AM_tenants.csv")

if __name__ == "__main__":
    tenants = scrape_100am_tenants()
    save_to_csv(tenants)
