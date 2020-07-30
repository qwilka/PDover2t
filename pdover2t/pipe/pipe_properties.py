

#import inspect
import logging

import numpy as np

# __all__ = [
#     "pipe_basic_dims",
#     "pipe_weight",
# ]

logger = logging.getLogger(__name__)


def pipe_equivalent_layers(layer_props, *, Di_ref=None, Do_ref=None):
    """calculate equivalent properties for stacked pipe layers.

    :param layer_props: list of layer properties, each element is
    a tuple consisting of (layer_thickness, layer_mass_density)
    :type layer_props: list, tuple
    :returns: tuple with equivalent properties (thickness, density, mass/length)
    :rtype: tuple

    .. doctest::

        >>> pipe_equivalent_layers([(0.0185,7850),(0.003,7000)], Do_ref=0.3229)
        (0.0215, 7738.675329084429, 157.54267202070224)
    """
    if (Di_ref is not None) and (Do_ref is not None):
        raise ValueError(f"arguments not correctly specified: Di_ref={Di_ref}, Do_ref={Do_ref}")
    _dref = Di_ref if Di_ref else Do_ref
    _equiv_mass = 0
    _total_wt = 0
    for layer in layer_props:
        wt, rho, *_ = layer
        _total_wt += wt
        if Di_ref:
            _Do, _Di, _WT = pipe_Do_Di_WT(Do=None, Di=_dref, WT=wt)
            _dref = _Do
        else:
            _Do, _Di, _WT = pipe_Do_Di_WT(Do=_dref, Di=None, WT=wt)
            _dref = _Di
        _csa = np.pi/4 * (_Do**2 - _Di**2)
        _mass = _csa * rho
        _equiv_mass += _mass
    if Di_ref:
        _csa = np.pi/4 * (_dref**2 - Di_ref**2)
    else:
        _csa = np.pi/4 * (Do_ref**2 - _dref**2)
    _equiv_rho = _equiv_mass / _csa
    return (_total_wt, _equiv_rho, _equiv_mass)





def resolveDWT(*, Do=None, Di=None, WT=None):
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

        >>> resolveDWT(Do=0.660, WT=0.05)
        (0.66, 0.56, 0.05)
    """
    if all([isinstance(x, (float, int)) for x in [Do, Di, WT]]):
        assert Di==Do-2*WT, f"pipe_Do_Di_WT: inconsistent pipe dimensions Do={Do} Di={Di}, WT={WT}."
    elif Do is None and all([isinstance(x, (float, int)) for x in [Di, WT]]):
        Do = Di + 2*WT
    elif Di is None and all([isinstance(x, (float, int)) for x in [Do, WT]]):
        Di = Do - 2*WT
    elif WT is None and all([isinstance(x, (float, int)) for x in [Do, Di]]):
        WT = (Do - Di)/2
    else:
        logger.error("pipeDWT: arguments incorrectly specified: Do=%s, Di=%s, WT=%s" % (Do,Di,WT))
    return Do, Di, WT





def calcCSA(*, Do=None, Di=None, WT=None):
    """Calculate pipe cross sectional area by specifying at least
    two of the three dimensional arguments outer diameter Do, 
    inner diameter Di, wall thickness WT.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :param WT: pipe wall thickness :math:`(WT)`
    :type WT: float
    :returns: pipe cross sectional area
    :rtype: float

    .. doctest::

        >>> calcCSA(Do=0.660, WT=0.05)
        0.09581857593448868
    """
    _Do, _Di, _WT = resolveDWT(Do=Do, Di=Di, WT=WT)
    csa = np.pi/4 * (_Do**2 - _Di**2)
    return csa


def pipeCSM(density, csa):
    """Calculate pipe cross sectional mass (per unit length),
    by specifying the material density, and the pipe cross
    sectional area (csa). 

    :param density: material density :math:`(\\rho)`
    :type p_d: float
    :param csa: pipe cross sectional area :math:`(pipe_{CSA})`
    :type p_d: float
    :returns: pipe cross section mass per unit length
    :rtype: float

    .. math:: pipe_{cs_mass} = \\rho * pipe_{CSA}

    .. doctest::

        >>> pipeCSM(7850, 0.095818)
        752.1713
    """
    cs_mass = density * csa
    return cs_mass



def Do_from_pipe_Di(Di, WT):
    """Calculate pipe outer diameter (Do), given a reference inner diameter (Di)
    and a wall thickness dimension (WT). WT can be a list or tuple of wall
    thicknesses for compound section pipes.

    .. math::
        D_o = D_i + 2 * WT

    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :param WT: pipe wall thickness, or list/tuple of wall thicknesses
    :type WT: float, list, tuple
    :returns: pipe outer diameter :math:`(D_o)`
    :rtype: float

    .. doctest::

        >>> Do_from_pipe_Di(0.660, 0.045)
        0.75
        >>> Do_from_pipe_Di(203.2, [3, 45, 5])
        309.2
    """
    if isinstance(WT, (list, tuple)):
        _wt_list = WT
    else:
        _wt_list = [WT]
    Do = Di
    for _wt in _wt_list:
        Do = Do + 2 * _wt
    return Do


def Di_from_pipe_Do(Do, WT):
    """Calculate pipe inner diameter (Di), given a reference outer diameter (Do)
    and a wall thickness dimension (WT). WT can be a list or tuple of wall
    thicknesses for compound section pipes.

    .. math::
        D_i = D_o - 2 * WT

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param WT: pipe wall thickness, or list/tuple of wall thicknesses
    :type WT: float, list, tuple
    :returns: pipe inner diameter :math:`(D_i)`
    :rtype: float

    .. doctest:: 

        >>> Di_from_pipe_Do(203.2, 3.0)
        197.2
    """
    if isinstance(WT, (list, tuple)):
        _wt_list = WT
    else:
        _wt_list = [WT]
    Di = Do
    for _wt in _wt_list:
        Di = Di - 2 * _wt
    return Di


# alias
pipe_Do_Di_WT = resolveDWT
pipe_cs_area = calcCSA
pipe_cs_mass = pipeCSM
#pipeCSA = tubeCSA

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)





