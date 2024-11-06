from tool_updater.classes.tool_classes.axial.drill import Drill
from tool_updater.classes.tool_generator import ToolGenerator


def main():
    # ToolGenerator.create_tools(
    #     tool_class=Drill,
    #     file_name_prefix="sv_test_",
    #     file_name_suffix="",
    #     path_to_catalog_geometry="catalogs/drills/hss_regular_drills/geom_test.json",
    #     path_to_catalog_cut_data="catalogs/drills/hss_regular_drills/osawa_drills_2386STI_cut_data.json",
    #     target_path=r"c:\WORK_DIRECTORY\01 WORK\3 Изменения\база инструмента\mfg_new_tool_dir__idd\3.1 Свёрла/1 hss regular"
    # )

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
