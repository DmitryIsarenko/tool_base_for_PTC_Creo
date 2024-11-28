from src.tool_updater import config
import logging

from src.tool_updater.classes.tool_classes.base_tool import BaseTool

logger = logging.getLogger(__name__)


class ThreadMill(BaseTool):

    # MANUAL TOOL DATA
    tool_material_manual = "HSS"
    tool_type = "THREAD_MILL"

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
    radial_depth_modifiyers = {
        "iso_P": 0.15,
        "iso_M": 0.1,
        "iso_K": 0.1,
        "iso_N": 0.2,
        "iso_S": 0.1,
        "iso_H": 0.025,
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
        self.insert_length = self.get_insert_length()
        self.end_offset = self.get_end_offset()

    def get_insert_length(self):
        return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["cutter_len"]

    def get_end_offset(self):
        return 0

    def get_tool_teeth_num(self):
        return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["feathers_num"]

    def get_tool_diam_float(self):
        return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["flute_diam"]

    def get_cutter_diam(self):
        return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["flute_diam"]

    def get_tool_flute_length(self) -> float:
        l = self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["cutter_len"]
        return l

    def calc_axial_depth(self, key_iso_material) -> float:
        return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["cutter_len"]

    def get_thread_step(self):
        try:
            return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["thread_pitch"]
        except KeyError:
            return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["threads_per_inch"]

    def get_full_tool_length(self) -> float:
        return self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["full_body_len"]

    def calc_len_out_of_holder(self):
        full_body_len = self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["full_body_len"]
        try:
            flute_len = self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["cutter_len_plus_csink"]
        except KeyError:
            flute_len = self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["cutter_len"]

        flute_diam = self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["flute_diam"]

        len_1 = max([flute_len + flute_diam, full_body_len / 2])
        return round(len_1, ndigits=1)

    def calc_nut_diam(self) -> int:
        # try:
        cut_d = self.get_cutter_diam()
        nut_diam = 0
        for er in config.collet_sizes:
            max_d: int = config.collet_sizes[er]["max_diam"]
            if cut_d <= max_d:
                nut_diam: int = config.collet_sizes[er]["nut_diam"]
                break
            else:
                continue
        return nut_diam

    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA
    def create_tool_name_for_geom_catalogue(self):
        t_name = self.tool_data["tool_name_str"]
        return t_name

    def create_tool_name_for_cut_catalogue(self):
        t_name = self.tool_data["tool_diam_float"]
        return t_name

    def create_tool_name_for_xml(self):
        t_prefix = self.tool_data["file_name_prefix"].upper()
        t_suffix = self.tool_data["file_name_suffix"].upper()
        name = self.tool_size_from_geom_catalogue.replace(".", "-")
        d = self.clear_str_from_trailing_zeros(str(self.get_cutter_diam()), sep=".").replace(".", "-")
        l1 = self.clear_str_from_trailing_zeros(str(self.get_insert_length()), sep=".").replace(".", "-")
        l2 = self.clear_str_from_trailing_zeros(str(self.get_full_tool_length()), sep=".").replace(".", "-")

        t_name = (
            f"{t_prefix}"
            f"{name}"
            f"_D{d}"
            f"_L{l1}"
            f"_L{l2}"
            f"{t_suffix}"
        )
        return t_name

    def create_file_name(self):

        name = self.tool_size_from_geom_catalogue
        d = self.clear_str_from_trailing_zeros(str(self.get_cutter_diam()), sep=".")
        l1 = self.clear_str_from_trailing_zeros(str(self.get_insert_length()), sep=".")
        l2 = self.clear_str_from_trailing_zeros(str(self.get_full_tool_length()), sep=".")

        t_name = (
            f"{name}"
            f"_D{d}"
            f"_L{l1}"
            f"_L{l2}"
        )
        return t_name




    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        try:
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            teeth = self.catalog_tool_geometry[self.tool_size_from_geom_catalogue]["feathers_num"]
            Fz = self.catalog_cut_data[key_iso_material][config.key_fz][self.tool_data["cut_data_diam_group"]]
            F = Fz * feed_multiplier * teeth * RPM
            return round(F, ndigits=config.NDIGITS_FEED)
        except:
            # logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0

    def calc_feed_per_unit(self, key_iso_material, fin_or_rough: str) -> float:
        try:
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            Fz = self.catalog_cut_data[key_iso_material][config.key_fz][self.tool_data["cut_data_diam_group"]]
            Fz = Fz * feed_multiplier
            return round(Fz, ndigits=config.NDIGITS_FEED)
        except:
#             logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0



    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="INSERT_LENGTH" Value="{self.insert_length}"/>
            <MfgParam Name="END_OFFSET" Value="{self.end_offset}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
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
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.get_thread_step()}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_AXIAL_DEPTH"]}"/>
                    <MfgParam Name="TOOL_RADIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_RADIAL_DEPTH"]}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.get_thread_step()}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                    <MfgParam Name="TOOL_RADIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_RADIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
        """
            total_string += xml_part_str

        logger.debug(f"xml_tool_cut_data generated...")
        return total_string

