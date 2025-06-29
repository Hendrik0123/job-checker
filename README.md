# Job Checker

Job Checker is a Python application that regularly checks specified websites for job postings. It allows users to add or remove websites to monitor and manages the data using an SQL database.

## Project Structure

```
job-checker
├── src
│   ├── main.py          # Entry point of the application
│   ├── db
│   │   └── database.py  # Database operations
│   ├── jobs
│   │   └── checker.py   # Logic for checking job postings
│   ├── utils
│   │   └── scheduler.py  # Scheduling of job checks
│   └── config.py        # Configuration settings
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/job-checker.git
   cd job-checker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Configure the database connection and scheduling intervals in `src/config.py`.
2. Run the application:
   ```
   python src/main.py
   ```

## Features

- Add and remove websites to monitor for job postings.
- Periodically check for new job postings on specified websites.
- Store and manage website data using an SQL database.

## Contribution

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to add.