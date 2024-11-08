import logging
from tool_updater.classes.tool_classes.axial.drill import Drill
from tool_updater.classes.tool_classes.base_tool import BaseTool
from tool_updater.classes.tool_generator import ToolGenerator

logger = logging.getLogger("src")

def main():
    ToolGenerator.create_tools(
        tool_class=BaseTool,
        file_name_prefix="sv_test_",
        file_name_suffix="",
        path_to_catalog_geometry="catalogs/templates/geom_test.json",
        path_to_catalog_cut_data="catalogs/drills/Osawa/hss_regular_drills/2386STI_cut_data.json",
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
        debug_mode=True,
    )

    # ToolGenerator.create_tools(
    #     tool_class=Drill,
    #     file_name_prefix="sv_osawa_",
    #     file_name_suffix="",
    #     path_to_catalog_geometry="catalogs/drill/hss_regular_drills/2386STI_geometry.json",
    #     path_to_catalog_cut_data="catalogs/drill/hss_regular_drills/2386STI_cut_data.json",
    #     target_path=r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла\1 hss regular"
    # )
    #
    # ToolGenerator.create_tools(
    #     tool_class=Drill,
    #     file_name_prefix="sv_osawa_",
    #     file_name_suffix="_long",
    #     path_to_catalog_geometry="catalogs/drill/hss_extended_drills/1692LS_geometry.json",
    #     path_to_catalog_cut_data="catalogs/drill/hss_extended_drills/1692LS_cut_data.json",
    #     target_path=r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла\1 hss extended"
    # )



if __name__ == '__main__':
    main()
