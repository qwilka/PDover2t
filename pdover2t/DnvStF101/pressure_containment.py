#import math

import numpy as np

# from . import factor
# from .material import char_mat_strength


# __all__ = [ "pressure_containment_all", 
#             "press_contain_unity" ]

tex_map = {
    "p_incid_ref": "p_{inc} = p_d \cdot \gamma_{inc}",
    "p_system_test_ref": "p_t = p_d \cdot \gamma_{inc} \cdot \alpha_{spt}",
    "p_incid_loc": "p_{li} = p_{inc} - \rho_{cont} \cdot g \cdot \left( h_l - h_{ref} \right)",
    #"p_test_loc": "p_{inc} = p_d \cdot \gamma_{inc}",
}

return_map = {
    "p_incid_ref": "p_inc",
    "p_system_test_ref": "p_t",
    "p_incid_loc": "p_li",
    "p_test_loc": "p_lt",
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


# long-name function aliases
incidental_reference_pressure = p_incid_ref
system_test_pressure = p_system_test_ref
local_incidental_pressure = p_incid_loc
local_test_pressure = p_test_loc
local_test_pressure_unity = p_test_loc_uty


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
