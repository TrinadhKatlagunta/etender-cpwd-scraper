from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--headless") 
options.add_argument("--window-size=1920,1080")

# Verify ChromeDriver path
chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
if not os.path.exists(chromedriver_path):
    raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}. Ensure it's in the working directory.")

# Initialize WebDriver
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)  # 30-second timeout

try:
    # Navigate to the website
    driver.get("https://etender.cpwd.gov.in/")
    print("✅ Page loaded")
    time.sleep(3)

    # Dismiss alert if present
    try:
        alert = driver.switch_to.alert
        print("Alert found:", alert.text)
        alert.dismiss()
        time.sleep(2)
    except:
        print("No alert found.")

    # Click "New Tenders"
    try:
        new_tenders = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "New Tenders")))
        new_tenders.click()
        print("✅ Clicked 'New Tenders'")
        time.sleep(2)
    except Exception as e:
        print("Error clicking 'New Tenders':", e)
        raise

    # Click "All"
    try:
        all_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "All")))
        all_link.click()
        print("✅ Clicked 'All'")
        time.sleep(3)
    except Exception as e:
        print("Error clicking 'All':", e)
        raise

    # Update dropdown to show 20 records
    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@name="awardedDataTable_length"]')))
        select = Select(dropdown)
        select.select_by_value("20")
        print("✅ Set dropdown to show 20 records")
        time.sleep(3)
    except Exception as e:
        print("Error selecting 20 records from dropdown:", e)
        print("Page title:", driver.title)
        print("Current URL:", driver.current_url)
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Page source saved to 'page_source.html' for debugging")
        raise

    # Scroll down to trigger table load
    for i in range(5): 
        driver.execute_script("window.scrollBy(0, 1000);")
        print(f"Scroll {i+1}/5 completed")
        time.sleep(2)

    # Debug: Check page source for table
    page_source = driver.page_source
    if "awardedDataTable" not in page_source:
        print("⚠️ Table ID 'awardedDataTable' not found in page source. Check website structure.")
        raise Exception("Table not found")

    # Wait for table rows
    try:
        tender_rows = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@id="awardedDataTable"]/tbody/tr'))
        )
        print(f"✅ Found {len(tender_rows)} tenders")
    except Exception as e:
        print("Error finding table rows:", e)
        print("Page title:", driver.title)
        print("Current URL:", driver.current_url)
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Page source saved to 'page_source.html' for debugging")
        raise

    # Extract top 20 tenders with specific fields
    tenders = []
    for row in tender_rows[:20]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 8:
            estimated_cost = cols[4].text.strip().replace('₹', '').replace(',', '')
            emd_amount = cols[5].text.strip().replace('₹', '').replace(',', '')
            tenders.append({
                "NIT/RFP NO": cols[1].text.strip(),
                "Name of Work / Subwork / Packages": cols[2].text.strip(),  
                "Estimated Cost": estimated_cost,  
                "Bid Submission Closing Date & Time": f'"{cols[6].text.strip()}"',  
                "EMD Amount": emd_amount,  
                "Bid Opening Date & Time": f'"{cols[7].text.strip()}"',  
            })
        else:
            print(f"⚠️ Row skipped: insufficient columns ({len(cols)} found, 8 expected)")

    # Save to CSV with custom column names
    if tenders:
        df = pd.DataFrame(tenders)
        csv_cols = {
            "NIT/RFP NO": "ref_no",
            "Name of Work / Subwork / Packages": "title",
            "Estimated Cost": "tender_value",
            "Bid Submission Closing Date & Time": "bid_submission_end_date",
            "EMD Amount": "emd",
            "Bid Opening Date & Time": "bid_open_date"
        }
        df = df.rename(columns=csv_cols)
        df.to_csv("tenders.csv", index=False, encoding='utf-8')
        print("✅ Data saved to tenders.csv")
        print(df.head())
    else:
        print("⚠️ No tenders extracted. CSV not created.")

except Exception as e:
    print("Unexpected error:", e)
finally:
    driver.quit()
    print("✅ Browser closed")