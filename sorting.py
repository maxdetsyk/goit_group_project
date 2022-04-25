import os
from struct import unpack
import sys
import shutil


"""
Sorting
"""

folders_dict = {'images': ('.JPEG', '.PNG', '.JPG', '.SVG'),
          'documents': ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'),
          'video': ('.AVI', '.MP4', '.MOV', '.MKV'),
          'audio': ('.MP3', '.OGG', '.WAV', '.AMR'),
          'archives': ('.ZIP', '.GZ', '.TAR')}

LATIN_SYMBOLS = 'abvhgdezyijklmnoprstuf\'ABVHGDEZYIJKLMNOPRSTUF\''
CYRILLIC_SYMBOLS = 'абвгґдезиійклмнопрстуфьАБВГҐДЕЗИІЙКЛМНОПРСТУФЬ'
TRANS = {}


for l, s in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):
    TRANS[ord(l)] = s


def normalize_names(file_name):
    for sym in file_name:
        if sym not in LATIN_SYMBOLS and sym != int:
            sym.replace(sym, "_")
    return file_name.translate(TRANS)


def create_folders(path):
    for keys in folders_dict.keys():
        if not os.path.exists(os.path.join(path, keys)):
            os.mkdir(os.path.join(path, keys))


def sort_files(file_list, path):
    for file in file_list:
        if not os.path.isfile(os.path.join(path, file)):
            continue
        know = False
        file_name, file_ext = os.path.splitext(file)
        for key, value in folders_dict.items():
            if file_ext.upper() in value:
                src = os.path.join(path, normalize_names(file_name)+file_ext)
                dst = os.path.join(path, key, file_name+file_ext)
                os.replace(src, dst)
                know = True
            continue
        if not know:
            print(f'Unknown: {file_name}')


def unpack_arc(path):
    list_arch = os.listdir(os.path.join(path, "archives"))
    for arch in list_arch:
        file_name, file_ext = os.path.splitext(arch)
        if os.path.isfile(os.path.join(path, "archives", arch)) and (file_ext.upper() in folders_dict.get('archives')):
            shutil.unpack_archive(os.path.join(
                path, "archives", arch), os.path.join(path, "archives", os.path.splitext(arch)[0]))


def make_list_files(path):
    os.listdir(path)
    create_folders(path)
    sort_files(os.listdir(path), path)
    unpack_arc(path)


try:
    ps_2 = sys.argv[1]
    make_list_files(ps_2)
except IndexError as e:
    print(e)
