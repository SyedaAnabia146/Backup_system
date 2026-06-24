# Automated Data Backup and Recovery System

Hi! This is my Python project for the backup and recovery system. I built this using Streamlit for the user interface, SQLite for storing the logs, and Python's threading to run the auto-scheduler in the background.

## What this project does:
* **Manual Backup:** You can type any folder path (like MyData) and copy it into another folder (like MyBackups) as a zip file.
* **Auto Scheduler:** You can set a time in minutes, and it will automatically keep taking backups in the background. You can also stop it anytime with the stop button.
* **Disaster Recovery:** If you want your files back, just select the backup ID from the dropdown, give a folder path, and it will extract everything safely.
* **Integrity Check:** Before extracting, the code checks if the zip file is corrupted or damaged using `zipf.testzip()`. If it's corrupted, it won't extract.
* **Dashboard:** Shows a simple table of all historical backups, total size, and whether they were successful or failed.

## Project Files structure:
* `app.py` - The main UI code for Streamlit.
* `backup_manager.py` - The backend logic, database functions, and threading.
* `backup_history.db` - SQLite database file where all logs are saved.

## How to run it on your computer:

1. First, make sure you have python installed.
2. Open your terminal in this project folder and install the requirements:
   ```bash
   pip install streamlit pandas