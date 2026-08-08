import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Page Config
st.set_page_config(
    page_title="AI Data & Lead Intelligence Suite",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #06b6d4, #2563eb); color: white; font-weight: bold; border-radius: 8px; border: none; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Web Intelligence & Lead Extraction SaaS")
st.subheader("Extract structured SEO metadata, headings, and business intelligence in seconds.")

# Sidebar Configuration
st.sidebar.header("⚙️ Scraper Controls")
target_url = st.sidebar.text_input("Enter Target Website URL:", "https://news.ycombinator.com/")
max_headings = st.sidebar.slider("Max Headings to Scrape:", 5, 50, 15)

if st.sidebar.button("🚀 Run Automation Scraper"):
    with st.spinner("Fetching and analyzing target web data..."):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(target_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                page_title = soup.title.string if soup.title else "N/A"
                headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3']) if h.text.strip()][:max_headings]
                links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')][:10]

                # Metric Cards
                col1, col2, col3 = st.columns(3)
                col1.metric("HTTP Status", f"{response.status_code} OK")
                col2.metric("Headings Found", len(headings))
                col3.metric("Outbound Links", len(links))

                st.markdown("---")
                st.subheader(f"📌 Page Title: `{page_title}`")

                # Data Table
                df_headings = pd.DataFrame({"Extracted Headings / Topics": headings})
                st.write("### 📊 Extracted Content Structure")
                st.dataframe(df_headings, use_container_width=True)

                # Download CSV
                csv_data = df_headings.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Data as CSV",
                    data=csv_data,
                    file_name="extracted_leads.csv",
                    mime="text/csv"
                )

            else:
                st.error(f"Failed to fetch website. HTTP Status: {response.status_code}")

        except Exception as e:
            st.error(f"An error occurred during extraction: {e}")

else:
    st.info("👈 Enter a URL in the sidebar and click 'Run Automation Scraper' to test live extraction.")
