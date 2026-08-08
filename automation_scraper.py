import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Page Config
st.set_page_config(
    page_title="AI Web Intelligence & Lead SaaS",
    page_icon="⚡",
    layout="wide"
)

# Custom Sleek Styling (Dark Mode Aesthetic)
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stTextInput > div > div > input { background-color: #1e293b; color: #ffffff; border-radius: 8px; border: 1px solid #334155; }
    .stButton > button { width: 100%; background: linear-gradient(90deg, #06b6d4, #2563eb); color: white; font-weight: bold; border-radius: 8px; border: none; padding: 10px; transition: 0.3s; }
    .stButton > button:hover { background: linear-gradient(90deg, #0891b2, #1d4ed8); }
    .metric-card { background-color: #1e293b; border: 1px solid #334155; padding: 15px; border-radius: 12px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# App Title & Subtitle
st.title("⚡ Web Intelligence & Lead Scraper SaaS")
st.caption("Automated SEO metadata extraction, smart news headlines capture, and data pipeline generator.")

# Sidebar Configuration
st.sidebar.header("⚙️ Scraper Controls")
target_url = st.sidebar.text_input("Target Website URL:", "https://www.express.com.pk/")
max_items = st.sidebar.slider("Max Headlines/Topics to Fetch:", 5, 50, 20)

if st.sidebar.button("🚀 Run Live Extraction"):
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    with st.spinner("Extracting web structure and analyzing page content..."):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(target_url, headers=headers, timeout=12)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 1. Page Title & Meta Description
                page_title = soup.title.string.strip() if soup.title else "No Title Found"
                meta_desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
                meta_desc = meta_desc_tag['content'].strip() if meta_desc_tag and 'content' in meta_desc_tag.attrs else "No Meta Description available."

                # 2. Smart Headline / Heading Extractor
                headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4']) if h.text.strip()]
                
                # Fallback Logic: News portals using links/divs for headlines
                if len(headings) < 3:
                    fallback_headlines = list(set([a.text.strip() for a in soup.find_all('a') if len(a.text.strip()) > 25]))
                    headings = (headings + fallback_headlines)[:max_items]
                else:
                    headings = headings[:max_items]

                # 3. Outbound Links & Media Count
                links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
                images = [img['src'] for img in soup.find_all('img', src=True)]

                # Metrics Dashboard
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("HTTP Status", f"{response.status_code} OK")
                col2.metric("Headings / Topics", len(headings))
                col3.metric("Outbound Links", len(links))
                col4.metric("Images Detected", len(images))

                st.markdown("---")

                # Overview Box
                st.subheader("📌 SEO Overview")
                st.markdown(f"**Site Title:** `{page_title}`")
                st.markdown(f"**Meta Description:** {meta_desc}")

                st.markdown("---")

                # Structured Data Table
                st.subheader("📊 Extracted Headlines & Topics")
                if headings:
                    df_headings = pd.DataFrame({
                        "Index": range(1, len(headings) + 1),
                        "Extracted Content / Headline": headings
                    })
                    st.dataframe(df_headings, use_container_width=True)

                    # Export Buttons
                    col_csv, col_json = st.columns(2)
                    
                    csv_data = df_headings.to_csv(index=False).encode('utf-8')
                    col_csv.download_button(
                        label="📥 Download Data as CSV",
                        data=csv_data,
                        file_name="extracted_intelligence.csv",
                        mime="text/csv"
                    )

                    json_output = {
                        "url": target_url,
                        "title": page_title,
                        "meta_description": meta_desc,
                        "extracted_content": headings
                    }
                    col_json.download_button(
                        label="📦 Download Full JSON Report",
                        data=json.dumps(json_output, indent=4),
                        file_name="site_report.json",
                        mime="application/json"
                    )
                else:
                    st.warning("No structured text found on this page.")

            else:
                st.error(f"Failed to access site. HTTP Status Code: {response.status_code}")

        except Exception as e:
            st.error(f"Error encountered during web scraping: {str(e)}")
else:
    st.info("👈 Enter any website URL in the left sidebar and click 'Run Live Extraction' to view the intelligence report.")
