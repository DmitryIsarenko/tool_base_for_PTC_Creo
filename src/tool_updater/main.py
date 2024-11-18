import logging
from tool_updater.classes.tool_classes.axial.drill import Drill
from tool_updater.classes.tool_classes.base_tool import BaseTool
from tool_updater.classes.tool_classes.milling.endmill import EndMill
from tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from tool_updater.classes.tool_generator import ToolGenerator

logger = logging.getLogger("src")
# logger = logging.getLogger(__name__)

def main():

    # ToolGenerator.create_tools(
    #     tool_class=BallMill,
    #     file_name_prefix="ballnose_",
    #
    #     # teeth_num=2,
    #     # file_name_suffix="_UA100-B2",
    #     # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\UA100-B2\UA100-B2.json",
    #     # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\UA100-B2\UA100-B2_cut_data.json",
    #
    #     teeth_num=4,
    #     file_name_suffix="_SS600-B4",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\SS600-B4/SS600-B4.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\SS600-B4/SS600-B4_cut_data.json",
    #
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     debug_mode=False,
    #     # debug_mode=True,
    # )

    ToolGenerator.create_tools(
        tool_class=EndMill,
        file_name_prefix="endmill_",

        # teeth_num=2,
        # file_name_suffix="_UA100-S2",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S2\UA100-S2.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S2\UA100-S2_cut_data.json",

        # teeth_num=3,
        # file_name_suffix="_UA100-S3",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3_cut_data.json",

        # teeth_num=3,
        # file_name_suffix="_UA100-SL3",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3_cut_data.json",

        # teeth_num=4,
        # file_name_suffix="_UH360-S4",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4).json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4)_cut_data.json",

        # teeth_num=4,
        # file_name_suffix="_UP210-SL4",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4).json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4)_cut_data.json",

        teeth_num=4,
        file_name_suffix="_STR340-S4",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4).json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4)_cut_data.json",

        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
        debug_mode=False,
        # debug_mode=True,
    )



if __name__ == '__main__':
    main()
