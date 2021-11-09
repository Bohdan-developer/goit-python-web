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


async def normalize(path_to_sorting):

    alphabet = {ord('А'): 'A',
                ord('Б'): 'B',
                ord('В'): 'V',
                ord('Г'): 'G',
                ord('Д'): 'D',
                ord('Е'): 'E',
                ord('Ё'): 'Je',
                ord('Ж'): 'Zh',
                ord('З'): 'Z',
                ord('И'): 'I',
                ord('Й'): 'Y',
                ord('К'): 'K',
                ord('Л'): 'L',
                ord('М'): 'M',
                ord('Н'): 'N',
                ord('П'): 'P',
                ord('Р'): 'R',
                ord('С'): 'S',
                ord('Т'): 'T',
                ord('У'): 'U',
                ord('Ф'): 'F',
                ord('Х'): 'Kh',
                ord('Ц'): 'C',
                ord('Ч'): 'Ch',
                ord('Ш'): 'Sh',
                ord('Щ'): 'Jsh',
                ord('Ъ'): 'Z',
                ord('Ы'): 'Ih',
                ord('Ь'): 'Jh',
                ord('Э'): 'Eh',
                ord('Ю'): 'Ju',
                ord('Я'): 'Ja',
                ord('а'): 'a',
                ord('б'): 'b',
                ord('в'): 'v',
                ord('г'): 'g',
                ord('д'): 'd',
                ord('е'): 'e',
                ord('ё'): 'je',
                ord('ж'): 'zh',
                ord('з'): 'z',
                ord('и'): 'i',
                ord('й'): 'y',
                ord('к'): 'k',
                ord('л'): 'l',
                ord('м'): 'm',
                ord('н'): 'n',
                ord('п'): 'p',
                ord('р'): 'r',
                ord('с'): 's',
                ord('т'): 't',
                ord('у'): 'u',
                ord('ф'): 'f',
                ord('х'): 'kh',
                ord('ц'): 'c',
                ord('ч'): 'ch',
                ord('ш'): 'sh',
                ord('щ'): 'jsh',
                ord('ъ'): 'z',
                ord('ы'): 'ih',
                ord('ь'): 'jh',
                ord('э'): 'eh',
                ord('ю'): 'ju',
                ord('я'): 'ja'}
    for root, dirs, files in os.walk(path_to_sorting):
        for dir in dirs:
            path_folder = os.path.join(root, dir)
            if os.path.exists(path_folder):
                os.rename(str(path_folder), str(path_folder).translate(alphabet))
        for file in files:
            path_file = os.path.join(root, file)
            if os.path.exists(path_file):
                os.rename(str(path_file), str(path_file).translate(alphabet))


async def main():
    files_list = list()
    try:
        path_to_sorting = AsyncPath(sys.argv[1])
    except Exception:
        print("Wrong! Please try again")
    print(f'Started in {path_to_sorting}')
    start = time()
    await normalize(path_to_sorting)
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
