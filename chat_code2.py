import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import datetime
import csv
import schedule
import threading

# Create the main window
window = tk.Tk()
window.title("Data Backup Software")
window.geometry("600x400")
window.configure(bg="#F8F8F8")

# Variable to store the password
password = "12345"  # Set your desired password

# Function to check the entered password
def check_password():
    entered_password = password_entry.get()
    if entered_password == password:
        password_entry.destroy()
        submit_button.destroy()
        #schedule_button.destroy()
        backup_button.config(state=tk.NORMAL)
        restore_button.config(state=tk.NORMAL)
        history_button.config(state=tk.NORMAL)
        logs_button.config(state=tk.NORMAL)
        delete_button.config(state=tk.NORMAL)
        export_button.config(state=tk.NORMAL)
    else:
        messagebox.showerror("Invalid Password", "Incorrect password entered!")
# Create the password entry field
password_entry = tk.Entry(window, show="*")
password_entry.place(x=250, y=50)

# Function to perform backup
def perform_backup():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        backup_folder = filedialog.askdirectory()
        if backup_folder:
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                backup_dir = os.path.join(backup_folder, f"backup_{timestamp}")
                shutil.copytree(selected_folder, backup_dir)
                # Add backup to history
                with open("backup_history.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([backup_dir, selected_folder, timestamp])
                messagebox.showinfo("Backup", "Backup completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Backup failed: {str(e)}")

# Function to perform restore
def perform_restore():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        restore_folder = filedialog.askdirectory()
        if restore_folder:
            try:
                backup_folder = os.path.basename(selected_folder)
                shutil.copytree(selected_folder, os.path.join(restore_folder, backup_folder))
                messagebox.showinfo("Restore", "Restore completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Restore failed: {str(e)}")

# Function to show backup history
def show_backup_history():
    history_window = tk.Toplevel()
    history_window.title("Backup History")
    history_window.geometry("600x400")
    history_window.configure(bg="#F8F8F8")
    # Create table headers
    headers = ["Backup Folder", "Source Folder", "Timestamp", "Action"]
    for i, header in enumerate(headers):
        header_label = tk.Label(history_window, text=header, font=("Arial", 12, "bold"), bg="#F8F8F8")
        header_label.grid(row=0, column=i, padx=10, pady=10)
    # Read backup history from file and populate the table
    with open("backup_history.csv", "r", newline="") as f:
        reader = csv.reader(f)
        for i, backup_parts in enumerate(reader):
            backup_folder_label = tk.Label(history_window, text=backup_parts[0], font=("Arial", 10), bg="#F8F8F8")
            backup_folder_label.grid(row=i+1, column=0, padx=10, pady=10)
            source_folder_label = tk.Label(history_window, text=backup_parts[1], font=("Arial", 10), bg="#F8F8F8")
            source_folder_label.grid(row=i+1, column=1, padx=10, pady=10)
            timestamp_label = tk.Label(history_window, text=backup_parts[2], font=("Arial", 10), bg="#F8F8F8")
            timestamp_label.grid(row=i+1, column=2, padx=10, pady=10)
            restore_button = tk.Button(history_window, text="Restore", width=10,
                                        command=lambda b=i: restore_backup(b))
            restore_button.grid(row=i+1, column=3, padx=10, pady=10)

# Function to restore backup from history
def restore_backup(index):
    with open("backup_history.csv", "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
        if 0 <= index < len(rows):
            selected_folder = rows[index][0]
            restore_folder = filedialog.askdirectory()
            if restore_folder:
                try:
                    backup_folder = os.path.basename(selected_folder)
                    shutil.copytree(selected_folder, os.path.join(restore_folder, backup_folder))
                    messagebox.showinfo("Restore", "Restore completed successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Restore failed: {str(e)}")
        else:
            messagebox.showerror("Error", "Invalid backup index.")

def show_logs():
    logs_window = tk.Toplevel()
    logs_window.title("Logs")
    logs_window.geometry("600x400")
    logs_window.configure(bg="#F8F8F8")

    # Read logs from file
    logs_data = []
    with open("logs.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            logs_data.append(row)

    # Create table headers
    headers = ["Backups Done", "App Opened"]
    for i, header in enumerate(headers):
        header_label = tk.Label(logs_window, text=header, font=("Arial", 12, "bold"), bg="#F8F8F8")
        header_label.grid(row=0, column=i, padx=10, pady=10)

    # Populate the table with logs data
    for i, row in enumerate(logs_data, start=1):
        for j, item in enumerate(row):
            data_label = tk.Label(logs_window, text=item, font=("Arial", 10), bg="#F8F8F8")
            data_label.grid(row=i, column=j, padx=10, pady=10)

def export_backup_history():
    with filedialog.asksaveasfile(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]) as f:
        fieldnames = ["Backup File", "Source Folder", "Timestamp"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        with open("backup_history.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                writer.writerow({"Backup File": row[0], "Source Folder": row[1], "Timestamp": row[2]})
        messagebox.showinfo("Export", "Backup history exported successfully.")


# Function to perform backup in a separate thread
def perform_backup_threaded():
    threading.Thread(target=perform_backup).start()

# Increment the number of backups done
def increment_backups_done():
    backups_done_label["text"] = str(int(backups_done_label["text"]) + 1)

# Increment the number of times the app opened
def increment_app_opened():
    app_opened_label["text"] = str(int(app_opened_label["text"]) + 1)

# Create the backup button
backup_button = tk.Button(window, text="Backup", width=20, command=perform_backup, state=tk.DISABLED)
backup_button.place(x=50, y=50)

#create submit button
submit_button = tk.Button(window, text="Submit", command=check_password)
submit_button.place(x=400, y=50)

# Create the restore button
restore_button = tk.Button(window, text="Restore", width=20, command=perform_restore, state=tk.DISABLED)
restore_button.place(x=50, y=100)

# Create the backup history button
history_button = tk.Button(window, text="Backup History", width=20, command=show_backup_history, state=tk.DISABLED)
history_button.place(x=50, y=150)

# Create the logs button
logs_button = tk.Button(window, text="Logs", width=20, command=show_logs, state=tk.DISABLED)
logs_button.place(x=50, y=200)

# Create the delete backup button
delete_button = tk.Button(window, text="Delete Backup", width=20, command=lambda: delete_backup(selected_index), state=tk.DISABLED)
delete_button.place(x=50, y=250)

# Create the export history button
export_button = tk.Button(window, text="Export History", width=20, command=export_backup_history, state=tk.DISABLED)
export_button.place(x=50, y=300)


# Create the backups done label
backups_done_label = tk.Label(window, text="0", font=("Arial", 12, "bold"), bg="#F8F8F8")
backups_done_label.place(x=250, y=100)

# Create the app opened label
app_opened_label = tk.Label(window, text="0", font=("Arial", 12, "bold"), bg="#F8F8F8")
app_opened_label.place(x=250, y=150)


# Run the main window
window.mainloop()

