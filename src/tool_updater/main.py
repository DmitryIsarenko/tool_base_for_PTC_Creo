import logging

from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrill
from tool_updater.classes.tool_classes.axial.drill import Drill
from tool_updater.classes.tool_classes.axial.countersink import CounterSink
from tool_updater.classes.tool_classes.axial.reamer import Reamer
from tool_updater.classes.tool_classes.axial.tap import Tap
from tool_updater.classes.tool_classes.base_tool import BaseTool
from tool_updater.classes.tool_classes.milling.disk_mill import DiskOtreznoi
from tool_updater.classes.tool_classes.milling.endmill import EndMill
from tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidMill
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import VnutrRadMill
from tool_updater.classes.tool_generator import ToolGenerator

logger = logging.getLogger("src")
# logger = logging.getLogger(__name__)

def main():
    """
        freza_konts_
        freza_konts_udlin_
        freza_konts_strujkolom_
        freza_toroid_
        freza_sfera_
        freza_sfera_udlin_
    freza_uglov_
        freza_otrez_disk_
    freza_grib_
    freza_vnutr_rad_
    rezbofr_metrich_
    rezbofr_trubn_
    centrovka_
        sverlo_
        sverlo_udlin_
    zenkovka_
    cekovka_
    metchik_m..
    metchik_g..
    razvertka_
    blok_rastoch_
    """

    # ToolGenerator.create_tools(
    #     tool_class=BallMill,
    #     file_name_prefix="freza_sfera_",
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        # teeth_num=2,
        # file_name_suffix="_UA100-B2",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\UA100-B2\UA100-B2.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\UA100-B2\UA100-B2_cut_data.json",

        # teeth_num=4,
        # file_name_suffix="_SS600-B4",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\SS600-B4/SS600-B4.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\ballnose_mills\Gesac\SS600-B4/SS600-B4_cut_data.json",
    # )

    # ToolGenerator.create_tools(
    #     tool_class=EndMill,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        # file_name_prefix="freza_konts_",
        # teeth_num=2,
        # file_name_suffix="_UA100-S2",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S2\UA100-S2.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S2\UA100-S2_cut_data.json",

        # teeth_num=3,
        # file_name_suffix="_UA100-S3",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3_cut_data.json",

        # teeth_num=4,
        # file_name_suffix="_UH360-S4",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4).json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4)_cut_data.json",

        # teeth_num=4,
        # file_name_suffix="_STR340-S4",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4).json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4)_cut_data.json",

        # file_name_prefix="freza_konts_udlin_",
        # teeth_num=3,
        # file_name_suffix="_UA100-SL3",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3_cut_data.json",

    #     teeth_num=4,
    #     file_name_suffix="_UP210-SL4",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4).json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4)_cut_data.json",
    # )


    # ToolGenerator.create_tools(
    #     tool_class=Drill,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     debug_mode=0,
    #
    #     teeth_num=1,
    #     file_name_prefix="sverlo_",
    #     file_name_suffix="_2386STI",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\drills\Osawa\hss_regular_drills\2386STI.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\drills\Osawa\hss_regular_drills\2386STI_cut_data.json",
    #
    #     teeth_num=1,
    #     file_name_prefix="sverlo_udlin_",
    #     file_name_suffix="_1692LS",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\drills\Osawa\hss_extended_drills\1692LS.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\drills\Osawa\hss_extended_drills\1692LS_cut_data.json",
    # )

    # ToolGenerator.create_tools(
    #     tool_class=ToroidMill,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     debug_mode=0,
    #
    #     teeth_num=3,
    #     file_name_prefix="freza_toroid_",
    #     file_name_suffix="_UA100-R3",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\toroidal_endmills\Gesac\isoN\UA100-R3\UA100-R3.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\toroidal_endmills\Gesac\isoN\UA100-R3\UA100-R3_cut_data.json",

        # teeth_num=4,
        # file_name_prefix="freza_toroid_",
        # file_name_suffix="_SS600-R4",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\toroidal_endmills\Gesac\isoP_isoM\SS600-R4\SS600-R4.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\toroidal_endmills\Gesac\isoP_isoM\SS600-R4\SS600-R4_cut_data.json",
    # )

    # ToolGenerator.create_tools(
    #     tool_class=DiskOtreznoi,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     teeth_num=1,
    #     debug_mode=0,
    #
    #     file_name_prefix="disk_",
    #     file_name_suffix="_SGSF",
    #     path_to_catalog_geometry=r"/tool_updater/catalogs/milling/otrez_disk\Iscar\SGSF.json",
    #     path_to_catalog_cut_data=r"/tool_updater/catalogs/milling/otrez_disk\Iscar\SGSF_cut_data.json",
    # )

    # ToolGenerator.create_tools(
    #     tool_class=CounterSink,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     teeth_num=1,
    #     debug_mode=0,
    #
    #     file_name_prefix="zenkovka_",
    #     file_name_suffix="",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\countersinks\Precitool\110120\110120.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\countersinks\Precitool\110120\110120_cut_data.json",
    # )

    # ToolGenerator.create_tools(
    #     tool_class=CenterDrill,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     teeth_num=1,
    #     debug_mode=0,
    #
    #     file_name_prefix="centrovka_",
    #     file_name_suffix="",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105200\105200.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105200\105200_cut_data.json",

        # file_name_prefix="centrovka_udlin_",
        # file_name_suffix="",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105600L - extended\105600L.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105600L - extended\105600L_cut_data.json",
    # )

    # ToolGenerator.create_tools(
    #     tool_class=Tap,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     teeth_num=1,
    #     debug_mode=0,
    #
    #     file_name_prefix="metchik_",
    #     file_name_suffix="_gluhoi",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\blind_hole\135850\135850.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\blind_hole\135850\135850_cut_data.json",

        # file_name_prefix="metchik_",
        # file_name_suffix="_skvoznoi",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\through_hole\132640\132640.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\through_hole\132640\132640_cut_data.json",
        #
        # file_name_prefix="metchik_",
        # file_name_suffix="_gluhoi",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\blind_hole\137805\137805.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\blind_hole\137805\137805_cut_data.json",
        #
    #     file_name_prefix="metchik_",
    #     file_name_suffix="_skvoznoi",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\through_hole\133300\133300.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\through_hole\133300\133300_cut_data.json",
    # )

    # ToolGenerator.create_tools(
    #     tool_class=VnutrRadMill,
    #     target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
    #     teeth_num=4,
    #     debug_mode=0,
    #
    #     file_name_prefix="vnutr_rad_",
    #     file_name_suffix="",
    #     path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\internal_R\Precitool\178815\178815.json",
    #     path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\internal_R\Precitool\178815\178815_cut_data.json",
    # )
    #
    ToolGenerator.create_tools(
        tool_class=Reamer,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="razvertka_",
        file_name_suffix="",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1409\1409.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1409\1409_cut_data.json",

        # file_name_prefix="razvertka_udlin_",
        # file_name_suffix="",
        # path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Garant\162961\162961.json",
        # path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Garant\162961\162961_cut_data.json",
    )
    pass


if __name__ == '__main__':
    main()
