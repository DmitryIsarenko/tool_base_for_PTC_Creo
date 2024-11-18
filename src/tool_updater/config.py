NDIGITS_FEED = 2
NDIGITS_FEED_PER_UNIT = 4
NDIGITS_AXIAL_FEED = 2
NDIGITS_RADIAL_FEED = 2
NDIGITS_SPINDLE = 2
NDIGITS_SURFACE_SPEED = 3

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


# GEOMETRY DATA CATALOGUE
key_order_no = "order_no"
key_body_len = "full_body_len"
key_body_diam = "full_body_diam"
key_flute_len = "flute_len"
key_flute_diam = "flute_diam"
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

# Subkeys for cutdata catalogue
key_vc = "Vc"  # Скорость резания
key_z = "z"  # Число режущих кромок или пластин
key_fn = "Fn"  # Подача на мм/оборот
key_fz = "Fz"  # Подача мм/зуб
key_f = "F"  # Подача мм/мин


mfg_materials_dict = {
    "ALUMINIUM": key_iso_N,
    "STEEL-20": key_iso_P,
    "12X18H10T": key_iso_M,
    "Не указано": key_iso_M,
}


lst_of_material_groups: list[str] = [
    key_iso_P,
    key_iso_M,
    key_iso_K,
    key_iso_N,
    key_iso_S,
    key_iso_H,
]




# ER collet sizes
collet_sizes = {
    "ER16": {
        "max_diam": 10,
        "nut_diam": 28,
    },
    "ER20": {
        "max_diam": 13,
        "nut_diam": 34,
    },
    "ER25": {
        "max_diam": 16,
        "nut_diam": 42,
    },
    "ER32": {
        "max_diam": 20,
        "nut_diam": 50,
    },
}