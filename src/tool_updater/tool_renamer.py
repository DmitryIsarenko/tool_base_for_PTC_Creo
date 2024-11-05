import os
import io
from pprint import pprint

extension = ".xml"
prefix = ""
suffix = "_B"
new_register = "2"
if_delete_old_files = False

path_pairs = [
    # {
    #     "path_from": r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\rename_from/",
    #     "path_to": r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\rename_to/",
    # },
    {
        "path_from": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Канавочные/",
        "path_to": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Канавочные_B/",
    },
    {
        "path_from": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Проходные/",
        "path_to": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Проходные_B/",
    },
    {
        "path_from": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Расточные/",
        "path_to": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Расточные_B/",
    },
    {
        "path_from": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Резьбовые/",
        "path_to": r"w:\ROBOCOPY\sharing\CREO8_START_NC\Mfg_Settings\mfg_new_tool_dir\Токарные\Резьбовые_B/",
    },
]


def execute_renaming(
        path_from: str,
        path_to: str,
        preffix: str,
        suffix: str,
        new_register: str,
        if_delete_old_files: bool = False,
):
    lst_of_files: list[str] = os.listdir(path=path_from)
    pprint(lst_of_files)

    for old_filename in lst_of_files:
        if extension in old_filename:
            with io.open(file=f"{path_from}{old_filename}", mode="r", encoding="utf-8") as f:
                file_lines = f.readlines()

            new_file_lines = change_tool_id(file_lines=file_lines, preffix=preffix, suffix=suffix)
            new_file_lines = change_register(file_lines=new_file_lines, new_register=new_register)

            new_filename = preffix + old_filename.split(".")[0] + suffix + "." + old_filename.split(".")[1]

            with io.open(file=f"{path_to}{new_filename}", mode="w", encoding="utf-8") as f:
                f.writelines(new_file_lines)

        if if_delete_old_files:
            delete_old_files(path_from)


def delete_old_files(path):
    for filename in os.listdir(path):
        os.remove(path=f"{path}{filename}")


def change_tool_id(file_lines: list[str], preffix, suffix):
    for ind, line in enumerate(file_lines):
        if "<Tool Id=" in line:
            splitted_line = line.split('"')

            splitted_line[1] = preffix + splitted_line[1] + suffix
            new_line = '"'.join(splitted_line)

            file_lines[ind] = new_line
    return file_lines


def change_register(file_lines: list[str], new_register: str):
    for ind, line in enumerate(file_lines):
        if 'Register="' in line:
            full_line_list = line.split('Register')
            right_part_list = full_line_list[1].split('"')
            right_part_list[1] = new_register
            new_right_part = '"'.join(right_part_list)
            new_line = "Register".join([
                full_line_list[0],
                new_right_part,
            ])
            file_lines[ind] = new_line
    return file_lines


if __name__ == '__main__':
    for path in path_pairs:
        execute_renaming(
            path_from=path["path_from"],
            path_to=path["path_to"],
            preffix=prefix,
            suffix=suffix,
            new_register=new_register,
            if_delete_old_files=if_delete_old_files,
        )
