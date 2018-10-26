import math

from .factor import calc_alpha_mpt

testlam = lambda x: "just a test..."

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
    p_cont_uty = min(p_cont_res_uty, p_lt_uty, p_mpt_uty)
    return p_cont_uty


# def press_contain_unity(p_li, p_e,
#                         p_b, gamma_m, gamma_SCPC,
#                         p_lt, alpha_spt, 
#                         p_mpt, alpha_U, alpha_mpt, long_op=False) -> "p_cont_uty":
#     """Pressure containment unity check in accordance with DNVGL-ST-F101.

#     :param D: Pipe diameter       
#     :param f_y: Pipe material yield stress
#     :param f_u: Pipe material tensile strength
#     :param t: Pipe wall thickness     
#     :param p_li: local incidental internal pressure
#     :param p_e: External pressure
#     :param gamma_m: Material resistance factor, :math:`\gamma_m`
#     :param gamma_SC: Safety class resistance factor, :math:`\gamma_{SC}`
#     :returns: unity check value: (p_li-p_e) / min(...)

#     .. math::
#         p_{li} - p_e \:\leq\: \min \left( 
#         \frac{p_b(t_1)}{\gamma_m \,\cdot\, \gamma_{SC,PC}} ;
#         \frac{p_{lt}}{\alpha_{spt}}  - p_e ;
#         \frac{p_{mpt} \cdot \alpha_U}{\alpha_{mpt}}  \right) \\ 
#         p_{lt} - p_e \:\leq\: \min \left( 
#         \frac{p_b(t_1)}{\gamma_m \,\cdot\, \gamma_{SC,PC}} ;
#         p_{mpt}  \right)

#     Reference:
#     DNVGL-ST-F101 (2017-12) 
#         sec:5.4.2.1 eq:5.6 page:93 $p_{li}$
#         sec:5.4.2.1 eq:5.7 page:94 p_lt

#     Examples:    
#     >>> P_containment(660.e-3, 4.32e8, 5.136e8, 0.0199, 2.5e7, 2.5e6,
#     ...                1.15, 1.138)
#     """
#     # _items = [press_contain_resis(D, t, f_y, f_u, gamma_m, gamma_SCPC)]
#     # p_t = (p_d, gamma_inc, alpha_spt)
#     # _items.append(local_test_press(p_t, rho_t, h_l, h_ref, p_e, alpha_spt, g))
#     burst = p_b / gamma_m / gamma_SCPC
#     systest = p_lt/alpha_spt - p_e
#     milltest = p_mpt * alpha_U / alpha_mpt
#     pdiff = p_li - p_e
#     if long_op:
#         unity_check = (pdiff/burst, pdiff/systest, pdiff/milltest)
#     else:
#         unity_check = pdiff / min(burst, systest, milltest)
#     return unity_check






if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
