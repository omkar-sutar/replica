import tkinter as tk
from config import *
from utils import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x500")
        self.title("Replica")
        self.place_frames()
    def place_frames(self):
        self.fleft=tk.Frame(master=self,height=500,width=200,background="red")
        self.fright=tk.Frame(master=self,height=500,width=650,background="green")
        self.fleft.place(x=0,y=0)
        self.fright.place(x=200,y=0)
        self.fleft_init()
        self.setscreen_backup()
    def fleft_init(self):
        self.l1=tk.Label(master=self.fleft,text="Backup",background="grey",width=28,height=3)
        self.l1.pack(side=tk.TOP,fill=tk.X,expand=False)
        self.l1.bind("<Button-1>", lambda e: self.setscreen_backup())
        self.l2=tk.Label(master=self.fleft,text="Restore",background="grey",width=28,height=3)
        self.l2.pack(side=tk.BOTTOM,expand=False)
        self.l2.bind("<Button-1>", lambda e: self.setscreen_restore())
    def fright_reset(self):
        self.fright.destroy()
        self.fright=tk.Frame(master=self,height=500,width=650,background="white")
        self.fright.place(x=200,y=0)
    def setscreen_backup(self):
        self.fright_reset()
        self.lbackup_status=tk.Label(master=self.fright,text="Backup Status: "+("Enabled" if BACKUP_STATUS==True else "Disabled"),
                                     font=("Arial Bold",20),background="white")
        self.lbackup_status.place(x=20,y=20)
        self.lbackup_summary=tk.Label(master=self.fright,text="Backup Summary:",font=("Arial",12),background="white")
        self.lbackup_summary.place(x=30,y=90)
        self.lbackup_summary_labels_text=["Last Backup: "+getLastBackupString(),"Total Backups: "+getTotalBackupsString(),
                                          "Backup Location: "+getBackupPath(),"Space utilization: "+getBackupSpaceUtilizationString()]
        self.lbackup_summary_labels=[]
        for i,label_text in enumerate(self.lbackup_summary_labels_text):
            self.lbackup_summary_labels.append(tk.Label(master=self.fright,background="white",font=("Normal",9),
                                                        text=self.lbackup_summary_labels_text[i]))
            self.lbackup_summary_labels[-1].place(x=70,y=130+19*i)
        

    def setscreen_restore(self):
        pass
def main():
    w=Window()
    w.mainloop()

if __name__ == '__main__':
    main()
