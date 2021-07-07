"""
Pipeline pressure containment according to DNVGL-ST-F101 (2017-12)
refs:


Notes:


to run:
python DnvStF101_pressure_containment.py 
"""
from pdover2t.DnvStF101 import *

# Gas Export (0-0.3 km) location class II, 60°C max. Temp. 340-370m depth
p_d = 240.e5  # (Pa) design pressure at reference elevation Z_ref
h_ref = 30.0  # (m) reference elevation for pressure (LAT=0m)
ρ_cont = 275. # (kg/m3) density of pipeline contents



γ_inc = 1.10  # incidental to design pressure ratio
α_spt = 1.05  # DNVGL-ST-F101 (2017-12) p94


p_inc = p_incid_ref(p_d, γ_inc)
p_t = p_system_test_ref(p_d,  γ_inc, α_spt)
p_li = p_incid_loc(p_d, ρ_cont, h_ref, h_ref, γ_inc)  # h_l=h_ref

# #import argparse
# import numpy as np


# from pdover2t.utilities import turn_on_logging
# turn_on_logging(template='%(levelname)s: %(message)s')

# from pdover2t.dnvgl_st_f101 import pressure_containment_all
# from pdover2t.pipe import pipe_Do_Di_WT

# # p32  
# # Gas Export (0-0.3 km) location class II, 60°C max. Temp. 340-370m depth
# p_d = 240.e5  # (Pa) design pressure at reference elevation Z_ref
# h_ref = 30.0  # (m) reference elevation for pressure (LAT=0m)
# γ_inc = 1.10  # incidental to design pressure ratio

# ρ_cont = 275. # (kg/m3) density of pipeline contents

# ρ_seawater = 1027. # (kg/m3) density of seawater
# MSL = 340. # (m) seawater depth (wrt MSL)
# LAT = MSL - 1.1 # adjust tide
# h_l = -LAT   # adjust h_l for tide and 

# SMYS = 450.e6 # (Pa) pipe steel SMYS
# f_ytemp = 6.e6 # (Pa) steel yield strength temperature de-rating
# SMTS = 535.e6 # (Pa) pipe steel SMTS
# f_utemp = 6.e6 # (Pa) steel ultimate strength temperature de-rating

# α_U = 1.0 # material strength factor
# #α_Ahoop = 1.0 # anisoptropy factor, hoop
# γ_m = 1.15  # material resistance factor


# D_i = 0.6172  # (m) pipe internal diameter
# t_nom = 0.0242  # (m) pipe wall thickness
# t_corr = 0.0005 # (m) corrosion allowance
# t_fab = 0.001 # (m) thickness negative fabrication tolerance

# ρ_t = ρ_seawater  # test fluid density

# α_mpt = 1.251  # p94
# α_spt = 1.05  # p94

# #Do, Di, WT = pipe_Do_Di_WT(Di=D_i, WT=t_nom-t_corr-t_fab)
# Do, Di, WT = pipe_Do_Di_WT(Di=D_i, WT=t_nom)
# t = WT

# # p32  
# γ_SCPC = 1.308  # safety class resistance factor for pressure containment

# KP300m = pressure_containment_all(p_d,  
#         Do, t, t_corr, t_fab,
#         h_l, h_ref, ρ_cont, ρ_seawater, ρ_t,
#         γ_inc=γ_inc,
#         γ_m=γ_m, γ_SCPC=γ_SCPC, α_U=α_U, 
#         α_spt=α_spt, α_mpt=α_mpt, 
#         SMYS=SMYS, SMTS=SMTS,  
#         f_ytemp=f_ytemp, f_utemp=f_utemp)


# # p33
# γ_SCPC = 1.138 

# KP15 = pressure_containment_all(p_d,  
#         Do, t, t_corr, t_fab,
#         h_l, h_ref, ρ_cont, ρ_seawater, ρ_t,
#         γ_inc=γ_inc,
#         γ_m=γ_m, γ_SCPC=γ_SCPC, α_U=α_U, 
#         α_spt=α_spt, α_mpt=α_mpt, 
#         SMYS=SMYS, SMTS=SMTS,  
#         f_ytemp=f_ytemp, f_utemp=f_utemp)


# # p34
# t_nom = 0.0214
# Do, Di, WT = pipe_Do_Di_WT(Di=D_i, WT=t_nom)
# t = WT
# MSL = 250. # (m) seawater depth (wrt MSL)
# LAT = MSL - 1.1 # adjust tide
# h_l = -LAT   # adjust h_l for tide and 
# f_ytemp = 0.0
# f_utemp = 0.0
# γ_SCPC = 1.138 

# KP80 = pressure_containment_all(p_d,  
#         Do, t, t_corr, t_fab,
#         h_l, h_ref, ρ_cont, ρ_seawater, ρ_t,
#         γ_inc=γ_inc,
#         γ_m=γ_m, γ_SCPC=γ_SCPC, α_U=α_U, 
#         α_spt=α_spt, α_mpt=α_mpt, 
#         SMYS=SMYS, SMTS=SMTS,  
#         f_ytemp=f_ytemp, f_utemp=f_utemp)


# # repeat 3 cases as a single array 
# t_nom = np.array([0.0242, 0.0242, 0.0214])
# Do, Di, WT = pipe_Do_Di_WT(Di=D_i, WT=t_nom)

# MSL = np.array([340., 340., 250.])
# LAT = MSL - 1.1 
# h_l = -LAT
# f_utemp = f_ytemp = np.array([6.e6, 6.e6, 0.0])

# γ_SCPC = np.array([1.308, 1.138, 1.138])

# arr = pressure_containment_all(p_d,  
#         Do, WT, t_corr, t_fab,
#         h_l, h_ref, ρ_cont, ρ_seawater, ρ_t,
#         γ_inc=γ_inc,
#         γ_m=γ_m, γ_SCPC=γ_SCPC, α_U=α_U, 
#         α_spt=α_spt, α_mpt=α_mpt, 
#         SMYS=SMYS, SMTS=SMTS,  
#         f_ytemp=f_ytemp, f_utemp=f_utemp)




