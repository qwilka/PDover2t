"""
Graphtik 
Pressure containment
design pressure



#### NOTE
UnicodeEncodeError: 'charmap' codec can't encode character '\u03b1' in position 3695: character maps to <undefined>
https://stackoverflow.com/questions/50933194/how-do-i-set-the-pythonutf8-environment-variable-to-enable-utf-8-encoding-by-def
Graphtik plot: To plot graphs on Windows, set the following enviromental varibale  before launching Jupyter notebook   
set PYTHONUTF8=1  
set PYTHONUTF8="1"   avoid trailing space 
"""
from graphtik import compose, operation, keyword
from pdover2t.dnvstf101 import *
from pdover2t.pipe import dowt2di


use_numpy = False
if use_numpy:
    import numpy as np
#     _max = np.maximum
# else:
#     _max = max


import pandas as pd


params = {
    "D_o": 24 * 25.4 * 1.e-3,  # (m) pipe internal diameter
    "t_nom": 0.0159,  # (m) pipe wall thickness
    "t_corr": 0.0, # (m) corrosion allowance
    "t_fab": 0.001, # (m) thickness negative fabrication tolerance

    "SMYS": 450.e6, # (Pa) pipe steel SMYS
    "f_ytemp": 35.e6, # (Pa) steel yield strength temperature de-rating
    "SMTS": 535.e6, # (Pa) pipe steel SMTS
    "f_utemp": 0.e6, # (Pa) steel ultimate strength temperature de-rating
    "α_U": 0.96, # material strength factor
    "α_U_pt": 1.0, # material strength factor for prssure test cacls
    "γ_m": 1.15,  # material resistance factor

    "p_d": 150.e5,  # (Pa) design pressure at reference elevation Z_ref
    "γ_inc": 1.10 , # incidental to design pressure ratio
    "h_ref": 0.0 , # (m) reference elevation for pressure (LAT=0m)
    "ρ_cont": 20., # (kg/m3) density of pipeline contents
    "ρ_t": 1025. ,  # test fluid density

    "ρ_seawater": 1025., # (kg/m3) density of seawater

    "α_spt": 1.05,  # DNVGL-ST-F101 (2017-12) p94gamma
    "α_mpt": 1.038,  # p94
    "α_spt": 1.05,  # p94
    "γ_SCPC": 1.138,  # safety class resistance factor for pressure containment

    "mill_test_k": 1.0,   # k parameter used for calculating mill test pressure
    "t_corr_mill_test": 0.0,

    "MSL": 55.0,
    "tide": 1.0,
}

if use_numpy:
    params["p_d"] = np.array([50.e5, 150.e5])



cgraph = compose("start",
  operation(lambda sea_level,tide: -(sea_level - tide), name="seabed level", needs=["MSL", "tide"], provides=["h_l"]),
  operation(char_WT, name="characteristic WT", needs=["t_nom", "t_fab", "t_corr"],  provides=["t_1"]),
    ##operation(p_incid_loc, name="local_incidental_pressure", needs=["p_d", "ρ_cont", "h_l", "h_ref", "γ_inc"], provides=["p_li"]),
    operation(p_ext, name="external pressure", needs=["h_l", "ρ_seawater"],  provides=["p_e"])
)

cgraph= compose("material strength", cgraph,
    operation(char_strength, name="char_fy", needs=["SMYS", "α_U", keyword("f_ytemp")], provides=["f_y"]), 
    operation(char_strength, name="char_fu", needs=["SMTS", "α_U", keyword("f_utemp", "f_ytemp")], provides=["f_u"])
)

cgraph = compose("pressure test", cgraph,
    operation(p_incid_loc, name="local_incidental_pressure", needs=["p_d", "ρ_cont", "h_l", "h_ref", "γ_inc"], provides=["p_li"]),
    operation(p_system_test_ref, name="test pressure", needs=["p_d", "γ_inc", "α_spt"], provides=["p_t"]),
    operation(p_test_loc, name="local test pressure", needs=["p_t", "ρ_t", "h_l", "h_ref"], provides=["p_lt"])
)


cgraph= compose("incidental pressure", cgraph, 
   # operation(p_incid_ref, name="incidental pressure", needs=["p_d", "γ_inc"], provides=["p_inc"]),
    operation(p_incid_loc, name="local_incidental_pressure", needs=["p_d", "ρ_cont", "h_l", "h_ref", "γ_inc"], provides=["p_li"]),
    operation(p_test_loc_uty2, name="pli hydrotest", needs=["α_spt", "p_lt", "p_li"], provides=["pli_lt_uty"])
)


cgraph= compose("mill test calcs", cgraph, 
   operation(char_WT, name="t_min for mill_test", needs=["t_nom", "t_fab", "t_corr_mill_test"],  provides=["t_min_mill_test"]),
   operation(p_mill_test, name="mill_test pressure", needs=["D_o", "t_min_mill_test", "SMYS", "SMTS", "α_U", "α_mpt", keyword("mill_test_k", "k")],  provides=["p_mpt"]),
   operation(p_mill_test_uty, name="pli mill test unity", needs=["p_li", "p_e", "p_mpt"], provides=["pli_mpt_uty"])
)


cgraph= compose("pressure containment (operation)", cgraph, 
operation(p_contain_resist, name="containment resistance", needs=["D_o", "t_1", "f_y", "f_u"], provides=["p_b"]),
operation(p_contain_resist_uty, name="containment resistance unity", needs=["p_li", "p_e",  "p_b", "γ_m", "γ_SCPC"],  provides=["pli_cont_res_uty"]),
operation(p_contain_uty2, name="containment resistance oepration", needs=["pli_cont_res_uty", "pli_mpt_uty", "pli_lt_uty"], provides=["pli_cont_uty"])
)





cgraph= compose("pt material strength", cgraph,
    operation(char_strength, name="pt_char_fy", needs=["SMYS", "α_U_pt", keyword("f_ytemp")], provides=["pt_f_y"]), 
    operation(char_strength, name="pt_char_fu", needs=["SMTS", "α_U_pt", keyword("f_utemp", "f_ytemp")], provides=["pt_f_u"])
)

cgraph= compose("pressure containment (operation)", cgraph, 
operation(p_contain_resist, name="pt p_b", needs=["D_o", "t_1", "pt_f_y", "pt_f_u"], provides=["pt_p_b"]),
operation(p_mill_test, name="pt mill_test pressure", needs=["D_o", "t_min_mill_test", "SMYS", "SMTS", "α_U_pt", "α_mpt", keyword("mill_test_k", "k")],  provides=["pt_p_mpt"]),
operation(p_mill_test_uty, name="plt mill test unity", needs=["p_lt", "p_e", "pt_p_mpt"], provides=["plt_mpt_uty"]),
operation(p_contain_resist_uty, name="pt containment resistance unity", needs=["p_lt", "p_e",  "pt_p_b", "γ_m", "γ_SCPC"],  provides=["plt_cont_res_uty"]),
operation(p_contain_uty2, name="pt containment resistance", needs=["plt_cont_res_uty", "plt_mpt_uty"], provides=["plt_cont_uty"])
)
#cgraph


cgraph= compose("pressure containment (operation)", cgraph, 
# operation(p_contain_resist, name="pt p_b", needs=["D_o", "t_1", "pt_f_y", "pt_f_u"], provides=["pt_p_b"]),
# operation(p_mill_test, name="pt mill_test pressure", needs=["D_o", "t_min_mill_test", "SMYS", "SMTS", "α_U_pt", "α_mpt", keyword("mill_test_k", "k")],  provides=["pt_p_mpt"]),
# operation(p_mill_test_uty, name="plt mill test unity", needs=["p_lt", "p_e", "pt_p_mpt"], provides=["plt_mpt_uty"]),
# operation(p_contain_resist_uty, name="pt containment resistance unity", needs=["p_lt", "p_e",  "pt_p_b", "γ_m", "γ_SCPC"],  provides=["plt_cont_res_uty"]),
operation(p_contain_uty2, name="press contain unity check", needs=["pli_cont_uty", "plt_cont_uty"], provides=["press_contain_unity"])
)

cgraph.plot("design-pressure_test1.svg")

# result = cgraph.compute(params, outputs=["p_e", "p_li", "p_mpt", "pli_cont_res_uty", "pli_mpt_uty", "pli_lt_uty", "pli_cont_uty"])
result = cgraph.compute(params)
result.plot("design-pressure_test2.svg")

#df = pd.DataFrame(data=dict(result), index=["one", "two"])

try:
    df = pd.DataFrame(data=dict(result))
except ValueError:
    df = pd.DataFrame(data=dict(result), index=[0]) # ValueError: If using all scalar values, you must pass an index


# ===============================================
# cgraph= compose("pressures", cgraph, 
#     operation(char_WT, name="t_min for mill_test", needs=["t_nom", "t_fab", "t_corr_mill_test"],  provides=["t_min_mill_test"])
# )


# cgraph= compose("mill test calcs", cgraph, 
#    operation(p_mill_test, name="mill_test pressure", needs=["D_o", "t_min_mill_test", "SMYS", "SMTS", "α_U", "α_mpt", keyword("mill_test_k", "k")],  provides=["p_mpt"]),
#    operation(p_mill_test_uty, name="p_mill_test_unity", needs=["p_li", "p_e", "p_mpt"], provides=["pli_mpt_uty"])
# )
# cgraph
