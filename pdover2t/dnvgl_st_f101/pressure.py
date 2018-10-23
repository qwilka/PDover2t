import math





def incid_ref_press(p_d: float, gamma_inc: float) -> float:
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


def system_test_press(p_d: float, gamma_inc: float, alpha_spt: float) -> float:
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


def local_incid_press(p_d: float, rho_cont: float,
        h_l: float, h_ref: float, gamma_inc: float = 1.1, 
        g: float = 9.81) -> float:
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
                        g=9.81):
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


def external_pressure(h_l, rho_water, g=9.81):
    """Water pressure, external to pipe.
    """
    return h_l * rho_water * g


#def press_contain_resis(D, t, f_y, f_u=None, gamma_m=None, gamma_SCPC=None):
def press_contain_resis(D, t, f_y, f_u=None):
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
    # if (gamma_m and gamma_SCPC):
    #     p_b = p_b / gamma_m / gamma_SCPC
    return p_b


def mill_test_press(D, t_min, SMYS, SMTS):
    """
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:7.5.1.2 eq:7.3 page:175 $p_{mpt}$
    """
    k=1.15  # assuming end-cap effect applies
    p_mpt = k * (2*t_min)/(D-t_min) * min(SMYS*0.96, SMTS*0.84)
    return p_mpt


# def press_contain_unity(D, t, f_y, p_li, f_u,   
#                     p_d, h_l, h_ref,
#                  p_e=0, gamma_m=1.15, gamma_SCPC=1.138, 
#                  alpha_spt=None, alpha_mpt=None, alpha_U=None):
def press_contain_unity(p_li, p_e,
                        p_b, gamma_m, gamma_SCPC,
                        p_lt, alpha_spt, 
                        p_mpt, alpha_U, alpha_mpt):
    """Pressure containment unity check in accordance with DNVGL-ST-F101.

    :param D: Pipe diameter       
    :param f_y: Pipe material yield stress
    :param f_u: Pipe material tensile strength
    :param t: Pipe wall thickness     
    :param p_li: local incidental internal pressure
    :param p_e: External pressure
    :param gamma_m: Material resistance factor, :math:`\gamma_m`
    :param gamma_SC: Safety class resistance factor, :math:`\gamma_{SC}`
    :returns: unity check value: (p_li-p_e) / min(...)

    .. math::
        p_{li} - p_e \:\leq\: \min \left( 
        \frac{p_b(t_1)}{\gamma_m \,\cdot\, \gamma_{SC,PC}} ;
        \frac{p_{lt}}{\alpha_{spt}}  - p_e ;
        \frac{p_{mpt} \cdot \alpha_U}{\alpha_{mpt}}  \right) \\ 
        p_{lt} - p_e \:\leq\: \min \left( 
        \frac{p_b(t_1)}{\gamma_m \,\cdot\, \gamma_{SC,PC}} ;
        p_{mpt}  \right)

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 page:93 $p_{li}$
        sec:5.4.2.1 eq:5.7 page:94 p_lt

    Examples:    
    >>> P_containment(660.e-3, 4.32e8, 5.136e8, 0.0199, 2.5e7, 2.5e6,
    ...                1.15, 1.138)
    """
    # _items = [press_contain_resis(D, t, f_y, f_u, gamma_m, gamma_SCPC)]
    # p_t = (p_d, gamma_inc, alpha_spt)
    # _items.append(local_test_press(p_t, rho_t, h_l, h_ref, p_e, alpha_spt, g))
    _term1 = p_b / gamma_m / gamma_SCPC
    _term2 = p_lt/alpha_spt - p_e
    _term3 = p_mpt * alpha_U / alpha_mpt
    unity_check = (p_li - p_e) / min(_term1, _term2, _term3)
    return unity_check


def P_containment(D, f_y, f_u=None,t=None, p_lx=None, p_e=0,  
                 gamma_m=1.15, gamma_SC=1.138, mode=None):                 
    r'''Pressure containment check in accordance with DNVGL-ST-F101.
    
    .. math::
        p_{lx} - p_e \:\leq\: \frac{p_b}{\gamma_m \,\cdot\, \gamma_{SC}}, 
        \quad where \quad p_b = \frac{2 \cdot t}{D - t} \cdot 
        f_{cb} \cdot \frac{2}{\sqrt{3}},
        \quad and \quad f_{cb} = Min\left[f_y, \frac{f_u}{1.15}  \right]

    :param D: Pipe diameter       
    :param f_y: Pipe material yield stress
    :param f_u: Pipe material tensile strength
    :param t: Pipe wall thickness     
    :param p_lx: Internal pressure
    :param p_e: External pressure
    :param gamma_m: Material resistance factor, :math:`\gamma_m`
    :param gamma_SC: Safety class resistance factor, :math:`\gamma_{SC}`
    :param mode: 'check' [default], 'WT', 'P', or 'func', (see returns)
    :returns: According to the value for **mode**:  
              mode='check' return True or False (pass or fail resp.); 
              mode='util' return utilisation factor;
              mode='WT' return minimum pipe wall thickness; 
              mode='P' return maximum internal pressure (pl_x); 
              mode='func' return pressure containment function. 

    The default value for **gamma_m** corresponds to limit state 
    categories SLS/ULS/ALS.  The default for **gamma_SC** corresponds
    to safety class *Medium* for the *Pressure Containment* case. If
    **f_u** is not specified, then :math:`f_{cb}=f_y`.
    
    Examples:    
    >>> P_containment(660.e-3, 4.32e8, 5.136e8, 0.0199, 2.5e7, 2.5e6,
    ...                1.15, 1.138, 'check')
    True
    >>> P_containment(660.e-3, 4.32e8, 5.136e8, 0.0199, 2.5e7, 2.5e6,
    ...                1.15, 1.138, 'WT')
    0.018921...
    >>> P_containment(660.e-3, 4.32e8, 5.136e8, 0.0199, 2.5e7, 2.5e6,
    ...                1.15, 1.138, 'P')
    26199995.17...
    '''
    if not mode:
        if p_lx and t:
            mode='check'
        elif p_lx and not t:
            mode='WT'
        elif not p_lx and t:
            mode='P'
        else:
            raise ValueError("arguments not correctly specified")

    if f_u:
        f_cb = min(f_y, f_u/1.15)
    else:
        f_cb = f_y

    if mode.upper()=='WT':
        p_b  = (p_lx - p_e)*gamma_m*gamma_SC
        return p_b*D / (2*f_cb*2/math.sqrt(3) + p_b)
    else:
        p_b  = 2*t/(D-t) * f_cb * 2/math.sqrt(3)

    if mode.lower()=='check':
        return p_lx - p_e <= p_b/gamma_m/gamma_SC
    elif mode.lower()=='util':
        return (p_lx - p_e) / (p_b/gamma_m/gamma_SC)
    elif mode.upper()=='P':
        return p_b/gamma_m/gamma_SC + p_e
    elif mode.lower()=='func':
        return p_lx - p_e - p_b/gamma_m/gamma_SC



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
