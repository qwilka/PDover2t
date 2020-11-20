import logging

import numpy as np

#from ..utilities.function_tools import func_call_exception_trap
from . import factor
from .material import char_mat_strength


logger = logging.getLogger(__name__)


def incid_ref_press(p_d, γ_inc):
    """Calculate DNVGL-ST-F101 «incidental reference pressure». 

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

        >>> incid_ref_press(100e5, 1.1)
        11000000.0
    """
    p_inc = p_d * γ_inc
    return p_inc


def system_test_press(p_d, γ_inc, α_spt):
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
        | eq:4.3 sec:4.2.2.2 page:67 :math:`p_{inc}`  
        | table:5.8 sec:5.4.2.1 page:94 :math:`\alpha_{spt}`  
        | sec:5.2.2.1 page:84  

    .. doctest::    
    
        >>> incid_ref_press(100e5, 1.1)
        11000000.0
    """
    p_t = p_d * γ_inc * α_spt
    return p_t


def local_incid_press(p_d, ρ_cont, h_l, h_ref, γ_inc=1.1, g=9.80665):
    '''Calculate local incidental pressure. Also applicable for 
    local system test pressure.

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
    p_inc = p_d * γ_inc
    p_li = p_inc - ρ_cont * g * (h_l - h_ref)
    return p_li


def local_test_press(p_t, ρ_t, h_l, h_ref, p_e=None, α_spt=None, g=9.80665):
    """Calculate local test pressure.
    
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:4.2.2.2 eq:4.2 page:67 $p_{lt}$
        sec:5.4.2.1 eq:5.6 page:93 $p_{li}$
    (local_test_press)
    """
    p_lt = local_incid_press(p_t, ρ_t, h_l, h_ref, g)
    if α_spt:
        p_lt = p_lt / α_spt
    if p_e is not None:
        p_lt = p_lt - p_e
    return p_lt


def local_test_press_unity(p_li, p_e, p_lt):
    """Local test pressure unity

    (local_test_press_unity)
    """
    p_lt_uty = (p_li - p_e) / p_lt
    return p_lt_uty


def external_pressure(h_l, ρ_seawater, g=9.80665):
    """Water pressure, external to pipe.
    """
    p_e = np.abs(h_l) * ρ_seawater * g
    return p_e


def press_contain_resis(D, t, f_y, f_u=None, γ_m=1.0, γ_SCPC=1.0):
    """Pressure containment resistance in accordance with DNVGL-ST-F101.

    (press_contain_resis)

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.2 eq:5.8 page:94 $p_{b}(t)$

    """
    if f_u:
        f_cb = np.minimum(f_y, f_u/1.15)
    else:
        f_cb = f_y
    p_b = (2*t/(D-t) * f_cb * 2/np.sqrt(3)) / γ_m / γ_SCPC
    return p_b


def press_contain_resis_unity(p_li, p_e, p_b):
    """Pressure containment resistance unity

    (press_contain_resis_unity)
    """
    p_cont_res_uty = (p_li - p_e) / p_b
    return p_cont_res_uty


def mill_test_press(D, t_min, SMYS, SMTS, 
                    α_U=None, α_mpt=None):
    """Mill test pressure

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:7.5.1.2 eq:7.3 page:175 $p_{mpt}$
    (mill_test_press)
    """
    k=1.15  # assuming end-cap effect applies
    p_mpt = k * (2*t_min)/(D-t_min) * np.minimum(SMYS*0.96, SMTS*0.84)
    if α_U and α_mpt:
        p_mpt = p_mpt * α_U / α_mpt
    return p_mpt


def mill_test_press_unity(p_li, p_e, p_mpt):
    """Mill test pressure unity

    (mill_test_press_unity)
    """
    p_mpt_uty = (p_li - p_e) / p_mpt
    return p_mpt_uty


def press_contain_unity(p_cont_res_uty, p_lt_uty, p_mpt_uty):
    """Pressure containment unity

    (press_contain_unity)
    """
    p_cont_uty = np.maximum(p_cont_res_uty, p_lt_uty, p_mpt_uty)
    return p_cont_uty



if __name__ == "__main__":
    """ To run doctests:
    $ python -m pdover2t.pipe.pipe
    """
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)

