# Rural-india-webscrap

# Rural India Online Web Scraper 🧑‍🌾📄

This project extracts article content from [ruralindiaonline.org](https://ruralindiaonline.org/articles) using Python. It scrapes over 1000 articles and exports structured data into an Excel sheet.

## Use below command to Run
python Scraper.py    (CMD)
or  use Rural_india.ipynb to run each cell (Google collab or Jupyter Notebook)

## 🔍 Overview

This script performs the following tasks:

1. Fetches all article URLs from the main articles page.
2. Iterates through each URL to extract data using `BeautifulSoup`, `re`, and `requests`.
3. Extracts structured data such as:
   - 🏷️ Title/Subject
   - 📍 Location
   - 📄 Full Content (Collection)
   - 🔗 Story Link
   - ✍️ Author
   - 🗂️ Categories
   - 🖼️ Images
4. Stores the extracted data in an Excel file using `pandas`.

## 🛠️ Tech Stack

- `Python`
- `BeautifulSoup` – for parsing HTML content
- `requests` – for fetching web pages
- `re` – for extracting data using regular expressions
- `pandas` – for storing data into Excel



