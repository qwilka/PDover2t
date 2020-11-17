import logging

import numpy as np


logger = logging.getLogger(__name__)

π = np.pi


def WT_from_D(Do, Di):
    """Calculate pipe wall thickness from outer diameter and inner diameter.
    """
    return (Do - Di) / 2

def Di_from_WT(Do, WT):
    """Calculate pipe inner diameter from outer diameter and wall thickness.
    """
    return Do - 2 * WT

def Do_from_WT(Di, WT):
    """Calculate pipe outer diameter from inner diameter and wall thickness.
    """
    return Di + 2 * WT


def pipe_Do_Di_WT(*, Do=None, Di=None, WT=None):
    """Calculate pipe wall thickness / outer diameter / inner diameter.
    """
    if Do is not None and Di is not None and WT is not None:
        assert Do==Di+2*WT, f"pipe_D_WT: inconsistent pipe dimensions Do={Do} Di={Di} WT={WT}."
    elif WT is None:
        WT = (Do - Di) / 2
    elif Di is None:
        Di = Do - 2 * WT
    elif Do is None:
        Do = Di + 2 * WT
    else:
        return False
    return Do, Di, WT


def pipe_CSA(Do, Di):
    """Calculate pipe cross sectional area.
    """
    return π / 4 * (Do**2 - Di**2)


def pipe_umass(CSA, pipe_ρ):
    """Calculate pipe unit mass (mass/length).
    """
    return CSA * pipe_ρ

def pipe_uwgt(umass, g=9.806650):
    """Calculate pipe unit weight (weight/length).
    """
    return umass * g

def pipe_usubwgt(uwgt, Dbuoy, seawater_ρ, g=9.806650):
    """Calculate pipe unit submerged weight (weight/length).
    """
    return uwgt - π/4*Dbuoy**2 * seawater_ρ * g


# def pipe_layers(layers, *, Di=None, Do=None, umass=0):
#     """calculate equivalent properties for stacked ring layers.

#     :param layers: list of layer properties, each element is
#     a tuple consisting of (layer_thickness, layer_mass_density)
#     :type layers: list, tuple
#     :returns: tuple with equivalent properties (thickness, density, mass/length)
#     :rtype: tuple

#     .. doctest::

#         >>> pipe_layers([(0.0185,7850),(0.003,7000)], Do=0.3229)
#         (0.0215, 7738.675329084429, 157.54267202070224)
#     """
#     if (Di is not None) and (Do is not None):
#         raise ValueError(f"pipe_layers: arguments not correctly specified: Di={Di}, Do={Do}")
#     #_dref = Di_ref if Di_ref else Do_ref
#     _dref = Di if Do is None else Do
#     _equiv_mass = umass
#     _total_wt = 0
#     for layer in layers:
#         wt, rho, *_ = layer
#         _total_wt += wt
#         #if Di_ref:
#         if Do is None:
#             #_Do, _Di, _WT = lpipe_D_WT(Do=None, Di=_dref, WT=wt)
#             _WT = None
#             _Do = _dref + 2*wt
#             _Di = _dref
#             _dref = _Do
#         else:
#             _Do, _Di, _WT = lpipe_D_WT(Do=_dref, Di=None, WT=wt)
#             _dref = _Di
#         #_csa = np.pi/4 * (_Do**2 - _Di**2)
#         _csa = np.pi/4 * (np.power(_Do,2) - np.power(_Di,2))
#         _mass = _csa * rho
#         _equiv_mass += _mass
#     #if Di_ref:
#     if Do is None:
#         #_csa = np.pi/4 * (_dref**2 - Di_ref**2)
#         _csa = np.pi/4 * (np.power(_dref,2) - np.power(Di,2))
#         Do = Di + 2*_total_wt
#     else:
#         #_csa = np.pi/4 * (Do_ref**2 - _dref**2)
#         _csa = np.pi/4 * (np.power(Do,2) - np.power(_dref,2))
#         Di = Do - 2*_total_wt
#     _equiv_rho = _equiv_mass / _csa
#     return (_equiv_rho, _equiv_mass, Do, Di, _total_wt)


def pipe_layers(layers, *, Di_ref=None, Do_ref=None, umass=0):
    """calculate equivalent properties for stacked ring layers.

    :param layers: list of layer properties, each element is
    a tuple consisting of (layer_thickness, layer_mass_density)
    The first layer is the layer at Do_ref|Di_ref. Subsequent layers
    are ordered outwards (increasing D) when Di_ref is reference diameter. 
    Layers are ordered inwards when Do_ref is reference diameter (decreasing D).
    :type layers: list, tuple
    :returns: tuple with equivalent properties (density, umass, Do, Di, WT)
    :rtype: tuple

    .. doctest::

        >>> pipe_layers([(0.0185,7850),(0.003,7000)], Di_ref=0.3229)
        (0.0215, 7738.675329084429, 157.54267202070224)
    """
    #if (Di is not None) and (Do is not None):
    if len([None for x in [Di_ref, Do_ref] if x is None]) != 1:
        raise ValueError(f"pipe_layers: arguments not correctly specified: Di_ref={Di_ref}, Do_ref={Do_ref}")

    #alayers = np.array(layers, dtype=[('WT', 'f4'), ('density', 'f4')])
    alayers = layers
    print(alayers)
    if Do_ref:
    #     Di_ref = Do_ref - np.sum(alayers["WT"]) * 2
    #     alayers = alayers[::-1]
        Di_ref = sum([x for x,y in layers])
        alayers = layers[::-1]
    WT_total = 0.0
    equiv_umass = umass
    layer_Di = Di_ref 
    for layer in alayers:
        print(layer)
        layer_Do = layer_Di + 2*layer[0]
        WT_total += layer[0]
        _csa = np.pi/4 * (np.power(layer_Do,2) - np.power(layer_Di,2))
        equiv_umass += _csa * layer[1]
        layer_Di = layer_Do
    if Do_ref is None:
        Do_ref = Di_ref + 2 * WT_total
    _csa = np.pi/4 * (np.power(Do_ref,2) - np.power(Di_ref,2))
    equiv_density = equiv_umass / _csa
    return (equiv_density, equiv_umass, Do_ref, Di_ref, WT_total)


if __name__ == "__main__":
    # import doctest
    # doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    if True:
        Do = 0.660
        WT = 0.0214
        coating_layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
    else:
        Do = np.array([0.660, 0.6656])
        WT = np.array([0.0214, 0.0242])
        # coating_layers = [ (np.array([0.0003, 0.0003]), np.array([1450., 1450.])), 
        #     (np.array([0.0038, 0.0038]), np.array([960., 960.]) ), 
        #     (np.array([0.045, 0.045]), np.array([2250., 1900.]) )]
        coating_layers = [ (0.0003, 1450.), (0.0038, 960. ), 
            (0.045, np.array([2250., 1900.]) )]
    length = 12.2
    pipe_ρ = 7850.    
    seawater_ρ = 1027.0
    g = 9.81

    Do, Di, WT = pipe_Do_Di_WT(Do=Do, WT=WT)
    CSA = pipe_CSA(Do, Di)
    umass = pipe_umass(CSA, pipe_ρ)
    joint_mass = umass * length
    uwgt = pipe_uwgt(umass, g)
    usubwgt = pipe_usubwgt(uwgt, Do, seawater_ρ, g)
    joint_subwgt = usubwgt * length

    layersObj = pipe_layers(coating_layers, Di_ref=Do, umass=umass)
    pl_umass = layersObj[1]
    pl_Do = layersObj[2]
    pl_uwgt = pipe_uwgt(pl_umass, g)
    pl_usubwgt = pipe_usubwgt(pl_uwgt, pl_Do, seawater_ρ, g)

