"""

"""

import logging

import numpy as np

from .material import char_strength, char_WT
from ..pipe import calc_pipe_Do_Di_WT as pipe_Do_Di_WT


tex_map = {
    "p_incid_ref": "p_{inc} = p_d \cdot \gamma_{inc}",
    "p_system_test_ref": "p_t = p_d \cdot \gamma_{inc} \cdot \alpha_{spt}",
    "p_incid_loc": "p_{li} = p_{inc} - \rho_{cont} \cdot g \cdot \left( h_l - h_{ref} \right)",
    #"p_test_loc": "p_{inc} = p_d \cdot \gamma_{inc}",
    "p_ext": "\rho_{seawater}  \cdot h_l  \cdot g",
    "p_mill_test": "p_{mpt} = k \cdot \frac{2 \cdot t_{min}}{D - t_{min}} \cdot \min \left[SMYS \cdot 0.96,  SMTS \cdot 0.84\right]", 
    "p_cont_resist": "p_{b}(t) = \frac{2 \cdot t}{D - t} \cdot f_{cb} \cdot \frac{2}{\sqrt{3}}",
}

return_map = {
    "p_incid_ref": "p_inc",
    "p_system_test_ref": "p_t",
    "p_incid_loc": "p_li",
    "p_test_loc": "p_lt",
    "p_ext": "p_e",
    "p_mill_test": "p_mpt",
    "p_cont_resist": "p_b",
}



def p_incid_ref(p_d, γ_inc):
    r"""Calculate DNVGL-ST-F101 «incidental reference pressure». 

    p_inc : the incidental reference pressure at the reference elevation

    :param p_d: design pressure :math:`(p_d)`
    :type p_d: float
    :param γ_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type γ_inc: float
    :returns: p_inc incidental reference pressure :math:`(p_{inc})`
    :rtype: float

    Reference:
    DNVGL-ST-F101 (2017-12) 
        eq:4.3 sec:4.2.2.2 page:67 :math:`(p_{inc})`

    .. doctest:: 

        >>> p_incid_ref(100e5, 1.1)
        11000000.0
    """
    p_inc = p_d * γ_inc
    return p_inc

p_incid_ref.tex = "p_{inc} = p_d \cdot \gamma_{inc}"
p_incid_ref.rsig = "p_inc"


def p_system_test_ref(p_d,  γ_inc, α_spt):
    r"""Calculate DNVGL-ST-F101 «system test pressure». 

    p_t : the system test reference pressure at the reference elevation

    :param p_d: design pressure :math:`(p_d)`
    :type p_d: float
    :param γ_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type γ_inc: float
    :param α_spt: system pressure test factor :math:`(\alpha_{spt})`
    :type α_spt: float
    :returns: p_t system test pressure :math:`(p_t)`
    :rtype: float

    Reference:
    DNVGL-ST-F101 (2017-12)  
        | eq:4.3 sec:4.2.2.2 p:67 :math:`p_{inc}`  
        | table:5.8 sec:5.4.2.1 p:94 :math:`\alpha_{spt}`  
        | sec:5.2.2.1 p:84  

    .. doctest::    
    
        >>> p_system_test_ref(100e5, 1.1, 1.05)
        11550000.0
    """
    p_t = p_d * γ_inc * α_spt
    return p_t


def p_incid_loc(p_d, ρ_cont, h_l, h_ref, γ_inc, g=9.80665):
    '''Calculate local incidental pressure. 

    :param p_d: design pressure at ref elevation :math:`(p_d)`
    :type p_d: float
    :param ρ_cont: density of pipeline contents :math:`(\rho_{cont})`
    :type ρ_cont: float
    :param h_l: elevation of the local pressure point :math:`(h_l)`
    :type h_l: float
    :param h_ref: elevation of the reference point :math:`(h_{ref})`
    :type h_ref: float
    :param γ_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type γ_inc: float
    :param g: gravitational acceleration :math:`(g)`
    :type g: float
    :returns: p_li local incidental pressure :math:`(p_{li})`
    :rtype: float

    Notes:
        γ_inc=1.0 for local system test pressure :math:`(p_{lt})`.

    .. math::
        p_{li} = p_{inc} - \rho_{cont} \cdot g \cdot \left( h_l - h_{ref} \right)

    Reference:
    DNVGL-ST-F101 (2017-12) 
        | sec:4.2.2.2 eq:4.1 p:67 :math:`(p_{li})`
        | sec:4.2.2.2 eq:4.3 p:67 :math:`(p_{inc})` 

    .. doctest::

        >>> p_incid_loc(100.e-5, 810., -125.0, 30.0, 1.1)
        1231224.9086
    '''
    p_inc = p_d * γ_inc
    p_li = p_inc - ρ_cont * g * (h_l - h_ref)
    return p_li


def p_test_loc(p_t, ρ_t, h_l, h_ref, g=9.80665):
    """Calculate local test pressure.  
    
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:4.2.2.2 eq:4.2 p:67 $p_{lt}$

    """
    _γ_inc = 1.0
    p_lt = p_incid_loc(p_t, ρ_t, h_l, h_ref, _γ_inc, g)
    return p_lt


def p_test_loc_uty(α_spt, p_lt, p_li, p_e):
    """Local test pressure unity check.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 

    (local_test_press_unity)
    """
    p_lt_uty = (p_li - p_e) * α_spt / p_lt
    return p_lt_uty


def p_ext(h_l, ρ_seawater, g=9.80665):
    """Water pressure, external to pipe.
    """
    p_e = np.abs(h_l) * ρ_seawater * g
    return p_e


def p_mill_test(D, t_min, SMYS, SMTS, α_U=None, α_mpt=None, k=1.15):
    """Mill test pressure

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:7.5.1.2 eq:7.3 p:175 $p_{mpt}$
    (mill_test_press)
    see also p93.
    """
    #k=1.15  # assuming end-cap effect applies
    # if t_min is None:
    #     t_min = char_wall_thickness(t, t_fab, t_corr=0.0)
    p_mpt = k * (2*t_min)/(D-t_min) * np.minimum(SMYS*0.96, SMTS*0.84)
    if α_U and α_mpt:
        p_mpt = p_mpt * α_U / α_mpt
    return p_mpt


def p_mill_test_uty(p_li, p_e, p_mpt):
    """Mill test pressure unity


    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 
    (mill_test_press_unity)
    """
    p_mpt_uty = (p_li - p_e) / p_mpt
    return p_mpt_uty


def p_contain_resist(D, t, f_y, f_u=None):
    """Pressure containment resistance in accordance with DNVGL-ST-F101.

    (press_contain_resis)

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.2 eq:5.8 p:94 $p_{b}(t)$

    """
    if f_u is None:
        f_cb = f_y
    else:
        f_cb = np.minimum(f_y, f_u/1.15)
    p_b = (2*t/(D-t) * f_cb * 2/np.sqrt(3))
    return p_b


def p_contain_resist_uty(p_li, p_e,  p_b, γ_m, γ_SCPC):
    """Pressure containment resistance unity check.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 

    (press_contain_resis_unity)
    """
    p_cont_res_uty =  (p_li - p_e) * γ_m * γ_SCPC / p_b
    return p_cont_res_uty


def p_contain_uty(p_cont_res_uty, p_lt_uty, p_mpt_uty):
    """Pressure containment (bursting) unity check.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 

    (press_contain_unity)
    """
    _max1 = np.maximum(p_cont_res_uty, p_lt_uty)
    p_cont_uty = np.maximum(_max1, p_mpt_uty)
    return p_cont_uty


def pressure_containment_all(p_d,  
        D_o, t_nom, t_corr, t_fab,
        h_l, h_ref, ρ_cont, ρ_seawater, ρ_t,
        γ_inc, γ_m, γ_SCPC, α_U, α_spt, α_mpt, 
        t_1=None, t_2=None, p_t=None, 
        SMYS=None, SMTS=None, f_y=None, f_u=None, T=None, material=None,  
        f_ytemp=None, f_utemp=None, g=9.80665):
    #Do, _, _ = pipe_Do_Di_WT(Di=D_i, WT=t)
    f_y = char_strength(SMYS, α_U, f_ytemp=f_ytemp)
    f_u = char_strength(SMTS, α_U, f_ytemp=f_utemp)

    p_inc = p_incid_ref(p_d, γ_inc)
    p_li = p_incid_loc(p_d, ρ_cont, h_l, h_ref, γ_inc)  
    p_t = p_system_test_ref(p_d,  γ_inc, α_spt)
    p_e = p_ext(h_l, ρ_seawater)

    p_t = p_system_test_ref(p_d, γ_inc, α_spt)
    p_lt = p_test_loc(p_t, ρ_t, h_l, h_ref)

    t_min_mill_test = char_WT(t_nom, t_fab, t_corr=0.0)
    p_mpt = p_mill_test(D_o, t_min_mill_test, SMYS, SMTS, α_U, α_mpt, k=1.15)

    t_1 = char_WT(t_nom, t_fab, t_corr)
    p_b = p_contain_resist(D_o, t_1, f_y, f_u)

    p_cont_res_uty = p_contain_resist_uty(p_li, p_e,  p_b, γ_m, γ_SCPC)
    p_lt_uty = p_test_loc_uty(α_spt, p_lt, p_li, p_e)
    p_mpt_uty = p_mill_test_uty(p_li, p_e, p_mpt)
    p_cont_uty = p_contain_uty(p_cont_res_uty, p_lt_uty, p_mpt_uty)

    return {
        "p_inc": p_inc,
        "p_li": p_li,
        "p_e": p_e,
        "f_y": f_y,
#        "γ_m": γ_m,
#        "γ_SCPC": gamma_SCPC,
#        "alpha_spt": alpha_spt,
        "t_1": t_1,
#        "t_min": t_min,
        "p_b": p_b,
        "p_t": p_t,
#        "rho_t": rho_t,
        "p_lt": p_lt,
#        "alpha_U": alpha_U,
#        "alpha_mpt": alpha_mpt,
        "p_mpt": p_mpt,
#        "p_cont_res_uty": p_cont_res_uty,
        "p_lt_uty": p_lt_uty,
        "p_mpt_uty": p_mpt_uty,
        "p_cont_res_uty": p_cont_res_uty,
        "p_cont_uty": p_cont_uty,
    }



# long-name function aliases
incidental_reference_pressure = p_incid_ref
system_test_pressure = p_system_test_ref
local_incidental_pressure = p_incid_loc
local_test_pressure = p_test_loc
local_test_pressure_unity = p_test_loc_uty
mill_test_pressure = p_mill_test
mill_test_pressure_unity = p_mill_test_uty
pressure_containment_resistance = p_contain_resist
pressure_containment_resistance_unity = p_contain_resist_uty
pressure_containment_unity = p_contain_uty



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    # parameters = {
    #     "alpha_U": 1.0,
    #     "D": 0.660,
    #     "g": 9.81,
    #     "gamma_inc": 1.1,
    #     "gamma_SCPC": 1.138,
    #     "h_ref": 30.,
    #     "h_l": 0.,
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
    # #parameters["h_l"] = np.array([-340., -300, 0])
    # p_cont_overall = pressure_containment_all(**parameters)
    # print("pressure_containment_all=", p_cont_overall)
