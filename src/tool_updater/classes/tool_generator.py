import json
import os


class ToolGenerator:
    @staticmethod
    def create_tools(*,
                     tool_class,
                     path_to_catalog_geometry: str,
                     path_to_catalog_cut_data: str,
                     teeth_num:int,
                     target_path: str,
                     file_name_prefix: str,
                     file_name_suffix: str,
                     debug_mode: int,
                     ):
        with open(path_to_catalog_geometry, mode="r") as f:
            catalog_tool_geometry = json.load(f)
        with open(path_to_catalog_cut_data, mode="r") as f:
            catalog_tool_cut_data = json.load(f)

        list_of_tool_sizes = [tool_size for tool_size in catalog_tool_geometry.keys()]
        list_of_new_tool_obj = list()

        for tool_size in list_of_tool_sizes:
            tool = tool_class(
                tool_size_from_geom_catalogue=tool_size,
                catalog_tool_cut_data=catalog_tool_cut_data,
                catalog_tool_geometry=catalog_tool_geometry,
                teeth_num=teeth_num,
                file_name_prefix=file_name_prefix,
                file_name_suffix=file_name_suffix,
                debug_mode=debug_mode,
            )
            list_of_new_tool_obj.append(tool)

        for t in list_of_new_tool_obj:
            print(t.tool_data["tool_name_str"])

        if not os.path.exists(target_path):
            os.makedirs(target_path)

        for tool in list_of_new_tool_obj:
            tool.set_tool_xml()
            tool.write_new_file(path=target_path)
