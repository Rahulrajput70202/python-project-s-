import os
import shutil
import smtplib
import threading
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Email Configuration ===
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

# === Auto Backup GUI Class ===
class AutoBackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔁 Auto Backup System with Email Notification")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(False, False)

        self.source_var = StringVar()
        self.dest_var = StringVar()
        self.interval_var = StringVar(value="30 mins")
        self.status_var = StringVar(value="Waiting...")

        self.interval_map = {
            "5 mins": 300,
            "15 mins": 900,
            "30 mins": 1800,
            "1 hour": 3600
        }

        self.running = False
        self.build_ui()

    def build_ui(self):
        Label(self.root, text="Auto Backup System", font=("Segoe UI", 18, "bold"), bg="#f0f2f5", fg="#333").pack(pady=15)

        self.make_picker("📁 Select Source Folder", self.source_var, self.select_source)
        self.make_picker("💾 Select Backup Destination", self.dest_var, self.select_dest)

        Label(self.root, text="⏱ Select Backup Frequency:", bg="#f0f2f5", font=("Segoe UI", 11)).pack(pady=5)
        OptionMenu(self.root, self.interval_var, *self.interval_map.keys()).pack()

        Button(self.root, text="▶️ Start Backup", command=self.start_backup, bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), padx=10, pady=5).pack(pady=10)
        Button(self.root, text="⛔ Stop Backup", command=self.stop_backup, bg="#dc3545", fg="white", font=("Segoe UI", 11, "bold")).pack()

        Label(self.root, textvariable=self.status_var, bg="#f0f2f5", fg="purple", wraplength=550, font=("Segoe UI", 10, "italic")).pack(pady=20)

    def make_picker(self, label_text, variable, command):
        Label(self.root, text=label_text, bg="#f0f2f5", font=("Segoe UI", 11)).pack()
        Button(self.root, text="Browse", command=command, bg="#007bff", fg="white", font=("Segoe UI", 10)).pack()
        Label(self.root, textvariable=variable, bg="#f0f2f5", fg="blue", wraplength=550, font=("Segoe UI", 9)).pack(pady=5)

    def select_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_var.set(path)

    def select_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_var.set(path)

    def send_email(self, subject, message):
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            print("Email error:", e)

    def perform_backup(self):
        while self.running:
            src = self.source_var.get()
            dest_base = self.dest_var.get()
            try:
                if not os.path.exists(src) or not os.path.exists(dest_base):
                    self.status_var.set("⚠️ Folder not found.")
                    self.send_email("📛 Backup Failed", "Source or Destination folder is missing.")
                else:
                    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    dest_folder = os.path.join(dest_base, f"Backup_{now}")
                    shutil.copytree(src, dest_folder)
                    self.status_var.set(f"✅ Backup created at {dest_folder}")
                    self.send_email("✅ Backup Successful", f"Backup created at {dest_folder}")
            except Exception as e:
                self.status_var.set(f"❌ Backup error: {str(e)}")
                self.send_email("❌ Backup Failed", str(e))

            time.sleep(self.interval_map[self.interval_var.get()])

    def start_backup(self):
        if not self.source_var.get() or not self.dest_var.get():
            messagebox.showerror("Missing Info", "Please select both source and destination folders.")
            return

        if not self.running:
            self.running = True
            threading.Thread(target=self.perform_backup, daemon=True).start()
            self.status_var.set("🔁 Backup started...")

    def stop_backup(self):
        self.running = False
        self.status_var.set("⛔ Backup stopped.")

# === Main App ===
if __name__ == "__main__":
    root = Tk()
    app = AutoBackupApp(root)
    root.mainloop()
