import os
import shutil


def copyfile_overwrite(src_file_name, dest_file_name):
    if os.path.exists(dest_file_name):
        os.remove(dest_file_name)
    shutil.copyfile(src_file_name, dest_file_name)
