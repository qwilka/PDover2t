"""


"""
from datetime import datetime, UTC
import sys

import pandas as pd 

import pdover2t.config
pdover2t.config.use_numpy = True
from pdover2t.pipe.environment import still_water_level
from pdover2t.DNVSTF101.pressure_containment_bursting import pressure_containment_bursting, pressure_containment_bursting_check
from pdover2t.DNVSTF101.buckling_collapse import local_buckling_collapse_all
from pdover2t.DNVSTF101.propagation_buckling import local_buckling_propagation_all
from pdover2t.utilities.dfxl import loadcases2excel


MSL = 55.0  # mean sea level/water depth 
tide = 1.0
LAT, MWL, HAT = still_water_level(MSL, WL_ref="MSL", tide_t1=tide, tide_t2=tide, storm_surge_pos=0.0, storm_surge_neg=0.0, fsurge=1.0)
h_l = -MSL
basecase = {
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

    "γ_inc": 1.10 , # incidental to design pressure ratio
    "ρ_cont_d": 20., # (kg/m3) density of pipeline design fluid content
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
    "h_l": h_l,
    "LAT": LAT,
}

if pdover2t.config.use_numpy:
    import numpy as np
    basecase["name"] = np.array(["basecase-24-50", "LC1-24-150", "LC2-36-50", "LC3-36-150", "LC3-40-150", "LC3-42-150"])
    basecase["comment"] = np.array(["24\" 50bar", "24\" 150bar", "36\" 50bar", "36\" 150bar", "40\" 150bar", "40\" 150bar"])
    basecase["NPS"] = np.array([24, 24, 36, 36, 40, 42])
    basecase["p_d"] = np.array([50.0, 150.0, 50.0, 150.0, 150.0, 150.0]) * 1.e5
    basecase["D_o"] = np.array([24.0, 24.0, 36.0, 36.0, 40.0, 42.0]) * 25.4 * 1.e-3
    basecase["t_nom"] = np.array([15.9, 15.9, 30.0, 30.0, 30.0, 30.0]) * 1.e-3
    basecase["h_l"] = np.array([-MSL, -MSL, -110.0, -110.0, -110.0, -110.0])

pc = pressure_containment_bursting(**basecase)
pc_check = pressure_containment_bursting_check(**basecase,**pc._asdict())
# # pc_dict = pc._asdict()
# # pc_dict.update(check._asdict())

coll = local_buckling_collapse_all(**basecase)
prop = local_buckling_propagation_all(**basecase)

df2xl = [
    (basecase, "premise", "Design premise data", "Big Development Project", "A. Pipeline-Engineer", datetime.now(UTC).isoformat()),
    (pc,       "bursting", "Pressure containment (bursting)", "DNV-ST-F101 (2021-08) sec:5.4.2"),
    (coll,     "collapse", "Collapse (local buckling)", "DNV-ST-F101 (2021-08) sec:5.4.4"),
    (prop,     "propagation", "Propagation buckling", "DNV-ST-F101 (2021-08) sec:5.4.5"),
]

# save excel file in _doc/ folder for gitignore
loadcases2excel("_doc/BHC_loadcases.xlsx", df2xl)



