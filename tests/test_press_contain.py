import unittest

from pdover2t.dnvgl_st_f101 import pressure_containment_all


parameters = {
    'alpha_mpt': 1.088,
    'alpha_spt': 1.05,
    "alpha_U": 1.0,
    "D": 0.6176,
    "g": 9.81,
    "gamma_inc": 1.1,
    'gamma_m': 1.15,
    'gamma_SCPC': 1.138,
    "h_ref": 30.,
    "h_l": -340.,
    "material": "CMn",
    "p_d": 240e5, 
    "rho_cont": 275.,
    "rho_water": 1027.,
    "rho_t": 1027.,
    "SMYS": 450.e6,
    "SMTS": 535.e6,
    "t": 0.0212,
    "t_corr": 0.0005,
    "t_fab": 0.001,
    "T": 60,
}


class BasicTests(unittest.TestCase):

    def test_press_contain_all_unity(self):
        retVal = pressure_containment_all(**parameters)
        p_cont_uty = retVal["p_cont_uty"]
        self.assertAlmostEqual(p_cont_uty, 0.928618343, places=4)

    def test_press_contain_all_all(self):
        retVal = pressure_containment_all(**parameters)
        self.assertAlmostEqual(retVal['p_inc'], 26400000.00000, places=2)
        self.assertAlmostEqual(retVal['p_li'], 27398167.5000, places=2)
        self.assertAlmostEqual(retVal['p_e'], 3425455.80, places=2)
        self.assertEqual(retVal['f_y'], 444000000.0)
        self.assertEqual(retVal['gamma_m'], 1.15)
        self.assertEqual(retVal['gamma_SCPC'], 1.138)
        self.assertEqual(retVal['alpha_spt'], 1.05)
        self.assertEqual(retVal['t_1'], 0.0197)
        self.assertEqual(retVal['t_min'], 0.0202)
        self.assertAlmostEqual(retVal['p_b'], 25815462.161414, places=2)
        self.assertAlmostEqual(retVal['p_lt'], 259108736.4857, places=2)
        self.assertAlmostEqual(retVal['p_mpt'], 30879398.9641387, places=2)
        self.assertAlmostEqual(retVal['p_cont_res_uty'], 0.928618343, places=5)
        self.assertAlmostEqual(retVal['p_lt_uty'], 0.092519889, places=5)
        self.assertAlmostEqual(retVal['p_mpt_uty'], 0.776333494, places=5)
        self.assertAlmostEqual(retVal['p_cont_uty'], 0.928618343, places=5)



if __name__ == '__main__':
    unittest.main()
    # p_cont_overall = press_contain_overall(ret="all", **parameters)
    # print("press_contain_overall=", p_cont_overall)

