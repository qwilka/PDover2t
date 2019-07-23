import math

import numpy as np

from . import factor
from .material import char_mat_strength


# __all__ = [ "pressure_containment_all", 
#             "press_contain_unity" ]





def incid_ref_press(p_d, gamma_inc) -> "p_inc":
    r"""Calculate DNVGL-ST-F101 «incidental reference pressure». 

    :param p_d: design pressure :math:`(p_d)`
    :type p_d: float
    :param gamma_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type gamma_inc: float
    :returns: p_inc incidental reference pressure :math:`(p_{inc})`
    :rtype: float

    Reference:
    DNVGL-ST-F101 (2017-12) 
        eq:4.3 sec:4.2.2.2 page:67 :math:`(p_{inc})`

    .. doctest:: 

        >>> incid_ref_press(100e5, 1.1)
        11000000.0
    """
    return p_d * gamma_inc


def system_test_press(p_d, gamma_inc, alpha_spt) -> "p_t":
    r"""Calculate DNVGL-ST-F101 «system test pressure». 

    (system_test_press)

    :param p_d: design pressure :math:`(p_d)`
    :type p_d: float
    :param gamma_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type gamma_inc: float
    :param alpha_spt: system pressure test factor :math:`(\alpha_{spt})`
    :type alpha_spt: float
    :returns: p_t system test pressure :math:`(p_t)`
    :rtype: float

    Reference:
    DNVGL-ST-F101 (2017-12)  
        | eq:4.3 sec:4.2.2.2 page:67 :math:`p_{inc}`  
        | table:5.8 sec:5.4.2.1 page:94 :math:`\alpha_{spt}`  
        | sec:5.2.2.1 page:84  

    .. doctest::    
    
        >>> incid_ref_press(100e5, 1.1)
        11000000.0
    """
    return p_d * gamma_inc * alpha_spt


def local_incid_press(p_d, rho_cont,
        h_l, h_ref, gamma_inc=1.1, 
        g=9.81) -> "p_li":
    r'''Calculate local incidental pressure. Also applicable for 
    local system test pressure.

    :param p_d: design pressure at ref elevation :math:`(p_d)`
    :type p_d: float
    :param rho_cont: density of pipeline contents :math:`(\rho_{cont})`
    :type rho_cont: float
    :param h_l: elevation of the local pressure point :math:`(h_l)`
    :type h_l: float
    :param h_ref: elevation of the reference point :math:`(h_{ref})`
    :type h_ref: float
    :param gamma_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type gamma_inc: float
    :param g: gravitational acceleration :math:`(g)`
    :type g: float
    :returns: p_li local incidental pressure :math:`(p_{li})`
    :rtype: float
    
    .. math::
        p_{li} = p_{inc} - \rho_{cont} \cdot g \cdot \left( h_l - h_{ref} \right)

    Reference:
    DNVGL-ST-F101 (2017-12) 
        | sec:4.2.2.2 eq:4.1 page:67 :math:`(p_{li})`
        | sec:4.2.2.2 eq:4.2 page:67 :math:`(p_{lt})` 

    .. doctest::

        >>> local_incid_press(100.e-5, 1025, -125, 30)
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
    (local_test_press)
    """
    p_lt = local_incid_press(p_t, rho_t, h_l, h_ref, g)
    if alpha_spt:
        p_lt = p_lt / alpha_spt
    if p_e is not None:
        p_lt = p_lt - p_e
    return p_lt


def local_test_press_unity(p_li, p_e, p_lt) -> "p_lt_uty":
    """Local test pressure unity

    (local_test_press_unity)
    """
    p_lt_uty = (p_li - p_e) / p_lt
    return p_lt_uty


def external_pressure(h_l, rho_water, g=9.81) -> "p_e":
    """Water pressure, external to pipe.
    """
    return abs(h_l) * rho_water * g


def press_contain_resis(D, t, f_y, f_u=None,
                        gamma_m=1.0, gamma_SCPC=1.0) -> "p_b":
    """Pressure containment resistance in accordance with DNVGL-ST-F101.

    (press_contain_resis)

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.2 eq:5.8 page:94 $p_{b}(t)$

    """
    if f_u:
        f_cb = min(f_y, f_u/1.15)
    else:
        f_cb = f_y
    p_b = (2*t/(D-t) * f_cb * 2/math.sqrt(3)) / gamma_m / gamma_SCPC
    # if (gamma_m and gamma_SCPC):
    #     p_b = p_b / gamma_m / gamma_SCPC
    return p_b


def press_contain_resis_unity(p_li, p_e, p_b) -> "p_cont_res_uty":
    """Pressure containment resistance unity

    (press_contain_resis_unity)
    """
    p_cont_res_uty = (p_li - p_e) / p_b
    return p_cont_res_uty


def mill_test_press(D, t_min, SMYS, SMTS, 
                    alpha_U=None, alpha_mpt=None) -> "p_mpt":
    """Mill test pressure

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:7.5.1.2 eq:7.3 page:175 $p_{mpt}$
    (mill_test_press)
    """
    k=1.15  # assuming end-cap effect applies
    p_mpt = k * (2*t_min)/(D-t_min) * min(SMYS*0.96, SMTS*0.84)
    if alpha_U and alpha_mpt:
        p_mpt = p_mpt * alpha_U / alpha_mpt
    return p_mpt


def mill_test_press_unity(p_li, p_e, p_mpt) -> "p_mpt_uty":
    """Mill test pressure unity

    (mill_test_press_unity)
    """
    p_mpt_uty = (p_li - p_e) / p_mpt
    return p_mpt_uty


def press_contain_unity(p_cont_res_uty, p_lt_uty,
                        p_mpt_uty) -> "p_cont_uty":
    """Pressure containment unity

    (press_contain_unity)
    """
    try:
        p_cont_uty = max(p_cont_res_uty, p_lt_uty, p_mpt_uty)
    except ValueError: # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        p_cont_uty = np.maximum(p_cont_res_uty, p_lt_uty, p_mpt_uty)
    return p_cont_uty


def pressure_containment_all(p_d,  
        D, t, t_corr, t_fab,
        h_l, h_ref, rho_cont, rho_water,
        gamma_m, gamma_SCPC, alpha_U, alpha_spt, alpha_mpt, 
        SMYS, SMTS, T, material, f_ytemp=None, p_t=None, rho_t=None,
        gamma_inc=1.1, 
        g=9.81) -> "{}":
    p_inc = incid_ref_press(p_d, gamma_inc)
    p_li = local_incid_press(p_d, rho_cont, h_l, h_ref, gamma_inc, g)
    p_e = external_pressure(h_l, rho_water, g)
    # _alpha_U = factor.alpha_U_map(alpha_U)
    f_y = char_mat_strength(SMYS, material, T, f_ytemp, alpha_U)
    # if gamma_m is None:
    #     gamma_m = factor.gamma_m_map[limit_state]
    # if gamma_SCPC is None:
    #     gamma_SCPC = factor.gamma_SCPC_map[SC]
    # if alpha_spt is None:
    #     alpha_spt = factor.alpha_spt_map[SC]
    t_1 = t - t_corr - t_fab
    t_min = t - t_fab
    p_b = press_contain_resis(D, t_1, f_y, f_u=None,
                        gamma_m=gamma_m, gamma_SCPC=gamma_SCPC)

    if p_t is None:
        p_t = system_test_press(p_d, gamma_inc, alpha_spt)
    if rho_t is None:
        rho_t = rho_water
    p_lt = local_test_press(p_t, rho_t, h_l, h_ref, p_e, alpha_spt, g)

    # if alpha_U is None:
    #     alpha_U = factor.alpha_U_map[alpha_U_loading]
    # if alpha_mpt is None:
    #     alpha_mpt = factor.alpha_mpt_map[SC]
    p_mpt = mill_test_press(D, t_min, SMYS, SMTS, alpha_U, alpha_mpt)

    p_cont_res_uty = press_contain_resis_unity(p_li, p_e, p_b)
    p_lt_uty = local_test_press_unity(p_li, p_e, p_lt)
    p_mpt_uty = mill_test_press_unity(p_li, p_e, p_mpt)
    p_cont_uty = press_contain_unity(p_cont_res_uty, p_lt_uty,
                        p_mpt_uty)

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




if __name__ == "__main__":
    #import doctest
    #doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    parameters = {
        "alpha_U": 1.0,
        "D": 0.660,
        "g": 9.81,
        "gamma_inc": 1.1,
        "gamma_SCPC": 1.138,
        "h_ref": 30.,
        "h_l": 0.,
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
    #parameters["h_l"] = np.array([-340., -300, 0])
    p_cont_overall = pressure_containment_all(**parameters)
    print("pressure_containment_all=", p_cont_overall)
