from config import *
import os
from datetime import datetime
import shutil
import time

def BACKUP_FOLDERS():
    f=open("backup_config.json","r")
    j=json.load(f)
    f.close()
    return j.get("backupfolders")

def start_backup():
    pass
def getLastBackupString():
    path=getBackupPath()
    dirs=get_directories_sorted_by_last_modified(path)
    if len(dirs)==0:
        return "N/A"
    return dirs[0]

def getTotalBackupsString():
    path=getBackupPath()
    cnt=0
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            cnt+=1
    return str(cnt)
    

def get_directories_sorted_by_last_modified(path):
    directories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item_path)
    # Sort directories based on last modified time in descending order
    directories.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
    return directories

def getBackupPath():
    path=os.path.join(BACKUP_DIRECTORY,DEVICE_NAME)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
def getBackupSpaceUtilizationString():
    total_size = 0.
    for dirpath, dirnames, filenames in os.walk(getBackupPath()):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    # Convert total size to megabytes
    size_mb = total_size / (1024 * 1024)
    return str(round(size_mb,2))+" MB"

def create_new_backup_dir():
    new_backup_dir=os.path.join(getBackupPath(),datetime.now().strftime("20%y-%m-%d-%H-%M-%S"))
    os.makedirs(new_backup_dir)
    return new_backup_dir

def doBackup(new_backup_dir=None):
    if new_backup_dir==None:
        new_backup_dir=create_new_backup_dir() 
    f=open(os.path.join(new_backup_dir,"data.txt"),mode="w")
    for folder_path in BACKUP_FOLDERS():
        if not os.path.exists(folder_path):
            continue
        folder_name=os.path.basename(os.path.normpath(folder_path))
        dst=os.path.join(new_backup_dir,folder_name)
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copytree(folder_path,dst,dirs_exist_ok=True)
        f.write(f"{folder_path},{dst}\n")
    f.close()
    return os.path.abspath(new_backup_dir)

def doRestore(backupString,remove_existing=False):
    f=open(os.path.join(backupString,"data.txt"),'r')
    for line in f.readlines():
        paths=line.split(',')
        dst=paths[0]
        src=paths[1][:-1]
        if remove_existing:
            os.removedirs(dst)
        shutil.copytree(src,dst,dirs_exist_ok=True)
    

def getDirectoryTree():
    tree=[]
    for folder in BACKUP_FOLDERS():
        for dirpath,subdirectories,files in os.walk(top=folder,topdown=False):
            tree.append((dirpath,subdirectories,files))
    return tree

def getButtonTheme():
    return {"background":"#4287f5","foreground":"white"}

#x=doBackup()
#time.sleep(7)
# doRestore(x)