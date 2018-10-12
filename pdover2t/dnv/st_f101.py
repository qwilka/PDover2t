import scipy as np
from math import sqrt
import logging
logger = logging.getLogger(__name__)
#from functools import partial

#__all__ = ["pipeCollapse", "P_containment", "derating_strength"]


def char_mat_prop(SMYS, f_ytemp=None, alpha_U=0.96, temp=None, mat='C-Mn'):
    """Characteristic material property in accordance with
    DNV-OS-F101 (2010) Sec.5 C302 

    .. math::
        f_y = \left(SMYS - f_{y,temp} \right) \cdot \alpha_U
    
    :param SMYS: material specified minimum yield stress (or SMTS)
    :param f_ytemp: de-rating values, $f_{y,temp}$ (or $f_{u,temp}$)
    :param alpha_U: material strength factor, $\alpha_U$
    :param temp: (if f_ytemp not specified) de-rating temperature 
    :param mat: (if f_ytemp not specified) material to be de-rated. mat='C-Mn'
    for carbon-manganese steel, or mat='DSS' for duplex steel.
    :returns: value of characteristic material property $f_y$ (or $f_u$)

    See also function derating_strength

    Examples:
    >>> char_mat_prop(450.e6, 35.e6, 1.0)
    415000000.0
    >>> char_mat_prop(450.e6, alpha_U=1.0, temp=100., mat='DSS')
    360000000.0
    """
    if alpha_U not in [0.96, 1.00]:
        logger.warning("non-standard value for alpha_U: %s" % alpha_U)
    if not f_ytemp:
        f_ytemp = derating_strength(temp, mat=mat)
    return (SMYS - f_ytemp) * alpha_U


def derating_strength(temp, mat='C-Mn', curve=None):
    """De-rating value for yield stress, in accordance with
    DNV-OS-F101:2010 Sec.5 C304 Fig. 2 
    
    :param temp: de-rating temperature 
    :param mat: material to be de-rated: mat='C-Mn' for carbon-manganese steel,
     or mat='DSS' for duplex steel; (material strength units: Pa)
    :param curve: de-rating curve, specified as a list of points (tuples)
    :returns: de-rating value
    
    Examples:
    >>> derating_strength(100,"DSS")
    90000000.0
    >>> derating_strength(120, curve=[(40,0), (100,50), (200,100)])
    60.0
    """
    if not curve:
        if mat == 'C-Mn':
            curve = [(50., 0.), (100., 30.e6), (150., 50.e6), (200., 70.e6) ]
        elif mat == 'DSS':
            curve = [(20., 0.), (50., 40.e6), (100., 90.e6), (150., 120.e6), 
                     (200., 140.e6) ]
        else:
            logger.error("de-rating curve not specified properly %s" % curve)
            return None
    #curve = np.array( zip(*curve) )  # python2.7 
    curve = np.array( list(zip(*curve)) )
    return np.interp(temp, curve[0,:], curve[1,:])

"""def calc_f_cb(f_y, f_u=None):
    '''DNV-OS-F101:2010 Sec.5 D203, return f_cb'''
    if not f_u:
        return  f_y
    else:
        return min(f_y, f_u/1.15)"""

"""def _f_cb(f_y, f_u=None):
    if f_u:
        return min(f_y, f_u/1.15)
    else:
        return f_y"""




def P_containment(D, f_y, f_u=None,t=None, p_lx=None, p_e=0,  
                 gamma_m=1.15, gamma_SC=1.138, mode=None):                 
    r'''Pressure containment check in accordance with
    DNV-OS-F101 (2010) Sec.5 D202
    
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
        return p_b*D / (2*f_cb*2/sqrt(3) + p_b)
    else:
        p_b  = 2*t/(D-t) * f_cb * 2/sqrt(3)

    if mode.lower()=='check':
        return p_lx - p_e <= p_b/gamma_m/gamma_SC
    elif mode.lower()=='util':
        return (p_lx - p_e) / (p_b/gamma_m/gamma_SC)
    elif mode.upper()=='P':
        return p_b/gamma_m/gamma_SC + p_e
    elif mode.lower()=='func':
        return p_lx - p_e - p_b/gamma_m/gamma_SC


# Aliases for pressure_containment
#P_contain_check = partial(P_containment, mode='check')
#P_contain_WT = partial(P_containment, mode='WT')


def ovality(D, D_max, D_min):
    return (D_max - D_min) / D


def pipeCollapse(t,D,P_c,SMYS,nu=0.3,E=207.*10**9, f_o=None):
    '''DNV-OS-F101:2010 Sec.5 D401, collapse due to external pressure '''
    P_el = 2*E*(t/D)**3/(1-nu**2)
    P_p = f_y*alpha_fab*(2*t/D)
    if not f_o:
        f_o = (D_max-D_min)/D
        if f_o<0.005: f_o = 0.005
    return (P_c-P_el)*(P_c**2-P_p**2) - P_c*P_el*P_p*f_o*D/t




if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS) # optionflags=(doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    #print P_containment(660.e-3, 4.32e8, 5.136e8, 0.0199, 2.5e7, 2.5e6,1.15, 1.138, 'P')
    depth = 340.
    p_lx = 240.e5*1.1 + 275.*9.81*(30.+depth )*1.1     #*1.1
    p_e = 1027.*9.81* (depth -1.1 )
    t_1 = 24.2e-3 - 1.e-3 - 0.5e-3 
    Do = 660.e-3
    gamma_m = 1.15
    gamma_SC = 1.138   # 1.138   1.308
    f_y = (450.e6 - derating_strength(60, mat='C-Mn'))*1.0      ## 0.96
    f_u = (535.e6 - derating_strength(60, mat='C-Mn'))*1.0
    f_u = None
    print("derating=", derating_strength(60, mat='C-Mn')/1.e6)

    WTmin= P_containment(Do, f_y, f_u,t_1, p_lx, p_e, gamma_m, gamma_SC, 'WT')
    print(WTmin, WTmin/t_1)
