import tkinter as tk
from tkinter import filedialog
from config import *
from utils import *


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x500")
        self.title("Replica")
        self.place_frames()

    def place_frames(self):
        self.fleft = tk.Frame(master=self, height=500,
                              width=200, background="red")
        self.fright = tk.Frame(master=self, height=500,
                               width=650, background="green")
        self.fleft.place(x=0, y=0)
        self.fright.place(x=200, y=0)
        self.fleft_init()
        self.setscreen_backup()

    def fleft_init(self):
        self.l1 = tk.Label(master=self.fleft, text="Backup",
                           background="grey", width=28, height=3)
        self.l1.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.l1.bind("<Button-1>", lambda e: self.setscreen_backup())
        self.l2 = tk.Label(master=self.fleft, text="Restore",
                           background="grey", width=28, height=3)
        self.l2.pack(side=tk.BOTTOM, expand=False)
        self.l2.bind("<Button-1>", lambda e: self.setscreen_restore())

    def fright_reset(self):
        self.fright.destroy()
        self.fright = tk.Frame(master=self, height=500,
                               width=650, background="white")
        self.fright.place(x=200, y=0)

    def setscreen_backup(self):
        self.fright_reset()
        self.lbackup_status = tk.Label(master=self.fright, text="Backup Status: "+("Enabled" if BACKUP_STATUS == True else "Disabled"),
                                     font=("Arial Bold", 20), background="white")
        self.lbackup_status.place(x=20, y=20)
        self.lbackup_summary = tk.Label(
            master=self.fright, text="Backup Summary:", font=("Arial", 12), background="white")
        self.lbackup_summary.place(x=30, y=90)
        self.lbackup_summary_labels_text = ["Last Backup: "+getLastBackupString(), "Total Backups: "+getTotalBackupsString(),
                                           "Backup Location: "+getBackupPath(), "Space utilization: "+getBackupSpaceUtilizationString()]
        self.lbackup_summary_labels = []
        for i, label_text in enumerate(self.lbackup_summary_labels_text):
            self.lbackup_summary_labels.append(tk.Label(master=self.fright, background="white", font=("Normal", 9),
                                                        text=self.lbackup_summary_labels_text[i]))
            self.lbackup_summary_labels[-1].place(x=70, y=130+19*i)
        self.folder_sel_label = tk.Label(
            self.fright, text="Selected folders: ", font=("Arial", 12), background="white")
        self.folder_sel_label.place(x=30, y=220)
        self.text_area = tk.Text(
            self.fright, height=8, width=70, borderwidth=2, relief="groove")
        for folder in BACKUP_FOLDERS():
            self.text_area.insert(tk.END, folder+"\n")
        self.text_area.config(state="disabled")
        self.text_area.place(x=50, y=250)
        self.add_button = tk.Button(
            self.fright, text="Add Folder", command=lambda: self.add_folder(self.text_area))
        self.add_button.place(x=350, y=400)
        self.delete_button = tk.Button(
            self.fright, text="Save changes", command=lambda: self.save_changes(self.text_area))
        self.delete_button.place(x=250, y=400)

        self.context_menu = tk.Menu(self.fright, tearoff=0)
        self.context_menu.add_command(
            label="Delete", command=lambda: self.delete_line())
        self.text_area.bind("<Button-1>", self.show_context_menu)

    def show_context_menu(self,event):
        # calculate the line number of the cursor position
        line_num = int(self.text_area.index("@%s,%s linestart" %
                   (event.x, event.y)).split(".")[0])
        if not self.text_area.get("%d.0" % line_num, "%d.0 lineend" % line_num).strip():
            return
        # activate the text area at the cursor position
        self.text_area.tag_add("sel", "%d.0" % line_num, "%d.0 lineend" % line_num)
        # show the context menu at the mouse position
        self.context_menu.post(event.x_root, event.y_root)
        # deactivate the text area after the context menu is closed
        self.text_area.tag_remove("sel", "1.0", tk.END)

    def save_changes(self,textarea):
         # Split the text area value by newlines
        lines = textarea.get("1.0",tk.END).split('\n')
        # Filter out any empty lines
        lines = [line for line in lines if line.strip()]
        with open("backup_config.json",'w') as f:
            d={"backupfolders":lines}
            f.write(json.dumps(d))


    def delete_line(self):
        self.text_area.config(state="normal")
        # calculate the line number of the selected text
        line_num = int(self.text_area.index("insert").split(".")[0])
        # delete the entire line containing the selected text
        self.text_area.delete("%d.0" % line_num, "%d.0 lineend" % line_num)
        for i in range(line_num, int(self.text_area.index(tk.END).split(".")[0])):
            text = self.text_area.get("%d.0" % (i + 1), "%d.0 lineend" % (i + 1))
            self.text_area.delete("%d.0" % (i + 1), "%d.0 lineend" % (i + 1))
            self.text_area.insert("%d.0" % i, text)
        self.text_area.config(state="disabled")

    def add_folder(self, text_area):
        self.text_area.config(state="normal")
        folder_path = filedialog.askdirectory(initialdir=os.getcwd())
        #check if folder already added:
        lines = text_area.get("1.0",tk.END).split('\n')
        for line in lines:
            if os.path.abspath(line)==os.path.abspath(folder_path):
                return
        text_area.insert(tk.END, folder_path + "\n")
        self.text_area.config(state="disabled")

    def setscreen_restore(self):
        pass


def main():
    w = Window()
    w.mainloop()


if __name__ == '__main__':
    main()
