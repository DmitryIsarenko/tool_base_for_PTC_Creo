from src.tool_updater.classes.mixin.mixin_root import MixinRoot

from math import pi

from src.tool_updater.catalogs.osawa_drills import osawa_drills_2386_sti_cut_data, osawa_drills_2386_sti_geometry


class MixinDrill(MixinRoot):
    DATETIME = "2024 - 11-13T12:12:12"

    catalog_geom = osawa_drills_2386_sti_geometry
    catalog_cut_data = osawa_drills_2386_sti_cut_data
    material_st_key = "P3_P4"
    material_nj_key = "M2"
    material_al_key = "N2_N3_N4"
    vc_key = "Vc"
    fn_key = "fn"

    vc_min_or_max = 0  # 0 для минимальной скорости, 1 для максимальной
    teeth_num = 2
    vc_modifier = 1


    def __init__(self,
                 tool_diam,
                 tool_obj_for_mixin_drill,
                 **kwargs):
        self.obj = tool_obj_for_mixin_drill
        self.obj.drill_diam = tool_diam
        # self.obj.file_name = file_name_for_drill


        self.obj.tool_name = self.set_tool_name()

        self.obj.feedrate_multiplier = 0.6
        self.obj.peck_depth_modifier = 0.25  # умножается на диаметр
        self.obj.st_peck_depth_modifier = 1.5  # умножается на величину общего peck depth
        self.obj.nj_peck_depth_modifier = 1  # умножается на величину общего peck depth
        self.obj.al_peck_depth_modifier = 2  # умножается на величину общего peck depth

        self.obj.CUTTER_DIAM = self.obj.get_cutter_diam_from_name()
        self.obj.cut_data_diam_group = self.obj.calc_diam_group_name()

        self.obj.LENGTH = self.get_tool_length()
        self.obj.FLUTE_LENGTH = self.get_tool_flute_length()

        self.obj.st_Vc = self.catalog_cut_data[self.obj.material_st_key][self.obj.vc_key][self.obj.vc_min_or_max]
        self.obj.nj_Vc = self.catalog_cut_data[self.obj.material_nj_key][self.obj.vc_key][self.obj.vc_min_or_max]
        self.obj.al_Vc = self.catalog_cut_data[self.obj.material_al_key][self.obj.vc_key][self.obj.vc_min_or_max]

        self.obj.TOOL_ROUGH_AXIAL_DEPTH = self.obj.calc_common_peck_depth()
        self.obj.TOOL_ROUGH_FEED_RATE = self.catalog_cut_data[self.obj.material_nj_key][self.obj.fn_key][
            self.obj.cut_data_diam_group]
        self.obj.TOOL_ROUGH_SPINDLE_RPM = self.obj.calc_rpm(Vc=self.obj.nj_Vc)

        self.obj.st_TOOL_SPINDLE_RPM = self.obj.calc_rpm(Vc=self.obj.st_Vc)
        self.obj.nj_TOOL_SPINDLE_RPM = self.obj.calc_rpm(Vc=self.obj.nj_Vc)
        self.obj.al_TOOL_SPINDLE_RPM = self.obj.calc_rpm(Vc=self.obj.al_Vc)

        self.obj.st_TOOL_SURFACE_SPEED = self.obj.st_Vc
        self.obj.nj_TOOL_SURFACE_SPEED = self.obj.nj_Vc
        self.obj.al_TOOL_SURFACE_SPEED = self.obj.al_Vc

        self.obj.st_TOOL_FEED_PER_UNIT = self.obj.calc_feed_per_tooth(material=self.obj.material_st_key)
        self.obj.nj_TOOL_FEED_PER_UNIT = self.obj.calc_feed_per_tooth(material=self.obj.material_nj_key)
        self.obj.al_TOOL_FEED_PER_UNIT = self.obj.calc_feed_per_tooth(material=self.obj.material_al_key)

        self.obj.st_TOOL_FEED_RATE = self.obj.calc_feed_rate(material=self.obj.material_st_key,
                                                             RPM=self.obj.st_TOOL_SPINDLE_RPM)
        self.obj.nj_TOOL_FEED_RATE = self.obj.calc_feed_rate(material=self.obj.material_nj_key,
                                                             RPM=self.obj.nj_TOOL_SPINDLE_RPM)
        self.obj.al_TOOL_FEED_RATE = self.obj.calc_feed_rate(material=self.obj.material_al_key,
                                                             RPM=self.obj.al_TOOL_SPINDLE_RPM)

        self.obj.st_TOOL_AXIAL_DEPTH = self.obj.calc_common_peck_depth() * self.obj.st_peck_depth_modifier
        self.obj.nj_TOOL_AXIAL_DEPTH = self.obj.calc_common_peck_depth() * self.obj.nj_peck_depth_modifier
        self.obj.al_TOOL_AXIAL_DEPTH = self.obj.calc_common_peck_depth() * self.obj.al_peck_depth_modifier
        super().__init__(**kwargs)

    # def get_cutter_diam_from_name(self) -> str:
    #     # example input
    #     # "SVERLO_D1-0_L34"
    #     # example output
    #     # t_d="12.10"
    #
    #     t_d = self.obj.tool_name.split("_")[1].replace("D", "").replace("-", ".")
    #     t_d = str(round(float(t_d), ndigits=2))
    #     return t_d

    def calc_diam_group_name(self):
        diam_groups = [key for key in self.catalog_cut_data[self.obj.material_nj_key][self.obj.fn_key]]
        t_diam = float(self.obj.CUTTER_DIAM)
        suitable_grp = None
        for grp in diam_groups:
            grp_float = float(grp)
            if t_diam >= grp_float:
                suitable_grp = grp
        return suitable_grp

    def get_tool_length(self) -> float:
        t_name = self.obj.CUTTER_DIAM
        fractional_part = t_name.split(".")[1]
        if len(fractional_part) < 2:
            t_name += "0"
        return self.catalog_geom[t_name]["length"]

    def get_tool_flute_length(self) -> float:
        t_name = self.obj.CUTTER_DIAM
        fractional_part = t_name.split(".")[1]
        if len(fractional_part) < 2:
            t_name += "0"
        return self.catalog_geom[t_name]["flute_len"]

    def calc_rpm(self, Vc: int | float) -> float:
        return round(1000 * Vc / (pi * float(self.obj.CUTTER_DIAM)), ndigits=2)

    def calc_feed_per_tooth(self, material) -> float:
        return self.catalog_cut_data[material][self.obj.fn_key][self.obj.cut_data_diam_group] / self.obj.teeth_num

    def calc_feed_rate(self, material, RPM) -> float:
        return self.catalog_cut_data[material][self.obj.fn_key][self.obj.cut_data_diam_group] * RPM

    def calc_common_peck_depth(self) -> float:
        return float(self.obj.CUTTER_DIAM) * self.obj.peck_depth_modifier

    def set_tool_name(self):
        t_name = f"SVERLO_D{self.obj.drill_diam}_L{self.obj.FLUTE_LENGTH}-{self.obj.LENGTH}"
        return t_name

    def write_new_file(self, path):
        try:
            with open(file=f"{path}\\new_{self.obj.tool_name}{self.obj.tool_file_extension}", mode="w") as f:
                # f.writelines(body_lines)
                f.writelines(self.obj.tool_xml)
        except:
            pass
