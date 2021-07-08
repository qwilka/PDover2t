
"""
Pipeline pressure containment according to DNVGL-ST-F101 (2017-12)
refs:
https://graphtik.readthedocs.io/en/latest/

Notes:


to run:
python DnvStF101_pressure_containment.py 
"""

from graphtik import compose, operation
from pdover2t.DnvStF101 import *


# Gas Export (0-0.3 km) location class II, 60°C max. Temp. 340-370m depth
p_d = 240.e5  # (Pa) design pressure at reference elevation Z_ref
h_ref = 30.0  # (m) reference elevation for pressure (LAT=0m)
ρ_cont = 275. # (kg/m3) density of pipeline contents



γ_inc = 1.10  # incidental to design pressure ratio
α_spt = 1.05  # DNVGL-ST-F101 (2017-12) p94




p_e_OP = operation(p_ext, needs=["h_l", "ρ_seawater", "g"], 
            provides=["p_e"])

p_inc_OP = operation(p_incid_ref, needs=["p_d", "γ_inc"], provides=["p_inc"])
p_li_OP = operation(p_incid_loc, needs=["p_d", "ρ_cont", "h_l", "h_ref", "γ_inc", "g"], 
            provides=["p_li"])

p_t_OP = operation(p_system_test_ref, needs=["p_d", "γ_inc", "α_spt"], 
            provides=["p_t"])
p_lt_OP = operation(p_test_loc, needs=["p_t", "ρ_t", "h_l", "h_ref", "g"], 
            provides=["p_lt"])

char_WT_OP = operation(char_wall_thickness, needs=["t", "t_fab", "t_corr"], 
            provides=["t_min"])
p_mill_test_OP = operation(p_mill_test, needs=["D", "t_min", "SMYS", "SMTS", "α_U", "α_mpt", "k"], 
            provides=["p_mpt"])




cgraph = operation("Pressure containment",
    p_inc_OP,
    p_li_OP,
    p_e_OP,
    p_t_OP,
    p_lt_OP,

    )

