import logging

import numpy as np

#from ..utilities.function_tools import func_call_exception_trap
from . import factor
from .material import characteristic_material_strength, characteristic_wall_thickness


logger = logging.getLogger(__name__)


def incidental_reference_pressure(p_d, γ_inc):
    """Calculate DNVGL-ST-F101 «incidental reference pressure». 

    :param p_d: design pressure :math:`(p_d)`
    :type p_d: float
    :param γ_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type γ_inc: float
    :returns: p_inc incidental reference pressure :math:`(p_{inc})`
    :rtype: float

    Reference:
    DNVGL-ST-F101 (2017-12) 
        eq:4.3 sec:4.2.2.2 p:67 :math:`(p_{inc})`

    .. doctest:: 

        >>> incid_ref_press(100e5, 1.1)
        11000000.0
    """
    p_inc = p_d * γ_inc
    return p_inc


def system_test_pressure(p_d, γ_inc, α_spt):
    """Calculate DNVGL-ST-F101 «system test pressure». 

    (system_test_press)

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
    
        >>> incid_ref_press(100e5, 1.1)
        11000000.0
    """
    p_t = p_d * γ_inc * α_spt
    return p_t


def local_incidental_pressure(p_d, ρ_cont, h_l, h_ref, γ_inc, g=9.80665):
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

        >>> local_incid_press(100.e-5, 1025, -125, 30)
        1558563.751
    '''
    p_inc = p_d * γ_inc
    p_li = p_inc - ρ_cont * g * (h_l - h_ref)
    return p_li


def local_test_pressure(p_t, ρ_t, h_l, h_ref, g=9.80665):
    """Calculate local test pressure.  
    
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:4.2.2.2 eq:4.2 p:67 $p_{lt}$

    """
    _γ_inc = 1.0
    p_lt = local_incidental_pressure(p_t, ρ_t, h_l, h_ref, _γ_inc, g)
    return p_lt


def local_test_pressure_unity(α_spt, p_lt=None, p_li=None, p_e=None, **kwargs):
    """Local test pressure unity check.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 

    (local_test_press_unity)
    """
    if p_e is None:
        p_e = external_pressure(h_l, ρ_seawater, g)
    if p_lt is None:
        p_lt = local_test_pressure(p_t, ρ_t, h_l, h_ref, p_e, α_spt, g)
    if p_li is None:
        p_li = local_incidental_pressure(p_d, ρ_cont, h_l, h_ref, γ_inc, g)
    p_lt_uty = (p_li - p_e) * α_spt / p_lt
    return p_lt_uty


def external_pressure(h_l, ρ_seawater, g=9.80665):
    """Water pressure, external to pipe.
    """
    p_e = np.abs(h_l) * ρ_seawater * g
    return p_e


def mill_test_pressure(D, SMYS, SMTS, α_U=None, α_mpt=None, 
        t_min=None, t=None, t_fab=None):
    """Mill test pressure

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:7.5.1.2 eq:7.3 p:175 $p_{mpt}$
    (mill_test_press)
    see also p93.
    """
    k=1.15  # assuming end-cap effect applies
    if t_min is None:
        t_min = characteristic_wall_thickness(t, t_fab, t_corr=0.0)
    p_mpt = k * (2*t_min)/(D-t_min) * np.minimum(SMYS*0.96, SMTS*0.84)
    if α_U and α_mpt:
        p_mpt = p_mpt * α_U / α_mpt
    return p_mpt


def mill_test_pressure_unity(p_li=None, p_e=None, p_mpt=None, **kwargs):
    """Mill test pressure unity


    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 
    (mill_test_press_unity)
    """
    if p_li is None:
        p_li = local_incid_press(p_d, ρ_cont, h_l, h_ref, γ_inc, g)
    if p_e is None:
        p_e = external_pressure(h_l, ρ_seawater, g)
    if p_mpt is None:
        p_mpt = mill_test_pressure(D, t_min, SMYS, SMTS, α_U, α_mpt)
    p_mpt_uty = (p_li - p_e) / p_mpt
    return p_mpt_uty


def pressure_containment_resistance(D, t, f_y, f_u=None):
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


def pressure_containment_resistance_unity(p_e, γ_m, γ_SCPC, p_li=None, p_b=None, **kwargs):
    """Pressure containment resistance unity check.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 

    (press_contain_resis_unity)
    """
    if p_li is None:
        p_li = local_incidental_pressure(p_d, ρ_cont, h_l, h_ref, γ_inc, g)
    if p_b is None:
        p_b = pressure_containment_resistance(D, t_1, f_y, f_u)
    p_cont_res_uty =  (p_li - p_e) * γ_m * γ_SCPC / p_b
    return p_cont_res_uty


#@func_call_exception_trap
def pressure_containment_unity(p_cont_res_uty=None, p_lt_uty=None, p_mpt_uty=None, **kwargs):
    """Pressure containment (bursting) unity check.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 

    (press_contain_unity)
    """
    if p_cont_res_uty is None:
        p_cont_res_uty = pressure_containment_resistance_unity(p_e, γ_m, γ_SCPC, p_li, p_b)
    if p_lt_uty is None:
        p_lt_uty = local_test_pressure_unity(p_li, p_e, p_lt)
    if p_mpt_uty is None:
        p_mpt_uty = mill_test_pressure_unity(p_li, p_e, p_mpt)
    #p_cont_uty = np.maximum(p_cont_res_uty, p_lt_uty, p_mpt_uty)
    # np.maximum only works for 2 arrays/numbers
    _max1 = np.maximum(p_cont_res_uty, p_lt_uty)
    p_cont_uty = np.maximum(_max1, p_mpt_uty)
    return p_cont_uty


def pressure_containment_all(p_d,  
        D, t, t_corr, t_fab,
        h_l, h_ref, ρ_cont, ρ_seawater, ρ_t,
        γ_inc, γ_m, γ_SCPC, α_U, α_spt, α_mpt, 
        t_1=None, t_2=None, p_t=None, 
        SMYS=None, SMTS=None, f_y=None, f_u=None, T=None, material=None,  
        f_ytemp=None, f_utemp=None, g=9.80665):
    p_inc = incidental_reference_pressure(p_d, γ_inc)
    p_li = local_incidental_pressure(p_d, ρ_cont, h_l, h_ref, γ_inc, g)
    p_e = external_pressure(h_l, ρ_seawater, g)

    #f_y = char_mat_strength(SMYS, material, T, f_ytemp, α_U)
    
    if p_t is None:
        p_t = system_test_pressure(p_d, γ_inc, α_spt)
    #t_1preop = characteristic_wall_thickness(t, t_fab, t_corr=0.0)
    p_lt = local_test_pressure(p_t, ρ_t, h_l, h_ref, g)
    p_mpt = mill_test_pressure(D, SMYS, SMTS, α_U, α_mpt, t=t, t_fab=t_fab)

    if f_y is None:
        f_y = characteristic_material_strength(SMYS, α_U, f_ytemp=f_ytemp)
    if f_u is None:
        f_u = characteristic_material_strength(SMTS, α_U, f_ytemp=f_utemp)
    if t_1 is None:
        t_1 = characteristic_wall_thickness(t, t_fab, t_corr)
    p_b = pressure_containment_resistance(D, t_1, f_y, f_u)

    p_cont_res_uty = pressure_containment_resistance_unity(p_e, γ_m, γ_SCPC, p_li, p_b)
    p_lt_uty = local_test_pressure_unity(α_spt, p_lt, p_li, p_e)
    p_mpt_uty = mill_test_pressure_unity(p_li, p_e, p_mpt)
    p_cont_uty = pressure_containment_unity(p_cont_res_uty, p_lt_uty, p_mpt_uty)
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



if __name__ == "__main__":
    """ To run doctests:
    $ python -m pdover2t.dnvgl_st_f101.pressure_containment
    """
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)

