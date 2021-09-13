from pdover2t.DnvStF101 import pressure_containment_all

def ttest():
    #D_i = 0.6172  # (m) pipe internal diameter
    t_nom = 0.0242  # (m) pipe wall thickness
    t_corr = 0.0005 # (m) corrosion allowance
    t_fab = 0.001 # (m) thickness negative fabrication tolerance
    D_o = 0.6656  # (m) pipe external diameter

    SMYS = 450.e6 # (Pa) pipe steel SMYS
    f_ytemp = 6.e6 # (Pa) steel yield strength temperature de-rating
    SMTS = 535.e6 # (Pa) pipe steel SMTS
    f_utemp = 6.e6 # (Pa) steel ultimate strength temperature de-rating
    α_U = 1.0 # material strength factor
    #α_Ahoop = 1.0 # anisoptropy factor, hoop
    γ_m = 1.15  # material resistance factor

    p_d = 240.e5  # (Pa) design pressure at reference elevation Z_ref
    γ_inc = 1.10  # incidental to design pressure ratio
    h_ref = 30.0  # (m) reference elevation for pressure (LAT=0m)
    ρ_cont = 275. # (kg/m3) density of pipeline contents
    ρ_t = 1027.   # test fluid density

    # MSL = 340. # (m) seawater depth (wrt MSL)
    # LAT = MSL - 1.1 # adjust tide
    h_l = -338.9   # adjust h_l for tide and 
    ρ_seawater = 1027. # (kg/m3) density of seawater


    α_spt = 1.05  # DNVGL-ST-F101 (2017-12) p94
    α_mpt = 1.251  # p94
    α_spt = 1.05  # p94
    γ_SCPC = 1.308  # safety class resistance factor for pressure containment

    return locals()
    

dd = ttest()
# dd.pop("D_i")
# dd.pop("MSL")
# dd.pop("LAT")
#print("locals()", dd)

sol = pressure_containment_all(**dd)
