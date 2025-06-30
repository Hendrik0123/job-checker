import time
import os
import google.generativeai as genai
from db.database import create_table, load_websites_from_file
from jobs.checker import check_for_changes
from utils.notify import send_email
from config import CHECK_INTERVAL
from dotenv import load_dotenv

Gemini_API_KEY = os.getenv("Gemini_API_KEY")
genai.configure(api_key=Gemini_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_change(model, url, old_html, new_html):
    prompt = (
        f"Deine Aufgabe ist es Änderungen auf Internetseiten für Stellenangebote zu finden und für Hendrik Becker zusammenzufassen, wenn sie für ihn als Sozialarbeiter relevant sein könnten. Die folgende Webseite hat sich geändert: {url}\n"
        "Fasse die wichtigsten inhaltlichen Änderungen für eine E-Mail verständlich zusammen.\n"
        "Vorher:\n"
        f"{old_html}\n"
        "Nachher:\n"
        f"{new_html}\n"
        "Bitte fasse die Änderungen in wenigen Sätzen zusammen. Falls keine relevanten Änderungen vorgenommen wurden, antworte nur mit 'Keine relevanten Änderungen'.\n"
    )
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else str(response)

def main():
    create_table()

    while True:
        load_websites_from_file()
        changes = check_for_changes()
        for url, result in changes.items():
            if result.get("changed"):
                summary = summarize_change(
                    model,
                    url,
                    result.get("old_html", ""),
                    result.get("new_html", "")
                )
                if summary.strip().lower() == "keine relevanten änderungen":
                    continue
                else:
                    send_email(
                        subject=f"Änderung erkannt auf {url}",
                        body=summary
                    )
        print("jetzt wird gewartet :)")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()