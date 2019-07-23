import logging

import numpy as np

from . import factor


logger = logging.getLogger(__name__)


# Definitions
# DNVGL-ST-F101 (2017-12) Table 4-1 page 66
definitions = {
    "P_h": np.nan,  # mill test pressure
    "P_t": np.nan,  # system test pressure
    "P_inc": np.nan,  # maximum incidental pressure
    "P_D": np.nan,  # design pressure
    "MAIP": np.nan,  # Maximum allowable incidental pressure
    "MAOP": np.nan,  # Maximum allowable operating pressure
    "p_li": {
        "func": "local_incid_press",
        "module": "pdover2t.dnvgl_st_f101.loads_pressure"
    },
    "p_lt": {
        "func": "local_test_press",
        "module": "pdover2t.dnvgl_st_f101.loads_pressure"
    },
    "p_inc": {
        "func": "incid_ref_press",
        "module": "pdover2t.dnvgl_st_f101.loads_pressure"
    },
}


def local_incid_press(p_inc, rho_cont,
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
    >>> local_incid_press(100.e-5, 1025, -125, 30)
    1558563.751
    '''
    #p_inc = p_d * gamma_inc
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

