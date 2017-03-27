from datetime import datetime
from shutil import copy
import os

def backup(path,file,additional_suffix=None):
    file_to_backup = os.path.join(path,file)
    backup_name = os.path.join('backup',file+'.backup_'+datetime.now().strftime('%Y%m%d'))
    if additional_suffix:
        backup_name = backup_name + additional_suffix
    copy(file_to_backup,backup_name)
