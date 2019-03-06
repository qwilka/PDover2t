import logging
import re

import numpy as np

from . import factor

logger = logging.getLogger(__name__)



def mat_strength_derating(T, material=None, curve=None):
    """Material strength de-rating value qith temperature, 
    according to DNVGL-ST-F101.
    
    :param T: de-rating temperature 
    :param material: material to be de-rated; 'CMn' for carbon-manganese steel,
     or '22Cr' for duplex stainless steel; (material strength units: Pa)
    :param curve: de-rating curve, specified as a list of points (tuples)
    :returns: de-rating value

    Reference:
    DNVGL-ST-F101 (2017-12) 
        fig:5.2 sec:5.3.3.4 page:90 f_ytemp, f_utemp

    Examples:
    >>> mat_strength_derating(100, material="22Cr")
    90000000.0
    >>> mat_strength_derating(120, curve=[(40,0), (100,50), (200,100)])
    60.0
    """
    if not curve:
        #if material.replace(" ", "").replace("-", "").upper() in ["CMN", "13CR"]:
        if re.sub("\s|-", "", material).upper() in ["CMN", "13CR"]:
            curve = [(50., 0.), (100., 30.e6), (200., 70.e6) ]
        elif re.sub("\s|-", "", material).upper() in ["22CR", "25CR", "DSS"]:
            curve = [(20., 0.), (50., 40.e6), (100., 90.e6), (150., 120.e6), 
                     (200., 140.e6) ]
        else:
            logger.error("mat_strength_derating: args not specified properly «material»=«%s», «curve»=«%s»" % (material,curve))
            return None 
    xy = np.array( list(zip(*curve)) )
    return np.interp(T, xy[0,:], xy[1,:])


def char_mat_strength(SMYS, material=None, T=None, f_ytemp=None, alpha_U="default"):
    """Characteristic material strength in accordance with DNVGL-ST-F101 .

    :param SMYS: material specified minimum yield stress (or SMTS)
    :param f_ytemp: de-rating values, $f_{y,temp}$ (or $f_{u,temp}$)
    :param alpha_U: material strength factor, $\alpha_U$
    :param T: (if f_ytemp not specified) de-rating temperature 
    :param material: (if f_ytemp not specified) material to be de-rated. mat='C-Mn'
    for carbon-manganese steel, or mat='DSS' for duplex steel.
    :returns: value of characteristic material property $f_y$ (or $f_u$)

    .. math::
        f_y = \left(SMYS - f_{y,temp} \right) \cdot \alpha_U \\
        f_u = \left(SMTS - f_{u,temp} \right) \cdot \alpha_U

    Reference:
    DNVGL-ST-F101 (2017-12) 
        eq:5.4 sec:5.3.3.2 page:89 f_y
        eq:5.5 sec:5.3.3.2 page:89 f_u

    Examples:
    >>> char_mat_strength(450.e6, 35.e6, 1.0)
    415000000.0
    >>> char_mat_strength(450.e6, alpha_U=1.0, temperature=100., material='DSS')
    360000000.0
    """
    if T is None and f_ytemp is None:
        logger.error("char_mat_strength: arguments «T» and «f_ytemp» cannot both be None.")
        raise ValueError('char_mat_strength: arguments not correctly specified.')
    # if alpha_U not in [0.96, 1.00]:
    #     logger.warning("char_mat_strength: non-standard value for arg «alpha_U»=«%s»" % alpha_U)
    _alpha_U = factor.alpha_U_map(alpha_U)
    if f_ytemp is None:
        f_ytemp = mat_strength_derating(T, material=material)
    return (SMYS - f_ytemp) * _alpha_U



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)