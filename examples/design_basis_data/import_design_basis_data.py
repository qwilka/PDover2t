"""
"""

import json

from pdover2t.utilities.data import json2globals


data_fp = "P01.json"

P01 = {
    "alpha_U": 1.0,
    "D": 0.6176,
    "g": 9.81,
    "gamma_inc": 1.1,
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


with open(data_fp, 'w') as _fh:
    json.dump(P01, _fh)

#del P01

# with open(data_fp, 'r') as _fh:
#     P01_copy = json.load(_fh)

json2globals(data_fp)   # , globals()
