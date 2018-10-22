from math import sqrt
import logging
logger = logging.getLogger(__name__)

import scipy as np

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
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
