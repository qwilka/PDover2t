import unittest

from pdover2t.dnv.st_f101 import P_containment




class BasicTests(unittest.TestCase):

    def test_P_containment(self):
        retVal = P_containment(660.e-3, 4.32e8, 5.136e8, 0.0199, 2.5e7, 2.5e6,
                        1.15, 1.138, 'P')
        self.assertAlmostEqual(retVal, 26199995.174492124, places=2)




if __name__ == '__main__':
    unittest.main()


