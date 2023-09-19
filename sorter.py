from sys import argv
from pathlib import Path
import os
import uuid
import shutil
import logging
from threading import Thread


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


replace_simb = "!@#$%&'№()*+,-/.:;<=>?-\\]^{|}\""

CATEGORIES = {
    "Audio": [".mp3", ".aiff", ".oog", ".wav", ".amr"],
    "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
    "Video": [".avi", ".mp4", ".mov", ".mkv"],
    "Images": [".jpeg", ".png", ".svg", ".jpg", ".gif", ".bmp"],
    "Archives": [".zip", ".rar", ".gz", ".tar"],
}


def unpack_archives(file_path: Path, main_path_folder: Path) -> None:
    archive_path = main_path_folder.joinpath("Archives")

    shutil.unpack_archive(file_path, archive_path, format="zip")
    os.remove(file_path)

    return "Archive unpacked"


def create_logs(new_name: Path, category: str, main_path: Path) -> Path:
    log_file_name = Path(f"{main_path.joinpath(category)}/_{category}.txt")

    with open(log_file_name, "a") as file:
        file.write(f"{new_name}\n")

    if category == "Other":
        log_file_un_ext = Path(f"{main_path}/unknow_ext.txt")
        with open(log_file_un_ext, "a") as file_un_ext:
            file_un_ext.write(f"{new_name.suffix}\n")

    else:
        log_file_kn_ext = Path(f"{main_path}/know_ext.txt")
        with open(log_file_kn_ext, "a") as file_kn_ext:
            file_kn_ext.write(f"{new_name.suffix}\n")


def move_file(path_file: Path, main_path: Path, category: str) -> None:
    sort_dir = main_path.joinpath(category)

    if not sort_dir.exists():
        sort_dir.mkdir()

    new_name = sort_dir.joinpath(f"{normalize(path_file.stem)}{path_file.suffix}")

    if new_name.exists():
        new_name = new_name.with_name(
            f"{new_name.stem}-{uuid.uuid4()}{path_file.suffix}"
        )

    path_after_move = path_file.rename(new_name)

    return path_after_move


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat

    return "Other"


def normalize(name_object: str) -> str:
    trans_name = name_object.translate(TRANS)

    for symbol in trans_name:
        if symbol in replace_simb:
            replace_name = trans_name.replace(symbol, "_")
            trans_name = replace_name

    return trans_name


def get_folder_list(path: Path) -> list:
    for file in path.iterdir():
        if file.is_dir():
            folders.append(file)
            get_folder_list(file)


def get_file_list(folder: Path) -> None:
    for file in folder.iterdir():
        if file.is_file():
            files.append(file)


def remove_empty_folders(main_path: Path) -> None:
    for folders in os.listdir(main_path):
        fold = os.path.join(main_path, folders)
        if os.path.isdir(fold):
            remove_empty_folders(fold)
            if not os.listdir(fold):
                os.rmdir(fold)


def main(file_path: list) -> None:
    try:
        main_path = Path(argv[1])
    except IndexError:
        return "No path to folder"

    if not main_path.exists():
        return f"Folder with path {main_path} dos`n exists."

    category = get_categories(file_path)

    if category == "Archives":
        unpack_archives(file_path, main_path)

    else:
        path_after_move = move_file(file_path, main_path, category)

    create_logs(path_after_move, category, main_path)

    remove_empty_folders(main_path)

    return "Sort is done"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format=" %(message)s")
    main_folder = Path(argv[1])

    # Get folders list

    folders = []
    folders.append(main_folder)
    get_folder_list(main_folder)

    # Get files list with the help of threads
    files = []
    threads_for_iter = []
    for num, path in enumerate(folders):
        th_iter = Thread(target=get_file_list, args=(path,))
        th_iter.start()
        logging.info(f"Start thread for iteration folder#{num}")
        threads_for_iter.append(th_iter)
        [th.join for th in threads_for_iter]

    # Moves file it by using threads

    threads_for_move = []
    for num, path in enumerate(files):
        th_move = Thread(target=main, args=(path,))
        th_move.start()
        logging.info(f"Start thread #{num} for move file")
        threads_for_move.append(th_move)
        [th.join for th in threads_for_move]
