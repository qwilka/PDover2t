import logging
#import math

import numpy as np
#import scipy.optimize

from . import factor
from .material import char_mat_strength

logger = logging.getLogger(__name__)


def prop_char_pressure(t_2, D, f_y, alpha_fab) -> "p_pr":
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.5.1, eq:5.16, page:96 $p_{pr}$
    """
    if np.any(D/t_2<15) or np.any(D/t_2>45):
        logger.warning("%s.propagation_char_pressure: D/t ratio «%s» outside valid range." % (__name__, D/t_2))
    p_pr = 35 * f_y * alpha_fab * (t_2/D)**2.5
    return p_pr

def prop_buckling_unity(p_e, p_pr, p_min=0,
        gamma_m=None, limit_state="ULS", gamma_SCLB=None, SC="medium"
        ) -> "prop_buck_uty":
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.5.1, eq:5.15, page:96 
    """
    if gamma_m is None:
        gamma_m = factor.gamma_m_map[limit_state]
    if gamma_SCLB is None:
        gamma_SCLB = factor.gamma_SCLB_map[SC]
    prop_buck_uty = (p_e - p_min) * gamma_m * gamma_SCLB / p_pr 
    return prop_buck_uty



if __name__ == "__main__":
    alpha_fab = 0.85
    alpha_U = 1.00
    D = 0.660
    g = 9.81
    h_l = -410.
    material = "CMn"
    rho_water = 1027.
    SMYS = 450.e6
    t = 0.0212
    t_corr = 0.0005
    T = 60
    t_2 = t - t_corr   # for operation (corrosion)  t_2 = t - t_corr np.array([t, t - t_corr])
    p_e = rho_water * g * abs(h_l)
    f_y = char_mat_strength(SMYS, T, material, alpha_U=alpha_U)
    p_pr = prop_char_pressure(t_2, D, f_y, alpha_fab)
    prop_buck_uty = prop_buckling_unity(p_e, p_pr)
