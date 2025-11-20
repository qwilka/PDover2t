"""

create_graph_images = True
Windows NOTE  Graphtik/pydot encoding error
UnicodeEncodeError: 'charmap' codec can't encode character '\u03b1' in position 3695: character maps to <und
UnicodeEncodeError: 'charmap' codec can't encode character '\u03c1' in position 3196: character maps to <undefined>  efined>
https://stackoverflow.com/questions/50933194/how-do-i-set-the-pythonutf8-environment-variable-to-enable-utf-8-encodin  g-by-def
Graphtik plot: To plot graphs on Windows, set the following enviromental varibale  before launching Jupyter no  tebook   
set PYTHONUTF8=1  
set PYTHONUTF8=1   avoid trailing space 

https://github.com/pygraphkit/graphtik/issues/10  Exception with the latest versions of networkx #10

"""


from graphtik import compose, operation, keyword

from pdover2t.DNVSTF101.pressure_containment_bursting import *
from pdover2t.pipe.pipe import characteristic_WT
from pdover2t.pipe.material import characteristic_material_strength

# set PYTHONUTF8=1
create_graph_images = True

cgraph = compose("start",
  operation(lambda sea_level,tide: -(sea_level - tide), name="seabed level", needs=["MSL", "tide"], provides=["h_l"]),
  operation(characteristic_WT, name="characteristic WT", needs=["t_nom", "t_fab", "t_corr", "t_ero"],  provides=["t_1", "t_2"]),
    ##operation(p_incid_loc, name="local_incidental_pressure", needs=["p_d", "ρ_cont", "h_l", "h_ref", "γ_inc"], provides=["p_li"]),
    operation(external_water_pressure, name="external pressure", needs=["h_l", "ρ_xwater"],  provides=["p_e"])
)

cgraph= compose("material strength", cgraph,
    operation(characteristic_material_strength, name="char_fy", needs=["SMYS", "α_U", keyword("f_ytemp")], provides=["f_y"]), 
    operation(characteristic_material_strength, name="char_fu", needs=["SMTS", "α_U", keyword("f_utemp", "f_ytemp")], provides=["f_u"])
)

cgraph = compose("pressure test", cgraph,
    operation(incidental_reference_pressure, name="incidental pressure", needs=["p_d", "γ_inc"], provides=["p_inc"]),
    operation(local_incidental_pressure, name="local_incidental_pressure", needs=["p_d", "ρ_cont", "h_l", "h_ref"], provides=["p_li"]),
    operation(system_test_pressure, name="test pressure", needs=["p_d", "γ_inc", "α_spt"], provides=["p_t"]),
    operation(local_test_pressure, name="local test pressure", needs=["p_t", "ρ_t", "h_l", "h_ref"], provides=["p_lt"]),
    operation(local_test_pressure_unity, name="pli hydrotest", needs=["p_lt", "p_li", "α_spt"], provides=["pli_lt_uty"])
)



cgraph= compose("mill test calcs", cgraph, 
   operation(characteristic_WT, name="t_min for mill_test", needs=["t_nom", "t_fab", "t_corr_mill_test", "t_ero"],  provides=["t_1_mill_test", "t_2_mill_test"]),
   operation(mill_test_pressure, name="mill_test pressure", needs=["D_o", "t_1_mill_test", "SMYS", "SMTS", "α_U", "α_mpt", keyword("mill_test_k", "k")],  provides=["p_mpt"]),
   operation(mill_test_pressure_unity, name="pli mill test unity", needs=["p_li", "p_e", "p_mpt"], provides=["pli_mpt_uty"])
)


cgraph= compose("pressure containment (operation)", cgraph, 
operation(pressure_containment_resistance, name="containment resistance", needs=["D_o", "t_1", "f_y", "f_u"], provides=["p_b"]),
operation(pressure_containment_resistance_unity, name="containment resistance unity", needs=["p_li", "p_e",  "p_b", "γ_m", "γ_SCPC"],  provides=["pli_cont_res_uty"]),
operation(p_contain_uty2, name="compare unity values", needs=["pli_cont_res_uty", "pli_mpt_uty", "pli_lt_uty"], provides=["pli_cont_uty"])
)


# if create_graph_images:
#     cgraph.plot("pressure-containment_graphtik.svg")
try:
    cgraph.plot("./_doc/pressure-containment_graphtik.svg")
except Exception as e:
    print(f"error: cgraph.plot exception: {e}")



pc_gtik = cgraph

if __name__=="__main__":
    from pdover2t.pipe.pipe import PipeCoat  # linepipe_properties, pipeline_properties, 

    premise = {
        "name" : "basecase",
        "comment": "Basecase: 24\" 50bar-150bar ",
        "NPS":  24,                       #"24\"", 
        "D_o": 24 * 25.4 * 1.e-3,  # (m) pipe external diameter
        "p_d": 50.e5,  #np.array([50.e5, 150.e5]),  # (Pa) design pressure at reference elevation Z_ref
        "t_nom": 0.0159,  # (m) pipe wall thickness
        "t_corr": 0.0, # (m) corrosion allowance
        "t_ero": 0.0, # (m) erosion allowance
        "t_fab": 0.001, # (m) thickness negative fabrication tolerance

        "SMYS": 450.e6, # (Pa) pipe steel SMYS
        "f_ytemp": 35.e6, # (Pa) steel yield strength temperature de-rating
        "SMTS": 535.e6, # (Pa) pipe steel SMTS
        "f_utemp": 0.e6, # (Pa) steel ultimate strength temperature de-rating
        "α_U": 0.96, # material strength factor
        "α_U_spt": 1.0, # material strength factor for system pressure test cacls
        "γ_m": 1.15,  # material resistance factor
        "α_fab": 0.93, 
        "O_0": 1.5 /100.0,
        "E": 207.e9,
        "ν": 0.3, 
        "ρ_pipe": 7850.0,
        "coat": PipeCoat([(3.5e-3, 1000.0, "3LPE"), (40.0e-3, 3040.0, "CWC")]),  # [[]]  double list to prevent pandas iterating

        "γ_inc": 1.10 , # incidental to design pressure ratio
        "ρ_cont": 20., # (kg/m3) density of pipeline design fluid content
        "ρ_t": 1025. ,  # test fluid density

        "ρ_xwater": 1025., # (kg/m3) density of seawater

        "α_spt": 1.05,  # DNVGL-ST-F101 (2017-12) p94gamma
        "α_mpt": 1.088,  # p94
        "α_spt": 1.05,  # p94
        "γ_SCPC": 1.138,  # safety class resistance factor for pressure containment
        "γ_SCPC_pt": 1.046,  # safety class resistance factor for hydrotest
        "γ_SCLB": 1.14,  # safety class resistance factor for local buckling and collapse

        "mill_test_k": 1.0,   # k parameter used for calculating mill test pressure
        "t_corr_mill_test": 0.0,

        "h_ref": 0.0 , # (m) reference elevation for pressure (MSL=0m)
#        "h_l": h_l,
        "MSL": 55.0,
        "tide": 1.0,
    }
    bcase = cgraph.compute(premise)
    # if create_graph_images:
    #     bcase.plot("pressure-containment_sol.svg")
    try:
        bcase.plot("./_doc/pressure-containment_sol.svg")
    except Exception as e:
        print(f"error: bcase.plot exception: {e}")


    import pdover2t.config
    pdover2t.config.use_numpy = True

    if True and pdover2t.config.use_numpy:
        import numpy as np
        premise["name"] = np.array(["basecase-24-50", "LC1-24-150", "LC2-36-50", "LC3-36-150", "LC3-40-150", "LC3-42-150"])
        premise["comment"] = np.array(["24\" 50bar", "24\" 150bar", "36\" 50bar", "36\" 150bar", "40\" 150bar", "40\" 150bar"])
        premise["NPS"] = np.array([24, 24, 36, 36, 40, 42])
        premise["p_d"] = np.array([50.0, 150.0, 50.0, 150.0, 150.0, 150.0]) * 1.e5
        premise["D_o"] = np.array([24.0, 24.0, 36.0, 36.0, 40.0, 42.0]) * 25.4 * 1.e-3
        premise["t_nom"] = np.array([15.9, 15.9, 30.0, 30.0, 30.0, 30.0]) * 1.e-3
        premise["MSL"] = np.array([55.0, 55.0, 110.0, 110.0, 110.0, 110.0])

        all_lcs = cgraph.compute(premise)
