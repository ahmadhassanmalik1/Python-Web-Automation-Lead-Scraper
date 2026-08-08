import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_website_leads(target_url):
    print(f"[+] Starting Automation Scraper for: {target_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("[-] Failed to retrieve website data.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract metadata
        page_title = soup.title.string if soup.title else "No Title"
        headings = [h.text.strip() for h in soup.find_all(['h1', 'h2']) if h.text.strip()]

        extracted_data = {
            "URL": target_url,
            "Page_Title": page_title,
            "Total_Headings_Found": len(headings),
            "Top_Headings": headings[:5]
        }

        # Save result to JSON
        with open("scraped_data.json", "w") as f:
            json.dump(extracted_data, f, indent=4)

        print("[+] Data Scraped & Saved to 'scraped_data.json' Successfully!")
        print(json.dumps(extracted_data, indent=2))

    except Exception as e:
        print(f"[-] Error encountered: {e}")

if __name__ == "__main__":
    # Test target
    url_to_scrape = "https://news.ycombinator.com/"
    scrape_website_leads(url_to_scrape)