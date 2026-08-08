# 🐍 Python Web Automation & Lead Scraper

An automated Python script built with BeautifulSoup4 and Requests to extract structured metadata, page titles, and headings (H1, H2) from target websites and export them to clean JSON/CSV format.

![Python Version](https://img.shields.io/badge/Python-3.x-blue)
![Dependencies](https://img.shields.io/badge/Dependencies-BeautifulSoup4%20%7C%20Requests-orange)

## ✨ Features

* 🔍 **Automated Data Extraction:** Efficiently parses HTML for key web metadata and headers.
* 🛡️ **Custom User-Agent:** Prevents scraper blocking by mimicking browser requests.
* 💾 **Structured Export:** Saves extracted data directly to `scraped_data.json`.
* ⚡ **Error Resilience:** Includes try-except handling for network timeouts.

## 🛠️ Requirements & Installation

Install dependencies via pip:

```bash
pip install requests bs4 pandas
