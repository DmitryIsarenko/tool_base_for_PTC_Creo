from copy import deepcopy
from math import pi
import io
import datetime
from src.tool_updater import config
from src.tool_updater.default_tool_dict import default_tool_dict

import logging

logger = logging.getLogger(__name__)


# noinspection PyBroadException
class BaseTool:
    # BASIC DATA
    tool_file_extension = ".xml"
    DATETIME = datetime.datetime.today().strftime("%Y - %m-%dT%H:%M:%S")
    # DATETIME = "2024 - 11-13T12:12:12"

    # MANUAL TOOL DATA
    tool_type = "default tool type"
    tool_material_manual = "HSS"

    holder_len_manual = 50

    # vc_min_or_max = 0  # 0 для минимальной скорости, -1 для максимальной, если их указано две или более
    finishing_roughing_options = {
        "roughing": {
            "vc_modifier": 1,  # Множитель для подачи (и на зуб, и на оборот)
            "feed_rate_multiplier": 0.6,  # Множитель для скорости резания
        },
        "finishing": {
            "vc_modifier": 1.2,
            "feed_rate_multiplier": 0.4,
        },
    }

    peck_depth_modifier_common = 0.25  # Общий множитель глубины прерывистого сверления (доля диаметра)
    peck_depth_modifier_iso_P = 1.5  # умножается на величину общего peck depth
    peck_depth_modifier_iso_M = 1  # умножается на величину общего peck depth
    peck_depth_modifier_iso_N = 2  # умножается на величину общего peck depth

    axial_depth_modifiyers = {
        "iso_P": 1.5,
        "iso_M": 1.5,
        "iso_K": 1.5,
        "iso_N": 1.5,
        "iso_S": 1.5,
        "iso_H": 1.5,
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
                 debug_mode: bool,
                 **kwargs):
        self.debug = debug_mode
        self.teeth_num = teeth_num
        if self.debug:
            config.finishing_roughing_options = {
                "roughing": {
                    "vc_modifier": 1,  # Множитель для подачи (и на зуб, и на оборот)
                    "feed_rate_multiplier": 1,  # Множитель для скорости резания
                },
                "finishing": {
                    "vc_modifier": 1,
                    "feed_rate_multiplier": 1,
                },
            }
        # 0 Задаем первоначальную структуру словаря значений параметров инструмента
        self.set_default_tool_data()

        # 1.1 Сохраняем имя инструмента в виде строки
        self.tool_data["tool_name_str"] = tool_size_from_geom_catalogue

        # 1.2 Сохраняем какие префиксы и суффиксы будут при имени файла
        self.tool_data["file_name_prefix"] = file_name_prefix
        self.tool_data["file_name_suffix"] = file_name_suffix

        # 1.3 Объявление каталогов
        self.catalog_geom = catalog_tool_geometry
        self.catalog_cut_data = catalog_tool_cut_data

        # 2.0 Независимые данные
        self.tool_data["HOLDER_LEN"] = self.holder_len_manual

        # 2.1 Создание данных, основанных на имени (диаметре) инструмента
        self.tool_data["tool_diam_float"] = float(self.tool_data["tool_name_str"])
        self.tool_data["CUTTER_DIAM"] = self.tool_data["tool_name_str"]
        self.tool_data["cut_data_diam_group"] = self.calc_diam_group_name()
        self.tool_data["HOLDER_DIA"] = self.calc_nut_diam()

        # 2.2 Объявление имен, по которым будет совершаться поиск в каталогах
        self.tool_data["tool_name_for_geom_catalogue"] = self.create_tool_name_for_geom_catalogue()
        self.tool_data["tool_name_for_cut_catalogue"] = self.create_tool_name_for_cut_catalogue()

        # 3 Объявление переменных, используемых в XML
        self.tool_data["TOOL_MATERIAL"] = self.tool_material_manual
        self.tool_data["NUM_OF_TEETH"] = self.teeth_num
        self.tool_data["tool_type"] = self.tool_type

        # 3.1 Получение данных из каталога геометрии
        self.tool_data["LENGTH"] = self.get_tool_length()
        self.tool_data["FLUTE_LENGTH"] = self.get_tool_flute_length()
        self.tool_data["TOOL_COMMENT"] = self.get_tool_comment()

        # 3.2 Создание данных, основанных на данных из каталога геометрии
        self.tool_data["len_out_of_holder"] = self.calc_len_out_of_holder()
        self.tool_data["tool_name_str"] = self.create_tool_name()
        self.tool_data["file_name"] = self.create_file_name()

        # 3.3 Расчет режимов резания для всех групп материалов
        self.calc_cut_data_for_all_material_groups()

        # 4 Генерация XML
        self.set_tool_xml()

    #
    #
    #
    # GET FROM GEOM CATALOGUE
    def get_tool_length(self) -> float:
        try:
            t_name = self.tool_data["tool_name_for_geom_catalogue"]
            fractional_part = t_name.split(".")[1]
            if len(fractional_part) < 2:
                t_name += "0"
            return self.catalog_geom[t_name][config.key_body_len]
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - Tool len not found")
            return 0

    def get_tool_flute_length(self) -> float:
        try:
            t_name = self.tool_data["tool_name_for_geom_catalogue"]
            fractional_part = t_name.split(".")[1]
            if len(fractional_part) < 2:
                t_name += "0"
            return self.catalog_geom[t_name][config.key_flute_len]
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - Tool flute len not found")
            return 0

    def get_tool_comment(self) -> str:
        try:
            t_name = self.tool_data["tool_name_for_geom_catalogue"]
            return self.catalog_geom[t_name][config.key_order_no]
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - Tool flute len not found")
            return ""

    #
    #
    #
    # GET FROM CUT DATA CATALOGUE
    def get_vc(self, key_iso_material: str, fin_or_rough):
        try:
            vc_data = self.catalog_cut_data[key_iso_material][config.key_vc]
            if type(vc_data) is int or type(vc_data) is float:
                vc_data *= self.finishing_roughing_options[fin_or_rough]["vc_modifier"]
                return vc_data
            if type(vc_data) is list or type(vc_data) is set or type(vc_data) is tuple:
                vc_data = vc_data[config.vc_min_or_max]
                vc_data *= self.finishing_roughing_options[fin_or_rough]["vc_modifier"]
                vc_data = round(vc_data, ndigits=config.NDIGITS_SURFACE_SPEED)
                return vc_data
        except KeyError:
            logger.critical(f"{self.tool_data["tool_name_str"]} - Vc not found")
            return 0

    #
    #
    #
    # CALCULATIONS FOR GEOMETRY CATALOGUE
    def calc_diam_group_name(self):
        try:
            iso_key = list(self.catalog_cut_data.keys())[0]
            diam_groups = [key for key in self.catalog_cut_data[iso_key][config.key_f]]
            t_diam = self.tool_data["tool_diam_float"]
            suitable_grp = list()
            for grp_ind, grp in enumerate(diam_groups):
                grp_float = float(grp)
                if t_diam == grp_float:
                    suitable_grp.append(grp)
                    break
                elif t_diam > grp_float:
                    suitable_grp.append(grp)
                elif t_diam < grp_float:
                    if grp_ind == 0:
                        suitable_grp.append(grp)
                    break

            return suitable_grp[-1]
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - Diam group not calculated")
            return "None"

    #
    #
    #
    # CALCULATIONS FOR CUT DATA CATALOGUE
    def calc_cut_data_for_all_material_groups(self):
        for key_iso_material in config.lst_of_material_groups:
            for fin_or_rough in self.finishing_roughing_options:
                tool_surface_speed = self.get_vc(key_iso_material=key_iso_material, fin_or_rough=fin_or_rough)
                tool_spindle_rpm = self.calc_rpm(Vc=tool_surface_speed)

                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SURFACE_SPEED"] = tool_surface_speed
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"] = tool_spindle_rpm

                tool_feed_per_unit = self.calc_feed_per_unit(key_iso_material=key_iso_material,
                                                             fin_or_rough=fin_or_rough)
                tool_feed_rate = self.calc_feed_rate(key_iso_material=key_iso_material, RPM=tool_spindle_rpm,
                                                     fin_or_rough=fin_or_rough)
                tool_axial_depth = self.calc_axial_depth(key_iso_material=key_iso_material)
                tool_radial_depth = self.calc_radial_depth(key_iso_material=key_iso_material)

                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_PER_UNIT"] = tool_feed_per_unit
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_RATE"] = tool_feed_rate
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_AXIAL_DEPTH"] = tool_axial_depth
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_RADIAL_DEPTH"] = tool_radial_depth

    def calc_rpm(self, Vc: int | float) -> float:
        try:
            rpm = 1000 * Vc / (pi * self.tool_data["tool_diam_float"])
            return round(rpm, ndigits=config.NDIGITS_SPINDLE)
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - RPM not calculated")
            return 0

    def calc_feed_per_unit(self, key_iso_material, fin_or_rough: str) -> float:
        try:
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            F = self.catalog_cut_data[key_iso_material][config.key_f][self.tool_data["cut_data_diam_group"]]
            RPM = self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"]
            fz = F / RPM / self.tool_data["NUM_OF_TEETH"] * feed_multiplier
            return round(fz, ndigits=config.NDIGITS_FEED_PER_UNIT)
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - feed per unit not calculated")
            return 0

    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        try:
            Fn = self.catalog_cut_data[key_iso_material][config.key_fn][self.tool_data["cut_data_diam_group"]]
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            rpm = Fn * RPM * feed_multiplier
            return round(rpm, ndigits=config.NDIGITS_FEED)
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0

    def calc_axial_depth(self, key_iso_material) -> float:
        try:
            axial_depth = float(self.tool_data["CUTTER_DIAM"]) * self.axial_depth_modifiyers[key_iso_material]
            return round(axial_depth, ndigits=config.NDIGITS_AXIAL_FEED)
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - axial depth not calculated")
            return 0

    def calc_radial_depth(self, key_iso_material):
        try:
            radial_depth = float(self.tool_data["CUTTER_DIAM"]) * self.radial_depth_modifiyers[key_iso_material]
            return round(radial_depth, ndigits=config.NDIGITS_RADIAL_FEED)
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - radial depth not calculated")
            return 0

    def calc_nut_diam(self) -> int:
        # try:
        cut_d = float(self.tool_data.get("CUTTER_DIAM"))
        nut_diam = 0
        for er in config.collet_sizes:
            max_d: int = config.collet_sizes[er]["max_diam"]
            if cut_d <= max_d:
                nut_diam: int = config.collet_sizes[er]["nut_diam"]
                break
            else:
                continue
        return nut_diam

    # except:
    #     logger.critical(f"{self.tool_data["tool_name_str"]} - nut diam not calculated")
    #     return 0

    def calc_len_out_of_holder(self):
        try:
            length = round(float(self.tool_data["FLUTE_LENGTH"]) + float(self.tool_data["CUTTER_DIAM"]), ndigits=0, )
            return length
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - nut diam not calculated")
            return 0

    #
    #
    #
    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA
    def create_tool_name_for_geom_catalogue(self):
        t_name = self.tool_data["tool_name_str"]
        return t_name

    def create_tool_name_for_cut_catalogue(self):
        t_name = self.tool_data["tool_diam_float"]
        return t_name

    def create_tool_name(self):
        t_prefix = self.tool_data["file_name_prefix"].upper()
        t_suffix = self.tool_data["file_name_suffix"].upper()
        t_name = f"{t_prefix}D{self.tool_data["CUTTER_DIAM"].replace(".", "-")}_L{self.tool_data["FLUTE_LENGTH"]}-{self.tool_data["LENGTH"]}{t_suffix}"
        return t_name

    def create_file_name(self):
        t_name = f"D{self.tool_data["tool_diam_float"]}_L{self.tool_data["FLUTE_LENGTH"]}-{self.tool_data["LENGTH"]}"
        return t_name

    #
    #
    #
    # FILE OPERATIONS
    def write_new_file(self, path):
        try:
            with io.open(
                    file=f"{path}\\{self.tool_data["file_name_prefix"]}{self.tool_data["file_name"]}{self.tool_data["file_name_suffix"]}{self.tool_file_extension}",
                    mode="w",
                    encoding="utf-8",
            ) as f:
                # f.writelines(body_lines)
                f.writelines(self.tool_xml)
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - file not created")
            pass

    #
    #
    #
    # DEFAULT TOOL DICT
    def set_default_tool_data(self):

        self.tool_data = deepcopy(default_tool_dict)

    #
    #
    #
    # XML DEFINITION
    def set_tool_xml(self):
        if self.debug is False:
            try:
                self.tool_xml = ""
                self.tool_xml += self.set_xml_head()
                self.tool_xml += self.set_xml_body_tool_params()
                self.tool_xml += self.set_xml_body_tool_cut_data()
                self.tool_xml += self.set_xml_bom_components()
                self.tool_xml += self.set_xml_tail()
            except:
                self.tool_xml = "ERROR IN XML GENERATION"
                logger.critical(f"{self.tool_data["tool_name_str"]} - XML not created")
        else:
            # try:
            self.tool_xml = \
                f"""\
<?xml version="1.0" encoding="UTF-8"?>
<DateTime>{self.DATETIME}</DateTime>
<Tool Id="{self.tool_data["tool_name_str"]}" RefXmlId="encref_1" Type="BASIC DRILL">

Общие:
    "GAUGE_X_LENGTH": "{self.tool_data["GAUGE_X_LENGTH"]}",
    "GAUGE_Z_LENGTH": "{self.tool_data["GAUGE_Z_LENGTH"]}",
    "LENGTH_UNITS": "{self.tool_data["LENGTH_UNITS"]}",
    "TOOL_MATERIAL": {self.tool_data["TOOL_MATERIAL"]},
    "TOOL_COMMENT": {self.tool_data["TOOL_COMMENT"]},
    "SPINDLE_SENSE": "{self.tool_data["SPINDLE_SENSE"]}",
    "COOLANT_OPTION": "{self.tool_data["COOLANT_OPTION"]}",
    "COOLANT_PRESSURE": "{self.tool_data["COOLANT_PRESSURE"]}",
# геометрия
    "CUTTER_DIAM": {self.tool_data["CUTTER_DIAM"]},
    "NUM_OF_TEETH": {self.tool_data["NUM_OF_TEETH"]},
    "HOLDER_DIA": {self.tool_data["HOLDER_DIA"]},
    "HOLDER_LEN": {self.tool_data["HOLDER_LEN"]},
    "LENGTH": {self.tool_data["LENGTH"]},
    "FLUTE_LENGTH": {self.tool_data["FLUTE_LENGTH"]},
    "len_out_of_holder": {self.tool_data["len_out_of_holder"]},
    "cut_data_diam_group": {self.tool_data["cut_data_diam_group"]},
# фрезы
# фрезы тороидальные
    "CORNER_RADIUS": {self.tool_data["CORNER_RADIUS"]},
# сверла
# центровки
    "POINT_ANGLE": {self.tool_data["POINT_ANGLE"]},
    "CSINK_ANGLE": {self.tool_data["CSINK_ANGLE"]},
# резьбофрезы
    "INSERT_LENGTH": {self.tool_data["INSERT_LENGTH"]},
    "END_OFFSET": {self.tool_data["END_OFFSET"]},
# не сортированное
    "SIDE_ANGLE": {self.tool_data["SIDE_ANGLE"]},
    "TOOL_LONG_FLAG": {self.tool_data["TOOL_LONG_FLAG"]},
    "CUT_LENGTH": {self.tool_data["CUT_LENGTH"]},
    "TIP_LENGTH": {self.tool_data["TIP_LENGTH"]},
    "SHANK_DIAM": {self.tool_data["SHANK_DIAM"]},
    "COMP_OVERSIZE": {self.tool_data["COMP_OVERSIZE"]},
    "DRILL_DIAMETER": {self.tool_data["DRILL_DIAMETER"]},
    "DRILL_LENGTH": {self.tool_data["DRILL_LENGTH"]},
    "CHAMFER_LENGTH": {self.tool_data["CHAMFER_LENGTH"]},
    
    
"STEEL-20"/>
    "ROUGHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_AXIAL_DEPTH"]}
    
    "FINISHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_AXIAL_DEPTH"]}


"12X18H10T"/>
    "ROUGHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_AXIAL_DEPTH"]}
    
    "FINISHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_AXIAL_DEPTH"]}


"ALUMINIUM"/>
    "ROUGHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_AXIAL_DEPTH"]}
    
    "FINISHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_AXIAL_DEPTH"]}
"""
            # except:
            #     self.tool_xml = "ERROR IN DEBUG XML GENERATION"
            #     logger.critical(f"{self.tool_data["tool_name_str"]} - debug XML not created")

    def set_xml_head(self) -> str:
        xml_part_str = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<MfgSetupDocument>
    <DocType>PRO_NC_CUTTING_TOOL_SETUP</DocType>
    <DocTitle>Инфо режущего инструмента</DocTitle>
    <DateTime>{self.DATETIME}</DateTime>
    <ApplicationInfo AppName="Creo" AppVersion="8.0.11.0" FtVersion="360051" Language="russian" MdlVersion="2012"/>
"""
        logger.debug(f"xml_head generated...")
        return xml_part_str

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_str"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
"""
        logger.debug(f"xml_tool_params generated...")
        return xml_part_str

    def set_xml_body_tool_cut_data(self) -> str:
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
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_PER_UNIT"]}"/>
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
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                    <MfgParam Name="TOOL_RADIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_RADIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
"""
            total_string += xml_part_str

        logger.debug(f"xml_tool_cut_data generated...")
        return total_string

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
            <BOM>
                <BOMComponent Comments=" " Name="holder" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="adapter" Quantity="1" Type="ADAPTER"/>
                <BOMComponent Comments=" " Name="insert" Quantity="1" Type="INSERT"/>
                <BOMComponent Comments=" " Name="common" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(f"xml_BOM_components generated...")
        return xml_part_str

    def set_xml_tail(self) -> str:
        xml_part_str = f"""\
            <ToolSetUpOnWorkcell>
                <OffsetDataCollection>
                    <OffsetData Comment="comment" OffsetZ="0.000000" Register="-1" Tip="1"/>
                </OffsetDataCollection>
            </ToolSetUpOnWorkcell>
        </Tool>
    </ToolingSetup>
</MfgSetupDocument>
"""
        logger.debug(f"xml_tail generated...")
        return xml_part_str
