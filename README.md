# Job Checker

Job Checker ist eine Python-Anwendung, die regelmäßig angegebene Webseiten auf Änderungen (z.B. neue Stellenangebote) prüft. Änderungen werden per E-Mail zusammengefasst und versendet. Die zu prüfenden Webseiten werden dynamisch über eine Textdatei verwaltet.

## Projektstruktur

```
job-checker
├── src
│   ├── main.py            # Einstiegspunkt der Anwendung
│   ├── db
│   │   └── database.py    # Datenbankoperationen (Tabellen, Insert, Select, Update)
│   ├── jobs
│   │   └── checker.py     # Logik zum Prüfen und Vergleichen der Webseiten
│   ├── utils
│   │   └── notify.py      # E-Mail-Benachrichtigung
│   └── config.py          # Zentrale Konfiguration (Intervall, DB-URL)
├── requirements.txt       # Abhängigkeiten
├── .env                   # Umgebungsvariablen (API-Keys, Mail-Zugang etc.)
├── .gitignore             # Ausschluss von sensiblen/generierten Dateien
├── job_checker.db         # SQLite-Datenbank (wird automatisch angelegt)
├── websites.txt           # Liste der zu prüfenden Webseiten (eine URL pro Zeile)
└── README.md              # Diese Dokumentation
```

## Installation

1. Repository klonen:
   ```sh
   git clone https://github.com/yourusername/job-checker.git
   cd job-checker
   ```

2. Virtuelle Umgebung anlegen und aktivieren (empfohlen):
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Abhängigkeiten installieren:
   ```sh
   pip install -r requirements.txt
   ```

4. `.env`-Datei anlegen und konfigurieren (siehe unten).

5. `websites.txt` anlegen und pro Zeile eine zu überwachende URL eintragen.

## Konfiguration

Lege eine `.env`-Datei im Projektverzeichnis an, z.B.:

```
EMAIL_FROM=deine@email.de
EMAIL_TO=empfaenger@email.de
EMAIL_USER=dein_email_user
EMAIL_PASSWORD=dein_passwort
SMTP_SERVER=smtp.deinprovider.de
SMTP_PORT=465
Gemini_API_KEY=dein_gemini_api_key
```

Passe das Intervall in `src/config.py` an (`CHECK_INTERVAL` in Sekunden, z.B. 180 für 3 Minuten).

## Nutzung

Starte die Anwendung mit:
```sh
python src/main.py
```

- Die Anwendung prüft regelmäßig alle URLs aus `websites.txt` auf sichtbare Änderungen.
- Änderungen werden per E-Mail zusammengefasst und versendet.
- Neue URLs in `websites.txt` werden automatisch beim nächsten Intervall übernommen.

## Features

- Dynamische Verwaltung der zu prüfenden Webseiten über `websites.txt`
- Nur sichtbare Textänderungen werden erkannt (keine False Positives durch dynamisches HTML)
- Änderungen werden mit Zeitstempel und Diff in der Datenbank gespeichert
- Automatische Zusammenfassung der Änderungen per Google Gemini AI
- E-Mail-Benachrichtigung bei relevanten Änderungen

## Hinweise

- Die Dateien `job_checker.db`, `.env`, `websites.txt` und das Verzeichnis `venv/` sind in `.gitignore` eingetragen und werden nicht mit ins Repository übernommen.
- Für produktiven Einsatz empfiehlt sich ein SMTP-Account mit App-Passwort und ein sicherer Umgang mit API-Keys.

## Beitrag & Support

Beiträge sind willkommen! Bitte öffne ein Issue oder einen Pull Request für Verbesserungen oder neue Features.

---