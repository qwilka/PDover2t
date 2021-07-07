import logging

import numpy as np

import pdover2t
from pflacs import Premise, Calc

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # logging.DEBUG 
lh = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# lh.setFormatter(formatter)
logger.addHandler(lh)

parameters = {
    "alpha_mpt": 1.088,
    "alpha_spt": 1.05,
    "alpha_U": 1.0,
    "D": 0.6176,
    "g": 9.81,
    "gamma_inc": 1.1,
    "gamma_m": 1.15,
    "gamma_SCPC": 1.138,
    "h_ref": 30.,
    "h_l": -340.,
    "material": "CMn",
    "p_d": 240e5, 
    "rho_cont": 275.,
    "rho_water": 1027.,
    "rho_t": 1027.,
    "SC": "medium",
    "SMYS": 450.e6,
    "SMTS": 535.e6,
    "t": 0.0212,
    "t_corr": 0.0005,
    "t_fab": 0.001,
    "T": 60,
}

vnpkl_file = "/home/develop/engineering/src/scratch/pflacs_test/pf_test.vnpkl"

basecase = Premise("Base case", parameters=parameters,
                data={"desc": "This is the base-case loadcase."},
                vnpkl_fpath=vnpkl_file)
lc1 = Premise("Load case 1", parent=basecase, 
            data={"desc": "This is the 1st child loadcase."})
gc1 = Premise("gchild lc1", parent=lc1, 
            data={"desc": "This is the 1st child loadcase."})
lc2 = Premise("Load case 2", parent=basecase, 
            data={"desc": "This is the 2nd child loadcase."})

basecase.plugin_func("pressure_containment_all", "pdover2t.dnvgl_st_f101")

lc1.rho_cont = np.linspace(100,1000,10) 
print("lc1.rho_cont", lc1.rho_cont) 
resdict = lc1.pressure_containment_all()
print(resdict["p_cont_uty"])


lc1_pcont = Premise("GROUP: lc1 press contain", parent=lc1, 
            data={"desc": "Group lc1 pressure contain calcs."}) 
_uty = lc1_pcont.pressure_containment_all(rho_cont=100)
print("lc1_pcont (rho_cont=100) ", _uty)

lc2_pcont = Calc("CallNode: lc2 press contain", parent=lc2, 
            data={"desc": "Group lc2 pressure contain calcs."},
            funcname="pressure_containment_all") 
lc2_pcont.rho_cont = np.linspace(100,1000,10) 
lc2_pcont()


basecase.savefile()
