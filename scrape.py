from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching chrome browser...")

    # Setup Chrome options
    options = Options()
    options.add_argument("--headless")  # Optional: Comment out if you want to see the browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use WebDriver Manager to auto-fetch compatible ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Open the website
        driver.get(website)
        print("Page loaded...")

        # Get the page source
        time.sleep(10)
        html = driver.page_source
        return html
    
    finally:
        # Close the browser
        driver.quit()

def extract_body_content(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style tags
    for script in soup(["script", "style"]):  
        script.extract()
    
    text = soup.get_text(separator="\n")
    return text.strip()

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(content, chunk_size=2000):
    """Splits content into chunks (increase chunk_size if content is cut off)."""
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]


