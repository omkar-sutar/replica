from config import *
import os
from datetime import datetime
import shutil
import time

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

def doBackup():
    new_backup_dir=os.path.join(getBackupPath(),datetime.now().strftime("20%y-%m-%d-%H-%M-%S"))
    os.makedirs(new_backup_dir)
    os.chdir(new_backup_dir)
    tree=getDirectoryTree()
    f=open(os.path.join(new_backup_dir,"data.txt"),mode="w")
    for folder in BACKUP_FOLDERS:
        if not os.path.exists(folder):
            continue
        dst=os.path.basename(os.path.normpath(folder))
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copytree(folder,dst,dirs_exist_ok=True)
        f.write(f"{folder},{os.path.join(new_backup_dir,dst)}\n")
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
    for folder in BACKUP_FOLDERS:
        for dirpath,subdirectories,files in os.walk(top=folder,topdown=False):
            tree.append((dirpath,subdirectories,files))
    return tree

# x=doBackup()
# time.sleep(7)
# doRestore(x)