import time
import requests
import difflib
from bs4 import BeautifulSoup
from db.database import get_websites, get_last_html, save_html

def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    if soup.body:
        # Entferne Skripte, Styles und unsichtbare Elemente
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()
        # Hole nur den sichtbaren Text
        text = soup.body.get_text(separator='\n', strip=True)
        return text
    return ""

def check_for_changes():
    websites = get_websites()
    changes = {}

    for url in websites:
        try:
            response = requests.get(url)
            response.raise_for_status()
            visible_text = extract_visible_text(response.text)

            last_html = get_last_html(url)
            last_visible_text = extract_visible_text(last_html) if last_html else None

            if last_visible_text != visible_text:
                diff = ""
                if last_visible_text is not None:
                    diff = '\n'.join(difflib.unified_diff(
                        last_visible_text.splitlines(),
                        visible_text.splitlines(),
                        fromfile='before',
                        tofile='after',
                        lineterm=''
                    ))
                else:
                    diff = "Kein vorheriger Inhalt vorhanden (erstmaliger Abruf)."

                changes[url] = {
                    "changed": True,
                    "diff": diff,
                    "old_html": last_visible_text,
                    "new_html": visible_text
                }
                save_html(url, response.text, diff)
            else:
                changes[url] = {
                    "changed": False,
                    "diff": ""
                }

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            changes[url] = {
                "changed": None,
                "diff": str(e)
            }

    return changes
