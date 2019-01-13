"""Analysis of gas pipeline «P-01»
"""
import logging

import numpy as np

import pdover2t
from pflacs import Premise, CallNode

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # logging.DEBUG 
lh = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# lh.setFormatter(formatter)
logger.addHandler(lh)


field_params = {
    "ast_country": "IRL",
    "ast_desc": "Pflacs oil&gas field, subsea",
    "ast_domain": "SUBSEA",
    "ast_field": "Pflacs",
    "ast_url": "IRL:PFLACS:SUBSEA",
    "design_life": 25,
}
constants = {
    "g": 9.81, 
}

pipeline_params = {
    "ast_desc": "P-01 gas pipeline",
    "ast_tag": "P-01",
    "ast_uri": "IRL:PFLACS:P-01",
    "D": 0.6176,
    "h_l": -340.,
    "material": "CMn",
    "SMYS": 450.e6,
    "SMTS": 535.e6,
    "t": 0.0212,
    "t_corr": 0.0005,
    "t_fab": 0.001,
}
process_params = {
    "h_ref": 30.,
    "p_d": 240e5,
    "rho_cont": 275.,
    "rho_t": 1027.,
    "T": 60,
}
design_params = {
    "alpha_U": 1.0,   
    "gamma_inc": 1.1,
    "SC": "medium",
}
env_params = {
    "rho_water": 1027.,    
}

# parameters = {
#     "alpha_U": 1.0,
#     "D": 0.6176,
#     "g": 9.81,
#     "gamma_inc": 1.1,
#     "h_ref": 30.,
#     "h_l": -340.,
#     "material": "CMn",
#     "p_d": 240e5, 
#     "rho_cont": 275.,
#     "rho_water": 1027.,
#     "rho_t": 1027.,
#     "SC": "medium",
#     "SMYS": 450.e6,
#     "SMTS": 535.e6,
#     "t": 0.0212,
#     "t_corr": 0.0005,
#     "t_fab": 0.001,
#     "T": 60,
# }

vnpkl_file = "/home/develop/engineering/src/scratch/pflacs_test/IRL--PFLACS--P-01.vnpkl"


rootnode = Premise("Pflacs oil&gas field, subsea", 
                parameters={ **field_params, 
                    **constants,
                    **env_params
                },
                data={"desc": "Top-level field details, environmental and universal parameters."},
                vnpkl_fpath=vnpkl_file)
P01 = Premise("P-01 gas pipeline", 
                parent=rootnode,
                parameters=env_params,
                data={"desc": "Environmental parameters."})

rootnode.savefile()