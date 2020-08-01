"""
Basic linepipe properties.

References:
1. https://en.wikipedia.org/wiki/Second_moment_of_area
1. https://en.wikipedia.org/wiki/Section_modulus
"""
import logging

import numpy as np


logger = logging.getLogger(__name__)


def lpipe_layers_equiv(layers, *, Di_ref=None, Do_ref=None):
    """calculate equivalent properties for stacked ring layers.

    :param layers: list of layer properties, each element is
    a tuple consisting of (layer_thickness, layer_mass_density)
    :type layers: list, tuple
    :returns: tuple with equivalent properties (thickness, density, mass/length)
    :rtype: tuple

    .. doctest::

        >>> ring_layers_equiv([(0.0185,7850),(0.003,7000)], Do_ref=0.3229)
        (0.0215, 7738.675329084429, 157.54267202070224)
    """
    if (Di_ref is not None) and (Do_ref is not None):
        raise ValueError(f"arguments not correctly specified: Di_ref={Di_ref}, Do_ref={Do_ref}")
    _dref = Di_ref if Di_ref else Do_ref
    _equiv_mass = 0
    _total_wt = 0
    for layer in layers:
        wt, rho, *_ = layer
        _total_wt += wt
        if Di_ref:
            _Do, _Di, _WT = lpipe_D_WT(Do=None, Di=_dref, t=wt)
            _dref = _Do
        else:
            _Do, _Di, _WT = lpipe_D_WT(Do=_dref, Di=None, t=wt)
            _dref = _Di
        #_csa = np.pi/4 * (_Do**2 - _Di**2)
        _csa = np.pi/4 * (np.power(_Do,2) - np.power(_Di,2))
        _mass = _csa * rho
        _equiv_mass += _mass
    if Di_ref:
        #_csa = np.pi/4 * (_dref**2 - Di_ref**2)
        _csa = np.pi/4 * (np.power(_dref,2) - np.power(Di_ref,2))
    else:
        #_csa = np.pi/4 * (Do_ref**2 - _dref**2)
        _csa = np.pi/4 * (np.power(Do_ref,2) - np.power(_dref,2))
    _equiv_rho = _equiv_mass / _csa
    return (_total_wt, _equiv_rho, _equiv_mass)





def lpipe_D_WT(*, Do=None, Di=None, WT=None, _round=False) -> "('Do', 'Di', 'WT')":
    """Resolve pipe radial dimensions. Given two of three dimensional arguments 
    outer diameter Do; inner diameter Di; wall thickness WT;
    calculate the missing dimension and return a tuple (Do, Di, WT).

    If all arguments are specified a consistency check is carried
    out, and an AssertionError is raised if the dimensions are inconsistent.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :param WT: pipe wall thickness :math:`(WT)`
    :type WT: float
    :returns: outer diameter, inner diameter, wall thickness
    :rtype: tuple

    .. doctest::

        >>> lpipe_D_WT(Do=0.660, WT=0.05)
        (0.66, 0.56, 0.05)
    """
    if _round and isinstance(_round, (int, bool)):
        Do = round(Do, _round)
        Di = round(Di, _round) 
        WT = round(WT, _round) 
    if all([isinstance(x, (float, int)) for x in [Do, Di, WT]]):
        try:
            assert Di==Do-2*WT, f"inconsistent pipe dimensions Do={Do} Di={Di}, WT={WT}."
            #return True
        except AssertionError as err:
            logger.error("lpipe_D_WT:  %s" % (err,))
            return False
    elif Do is None and all([isinstance(x, (float, int)) for x in [Di, WT]]):
        Do = Di + 2*WT
    elif Di is None and all([isinstance(x, (float, int)) for x in [Do, WT]]):
        Di = Do - 2*WT
    elif WT is None and all([isinstance(x, (float, int)) for x in [Do, Di]]):
        WT = (Do - Di)/2
    else:
        logger.error("lpipe_D_WT: arguments incorrectly specified: Do=%s, Di=%s, WT=%s" % (Do,Di,WT))
    return Do, Di, WT





def lpipe_CSA(*, Do=None, Di=None, WT=None, layers=None):
    """Calculate the area of a circular ring,
    by specifying at least
    two of the three dimensional arguments outer diameter Do, 
    inner diameter Di, thickness t.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :param WT: pipe wall thickness :math:`(WT)`
    :type WT: float
    :returns: pipe cross sectional area
    :rtype: float

    .. math::
        A =  \frac{\pi}{4} \left( D_o^2 - D_i^2   \right)  

    .. doctest::

        >>> lpipe_CSA(Do=0.660, WT=0.05)
        0.09581857593448868
    """
    _Do, _Di, _WT = lpipe_D_WT(Do=Do, Di=Di, WT=WT)
    _csa = np.pi/4 * (_Do**2 - _Di**2)
    #_csa = np.pi/4 * (np.power(_Do,2) - np.power(_Di,2))
    return _csa


def lpipe_Ix(*, Do=None, Di=None, t=None):
    """Calculate circular ring second moment of area
    (AKA moment of inertia), given
    two of the three dimensional arguments outer diameter Do, 
    inner diameter Di, wall thickness WT.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :param t: pipe wall thickness :math:`(t)`
    :type WT: float
    :returns: monent of inertia (second moment of area)
    :rtype: float

    .. math::
        I_x = I_y = \frac{\pi}{64} \left( D_o^4 - D_i^4   \right) 

    .. doctest::

        >>> lpipe_Ix(Do=0.660, WT=0.05)
        0.09581857593448868
    """
    _Do, _Di, _WT = lpipe_Ix(Do=Do, Di=Di, WT=WT)
    _moi = np.pi/64 * (_Do**4 - _Di**4)
    return _moi


def all_pipe_properties(*, Do=None, Di=None, WT=None):
    """All pipe properties
    """
    CSA = lpipe_CSA(Do=Do, Di=Di, WT=None)
    coat_WT, coat_ρ, coat_mass = lpipe_layers_equiv(layers, 
        Di_ref=Do)

    return {
        "CSA": CSA,
        "coat_WT": coat_WT,
        "coat_ρ": coat_ρ,
        "coat_mass": coat_mass,
    }



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)


