import math

import numpy as np

from . import factor
from .material import char_mat_strength

##testlam = lambda x: "just a test..."

def incid_ref_press(p_d, gamma_inc) -> "p_inc":
    """Calculate DNVGL-ST-F101 «incidental reference pressure». 

    :param p_d: $p_d$ design pressure
    :param gamma_inc: $\gamma_{inc}$ incidental to design pressure ratio
    :returns: p_inc: $p_{inc}$ incidental reference pressure

    Reference:
    DNVGL-ST-F101 (2017-12) 
        eq:4.3 sec:4.2.2.2 page:67 p_{inc}

    Example:    
    >>> incid_ref_press(100e5, 1.1)
    11000000.0
    """
    return p_d * gamma_inc


def system_test_press(p_d, gamma_inc, alpha_spt) -> "p_t":
    """Calculate DNVGL-ST-F101 «system test pressure». 

    :param p_d: $p_d$ design pressure
    :param gamma_inc: $\gamma_{inc}$ incidental to design pressure ratio
    :param alpha_spt: $\alpha_{spt}$ system pressure test factor
    :returns: p_t: $p_t$ system test pressure

    Reference:
    DNVGL-ST-F101 (2017-12) 
        eq:4.3 sec:4.2.2.2 page:67 p_{inc}
        table:5.8 sec:5.4.2.1 page:94 $alpha_{spt}$
        sec:5.2.2.1 page:84

    Example:    
    >>> incid_ref_press(100e5, 1.1)
    11000000.0
    """
    return p_d * gamma_inc * alpha_spt


def local_incid_press(p_d, rho_cont,
        h_l, h_ref, gamma_inc=1.1, 
        g=9.81) -> "p_li":
    r'''Calculate local incidental pressure. Also applicable for 
    local system test pressure.

    :param p_d: $p_d$ design pressure at ref elevation
    :param rho_cont: $\rho_{cont}$ density of pipeline contents
    :param h_l: $h_l$ elevation of the local pressure point
    :param h_ref: $h_{ref}$ elevation of the reference point
    :param gamma_inc: $\gamma_{inc}$ incidental to design pressure ratio
    :param g: $g$ gravitational acceleration
    :returns: p_li: $h_{ref}$ local incidental pressure
    
    .. math::
        p_{li} = p_{inc} - \rho_{cont} \cdot g \cdot \left( h_l - h_{ref} \right)

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:4.2.2.2 eq:4.1 page:67 p_{li}
        sec:4.2.2.2 eq:4.2 page:67 $p_{lt}$ 

    Example:    
    #>>> local_incid_press(100.e-5, 1025, -125, 30)
    1558563.751
    '''
    p_inc = p_d * gamma_inc
    p_li = p_inc - rho_cont * g * (h_l - h_ref)
    return p_li


def local_test_press(p_t, rho_t, h_l, h_ref, p_e=None, alpha_spt=None,
                        g=9.81) -> "p_lt":
    """Calculate local test pressure.
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:4.2.2.2 eq:4.2 page:67 $p_{lt}$
        sec:5.4.2.1 eq:5.6 page:93 $p_{li}$
    """
    p_lt = local_incid_press(p_t, rho_t, h_l, h_ref, g)
    if alpha_spt:
        p_lt = p_lt / alpha_spt
    if p_e:
        p_lt = p_lt - p_e
    return p_lt

def local_test_press_unity(p_li, p_e, p_lt) -> "p_lt_uty":
    p_lt_uty = p_lt / (p_li - p_e)
    return p_lt_uty


def external_pressure(h_l, rho_water, g=9.81) -> "p_e":
    """Water pressure, external to pipe.
    """
    return h_l * rho_water * g


#def press_contain_resis(D, t, f_y, f_u=None, gamma_m=None, gamma_SCPC=None):
def press_contain_resis(D, t, f_y, f_u=None,
                        gamma_m=None, gamma_SCPC=None) -> "p_b":
    """Pressure containment resistance in accordance with DNVGL-ST-F101.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.2 eq:5.8 page:94 $p_{b}(t)$

    """
    if f_u:
        f_cb = min(f_y, f_u/1.15)
    else:
        f_cb = f_y
    p_b = 2*t/(D-t) * f_cb * 2/math.sqrt(3)
    if (gamma_m and gamma_SCPC):
        p_b = p_b / gamma_m / gamma_SCPC
    return p_b

def press_contain_resis_unity(p_li, p_e, p_b) -> "p_cont_res_uty":
    p_cont_res_uty = p_b / (p_li - p_e)
    return p_cont_res_uty


def mill_test_press(D, t_min, SMYS, SMTS, 
                    alpha_U=None, alpha_mpt=None) -> "p_mpt":
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:7.5.1.2 eq:7.3 page:175 $p_{mpt}$
    """
    k=1.15  # assuming end-cap effect applies
    p_mpt = k * (2*t_min)/(D-t_min) * min(SMYS*0.96, SMTS*0.84)
    if alpha_U and alpha_mpt:
        p_mpt = p_mpt * alpha_U / alpha_mpt
    return p_mpt


def mill_test_press_unity(p_li, p_e, p_mpt) -> "p_mpt_uty":
    p_mpt_uty = p_mpt / (p_li - p_e)
    return p_mpt_uty


def press_contain_unity(p_cont_res_uty, p_lt_uty,
                        p_mpt_uty) -> "p_cont_uty":
    try:
        p_cont_uty = min(p_cont_res_uty, p_lt_uty, p_mpt_uty)
    except ValueError: # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        p_cont_uty = np.minimum(p_cont_res_uty, p_lt_uty, p_mpt_uty)
    return p_cont_uty


def press_contain_all(p_d,  
        D, t, t_corr, t_fab,
        h_l, h_ref, rho_cont, rho_water,
        SMYS, SMTS, T, material, f_ytemp=None, p_t=None, rho_t=None,
        gamma_m=None, limit_state="ULS",
        gamma_SCPC=None, alpha_spt=None, alpha_mpt=None, SC="medium",
        gamma_inc=1.1, alpha_U=None,  alpha_U_loading="other", 
        g=9.81, ret="unity" ) -> "p_cont_all":
    p_inc = incid_ref_press(p_d, gamma_inc)
    p_li = local_incid_press(p_d, rho_cont, h_l, h_ref, gamma_inc, g)
    p_e = external_pressure(h_l, rho_water, g)
    f_y = char_mat_strength(SMYS, T, material, f_ytemp, alpha_U)
    if gamma_m is None:
        gamma_m = factor.gamma_m_map[limit_state]
    if gamma_SCPC is None:
        gamma_SCPC = factor.gamma_SCPC_map[SC]
    if alpha_spt is None:
        alpha_spt = factor.alpha_spt_map[SC]
    t_1 = t - t_corr - t_fab
    t_min = t - t_fab
    p_b = press_contain_resis(D, t_1, f_y, f_u=None,
                        gamma_m=gamma_m, gamma_SCPC=gamma_SCPC)

    if p_t is None:
        p_t = system_test_press(p_d, gamma_inc, alpha_spt)
    if rho_t is None:
        rho_t = rho_water
    p_lt = local_test_press(p_t, rho_t, h_l, h_ref, p_e, alpha_spt, g)

    if alpha_U is None:
        alpha_U = factor.alpha_U_map[alpha_U_loading]
    if alpha_mpt is None:
        alpha_mpt = factor.alpha_mpt_map[SC]
    p_mpt = mill_test_press(D, t_min, SMYS, SMTS, alpha_U, alpha_mpt)

    p_cont_res_uty = press_contain_resis_unity(p_li, p_e, p_b)
    p_lt_uty = local_test_press_unity(p_li, p_e, p_lt)
    p_mpt_uty = mill_test_press_unity(p_li, p_e, p_mpt)
    p_cont_uty = press_contain_unity(p_cont_res_uty, p_lt_uty,
                        p_mpt_uty)
    if ret.lower()=="all":
        return {
            "p_inc": p_inc,
            "p_li": p_li,
            "p_e": p_e,
            "f_y": f_y,
            "gamma_m": gamma_m,
            "gamma_SCPC": gamma_SCPC,
            "alpha_spt": alpha_spt,
            "t_1": t_1,
            "t_min": t_min,
            "p_b": p_b,
            "p_t": p_t,
            "rho_t": rho_t,
            "p_lt": p_lt,
            "alpha_U": alpha_U,
            "alpha_mpt": alpha_mpt,
            "p_mpt": p_mpt,
            "p_cont_res_uty": p_cont_res_uty,
            "p_lt_uty": p_lt_uty,
            "p_mpt_uty": p_mpt_uty,
            "p_cont_uty": p_cont_uty,
        }
    elif ret.lower()=="unity":
        return p_cont_uty
    else:
        return p_cont_uty <= 1.0




if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    parameters = {
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
    p_cont_overall = press_contain_overall(ret="all", **parameters)
    print("press_contain_overall=", p_cont_overall)
