import os
from pprint import pprint

from drills import DrillTool

# drills
path_source_dir = r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла\1 hss\\"
path_target_dir = r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла\1 hss new\\"




def list_all_files_in_dir(*, path_to_dir: str) -> list:
    return os.listdir(path=path_to_dir)


def main():
    list_of_names = list_all_files_in_dir(path_to_dir=path_source_dir)
    list_of_new_drill_obj = [DrillTool(file_name=file_name) for file_name in list_of_names]
    for tool in list_of_new_drill_obj:
        tool.write_new_file()


if __name__ == '__main__':
    # pprint(list_all_files_in_dir(path_to_dir=path_source_dir))
    main()