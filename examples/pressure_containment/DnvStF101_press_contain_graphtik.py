
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
params = {
    "D_i": 0.6172,  # (m) pipe internal diameter
    "t_nom": 0.0242,  # (m) pipe wall thickness
    "t_corr": 0.0005, # (m) corrosion allowance
    "t_fab": 0.001, # (m) thickness negative fabrication tolerance

    "SMYS": 450.e6, # (Pa) pipe steel SMYS
    "f_ytemp": 6.e6, # (Pa) steel yield strength temperature de-rating
    "SMTS": 535.e6, # (Pa) pipe steel SMTS
    "f_utemp": 6.e6, # (Pa) steel ultimate strength temperature de-rating
    "α_U": 1.0, # material strength factor
    "γ_m": 1.15,  # material resistance factor

    "p_d": 240.e5,  # (Pa) design pressure at reference elevation Z_ref
    "γ_inc": 1.10 , # incidental to design pressure ratio
    "h_ref": 30.0 , # (m) reference elevation for pressure (LAT=0m)
    "ρ_cont": 275., # (kg/m3) density of pipeline contents
    "ρ_t": 1027. ,  # test fluid density

    "ρ_seawater": 1027., # (kg/m3) density of seawater

    "α_spt": 1.05,  # DNVGL-ST-F101 (2017-12) p94
    "α_mpt": 1.251,  # p94
    "α_spt": 1.05,  # p94
    "γ_SCPC": 1.308,  # safety class resistance factor for pressure containment


}

params["D_o"], _, _ = pipe_Do_Di_WT(Di=params["D_i"], WT=params["t_nom"])

MSL = 340. # (m) seawater depth (wrt MSL)
LAT = MSL - 1.1 # adjust tide
params["h_l"] = -LAT   # adjust h_l for tide and 

params["f_y"] =    char_strength(params["SMYS"], params["α_U"], f_ytemp=params["f_ytemp"])
params["f_u"] =    char_strength(params["SMTS"], params["α_U"], f_ytemp=params["f_utemp"])

# p_inc = p_incid_ref(p_d, γ_inc)
p_inc_OP = operation(p_incid_ref, needs=["p_d", "γ_inc"], provides=["p_inc"])

# p_li = p_incid_loc(p_d, ρ_cont, h_l, h_ref, γ_inc)  
p_li_OP = operation(p_incid_loc, needs=["p_d", "ρ_cont", "h_l", "h_ref", "γ_inc"], 
            provides=["p_li"])

# # p_t = p_system_test_ref(p_d,  γ_inc, α_spt)
# p_t_OP = operation(p_system_test_ref, needs=["p_d", "γ_inc", "α_spt"], 
#             provides=["p_t"])

# p_e = p_ext(h_l, ρ_seawater)
p_e_OP = operation(p_ext, needs=["h_l", "ρ_seawater"], 
            provides=["p_e"])

# p_t = p_system_test_ref(p_d, γ_inc, α_spt)
p_t_OP = operation(p_system_test_ref, needs=["p_d",  "γ_inc", "α_spt"], 
            provides=["p_t"])

# p_lt = p_test_loc(p_t, ρ_t, h_l, h_ref)
p_lt_OP = operation(p_test_loc, needs=["p_t", "ρ_t", "h_l", "h_ref"], 
            provides=["p_lt"])

# t_min_mill_test = char_WT(t_nom, t_fab, t_corr=0.0)
#t_corr_mill_test = 0.0
params["t_corr_mill_test"] = 0.0
t_min_mill_test_OP = operation(char_WT, name="t_min_mill_test_OP", 
            needs=["t_nom", "t_fab", "t_corr_mill_test"], 
            provides=["t_min_mill_test"])

# p_mpt = p_mill_test(D_o, t_min_mill_test, SMYS, SMTS, α_U, α_mpt, k=1.15)
params["k"] =1.15
p_mpt_OP = operation(p_mill_test, needs=["D_o", "t_min_mill_test", "SMYS", "SMTS", "α_U", "α_mpt", "k"], 
            provides=["p_mpt"])

# t_1 = char_WT(t_nom, t_fab, t_corr)
t_1_OP = operation(char_WT, name="t_1_OP", needs=["t_nom", "t_fab", "t_corr"], 
            provides=["t_1"])

# p_b = p_contain_resist(D_o, t_1, f_y, f_u)
p_b_OP = operation(p_contain_resist, needs=["D_o", "t_1", "f_y", "f_u"], 
            provides=["p_b"])

# p_cont_res_uty = p_contain_resist_uty(p_li, p_e,  p_b, γ_m, γ_SCPC)
p_cont_res_uty_OP = operation(p_contain_resist_uty, needs=["p_li", "p_e",  "p_b", "γ_m", "γ_SCPC"], 
            provides=["p_cont_res_uty"])

# p_lt_uty = p_test_loc_uty(α_spt, p_lt, p_li, p_e)
p_lt_uty_OP = operation(p_test_loc_uty, needs=["α_spt", "p_lt", "p_li", "p_e"], 
            provides=["p_lt_uty"])

# p_mpt_uty = p_mill_test_uty(p_li, p_e, p_mpt)
p_mpt_uty_OP = operation(p_mill_test_uty, needs=["p_li", "p_e", "p_mpt"], 
            provides=["p_mpt_uty"])

# p_cont_uty = p_contain_uty(p_cont_res_uty, p_lt_uty, p_mpt_uty)
p_cont_uty_OP = operation(p_contain_uty, needs=["p_cont_res_uty", "p_lt_uty", "p_mpt_uty"], 
            provides=["p_cont_uty"])



cgraph = compose("Pressure containment",
    p_inc_OP,
    p_li_OP,
    p_e_OP,
    p_t_OP,
    p_lt_OP,
    t_min_mill_test_OP,
    p_mpt_OP,
    t_1_OP,
    p_b_OP,
    p_cont_res_uty_OP,
    p_lt_uty_OP,
    p_mpt_uty_OP,
    p_cont_uty_OP
    )

sol = cgraph(**params)
sol.plot("press_conatin.svg")

#cgraph.compute(params, outputs=["t_1", "p_b", "p_cont_res_uty","p_lt_uty","p_mpt_uty", "p_cont_uty"])