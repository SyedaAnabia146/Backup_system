import os
import zipfile
import sqlite3
from datetime import datetime
import time
import threading

class BackupManager:
    def __init__(self, db_path="backup_history.db"):
        self.db_path = db_path
        self.scheduler_running = False
        self.scheduler_thread = None
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backup_logs (
                backup_id TEXT PRIMARY KEY,
                mode TEXT,
                source TEXT,
                destination TEXT,
                size_mb REAL,
                status TEXT,
                message TEXT,
                date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _log_to_db(self, backup_id, mode, source, destination, size_mb, status, message):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO backup_logs (backup_id, mode, source, destination, size_mb, status, message, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (backup_id, mode, source, destination, size_mb, status, message, date_str))
        conn.commit()
        conn.close()

    @property
    def history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT backup_id, mode, source, destination, size_mb, status, message, date FROM backup_logs ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        history_list = []
        for r in rows:
            history_list.append({
                "backup_id": r[0],
                "mode": r[1],
                "source": r[2],
                "destination": r[3],
                "size_mb": r[4],
                "status": r[5],
                "message": r[6],
                "date": r[7]
            })
        return history_list

    def create_backup(self, source_path, dest_path, mode="Manual"):
        if not os.path.exists(source_path):
            return {"status": "Fail", "message": "Source directory path not found on disk."}
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"BKP_{timestamp}"
        zip_name = f"backup_{timestamp}.zip"
        final_zip_path = os.path.join(dest_path, zip_name)
        
        try:
            with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isdir(source_path):
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, source_path)
                            zipf.write(full_path, rel_path)
                else:
                    zipf.write(source_path, os.path.basename(source_path))
                    
            size_mb = round(os.path.getsize(final_zip_path) / (1024 * 1024), 2)
            self._log_to_db(backup_id, mode, source_path, final_zip_path, size_mb, "Success", "Backup successfully completed.")
            return {
                "status": "Success",
                "data": {"backup_id": backup_id, "zip_path": final_zip_path, "size_mb": size_mb}
            }
        except Exception as e:
            self._log_to_db(backup_id, mode, source_path, final_zip_path, 0.0, "Fail", str(e))
            return {"status": "Fail", "message": str(e)}

    def restore_backup(self, backup_id, extract_to):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT destination FROM backup_logs WHERE backup_id=?", (backup_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {"status": "Fail", "message": "Backup record metadata not found in database."}
            
        zip_path = row[0]
        if not os.path.exists(zip_path):
            return {"status": "Fail", "message": f"Target zip file archive missing: {zip_path}"}
            
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                corrupt_file = zipf.testzip()
                if corrupt_file is not None:
                    return {"status": "Fail", "message": f"Integrity check failed: Archive corrupt at file {corrupt_file}"}
                
                if not os.path.exists(extract_to):
                    os.makedirs(extract_to)
                zipf.extractall(extract_to)
                
            return {"status": "Success", "message": f"🛡️ Integrity Verified! Data successfully extracted to: {extract_to}"}
        except Exception as e:
            return {"status": "Fail", "message": str(e)}

    def _schedule_worker(self, source, destination, interval_mins):
        while self.scheduler_running:
            self.create_backup(source, destination, mode="Auto")
            for _ in range(int(interval_mins * 60)):
                if not self.scheduler_running:
                    return  # Terminate thread immediately on stop
                time.sleep(1)

    def start_schedule(self, source, destination, interval_mins):
        if self.scheduler_running:
            self.stop_schedule()
            time.sleep(1)

        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(
            target=self._schedule_worker, 
            args=(source, destination, interval_mins), 
            daemon=True
        )
        self.scheduler_thread.start()

    def stop_schedule(self):
        self.scheduler_running = False
        self.scheduler_thread = None