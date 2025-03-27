import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching chrome browser...")

    # Correct path with proper escape characters
    chrome_driver_path = r"C:\Astro PPT'S\AI WebScrapping\chromedriver-win64\chromedriver.exe"
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
    try:
        # Open the website
        driver.get(website)
        print("Page loaded...")

        # Get the page source
        html = driver.page_source
        time.sleep(10)

        return html
    
    finally:
        # Close the browser
        driver.quit()

def extract_body_content(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Extracting text while preserving important structure
    for script in soup(["script", "style"]):  
        script.extract()  # Remove script and style elements
    
    text = soup.get_text(separator="\n")  # Preserve structure with newlines
    
    return text.strip()  # Return cleaned text

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script" , "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator = '\n')
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(content, chunk_size=2000):  
    """Splits content into chunks (increase chunk_size if content is cut off)."""
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

