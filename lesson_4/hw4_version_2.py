import sys
import os
import shutil
import concurrent.futures
from time import sleep, time


FORMATS = {"IMAGES": (".jpeg", ".png", ".jpg"),
           "VIDEOS": (".avi", ".mp4", ".mov"),
           "DOCUMENTS": (".doc", ".docx", ".txt", ".pdf",
                         ".xlsx", ".xls", ".pptx", ".csv"),
           "MUSIC": (".mp3", ".ogg", ".wav", ".amr"),
           "ARCHIV": (".zip", ".tar", ".gztar", ".bztar", ".xztar")}


IGNOR = "archives", "images", "music", "videos", "documents"


def creat_folder(path_to_sorting, folder, files, file):
    if not os.path.exists(path_to_sorting + "\\" + folder):
        os.mkdir(path_to_sorting + "\\" + folder)
    if files != path_to_sorting + "\\" + folder + "\\" + file:
        os.replace(files, path_to_sorting + "\\" + folder + "\\" + file)


def remove_folder(folder_path):
    if not os.listdir(folder_path):
        os.removedirs(folder_path)


def search_file(path_to_sorting, files_list):
    for root, dirs, files in os.walk(path_to_sorting):
        for file in files:
            path_file = os.path.join(root, file)
            ignor_dir = path_file.split("\\")
            if not ignor_dir[6] in IGNOR:
                files_list.append(path_file)


def sort_file(path_to_sorting, files_list):
    sleep(0.1)
    for files in files_list:
        file = files.split("\\")
        file = file[-1]
        for folder, format_files in FORMATS.items():
            if file.endswith(format_files):
                creat_folder(path_to_sorting, folder, files, file)
            else:
                continue


if __name__ == "__main__":

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
    for root, dirs, files in os.walk(path_to_sorting):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            remove_folder(folder_path)
    print(time()-start)
    print(f"Sorting files by the specified path {path_to_sorting} completed succesfully!")
