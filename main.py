import os
from pprint import pprint



def list_all_files_in_dir(*, path_to_dir: str) -> list:
    return os.listdir(path=path_to_dir)


if __name__ == '__main__':
    path = r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла\1 hss\\"
    pprint(list_all_files_in_dir(path_to_dir=path))