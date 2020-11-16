"""
Basic linepipe properties.

References:
1. https://en.wikipedia.org/wiki/Second_moment_of_area
1. https://en.wikipedia.org/wiki/Section_modulus
"""
import logging
import math

import numpy as np


logger = logging.getLogger(__name__)

π = math.pi


class Material:

    def __init__(self, name, ρ):
        self.name = name
        self.ρ = ρ



class LinePipe:

    def __init__(self, material, *, Do=None, Di=None, WT=None, length=None):
        self.Do, self.Di, self.WT = lpipe_D_WT(Do=Do, Di=Di, WT=WT) 
        self.CSA = π/4 * (self.Do**2 - self.Di**2)
        self.material = material if isinstance(material, Material) else None
        self.mass = self.CSA * self.material.ρ
        self.length = length
        self.weight = self.mass * self.length if self.length else None


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
    #_dref = Di_ref if Di_ref else Do_ref
    _dref = Di_ref if Do_ref is None else Do_ref
    _equiv_mass = 0
    _total_wt = 0
    for layer in layers:
        wt, rho, *_ = layer
        _total_wt += wt
        #if Di_ref:
        if Do_ref is None:
            #_Do, _Di, _WT = lpipe_D_WT(Do=None, Di=_dref, WT=wt)
            _WT = None
            _Do = _dref + 2*wt
            _Di = _dref
            _dref = _Do
        else:
            _Do, _Di, _WT = lpipe_D_WT(Do=_dref, Di=None, WT=wt)
            _dref = _Di
        #_csa = np.pi/4 * (_Do**2 - _Di**2)
        _csa = np.pi/4 * (np.power(_Do,2) - np.power(_Di,2))
        _mass = _csa * rho
        _equiv_mass += _mass
    #if Di_ref:
    if Do_ref is None:
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


def lpipe_umass(ρ, *, Do=None, Di=None, WT=None, CSA=None):
    """Calculate linepipe mass per unit length.
    """
    if CSA is None:
        CSA = lpipe_CSA(Do=Do, Di=Di, WT=WT)
    umass = CSA * ρ
    return umass


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

def circle_CSA(Do, Di=None):
    # if Di:
    #     CSA = np.pi/4 * (Do**2 - Di**2)
    # else:
    #     CSA = np.pi/4 * Do**2
    if Di is None:
        CSA = np.pi/4 * Do**2
    else:
        CSA = np.pi/4 * (Do**2 - Di**2)
    return CSA


def calc_pipeline_props(lpipe_Do=None, lpipe_Di=None, lpipe_WT=None,
    lpipe_ρ=None, coat_layers=None,
    content_ρ=None,
    seawater_ρ=None,
    g=9.806650, **kwargs):
    """Calculate all pipeline properties from basic data.
    """
    #if [lpipe_Do, lpipe_Di, lpipe_WT].count(None)>1: # Numpy bug ValueError: The truth value of an array with more than one element is ambiguous.
    if len([None for x in [lpipe_Do, lpipe_Di, lpipe_WT] if x is None])>1:
        logger.error("calc_pipeline_props: arguments not specified correcly lpipe_Do=%s, lpipe_Di=%s, lpipe_WT=%s" % (lpipe_Do, lpipe_Di, lpipe_WT))
        return False
    #lpipe_Do, lpipe_Di, lpipe_WT = lpipe_D_WT(Do=lpipe_Do, Di=lpipe_Di, WT=lpipe_WT, _round=False)
    if lpipe_Do is None:
        lpipe_Do = lpipe_Di + 2 * lpipe_WT
    elif lpipe_Di is None:
        lpipe_Di = lpipe_Do - 2 * lpipe_WT
    elif lpipe_WT is None:
        lpipe_WT = (lpipe_Do - lpipe_Di)/2
    # Numpy bug ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    try:
        assert np.array_equal(lpipe_Di, lpipe_Do-2*lpipe_WT), f"inconsistent pipe dimensions lpipe_Do={lpipe_Do} lpipe_Di={lpipe_Di}, lpipe_WT={lpipe_WT}."
        # try:
        #     assert np.array_equal(lpipe_Di, lpipe_Do-2*lpipe_WT), f"inconsistent pipe dimensions lpipe_Do={lpipe_Do} lpipe_Di={lpipe_Di}, lpipe_WT={lpipe_WT}."
        # except TypeError:
        #     assert lpipe_Di==lpipe_Do-2*lpipe_WT, f"inconsistent pipe dimensions lpipe_Do={lpipe_Do} lpipe_Di={lpipe_Di}, lpipe_WT={lpipe_WT}."
    except AssertionError as err:
        logger.error("calc_pipeline_props:  %s" % (err,))
        return False

    #lpipe_CSA = np.pi/4 * (lpipe_Do**2 - lpipe_Di**2)
    lpipe_CSA = circle_CSA(lpipe_Do, lpipe_Di)
    #lpipe_CSA = np.pi/4 * (np.power(lpipe_Do,2) - np.power(lpipe_Di,2))
    lpipe_I = np.pi/64 * (lpipe_Do**4 - lpipe_Di**4)
    # retObj = {
    #     "lpipe_Do": lpipe_Do,
    #     "lpipe_Di": lpipe_Di,
    #     "lpipe_WT": lpipe_WT,
    #     "lpipe_CSA": lpipe_CSA,
    #     "lpipe_I": lpipe_I,
    # }

    pl_Do = lpipe_Do
    lpipe_umass = None
    pl_empty_umass = None
    if lpipe_ρ:
        lpipe_umass = lpipe_CSA * lpipe_ρ
        #retObj["lpipe_umass"] = lpipe_umass
        pl_empty_umass = lpipe_umass

    coat_umass = None
    coat_WT = None
    coat_ρ = None
    if coat_layers:
        coat_WT, coat_ρ, coat_umass = lpipe_layers_equiv(coat_layers, Di_ref=lpipe_Do)
        pl_Do = pl_Do + 2 * coat_WT
        #retObj["coat_WT"] = coat_WT
        #retObj["coat_ρ"] = coat_ρ

    content_umass = None
    if content_ρ:
        content_Do = lpipe_Di
        content_CSA = circle_CSA(content_Do)
        content_umass = content_CSA * content_ρ
        #retObj["content_umass"] = content_umass

    if pl_empty_umass is not None:
        #retObj["pl_empty_umass"] = pl_empty_umass
        if coat_umass is not None:
            pl_empty_umass = pl_empty_umass + coat_umass
            #retObj["pl_empty_umass"] = pl_empty_umass
        if content_umass is not None:
            pl_content_umass = pl_empty_umass + content_umass
            #retObj["pl_content_umass"] = pl_content_umass
        #retObj["pl_uweight"] = total_umass * g

    pl_ubuoyf = None
    pl_empty_usubw = None
    pl_content_usubw = None
    if seawater_ρ:
        pl_CSA = circle_CSA(pl_Do)
        pl_ubuoyf = pl_CSA * seawater_ρ * g
        #retObj["pl_ubuoyf"] = pl_ubuoyf
        if pl_empty_umass is not None:
            pl_empty_usubw =  pl_empty_umass * g - pl_ubuoyf
            #retObj["pl_empty_usubw"] =  pl_empty_usubw
            # if coat_umass is not None:
            #     pl_empty_usubw = pl_empty_usubw + coat_umass * g
            #     retObj["pl_empty_usubw"] =  pl_empty_usubw
            if content_umass is not None:
                pl_content_usubw = pl_empty_usubw + content_umass * g
                #retObj["pl_content_usubw"] =  pl_content_usubw

    #retObj["pl_Do"] = pl_Do

    return {
        "lpipe_Do": lpipe_Do,
        "lpipe_Di": lpipe_Di,
        "lpipe_WT": lpipe_WT,
        "lpipe_CSA": lpipe_CSA,
        "lpipe_I": lpipe_I,     
        "lpipe_umass": lpipe_umass,   
        "coat_WT": coat_WT,
        "coat_ρ": coat_ρ,
        "content_umass": content_umass,
        "pl_Do": pl_Do,
        "pl_empty_umass": pl_empty_umass,
        "pl_content_umass": pl_content_umass,
        "pl_ubuoyf": pl_ubuoyf,
        "pl_empty_usubw": pl_empty_usubw,
        "pl_content_usubw": pl_content_usubw,
    }



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)


