import sys
import os
import shutil
import concurrent.futures
from time import sleep, time

SUFFIX_IMAGES = ".jpeg", ".png", ".jpg"
SUFFIX_VIDEOS = ".avi", ".mp4", ".mov"
SUFFIX_DOCUMENTS = ".doc", ".docx", ".txt", ".pdf", ".xlsx", ".xls",".pptx", ".csv"
SUFFIX_MUSIC = ".mp3", ".ogg", ".wav", ".amr"
SUFFIX_ARCHIV = ".zip", ".tar", ".gztar", ".bztar", ".xztar"

IGNOR= "archives", "images", "music", "videos", "documents"

def creat_folder_images(path_to_sorting, files, file):
    if not os.path.exists(path_to_sorting +"\\images"):
        os.mkdir(path_to_sorting + "\\images")
    if files != path_to_sorting + "\\images" + "\\" + file :
        os.replace(files , path_to_sorting + "\\images" + "\\" + file)


def creat_folder_videos(path_to_sorting, files, file):
    if not os.path.exists(path_to_sorting + "\\videos"):
        os.mkdir(path_to_sorting + "\\videos")
    if files != path_to_sorting + "\\videos" + "\\" + file:
        os.replace(files , path_to_sorting + "\\videos" + "\\" + file)

def creat_folder_documents(path_to_sorting, files, file):
    if not os.path.exists(path_to_sorting + "\\documents"):
        os.mkdir(path_to_sorting + "\\documents")
    if files != path_to_sorting + "\\documents" + "\\" + file:
        os.replace(files, path_to_sorting + "\\documents" + "\\" + file)
    
def creat_folder_music(path_to_sorting, files, file):
    if not os.path.exists(path_to_sorting + "\\music"):
        os.mkdir(path_to_sorting + "\\music")
    if files != path_to_sorting + "\\music" + "\\" + file:
        os.replace(files, path_to_sorting + "\\music" + "\\" + file)

def creat_folder_archive(path_to_sorting, files, file):
    if not os.path.exists(path_to_sorting + "\\archives"):
        os.mkdir(path_to_sorting + "\\archives")
    name_folder_archive = file.split(".")
    shutil.unpack_archive(files, path_to_sorting + "\\archives"+ "\\" + name_folder_archive[0])


def sort_file(path_to_sorting, files_list):
    sleep(0.1)
    for files in files_list:

        file = files.split("\\")
        file = file[-1]
      
        if file.endswith(SUFFIX_IMAGES):
            creat_folder_images(path_to_sorting, files, file)
            
        elif file.endswith(SUFFIX_VIDEOS):
            creat_folder_videos(path_to_sorting, files, file)
        
        elif file.endswith(SUFFIX_DOCUMENTS):
            creat_folder_documents(path_to_sorting, files, file)
        
        elif file.endswith(SUFFIX_MUSIC):
            creat_folder_music(path_to_sorting, files, file)

        elif file.endswith(SUFFIX_ARCHIV):
            creat_folder_archive(path_to_sorting, files, file)


def remove_folder(folder_path):
    if not os.listdir(folder_path):
        os.removedirs(folder_path)

def search_file(path_to_sorting, files_list):
     for root, dirs, files in os.walk(path_to_sorting):

        for file in files:
            path_file = os.path.join(root, file)
            # print(f"path_file {path_to_sorting}")
            ignor_dir = path_file.split("\\")
            # print(ignor_dir[6])
            if not ignor_dir[6] in IGNOR:
                files_list.append(path_file)
            


if __name__=="__main__":

    files_list = list()
    try:
        # path_to_sorting = sys.argv[1]
        path_to_sorting = r"C:\Users\Engineer\Desktop\lesson_4\t"
    except Exception:
        print("Wrong! Please try again")

    
    print(f'Started in {path_to_sorting}')
    start = time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(search_file, path_to_sorting, files_list)
        ex.submit(sort_file, path_to_sorting, files_list)
    
    # search_file(path_to_sorting, files_list)
    # sort_file(path_to_sorting, files_list)
    
    for root, dirs, files in os.walk(path_to_sorting):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            remove_folder(folder_path)
    print(time()-start)
    print (f"Sorting files by the specified path {path_to_sorting} completed succesfully!")
   

# 2.55859375 no pull