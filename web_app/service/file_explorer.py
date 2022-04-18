## credit to the user https://stackoverflow.com/users/1933372/cle 
import os
if os.name == 'nt':
    import win32api, win32con


def folder_is_hidden(f):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(f)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return f.startswith('.') #linux-osx
    
def get_project_files_directories_list(path):
    files_list=[]
    for f in os.listdir(path):
        if not folder_is_hidden(f):
            if not (os.path.isfile(os.path.join(path, f))): ## to get not hiddne folders
                files_list.append(f)
            else:
                if(f.endswith(".pickle")): ## get ony project files
                    files_list.append(f)
                    
    return files_list