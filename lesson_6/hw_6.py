import sys
import asyncio
import os
from aiopath import AsyncPath
import aioshutil
from time import time


FORMATS = {"IMAGES": (".jpeg", ".png", ".jpg"),
           "VIDEOS": (".avi", ".mp4", ".mov"),
           "DOCUMENTS": (".doc", ".docx", ".txt", ".pdf",
                         ".xlsx", ".xls", ".pptx", ".csv"),
           "MUSIC": (".mp3", ".ogg", ".wav", ".amr"),
           "ARCHIVE": (".zip", ".tar", ".gztar", ".bztar", ".xztar")}


IGNOR = "ARCHIVE", "IMAGES", "MUSIC", "VIDEOS", "DOCUMENTS", "UNPACKED ARCHIVES"


async def creat_folder(path_to_sorting, folder, files, file):
    path_to_sorting = str(path_to_sorting)
    if not os.path.exists(path_to_sorting + "\\" + folder):
        os.mkdir(path_to_sorting + "\\" + folder)
    if os.path.isfile(files):
        if files != path_to_sorting + "\\" + folder + "\\" + file:
            if file.endswith(FORMATS["ARCHIVE"]):
                name_folder_archive = file.split(".")
                await aioshutil.unpack_archive(files, path_to_sorting + "\\UNPACKED ARCHIVES\\" + name_folder_archive[0])
                os.replace(files, path_to_sorting + "\\" + folder + "\\" + file)
            else:
                os.replace(files, path_to_sorting + "\\" + folder + "\\" + file)


async def remove_folder(folder_path):
    if not os.listdir(folder_path):
        os.removedirs(folder_path)


async def search_file(path_to_sorting, files_list):
    for root, dirs, files in os.walk(path_to_sorting):
        for file in files:
            path_file = os.path.join(root, file)
            ignor_dir = path_file.split("\\")
            for _ in IGNOR:
                if _ not in ignor_dir:
                    files_list.append(path_file)
                else:
                    continue


async def sort_file(path_to_sorting, files_list):
    await asyncio.sleep(0.1)
    for files in files_list:
        file = files.split("\\")
        file = file[-1]
        for folder, format_files in FORMATS.items():
            if file.endswith(format_files):
                await creat_folder(path_to_sorting, folder, files, file)
            else:
                continue


async def main():
    files_list = list()
    try:
        # path_to_sorting = AsyncPath(sys.argv[1])
        path_to_sorting = AsyncPath(r"C:\Users\bohda\OneDrive\Документы\GitHub\goit-python-web\lesson_6\t")
    except Exception:
        print("Wrong! Please try again")

    print(f'Started in {path_to_sorting}')
    start = time()
    await search_file(path_to_sorting, files_list)
    await sort_file(path_to_sorting, files_list)
    for root, dirs, files in os.walk(path_to_sorting):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            await remove_folder(folder_path)
    print(f"Sorting files by the specified path {path_to_sorting} completed succesfully!")
    print(f"Program runtime {round(time() - start, 3)} s")

if __name__ == "__main__":
    asyncio.run(main())
