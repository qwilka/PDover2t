import logging

import pdover2t
from pflacs import Loadcase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # logging.DEBUG 
lh = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# lh.setFormatter(formatter)
logger.addHandler(lh)

params = {
    "alpha_U": 1.0,
    "D": 0.6176,
    "g": 9.81,
    "gamma_inc": 1.1,
    "h_ref": 30.,
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

basecase = Loadcase("Base case", params=params,
                data={"desc": "This is the base-case loadcase."})
lc1 = Loadcase("Load case 1", parent=basecase, 
            data={"desc": "This is the 1st child loadcase."})

basecase.plugin_func("incid_ref_press", "pdover2t.dnvgl_st_f101")
basecase.plugin_func("local_incid_press", "pdover2t.dnvgl_st_f101")
basecase.plugin_func("external_pressure", "pdover2t.dnvgl_st_f101")
basecase.plugin_func("char_mat_strength", "pdover2t.dnvgl_st_f101")
basecase.plugin_func("system_test_press", "pdover2t.dnvgl_st_f101")
basecase.plugin_func("press_contain_resis", "pdover2t.dnvgl_st_f101")

basecase.add_param("p_inc", basecase.incid_ref_press())
basecase.add_param("h_l", -340)
basecase.add_param("p_li", basecase.local_incid_press())
basecase.add_param("p_e", basecase.external_pressure())
basecase.add_param("f_y", basecase.char_mat_strength())
basecase.add_param("gamma_m", pdover2t.dnvgl_st_f101.factor.gamma_m["ULS"])
basecase.add_param("gamma_SCPC", pdover2t.dnvgl_st_f101.factor.gamma_SCPC[basecase.SC])

basecase.add_param("t_1", basecase.t-basecase.t_corr-basecase.t_fab)
basecase.add_param("p_b", basecase.press_contain_resis(t=basecase.t_1))

basecase.add_param("alpha_spt", pdover2t.dnvgl_st_f101.factor.alpha_spt[basecase.SC])
basecase.add_param("p_t", basecase.system_test_press())
basecase.plugin_func("local_test_press", "pdover2t.dnvgl_st_f101")
basecase.add_param("p_lt", basecase.local_test_press())

basecase.add_param("t_min", basecase.t - basecase.t_fab)  # t1, prior to operation table 5.5 p.91
basecase.plugin_func("mill_test_press", "pdover2t.dnvgl_st_f101")
basecase.add_param("p_mpt", basecase.mill_test_press())
basecase.add_param("alpha_mpt", pdover2t.dnvgl_st_f101.factor.alpha_mpt[basecase.SC])

basecase.plugin_func("press_contain_resis_unity", "pdover2t.dnvgl_st_f101")
basecase.add_param("p_cont_res_uty", basecase.press_contain_resis_unity())
basecase.plugin_func("local_test_press_unity", "pdover2t.dnvgl_st_f101")
basecase.add_param("p_lt_uty", basecase.local_test_press_unity())
basecase.plugin_func("mill_test_press_unity", "pdover2t.dnvgl_st_f101")
basecase.add_param("p_mpt_uty", basecase.mill_test_press_unity())


basecase.plugin_func("press_contain_unity", "pdover2t.dnvgl_st_f101")
basecase.add_param("p_cont_uty", basecase.press_contain_unity())


print("char_mat_strength=", basecase.char_mat_strength())
print("p_cont_uty=", basecase.p_cont_uty)
#print(basecase.local_incid_press(h_l=30)/1.e5)

treedict = basecase.to_treedict()
import pickle
#import dill as pickle
pkl_file = "/home/develop/engineering/src/scratch/pflacs_test/pf_test.pkl"
with open(pkl_file, "wb") as pf:
    #pickle.dump(basecase, pf, byref=True)
    pickle.dump(treedict, pf)
