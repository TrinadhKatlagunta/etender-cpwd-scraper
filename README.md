# Tender Scraper Automation 🛠️

Welcome to the **Tender Scraper** project! This Python script automates the process of scraping tender data from the Central Public Works Department (CPWD) e-tender portal. It’s designed to extract key tender details and save them to a clean, organized CSV file for easy analysis. Let’s take your tender tracking to the next level! 🚀

## 📋 What This Automation Does

This script uses Selenium to:

- 🌐 Navigate to the CPWD e-tender portal (`https://etender.cpwd.gov.in/`)
- 🖱️ Click through "New Tenders" and "All" to access the tender list
- 📏 Adjust the page to display 20 tender records
- ⬇️ Scrape 20 tenders from the `awardedDataTable` table
- 🧹 Clean `tender_value` and `emd` fields by removing "₹" and commas
- 💾 Save the following fields to `tenders.csv`:
  - `ref_no`: NIT/RFP number
  - `title`: Name of work, subwork, or packages
  - `tender_value`: Estimated cost (numeric)
  - `bid_submission_end_date`: Bid submission closing date and time
  - `emd`: EMD amount (numeric)
  - `bid_open_date`: Bid opening date and time

## 🛠️ Requirements & Dependencies

To run this automation, ensure you have the following:

### Software

- **Python 3.6+** 🐍: The script is written in Python.
- **Google Chrome Browser** 🌍: Required for Selenium to interact with the website.
- **ChromeDriver** ⚙️: A compatible version of ChromeDriver must be in the script’s working directory.

### Python Dependencies

Install these packages via `pip` using the provided `requirements.txt`:

- **selenium**: Drives the browser to scrape the website
- **pandas**: Handles data processing and CSV output

Run this command to install:

```bash
pip install -r requirements.txt
```

## 📦 Setup Instructions

1. **Clone the Repository** 📥

   ```bash
   git clone https://github.com/your-username/tender-scraper.git
   cd tender-scraper
   ```

2. **Install Dependencies** 🛠️

   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver** 🌐

   - Visit ChromeDriver downloads
   - Download the version matching your Chrome browser
   - Place `chromedriver.exe` (Windows) or equivalent in the project folder

4. **Run the Script** 🚀

   ```bash
   python main.py
   ```

5. **Check Output** 📊

   - The script generates `tenders.csv` in the project folder
   - Open it in Excel or a text editor to view the scraped tender data

## ⚠️ Notes

- **Internet Connection**: A stable connection is required to access the CPWD portal.
- **Headless Mode**: The script runs in headless mode (no browser window) for efficiency, but you can remove the `--headless` flag in `scrape_tenders.py` to watch it work!
- **Error Handling**: If `chromedriver.exe` is missing or the table isn’t found, the script logs errors and saves the page source to `page_source.html` for debugging.
- **Dynamic Content**: The script scrolls and waits to ensure all data loads.

## 📄 Sample Output

The `tenders.csv` file will look like this:

```
ref_no,title,tender_value,bid_submission_end_date,emd,bid_open_date
01/SE/Jalandhar/2025-26,Construction of Prahari Grah...,201974518,"06/06/2025 15:00",3019745,"06/06/2025 15:30"
02/CE/NDZ-I/DED-101/2025-26,Provision of Fire Safety Measures...,17747850,"19/06/2025 15:00",354957,"19/06/2025 15:30"
...
```
