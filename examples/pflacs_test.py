import logging

import pdover2t
from pflacs import Loadcase, Parameter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # logging.DEBUG 
lh = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# lh.setFormatter(formatter)
logger.addHandler(lh)

params = {
    "alpha_U": 1.0,
    "gamma_inc": 1.1,
    "h_ref": 30.,
    "material": "CMn",
    "p_d": 240e5, 
    "rho_cont": 275.,
    "rho_w": 1027.,
    "SC": "medium",
    "SMYS": 450.e6,
    "SMTS": 535.e6,
    "T": 60,
}

basecase = Loadcase("Base case", params=params,
                data={"description": "This is the base-case loadcase."})
basecase.plugin_func(pdover2t.dnvgl_st_f101.incid_ref_press)
basecase.plugin_func(pdover2t.dnvgl_st_f101.local_incid_press)
basecase.plugin_func(pdover2t.dnvgl_st_f101.char_mat_strength)

basecase.add_param("p_inc", basecase.incid_ref_press())

print(basecase.char_mat_strength())
#print(basecase.local_incid_press(h_l=30)/1.e5)