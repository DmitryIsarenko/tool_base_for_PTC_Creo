import json

from tool_updater.classes.drill import Drill
from tool_updater.classes.tool_generator import ToolGenerator


# def create_tools(tool_class,
#                  path_to_catalog_geometry:str,
#                  path_to_catalog_cut_data:str,
#                  target_path:str,
#                  ):
#     with open(path_to_catalog_geometry, mode="r") as f:
#         catalog_tool_geometry = json.load(f)
#     with open(path_to_catalog_cut_data, mode="r") as f:
#         catalog_tool_cut_data = json.load(f)
#
#     list_of_tool_sizes = [tool_size for tool_size in catalog_tool_geometry.keys()]
#     list_of_new_drill_obj = list()
#
#     for tool_name in list_of_tool_sizes:
#         tool = tool_class(
#             tool_size=tool_name,
#             catalog_tool_cut_data=catalog_tool_cut_data,
#             catalog_tool_geometry=catalog_tool_geometry,
#         )
#         list_of_new_drill_obj.append(tool)
#
#     for tool in list_of_new_drill_obj:
#         tool.write_new_file(path=target_path)


def main():
    ToolGenerator.create_tools(
        tool_class=Drill,
        file_name_prefix="sv_osawa_",
        file_name_suffix="",
        path_to_catalog_geometry="catalogs/drills/hss_regular_drills/osawa_drills_2386STI_geometry.json",
        path_to_catalog_cut_data="catalogs/drills/hss_regular_drills/osawa_drills_2386STI_cut_data.json",
        target_path=r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла\1 hss regular"
    )
    ToolGenerator.create_tools(
        tool_class=Drill,
        file_name_prefix="sv_osawa_",
        file_name_suffix="_long",
        path_to_catalog_geometry="catalogs/drills/hss_extended_drills/osawa_drills_1692LS_geometry.json",
        path_to_catalog_cut_data="catalogs/drills/hss_extended_drills/osawa_drills_1692LS_cut_data.json",
        target_path=r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла\1 hss extended"
    )


if __name__ == '__main__':
    main()
