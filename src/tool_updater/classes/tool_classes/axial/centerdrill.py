from src.tool_updater import config
from math import pi
import logging

from src.tool_updater.classes.tool_classes.base_tool import BaseTool

logger = logging.getLogger(__name__)


class CenterDrill(BaseTool):
    # MANUAL TOOL DATA

    """
    Если обычная центровка, то метод len_out_of_holder должен возвращать половину общей длины
    Если удлиненная центровка, то метод len_out_of_holder должен возвращать общую длину минус длину цанги ER16 = 27.5
    """

    tool_material_manual = "HSS"
    tool_type = "CENTER-DRILLING"
    finishing_roughing_options = {
        "roughing": {
            "vc_modifier": 1,  # Множитель для подачи (и на зуб, и на оборот)
            "feed_rate_multiplier": 0.6,  # Множитель для скорости резания
        },
        "finishing": {
            "vc_modifier": 1,
            "feed_rate_multiplier": 0.6,
        },
    }

    axial_depth_modifiyers = {
        "iso_P": 1,
        "iso_M": 1,
        "iso_K": 1,
        "iso_N": 1,
        "iso_S": 1,
        "iso_H": 1,
    }

    def __init__(self,
                 tool_size_from_geom_catalogue: str,
                 catalog_tool_cut_data: dict,
                 catalog_tool_geometry: dict,
                 teeth_num: int,
                 file_name_prefix: str,
                 file_name_suffix: str,
                 debug_mode: int,
                 **kwargs):
        self.tool_size_from_geom_catalogue = tool_size_from_geom_catalogue
        self.catalog_tool_cut_data = catalog_tool_cut_data
        self.catalog_tool_geometry = catalog_tool_geometry
        self.teeth_num = teeth_num
        self.file_name_prefix = file_name_prefix
        self.file_name_suffix = file_name_suffix
        self.debug_mode = debug_mode
        super().__init__(
            tool_size_from_geom_catalogue=self.tool_size_from_geom_catalogue,
            catalog_tool_cut_data=self.catalog_tool_cut_data,
            catalog_tool_geometry=self.catalog_tool_geometry,
            teeth_num=self.teeth_num,
            file_name_prefix=self.file_name_prefix,
            file_name_suffix=self.file_name_suffix,
            debug_mode=self.debug_mode,
        )
        self.point_angle = self.get_tool_point_angle()
        # self.point_diameter = self.get_tool_point_diameter()
        self.drill_diameter = self.get_tool_drill_diameter()
        self.csink_angle = self.get_tool_csink_angle()
        self.drill_length = self.get_tool_drill_length()
        self.set_tool_xml()

    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA
    def create_tool_name_for_geom_catalogue(self):
        t_name = self.tool_data["tool_name_str"]
        return t_name

    def create_tool_name_for_cut_catalogue(self):
        t_name = self.tool_data["tool_diam_float"]
        return t_name

    def create_file_name(self):
        d1 = self.clear_str_from_trailing_zeros(str(self.get_tool_drill_diameter()), sep=".")
        d2 = self.clear_str_from_trailing_zeros(str(self.get_tool_cutter_diam()), sep=".")
        l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".")

        t_name = (
            f"D{d1}"
            f"_D{d2}"
            f"_L{l1}"
            f"_L{l2}"
        )
        return t_name

    def create_tool_name_for_xml(self):
        t_prefix = self.tool_data["file_name_prefix"].upper()
        t_suffix = self.tool_data["file_name_suffix"].upper()

        d1 = self.clear_str_from_trailing_zeros(str(self.get_tool_drill_diameter()), sep=".").replace(".", "-")
        d2 = self.clear_str_from_trailing_zeros(str(self.get_tool_cutter_diam()), sep=".").replace(".", "-")
        l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".").replace(".", "-")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".").replace(".", "-")

        t_name = (
            f"{t_prefix}"
            f"D{d1}"
            f"_D{d2}"
            f"_L{l1}"
            f"_L{l2}"
            f"{t_suffix}"
        )
        return t_name



    def get_tool_point_angle(self) -> int:
        return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["point_angle"]

    def get_tool_csink_angle(self):
        return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["csink_angle"]

    # def get_tool_point_diameter(self) -> int:
    #     return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["point_diameter"]

    def get_tool_drill_diameter(self):
        return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["drill_diameter"]

    def get_tool_drill_length(self):
        return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["drill_length"]

    def get_tool_cutter_diam(self):
        return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["cutter_diam"]



    @staticmethod
    def clear_str_from_trailing_zeros(str_to_clean: str, sep: str):
        new_str = str_to_clean.split(sep=sep)[0]
        try:
            rev_str_pt2 = str_to_clean.split(".")[1][::-1]
            rev_new_pt = ""
            for ch_i, char in enumerate(rev_str_pt2):
                if char != "0":
                    rev_new_pt += char
                else:
                    continue
            if rev_new_pt:
                new_str += sep + rev_new_pt[::-1]
            else:
                new_str += sep + "0"

        except:
            pass
        return new_str

    def calc_len_out_of_holder(self):
        out_of_er = self.get_full_tool_length() - 27.5
        flute = self.get_tool_flute_length()
        diam = float(self.get_tool_cutter_diam())
        if out_of_er >= flute:
            return out_of_er
        else:
            return flute + diam

        # return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["full_body_len"] / 2

    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        try:
            Fn = self.catalog_cut_data[key_iso_material][config.key_fn][self.tool_data["cut_data_diam_group"]]
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            Fn = Fn * RPM * feed_multiplier
            return round(Fn, ndigits=config.NDIGITS_FEED)
        except:
            # logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0

    def calc_feed_per_unit(self, key_iso_material, fin_or_rough: str) -> float:
        try:
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            Fn = self.catalog_cut_data[key_iso_material][config.key_fn][self.tool_data["cut_data_diam_group"]]
            # RPM = self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"]
            Fn = Fn * feed_multiplier
            return round(Fn, ndigits=config.NDIGITS_FEED_PER_UNIT)
        except:
            # logger.critical(f"{self.tool_data["tool_name_str"]} - feed per unit not calculated")
            return 0

    def calc_radial_depth(self, key_iso_material):
        return 0

    # def calc_rpm(self, Vc: int | float) -> float:
    #     try:
    #         rpm = 1000 * Vc / (pi * self.get_cutter_diam())
    #         return round(rpm, ndigits=config.NDIGITS_SPINDLE)
    #     except:
    #         logger.critical(f"{self.tool_data["tool_name_str"]} - RPM not calculated")
    #         return 0

    # def get_cutter_diam(self):
    #     return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["cutter_diam"]

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="DRILL_DIAMETER" Value="{self.drill_diameter}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.get_tool_cutter_diam()}"/>
            <MfgParam Name="POINT_ANGLE" Value="{self.point_angle}"/>
            <MfgParam Name="CSINK_ANGLE" Value="{self.csink_angle}"/>
            <MfgParam Name="DRILL_LENGTH" Value="{self.drill_length}"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>            
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
    """
        logger.debug(f"{self.tool_size_from_geom_catalogue} - xml_tool_params generated...")
        return xml_part_str

    def set_xml_body_tool_cut_data(self):
        total_string = ""
        for material_name, mat_iso_name in config.mfg_materials_dict.items():
            xml_part_str = f"""\
        <ToolCutData>
                <Material>
                    <MfgParam Name="STOCK_MATERIAL" Value="{material_name}"/>
                </Material>
                <CutDataUnitSystem>
                    <MfgParam Name="CUT_DATA_UNITS" Value="METRIC"/>
                </CutDataUnitSystem>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="ROUGHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_rev" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_rev" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
        """
            total_string += xml_part_str

        logger.debug(f"{self.tool_size_from_geom_catalogue} - xml_tool_cut_data generated...")
        return total_string
