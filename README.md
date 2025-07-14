# 🔁 Auto Backup System with Email Notification

A Python automation tool with a user-friendly GUI that lets users back up selected folders at regular intervals. After each backup, an email notification is sent to the user indicating success or failure.

## 🚀 Features

- ✅ Select any folder to back up (source)
- ✅ Choose any destination folder (external drive or another location)
- ✅ Set backup frequency (5 mins, 15 mins, 30 mins, 1 hour)
- ✅ Automated, background backups using threading
- ✅ Email notifications on each backup status (success or failure)
- ✅ GUI built with Tkinter for a professional experience


## 🛠 Technologies Used

- Python 3.7+
- `Tkinter` (GUI)
- `shutil`, `os`, `datetime`, `smtplib`
- `threading` for background task handling

## ⚙️ How It Works

1. User selects:
   - Source folder (to back up)
   - Destination folder (where backup will be stored)
   - Backup interval (e.g., every 30 mins)
2. A background process runs the backup task every X minutes
3. Each backup is saved with a timestamp (e.g., `Backup_2025-07-08_22-30-12`)
4. After every backup:
   - If success → ✅ email sent
   - If failure → ❌ email sent

