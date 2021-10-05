import sys
import os
import shutil
import concurrent.futures
from time import sleep, time

suffix_imeges = ".jpeg", ".png", ".jpg"
suffix_videos = ".avi", ".mp4", ".mov"
suffix_documents = ".doc", ".docx", ".txt", ".pdf", ".xlsx", ".xls",".pptx", ".csv"
suffix_music = ".mp3", ".ogg", ".wav", ".amr"
suffix_archiv = ".zip", ".tar", ".gztar", ".bztar", ".xztar"

ignor = "archives", "images", "music", "videos", "documents"

def sort_file(p, files_list):
    sleep(0.1)
    for files in files_list:

        file = files.split("\\")
        file = file[-1]
      
        if file.endswith(suffix_imeges):
            if not os.path.exists(p +"\\images"):
                os.mkdir(p + "\\images")
            if  files != p + "\\images" + "\\" + file:
                os.replace(files , p + "\\images" + "\\" + file)
        
        elif file.endswith(suffix_videos):
            if not os.path.exists(p + "\\videos"):
                os.mkdir(p + "\\videos")
            if files != p + "\\videos" + "\\" + file:
                os.replace(files , p + "\\videos" + "\\" + file)
        
        elif file.endswith(suffix_documents):
            if not os.path.exists(p + "\\documents"):
                os.mkdir(p + "\\documents")
            if files != p + "\\documents" + "\\" + file:
                os.replace(files, p + "\\documents" + "\\" + file)
        
        elif file.endswith(suffix_music):
            if not os.path.exists(p + "\\music"):
                os.mkdir(p + "\\music")
            if files != p + "\\music" + "\\" + file:
                os.replace(files, p + "\\music" + "\\" + file)

        elif file.endswith(suffix_archiv):
            if not os.path.exists(p + "\\archives"):
                os.mkdir(p + "\\archives")
            name_folder_archive = file.split(".")
            shutil.unpack_archive(files, p + "\\archives"+ "\\" + name_folder_archive[0])

def remove_folder(f):
    if not os.listdir(f):
        os.removedirs(f)

def search_file(p, files_list):
     for root, dirs, files in os.walk(p):

        for file in files:
            i = os.path.join(root, file)

            ii =i.split("\\")
            if ii[7] in ignor:
                continue
            else:
                files_list.append(i)


if __name__=="__main__":

    files_list = list()
    try:
        p = sys.argv[1]
    except Exception:
        print("Wrong! Please try again")

    
    print(f'Started in {p}')
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(search_file, p, files_list)
        ex.submit(sort_file, p, files_list)

    
    for root, dirs, files in os.walk(p):
        for folder in dirs:
            f = os.path.join(root, folder)
            remove_folder(f)

    print (f"Sorting files by the specified path {p} completed succesfully!")
