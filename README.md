<<<<<<< HEAD
# Automated Data Backup and Recovery System
=======
<<<<<<< HEAD
# 🔄 Automated Data Backup & Recovery System
>>>>>>> f0e6462 (Add remaining project assets and configurations)

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

<<<<<<< HEAD
1. First, make sure you have python installed.
2. Open your terminal in this project folder and install the requirements:
   ```bash
   pip install streamlit pandas
=======
This implementation includes all advanced target milestones specified in the evaluation guidelines:

1.  **Production ZIP Compression:** Reduces storage footprints by utilizing `zipfile.ZIP_DEFLATED` algorithms to securely bundle directory structures into time-stamped portable archives.
2.  **Dedicated Automation User Interface:** A dedicated management view allowing dynamic setup, tracking, active background status verification, and safe instant termination of the automated scheduler thread.
3.  **Disaster Recovery & Integrity Verification:** Bypasses extraction if a file is damaged. It evaluates the archive layout via CRC32 validation hashes using `zipf.testzip()` before executing extraction sequences to ensure clean data restoration.

## 🛠️ Tech Stack & Architecture

* **Frontend UI:** Streamlit (Custom Premium Light Theme CSS Layout)
* **Core Logic Engine:** Python 3 (Threading, ZipFile, OS File System Operations)
* **Database Management:** SQLite3 (Local Persistent Storage Layer)
* **Data Manipulation:** Pandas

## 📁 Directory Structure

```text
BACKUP_SYSTEM/
│
├── MyData/               # Source folder containing your raw data files
├── MyBackups/            # Destination folder where compressed ZIP archives are saved
├── app.py                # Main Streamlit user interface & responsive layouts
├── backup_manager.py     # Backend automation logic, database management & recovery engine
├── backup_history.db     # SQLite database storing file records (generated automatically)
├── backup_history.json   # Backup metadata configuration logs
└── README.md             # Project documentation and architectural overview
=======
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
>>>>>>> 862b180 (Add documentation)
>>>>>>> f0e6462 (Add remaining project assets and configurations)
