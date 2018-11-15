import logging
#import math

import numpy as np
#import scipy.optimize

from . import factor
from .material import char_mat_strength
#from .. import misc

__all__ = [ "propbuck_char_pressure", 
            "propbuck_unity", 
            "propbuck_critical_wd",
            "propbuck_crossover_press",
            "propbuck_arrestor_unity",
            "propbuck_critical_wd" ]

logger = logging.getLogger(__name__)


def propbuck_char_pressure(t_2, D, f_y, alpha_fab) -> "p_pr":
    """Pipe propagating buckle characteristic pressure. 
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.5.1, eq:5.16, page:96 $p_{pr}$
    """
    if np.any(D/t_2<15) or np.any(D/t_2>45):
        logger.warning("%s.propagation_char_pressure: D/t ratio «%s» outside valid range." % (__name__, D/t_2))
    p_pr = 35 * f_y * alpha_fab * (t_2/D)**2.5
    return p_pr

def propbuck_unity(p_e, p_pr, p_min=0,
        gamma_m=None, limit_state="ULS", gamma_SCLB=None, SC="medium"
        ) -> "propbuck_uty":
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.5.1, eq:5.15, page:96 
    """
    if gamma_m is None:
        gamma_m = factor.gamma_m_map[limit_state]
    if gamma_SCLB is None:
        gamma_SCLB = factor.gamma_SCLB_map[SC]
    propbuck_uty = (p_e - p_min) * gamma_m * gamma_SCLB / p_pr 
    return propbuck_uty


def propbuck_crossover_press(p_pr, p_prBA, D, t_2, L_BA) -> "p_x":
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.5.2, eq:5.18, page:97 
    """
    p_x = p_pr + (p_prBA-p_pr) * (1 - np.exp(-20*t_2*L_BA/D**2))
    return p_x



def propbuck_arrestor_unity(p_e, p_x,
        gamma_m=None, limit_state="ULS", gamma_SCLB=None, SC="medium"
        ) -> "propbuck_arrestor_uty":
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.5.2, eq:5.17, page:97 
    """    
    if gamma_m is None:
        gamma_m = factor.gamma_m_map[limit_state]
    if gamma_SCLB is None:
        gamma_SCLB = factor.gamma_SCLB_map[SC]
    propbuck_arrestor_uty = p_e * 1.1 * gamma_m * gamma_SCLB / p_x
    return propbuck_arrestor_uty


def propbuck_critical_wd(t_2, D, p_pr, rho_water, SMYS, p_min=0, g=9.81,
        T=None, material="CMn", alpha_U=1.00, alpha_fab=1.0,
        gamma_m=None, limit_state="ULS", gamma_SCLB=None, SC="medium"
        ) -> "propbuck_crit_wd":
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.5.1, eq:5.15, page:96 
    """
    if gamma_m is None:
        gamma_m = factor.gamma_m_map[limit_state]
    if gamma_SCLB is None:
        gamma_SCLB = factor.gamma_SCLB_map[SC]
    if T is not None:
        f_y = char_mat_strength(SMYS, T, material, alpha_U=alpha_U)
    else:
        f_y = SMYS
    p_pr = propbuck_char_pressure(t_2, D, f_y, alpha_fab)
    propbuck_crit_wd = (p_pr - p_min*gamma_m*gamma_SCLB) / (gamma_m*gamma_SCLB*rho_water*g)
    return propbuck_crit_wd



if __name__ == "__main__":
    alpha_fab = 0.85
    alpha_U = 1.00
    D = 0.660
    g = 9.81
    h_l = -410.   # np.linspace(0,500,10)  
    material = "CMn"
    rho_water = 1027.
    SMYS = 450.e6
    t = 0.0212
    t_corr = 0.0005
    T = 60
    t_2 = t - t_corr   # for operation (corrosion)  t_2 = t - t_corr np.array([t, t - t_corr])
    p_e = rho_water * g * abs(h_l)
    f_y = char_mat_strength(SMYS, T, material, alpha_U=alpha_U)
    p_pr = propbuck_char_pressure(t_2, D, f_y, alpha_fab)
    propbuck_uty = propbuck_unity(p_e, p_pr)
    propbuck_crit_wd = propbuck_critical_wd(t_2, D, p_pr, rho_water, SMYS, 
        T=T, material=material, alpha_U=alpha_U, alpha_fab=alpha_fab )

    # buckle arrestor properties
    L_BA = 12.2
    t = 0.0319
    t_corr = 0.0005
    t_2 = t - t_corr
    p_prBA = propbuck_char_pressure(t_2, D, f_y, alpha_fab)
    p_x = propbuck_crossover_press(p_pr, p_prBA, D, t_2, L_BA)
    propbuck_arrestor_uty = propbuck_arrestor_unity(p_e, p_x)

