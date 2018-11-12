import logging

import numpy as np

import pdover2t
from pflacs import Loadcase, CallNode

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # logging.DEBUG 
lh = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# lh.setFormatter(formatter)
logger.addHandler(lh)

parameters = {
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

basecase = Loadcase("Base case", parameters=parameters,
                data={"desc": "This is the base-case loadcase."})
lc1 = Loadcase("Load case 1", parent=basecase, 
            data={"desc": "This is the 1st child loadcase."})
lc2 = Loadcase("Load case 2", parent=basecase, 
            data={"desc": "This is the 2nd child loadcase."})

basecase.plugin_func("press_contain_unity", "pdover2t.dnvgl_st_f101")
basecase.plugin_func("press_contain_all", "pdover2t.dnvgl_st_f101")
_uty = lc1.press_contain_all(ret="unity")
lc1.add_param("p_cont_uty", _uty)
print(_uty)
lc1.rho_cont = np.linspace(100,1000,10) 
print("lc1.rho_cont", lc1.rho_cont) 
_uty = lc1.press_contain_all(ret="unity")
print(_uty)




# class ExNode(Loadcase):
#     def __init__(self, name=None, parent=None, parameters=None, pyfile=None,
#                 data=None, treedict=None):
#         super().__init__(name, parent, data, treedict)
#         self.primfunc = None
#     def __call__(self, *args, **kwargs):
#         return self.primfunc(*args, **kwargs)
#     def set_primfunc(self, name):
#         _func = getattr(self, name)
#         self.primfunc = _func



lc1_pcont = Loadcase("GROUP: lc1 press contain", parent=lc1, 
            data={"desc": "Group lc1 pressure contain calcs."}) 
_uty = lc1_pcont.press_contain_all(ret="unity", rho_cont=100)
print("lc1_pcont (rho_cont=100) ", _uty)
_uty = lc1_pcont.press_contain_all(ret="unity", rho_cont=200)
print("lc1_pcont (rho_cont=200) ", _uty)

lc1_pcont.p_cont_uty = lc1_pcont.press_contain_all(ret="unity", rho_cont=100)


lc2_pcont = CallNode("CallNode: lc2 press contain", parent=lc2, 
            data={"desc": "Group lc2 pressure contain calcs."},
            callfunc="press_contain_all") 
lc2_pcont.rho_cont = np.linspace(100,1000,10) 
lc2_pcont()

cc = lc2_pcont.call_child(call=True, T=22)

treedict = basecase.to_treedict()
import pickle
#import dill as pickle
pkl_file = "/home/develop/engineering/src/scratch/pflacs_test/pf_test.pkl"
with open(pkl_file, "wb") as pf:
    #pickle.dump(basecase, pf, byref=True)
    pickle.dump(treedict, pf)
