import sqlite3
import datetime
import os

DATABASE_NAME = 'job_checker.db'
WEBSITES_FILE = "/home/hendrik/job-checker/websites.txt"

def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS website_html (
            url TEXT PRIMARY KEY,
            html_content TEXT,
            last_change TIMESTAMP,
            last_diff TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_websites_from_file():
    try:
        with open(WEBSITES_FILE, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        for url in urls:
            add_website(url)
            print(f"{url} geprüft.")
    except FileNotFoundError:
        print(f"{WEBSITES_FILE} nicht gefunden. Bitte Datei anlegen.")

def add_website(url):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO websites (url) VALUES (?)', (url,))
    conn.commit()
    conn.close()

def remove_website(url):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM websites WHERE url = ?', (url,))
    cursor.execute('DELETE FROM website_html WHERE url = ?', (url,))
    conn.commit()
    conn.close()

def get_websites():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT url FROM websites')
    websites = cursor.fetchall()
    conn.close()
    return [website[0] for website in websites]

def get_last_html(url):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT html_content FROM website_html WHERE url = ?', (url,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_html(url, html_content, diff_text):
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    cursor.execute('''
        INSERT INTO website_html (url, html_content, last_change, last_diff)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            html_content=excluded.html_content,
            last_change=excluded.last_change,
            last_diff=excluded.last_diff
    ''', (url, html_content, now, diff_text))
    conn.commit()
    conn.close()