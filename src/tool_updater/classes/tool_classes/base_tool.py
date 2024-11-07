from math import pi
import io
import datetime

import logging

from tool_updater.classes.transform_cut_data import multiplier_p3_p4_to_n2_n3_n4

logger = logging.getLogger(__name__)


# noinspection PyBroadException
class BaseTool:
    # BASIC DATA
    tool_file_extension = ".xml"
    DATETIME = datetime.datetime.today().strftime("%Y - %m-%dT%H:%M:%S")
    # DATETIME = "2024 - 11-13T12:12:12"

    # MANUAL TOOL DATA
    tool_material = "HSS"
    teeth_num = 2

    vc_min_or_max = 0  # 0 для минимальной скорости, -1 для максимальной, если их указано две или более
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
    # roughing_vc_modifier = 1  # Множитель для скорости резания
    # roughing_feed_rate_multiplier = 0.6  # Множитель для подачи (и на зуб, и на оборот)
    # finishing_vc_modifier = 1.2  # Множитель для скорости резания
    # finishing_feed_rate_multiplier = 0.4  # Множитель для подачи (и на зуб, и на оборот)

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

    # GEOMETRY DATA CATALOGUE
    key_order_no = "order_no"
    key_body_len = "full_body_len"
    key_body_diam = "full_body_diam"
    key_flute_len = "flute_len"
    key_flute_diam = "cutting_edge_diam"
    key_lowering_len = "neck_len"
    key_lowering_diam = "neck_diam"
    key_edge_radius = "cutting_edge_rad"
    key_edge_chamfer = "cutting_edge_chamfer"

    # CUT DATA CATALOGUE
    # main key. Value will be dictionary with subkeys
    key_iso_P = "iso_P"  # От низколегированных до высоколегированных и стальное литье
    key_iso_M = "iso_M"  # Вся нержавейка. 12% хрома и больше
    key_iso_K = "iso_K"  # Все чугуны. Серые, ковкие, с шаровидным, вермикулярным графитом, отпущенный ковкий
    key_iso_N = "iso_N"  # Цветные металлы. Алюминий, медь, латунь, бронза...
    key_iso_S = "iso_S"  # Жаропрочные сплавы. Высоколегированные материалы на основе железа, никеля, кобальта и титана
    key_iso_H = "iso_H"  # Матералы высокой твердости. Стали 45-65HRC и отбеленный чугун 400-600HB

    lst_of_material_groups: list[str] = [
        key_iso_P,
        key_iso_M,
        key_iso_K,
        key_iso_N,
        key_iso_S,
        key_iso_H,
    ]

    # Subkeys for cutdata catalogue
    key_vc = "Vc"  # Скорость резания
    key_z = "z"  # Число режущих кромок или пластин
    key_fn = "Fn"  # Подача на мм/оборот
    key_fz = "Fz"  # Подача мм/зуб
    key_f = "F"  # Подача мм/мин

    def __init__(self,
                 tool_size_from_geom_catalogue: str,
                 catalog_tool_cut_data: dict,
                 catalog_tool_geometry: dict,
                 file_name_prefix: str,
                 file_name_suffix: str,
                 debug_mode: bool,
                 **kwargs):
        self.debug = debug_mode
        if self.debug:
            self.finishing_roughing_options = {
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

        # 2.1 Создание данных, основанных на имени (диаметре) инструмента
        self.tool_data["tool_diam_float"] = float(self.tool_data["tool_name_str"])
        self.tool_data["CUTTER_DIAM"] = self.tool_data["tool_name_str"]
        self.tool_data["cut_data_diam_group"] = self.calc_diam_group_name()

        # 2.2 Объявление имен, по которым будет совершаться поиск в каталогах
        self.tool_data["tool_name_for_geom_catalogue"] = self.create_tool_name_for_geom_catalogue()
        self.tool_data["tool_name_for_cut_catalogue"] = self.create_tool_name_for_cut_catalogue()

        # 3 Объявление переменных, используемых в XML
        self.tool_data["TOOL_MATERIAL"] = self.tool_material

        # 3.1 Получение данных из каталога геометрии
        self.tool_data["LENGTH"] = self.get_tool_length()
        self.tool_data["FLUTE_LENGTH"] = self.get_tool_flute_length()
        self.tool_data["TOOL_COMMENT"] = self.get_tool_comment()

        # 3.2 Создание данных, основанных на данных из каталога геометрии
        self.tool_data["tool_name"] = self.create_tool_name()
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
            return self.catalog_geom[t_name][self.key_body_len]
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - Tool len not found")
            return 0

    def get_tool_flute_length(self) -> float:
        try:
            t_name = self.tool_data["tool_name_for_geom_catalogue"]
            fractional_part = t_name.split(".")[1]
            if len(fractional_part) < 2:
                t_name += "0"
            return self.catalog_geom[t_name][self.key_flute_len]
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - Tool flute len not found")
            return 0

    def get_tool_comment(self) -> str:
        try:
            t_name = self.tool_data["tool_name_for_geom_catalogue"]
            return self.catalog_geom[t_name][self.key_order_no]
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - Tool flute len not found")
            return ""

    #
    #
    #
    # GET FROM CUT DATA CATALOGUE
    def get_vc(self, key_iso_material: str, fin_or_rough):
        try:
            vc_data = self.catalog_cut_data[key_iso_material][self.key_vc]
            if type(vc_data) is int or type(vc_data) is float:
                vc_data *= self.finishing_roughing_options[fin_or_rough]["vc_modifier"]
                return vc_data
            if type(vc_data) is list or type(vc_data) is set or type(vc_data) is tuple:
                vc_data = vc_data[self.vc_min_or_max]
                vc_data *= self.finishing_roughing_options[fin_or_rough]["vc_modifier"]
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
            diam_groups = [key for key in self.catalog_cut_data[self.key_iso_M][self.key_fn]]
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
        for key_iso_material in self.lst_of_material_groups:
            for fin_or_rough in self.finishing_roughing_options:
                tool_surface_speed = self.get_vc(key_iso_material=key_iso_material, fin_or_rough=fin_or_rough)
                tool_spindle_rpm = self.calc_rpm(Vc=tool_surface_speed)
                tool_feed_per_unit = self.calc_feed_per_rev(key_iso_material=key_iso_material,
                                                            fin_or_rough=fin_or_rough)
                tool_feed_rate = self.calc_feed_rate(key_iso_material=key_iso_material, RPM=tool_spindle_rpm,
                                                     fin_or_rough=fin_or_rough)
                tool_axial_depth = self.calc_axial_depth(key_iso_material=key_iso_material)
                tool_radial_depth = self.calc_radial_depth(key_iso_material=key_iso_material)

                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SURFACE_SPEED"] = tool_surface_speed
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"] = tool_spindle_rpm
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_PER_UNIT"] = tool_feed_per_unit
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_RATE"] = tool_feed_rate
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_AXIAL_DEPTH"] = tool_axial_depth
                self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_RADIAL_DEPTH"] = tool_radial_depth

    def calc_rpm(self, Vc: int | float) -> float:
        try:
            rpm = 1000 * Vc / (pi * self.tool_data["tool_diam_float"])
            return round(rpm, ndigits=1)
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - RPM not calculated")
            return 0

    def calc_feed_per_rev(self, key_iso_material, fin_or_rough: str) -> float:
        try:
            Fn = self.catalog_cut_data[key_iso_material][self.key_fn][self.tool_data["cut_data_diam_group"]]
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            fn = Fn * feed_multiplier
            return round(fn, ndigits=2)
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - feed per rev not calculated")
            return 0

    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        try:
            Fn = self.catalog_cut_data[key_iso_material][self.key_fn][self.tool_data["cut_data_diam_group"]]
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            rpm = Fn * RPM * feed_multiplier
            return round(rpm, ndigits=1)
        except:
            logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0

    def calc_axial_depth(self, key_iso_material) -> float:
        try:
            axial_depth = float(self.tool_data["CUTTER_DIAM"]) * self.axial_depth_modifiyers[key_iso_material]
            return round(axial_depth, ndigits=2)
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - axial depth not calculated")
            return 0

    def calc_radial_depth(self, key_iso_material):
        try:
            return float(self.tool_data["CUTTER_DIAM"]) * self.radial_depth_modifiyers[key_iso_material]
        except:
            logger.warning(f"{self.tool_data["tool_name_str"]} - radial depth not calculated")
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
        self.tool_data = {
            # инфа для программы
            "tool_name_str": None,
            "tool_name_for_geom_catalogue": None,
            "tool_name_for_cut_catalogue": None,
            "tool_diam_float": None,
            "file_name_prefix": None,
            "file_name_suffix": None,
            "file_name": None,
            # инфа общая для всех инструментов
            # настройки
            "GAUGE_X_LENGTH": "-",
            "GAUGE_Z_LENGTH": "-",
            "LENGTH_UNITS": "MILLIMETER",
            "TOOL_MATERIAL": None,
            "TOOL_COMMENT": None,
            "SPINDLE_SENSE": "CW",
            "COOLANT_OPTION": "ON",
            "COOLANT_PRESSURE": "LOW",
            # геометрия
            "CUTTER_DIAM": None,
            "NUM_OF_TEETH": None,
            "HOLDER_DIA": None,
            "HOLDER_LEN": None,
            "LENGTH": None,
            "FLUTE_LENGTH": None,
            # фрезы
            # фрезы тороидальные
            "CORNER_RADIUS": None,
            # сверла
            # центровки
            "POINT_ANGLE": None,
            "CSINK_ANGLE": None,
            # резьбофрезы
            "INSERT_LENGTH": None,
            "END_OFFSET": None,
            # не сортированное
            "SIDE_ANGLE": None,
            "TOOL_LONG_FLAG": None,
            "CUT_LENGTH": None,
            "TIP_LENGTH": None,
            "SHANK_DIAM": None,
            "COMP_OVERSIZE": None,
            "DRILL_DIAMETER": None,
            "DRILL_LENGTH": None,
            "CHAMFER_LENGTH": None,
            "cut_data_diam_group": None,
            # данные резания инструментом по категориям материалов
            "cut_data": {
                "iso_P": {
                    "roughing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                    "finishing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                },
                "iso_M": {
                    "roughing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                    "finishing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                },
                "iso_K": {
                    "roughing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                    "finishing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                },
                "iso_N": {
                    "roughing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                    "finishing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                },
                "iso_S": {
                    "roughing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                    "finishing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                },
                "iso_H": {
                    "roughing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                    "finishing": {
                        "TOOL_SURFACE_SPEED": None,
                        "TOOL_SPINDLE_RPM": None,
                        "TOOL_FEED_RATE": None,
                        "TOOL_FEED_PER_UNIT": None,
                        "TOOL_AXIAL_DEPTH": None,
                        "TOOL_RADIAL_DEPTH": None,
                    },
                },
            },

        }

    #
    #
    #
    # XML DEFINITION
    def set_tool_xml(self):
        if self.debug is False:
            try:
                self.tool_xml = \
                    f"""<?xml version="1.0" encoding="UTF-8"?>
<MfgSetupDocument>
    <DocType>PRO_NC_CUTTING_TOOL_SETUP</DocType>
    <DocTitle>Инфо режущего инструмента</DocTitle>
    <DateTime>{self.DATETIME}</DateTime>
    <ApplicationInfo AppName="Creo" AppVersion="8.0.11.0" FtVersion="360051" Language="russian" MdlVersion="2012"/>
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name"]}" RefXmlId="encref_1" Type="BASIC DRILL">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <MfgParam Name="LENGTH_UNITS" Value="MILLIMETER"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="POINT_ANGLE" Value="118"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["LENGTH"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="-"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="-"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="NO"/>
            <MfgParam Name="HOLDER_DIA" Value="-"/>
            <MfgParam Name="HOLDER_LEN" Value="-"/>
            <MfgParam Name="COOLANT_OPTION" Value="ON"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="LOW"/>
            <MfgParam Name="SPINDLE_SENSE" Value="CW"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
            <ToolCutData>
                <Material>
                    <MfgParam Name="STOCK_MATERIAL" Value="ALUMINIUM"/>
                </Material>
                <CutDataUnitSystem>
                    <MfgParam Name="CUT_DATA_UNITS" Value="METRIC"/>
                </CutDataUnitSystem>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="ROUGHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
            <ToolCutData>
                <Material>
                    <MfgParam Name="STOCK_MATERIAL" Value="STEEL-20"/>
                </Material>
                <CutDataUnitSystem>
                    <MfgParam Name="CUT_DATA_UNITS" Value="METRIC"/>
                </CutDataUnitSystem>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="ROUGHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
            <ToolCutData>
                <Material>
                    <MfgParam Name="STOCK_MATERIAL" Value="12X18H10T"/>
                </Material>
                <CutDataUnitSystem>
                    <MfgParam Name="CUT_DATA_UNITS" Value="METRIC"/>
                </CutDataUnitSystem>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="ROUGHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][self.key_iso_M]["roughing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][self.key_iso_M]["roughing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][self.key_iso_M]["roughing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][self.key_iso_M]["roughing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][self.key_iso_M]["roughing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
            <ToolSetUpOnWorkcell>
                <OffsetDataCollection>
                    <OffsetData Comment="comment" OffsetZ="0.000000" Register="-1" Tip="1"/>
                </OffsetDataCollection>
            </ToolSetUpOnWorkcell>
        </Tool>
    </ToolingSetup>
</MfgSetupDocument>"""
            except:
                self.tool_xml = ""
                logger.critical(f"{self.tool_data["tool_name_str"]} - XML not created")
        else:
            try:
                self.tool_xml = \
                    f"""<?xml version="1.0" encoding="UTF-8"?>
<DateTime>{self.DATETIME}</DateTime>
<Tool Id="{self.tool_data["tool_name"]}" RefXmlId="encref_1" Type="BASIC DRILL">
<MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
<MfgParam Name="LENGTH" Value="{self.tool_data["LENGTH"]}"/>
<MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
<MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
<MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>

"STEEL-20"/>
    "ROUGHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][self.key_iso_P]["finishing"]["TOOL_AXIAL_DEPTH"]}
    
    "FINISHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][self.key_iso_P]["roughing"]["TOOL_AXIAL_DEPTH"]}


"12X18H10T"/>
    "ROUGHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_AXIAL_DEPTH"]}
    
    "FINISHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][self.key_iso_M]["finishing"]["TOOL_AXIAL_DEPTH"]}


"ALUMINIUM"/>
    "ROUGHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][self.key_iso_N]["finishing"]["TOOL_AXIAL_DEPTH"]}
    
    "FINISHING"/>
        "TOOL_SURFACE_SPEED" = {self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_SURFACE_SPEED"]}
        "TOOL_SPINDLE_RPM" =   {self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_SPINDLE_RPM"]}
        "TOOL_FEED_PER_UNIT" = {self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_FEED_PER_UNIT"]}
        "TOOL_FEED_RATE" =     {self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_FEED_RATE"]}
        "TOOL_AXIAL_DEPTH" =   {self.tool_data["cut_data"][self.key_iso_N]["roughing"]["TOOL_AXIAL_DEPTH"]}

Общие:
    "GAUGE_X_LENGTH": "-",
    "GAUGE_Z_LENGTH": "-",
    "LENGTH_UNITS": "MILLIMETER",
    "TOOL_MATERIAL": None,
    "TOOL_COMMENT": None,
    "SPINDLE_SENSE": "CW",
    "COOLANT_OPTION": "ON",
    "COOLANT_PRESSURE": "LOW",
# геометрия
    "CUTTER_DIAM": None,
    "NUM_OF_TEETH": None,
    "HOLDER_DIA": None,
    "HOLDER_LEN": None,
    "LENGTH": None,
    "FLUTE_LENGTH": None,
# фрезы
# фрезы тороидальные
    "CORNER_RADIUS": None,
# сверла
# центровки
    "POINT_ANGLE": None,
    "CSINK_ANGLE": None,
# резьбофрезы
    "INSERT_LENGTH": None,
    "END_OFFSET": None,
# не сортированное
    "SIDE_ANGLE": None,
    "TOOL_LONG_FLAG": None,
    "CUT_LENGTH": None,
    "TIP_LENGTH": None,
    "SHANK_DIAM": None,
    "COMP_OVERSIZE": None,
    "DRILL_DIAMETER": None,
    "DRILL_LENGTH": None,
    "CHAMFER_LENGTH": None,
"""
            except:
                self.tool_xml = ""
                logger.critical(f"{self.tool_data["tool_name_str"]} - debug XML not created")
