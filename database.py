import sqlite3
import json

DB_NAME = "scraped_data.db"

def create_table():
    """Create the table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extracted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            parsed_content TEXT UNIQUE
        )
    """)
    
    conn.commit()
    conn.close()

def check_if_data_exists(url, parsed_content):
    """Check if the extracted data already exists for the given URL."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM extracted_data WHERE url = ? AND parsed_content = ?", (url, parsed_content))
    result = cursor.fetchone()
    
    conn.close()
    
    return result is not None  # Returns True if data exists, else False

def insert_parsed_data(url, parsed_content):
    """Insert the parsed data into the database if it does not exist."""
    parsed_json = json.dumps(parsed_content)  # Convert parsed content to JSON format
    
    if not check_if_data_exists(url, parsed_json):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO extracted_data (url, parsed_content) VALUES (?, ?)", (url, parsed_json))
        conn.commit()
        conn.close()
        return f" Added new data for {url}"
    else:
        return f" Data already exists for {url}"



