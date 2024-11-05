from math import pi
import io


class Drill:
    tool_file_extension = ".xml"

    firm = "osawa"
    DATETIME = "2024 - 11-13T12:12:12"

    teeth_num = 2

    tool_material = "HSS"

    material_st_key = "P3_P4"
    material_nj_key = "M2"
    material_al_key = "N2_N3_N4"
    vc_key = "Vc"
    fn_key = "fn"
    vc_min_or_max = 0  # 0 для минимальной скорости, 1 для максимальной

    vc_modifier = 1
    # feed_rate_multiplier = 1
    feed_rate_multiplier = 0.6

    peck_depth_modifier = 0.25  # умножается на диаметр
    st_peck_depth_modifier = 1.5  # умножается на величину общего peck depth
    nj_peck_depth_modifier = 1  # умножается на величину общего peck depth
    al_peck_depth_modifier = 2  # умножается на величину общего peck depth

    def __init__(self,
                 tool_size: str,
                 catalog_tool_cut_data: dict,
                 catalog_tool_geometry: dict,
                 file_name_prefix: str,
                 file_name_suffix: str,
                 **kwargs):
        self.drill_diam = float(tool_size)
        self.catalog_cut_data = catalog_tool_cut_data
        self.catalog_geom = catalog_tool_geometry
        self.file_name_prefix = file_name_prefix
        self.file_name_suffix = file_name_suffix

        self.CUTTER_DIAM = tool_size
        self.cut_data_diam_group = self.calc_diam_group_name()

        self.TOOL_MATERIAL = self.tool_material

        self.LENGTH = self.get_tool_length()
        self.FLUTE_LENGTH = self.get_tool_flute_length()
        self.TOOL_COMMENT = self.get_tool_comment()
        self.tool_name = self.set_tool_name()
        self.file_name = self.set_file_name()

        self.st_Vc = self.catalog_cut_data[self.material_st_key][self.vc_key][self.vc_min_or_max]
        self.nj_Vc = self.catalog_cut_data[self.material_nj_key][self.vc_key][self.vc_min_or_max]
        self.al_Vc = self.catalog_cut_data[self.material_al_key][self.vc_key][self.vc_min_or_max]

        self.TOOL_ROUGH_AXIAL_DEPTH = self.calc_common_peck_depth()
        self.TOOL_ROUGH_FEED_RATE = self.catalog_cut_data[self.material_nj_key][self.fn_key][self.cut_data_diam_group]
        self.TOOL_ROUGH_SPINDLE_RPM = self.calc_rpm(Vc=self.nj_Vc)

        self.st_TOOL_SPINDLE_RPM = self.calc_rpm(Vc=self.st_Vc)
        self.nj_TOOL_SPINDLE_RPM = self.calc_rpm(Vc=self.nj_Vc)
        self.al_TOOL_SPINDLE_RPM = self.calc_rpm(Vc=self.al_Vc)

        self.st_TOOL_SURFACE_SPEED = self.st_Vc
        self.nj_TOOL_SURFACE_SPEED = self.nj_Vc
        self.al_TOOL_SURFACE_SPEED = self.al_Vc

        self.st_TOOL_FEED_PER_UNIT = self.calc_feed_per_rev(material=self.material_st_key)
        self.nj_TOOL_FEED_PER_UNIT = self.calc_feed_per_rev(material=self.material_nj_key)
        self.al_TOOL_FEED_PER_UNIT = self.calc_feed_per_rev(material=self.material_al_key)

        self.st_TOOL_FEED_RATE = self.calc_feed_rate(material=self.material_st_key,
                                                     RPM=self.st_TOOL_SPINDLE_RPM)
        self.nj_TOOL_FEED_RATE = self.calc_feed_rate(material=self.material_nj_key,
                                                     RPM=self.nj_TOOL_SPINDLE_RPM)
        self.al_TOOL_FEED_RATE = self.calc_feed_rate(material=self.material_al_key,
                                                     RPM=self.al_TOOL_SPINDLE_RPM)

        self.st_TOOL_AXIAL_DEPTH = self.calc_common_peck_depth() * self.st_peck_depth_modifier
        self.nj_TOOL_AXIAL_DEPTH = self.calc_common_peck_depth() * self.nj_peck_depth_modifier
        self.al_TOOL_AXIAL_DEPTH = self.calc_common_peck_depth() * self.al_peck_depth_modifier

        self.tool_xml = \
            f"""<?xml version="1.0" encoding="UTF-8"?>
<MfgSetupDocument>
    <DocType>PRO_NC_CUTTING_TOOL_SETUP</DocType>
    <DocTitle>Инфо режущего инструмента</DocTitle>
    <DateTime>{self.DATETIME}</DateTime>
    <ApplicationInfo AppName="Creo" AppVersion="8.0.11.0" FtVersion="360051" Language="russian" MdlVersion="2012"/>
    <ToolingSetup>
        <Tool Id="{self.tool_name}" RefXmlId="encref_1" Type="BASIC DRILL">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <MfgParam Name="LENGTH_UNITS" Value="MILLIMETER"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.CUTTER_DIAM}"/>
            <MfgParam Name="POINT_ANGLE" Value="118"/>
            <MfgParam Name="LENGTH" Value="{self.LENGTH}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.TOOL_MATERIAL}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="-"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="-"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="NO"/>
            <MfgParam Name="HOLDER_DIA" Value="-"/>
            <MfgParam Name="HOLDER_LEN" Value="-"/>
            <MfgParam Name="COOLANT_OPTION" Value="ON"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="LOW"/>
            <MfgParam Name="SPINDLE_SENSE" Value="CW"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.FLUTE_LENGTH}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.TOOL_COMMENT}"/>
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
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.al_TOOL_SURFACE_SPEED}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.al_TOOL_SPINDLE_RPM}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.al_TOOL_FEED_PER_UNIT}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.al_TOOL_FEED_RATE}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.al_TOOL_AXIAL_DEPTH}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.al_TOOL_SURFACE_SPEED}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.al_TOOL_SPINDLE_RPM}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.al_TOOL_FEED_PER_UNIT}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.al_TOOL_FEED_RATE}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.al_TOOL_AXIAL_DEPTH}"/>
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
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.st_TOOL_SURFACE_SPEED}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.st_TOOL_SPINDLE_RPM}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.st_TOOL_FEED_PER_UNIT}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.st_TOOL_FEED_RATE}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.st_TOOL_AXIAL_DEPTH}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="ROUGHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.st_TOOL_SURFACE_SPEED}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.st_TOOL_SPINDLE_RPM}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.st_TOOL_FEED_PER_UNIT}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.st_TOOL_FEED_RATE}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.st_TOOL_AXIAL_DEPTH}"/>
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
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.nj_TOOL_SURFACE_SPEED}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.nj_TOOL_SPINDLE_RPM}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.nj_TOOL_FEED_PER_UNIT}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.nj_TOOL_FEED_RATE}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.nj_TOOL_AXIAL_DEPTH}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.nj_TOOL_SURFACE_SPEED}"/>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.nj_TOOL_SPINDLE_RPM}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.nj_TOOL_FEED_PER_UNIT}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.nj_TOOL_FEED_RATE}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.nj_TOOL_AXIAL_DEPTH}"/>
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

    #     self.tool_xml = \
    #         f"""<?xml version="1.0" encoding="UTF-8"?>
    # <DateTime>{self.DATETIME}</DateTime>
    #     <Tool Id="{self.tool_name}" RefXmlId="encref_1" Type="BASIC DRILL">
    #         <MfgParam Name="CUTTER_DIAM" Value="{self.CUTTER_DIAM}"/>
    #         <MfgParam Name="LENGTH" Value="{self.LENGTH}"/>
    #         <MfgParam Name="TOOL_MATERIAL" Value="{self.TOOL_MATERIAL}"/>
    #         <MfgParam Name="FLUTE_LENGTH" Value="{self.FLUTE_LENGTH}"/>
    #         <MfgParam Name="TOOL_COMMENT" Value="{self.TOOL_COMMENT}"/>
    #                 <MfgParam Name="STOCK_MATERIAL" Value="ALUMINIUM"/>
    #                 <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.al_TOOL_SURFACE_SPEED}"/>
    #                 <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.al_TOOL_SPINDLE_RPM}"/>
    #                 <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.al_TOOL_FEED_PER_UNIT}"/>
    #                 <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.al_TOOL_FEED_RATE}"/>
    #                 <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.al_TOOL_AXIAL_DEPTH}"/>
    #             """

    def calc_diam_group_name(self):
        diam_groups = [key for key in self.catalog_cut_data[self.material_nj_key][self.fn_key]]
        t_diam = self.drill_diam
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

    def get_tool_length(self) -> float:
        t_name = self.CUTTER_DIAM
        fractional_part = t_name.split(".")[1]
        if len(fractional_part) < 2:
            t_name += "0"
        return self.catalog_geom[t_name]["length"]

    def get_tool_flute_length(self) -> float:
        t_name = self.CUTTER_DIAM
        fractional_part = t_name.split(".")[1]
        if len(fractional_part) < 2:
            t_name += "0"
        return self.catalog_geom[t_name]["flute_len"]

    def get_tool_comment(self) -> str:
        t_name = self.CUTTER_DIAM
        return self.catalog_geom[t_name]["edp_no"]

    def calc_rpm(self, Vc: int | float) -> float:
        return round(1000 * Vc / (pi * self.drill_diam), ndigits=0)

    def calc_feed_per_rev(self, material) -> float:
        return self.catalog_cut_data[material][self.fn_key][self.cut_data_diam_group] * self.feed_rate_multiplier

    def calc_feed_rate(self, material, RPM) -> float:
        rpm = self.catalog_cut_data[material][self.fn_key][self.cut_data_diam_group] * RPM * self.feed_rate_multiplier
        return round(rpm, ndigits=0)

    def calc_common_peck_depth(self) -> float:
        return float(self.CUTTER_DIAM) * self.peck_depth_modifier

    def set_tool_name(self):
        t_prefix = self.file_name_prefix.upper()
        t_suffix = self.file_name_suffix.upper()
        t_name = f"{t_prefix}D{self.CUTTER_DIAM.replace(".", "-")}_L{self.FLUTE_LENGTH}-{self.LENGTH}{t_suffix}"
        return t_name

    def set_file_name(self):
        t_name = f"D{self.drill_diam}_L{self.FLUTE_LENGTH}-{self.LENGTH}"
        return t_name

    def write_new_file(self, path):
        try:
            with io.open(
                    file=f"{path}\\{self.file_name_prefix}{self.file_name}{self.file_name_suffix}{self.tool_file_extension}",
                    mode="w",
                    encoding="utf-8",
            ) as f:
                # f.writelines(body_lines)
                f.writelines(self.tool_xml)
        except:
            pass
