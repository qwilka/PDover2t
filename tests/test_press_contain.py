import unittest

from pdover2t.dnvgl_st_f101.press_contain import press_contain_all


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


class BasicTests(unittest.TestCase):

    def test_press_contain_all_unity(self):
        retVal = press_contain_all(ret="unity", **parameters)
        self.assertAlmostEqual(retVal, 0.8375219, places=4)

    def test_press_contain_all_all(self):
        retVal = press_contain_all(ret="all", **parameters)
        self.assertAlmostEqual(retVal['p_inc'], 26400000.00000, places=2)
        self.assertAlmostEqual(retVal['p_li'], 27398167.5000, places=2)
        self.assertAlmostEqual(retVal['p_e'], -3425455.80000, places=2)
        self.assertEqual(retVal['f_y'], 444000000.0)
        self.assertEqual(retVal['gamma_m'], 1.15)
        self.assertEqual(retVal['gamma_SCPC'], 1.138)
        self.assertEqual(retVal['alpha_spt'], 1.05)
        self.assertEqual(retVal['t_1'], 0.0197)
        self.assertEqual(retVal['t_min'], 0.0202)
        self.assertAlmostEqual(retVal['p_b'], 25815462.161414, places=2)
        self.assertAlmostEqual(retVal['p_lt'], 265959648.0857, places=2)
        self.assertAlmostEqual(retVal['p_mpt'], 30879398.9641387, places=2)
        self.assertAlmostEqual(retVal['p_cont_res_uty'], 0.83752198, places=5)
        self.assertAlmostEqual(retVal['p_lt_uty'], 8.62843558, places=5)
        self.assertAlmostEqual(retVal['p_mpt_uty'], 1.00180951, places=5)
        self.assertAlmostEqual(retVal['p_cont_uty'], 0.83752198, places=5)


# pr_contain_overall= {
#     'p_inc': 26400000.000000004, 
#     'p_li': 27398167.500000004, 
#     'p_e': -3425455.8000000003, 
#     'f_y': 444000000.0, 
#     'gamma_m': 1.15, 
#     'gamma_SCPC': 1.138, 
#     'alpha_spt': 1.05, 
#     't_1': 0.0197, 
#     't_min': 0.0202, 
#     'p_b': 25815462.16141416, 
#     'p_t': 27720000.000000004, 
#     'rho_t': 1027.0, 
#     'p_lt': 265959648.0857143, 
#     'alpha_U': 1.0, 
#     'alpha_mpt': 1.088, 
#     'p_mpt': 30879398.964138713, 
#     'p_cont_res_uty': 0.837521984685498, 
#     'p_lt_uty': 8.628435583227306, 
#     'p_mpt_uty': 1.0018095103095395, 
#     'p_cont_uty': 0.837521984685498}


if __name__ == '__main__':
    unittest.main()
    # p_cont_overall = press_contain_overall(ret="all", **parameters)
    # print("press_contain_overall=", p_cont_overall)

