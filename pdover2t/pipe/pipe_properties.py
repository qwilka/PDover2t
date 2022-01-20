import logging
import math

import numpy as np


def dodi2wt(Do, Di):
    """Calculate pipe wall thickness from outer diameter and inner diameter.
    """
    return (Do - Di) / 2


def dowt2di(Do, WT):
    """Calculate pipe inner diameter from outer diameter and wall thickness.
    """
    return Do - 2 * WT


def diwt2do(Di, WT):
    """Calculate pipe outer diameter from inner diameter and wall thickness.
    """
    return Di + 2 * WT


def dodiwt(*, Do=None, Di=None, WT=None):
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



def dodi2CSA(Do, Di):
    """Calculate pipe cross sectional area, given the pipe outer diamater and inner diameter.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :returns: pipe cross sectional area
    :rtype: float

    .. math::
        A =  \frac{\pi}{4} \left( D_o^2 - D_i^2   \right)  

    .. doctest::

        >>> dodi2CSA(0.6656, 0.6172)
        0.19522098526377624
    """
    CSA = math.pi / 4 * (Do*Do - Di*Di)
    return CSA


def dodi2I(Do, Di):
    """Calculate pipe second moment of area (I), given the pipe outer diamater and inner diameter.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :returns: ipe second moment of area :math:`(I)`
    :rtype: float

    .. math::
        A =  \frac{\pi}{4} \left( D_o^2 - D_i^2   \right)  

    .. doctest::

        >>> dodi2CSA(0.6656, 0.6172)
        0.19522098526377624
    """
    CSA = math.pi / 64 * (Do**4 - Di**4)
    return CSA


def pipe_unit_mass(ρ, CSA):
    """Calculate pipe unit mass (mass/length).
    """
    # if CSA is None:
    #     CSA = dodi2CSA(Do=Do, Di=Di, WT=WT)
    return CSA * ρ



def pipe_unit_wgt(umass, g=9.806650):
    """Calculate pipe unit weight (weight/length).
    """
    # if umass is None:
    #     umass = calc_pipe_umass(pipe_ρ, Do=Do, Di=Di, WT=WT)
    return umass * g


def pipe_unit_subwgt(Dbuoy, seawater_ρ, uwgt, g=9.806650):
    """Calculate pipe unit submerged weight (weight/length).
    """
    # if uwgt is None:
    #     uwgt = calc_pipe_uwgt(g, Do=Do, Di=Di, WT=WT, umass=umass, pipe_ρ=pipe_ρ)
    usubwgt = uwgt - np.pi/4*Dbuoy**2 * seawater_ρ * g
    return usubwgt


def pipe_equiv_layers(layers, *, Di_ref=None, Do_ref=None, umass=0,
        returnDict=False):
    """calculate equivalent properties for stacked pipe layers.

    :param layers: list of layer properties, each element is
    a tuple consisting of (layer_thickness, layer_mass_density)
    The first layer is the layer at Do_ref|Di_ref. Subsequent layers
    are ordered outwards (increasing D) when Di_ref is reference diameter. 
    Layers are ordered inwards when Do_ref is reference diameter (decreasing D).
    :type layers: list, tuple
    :returns: tuple with equivalent properties (density, umass, Do, Di, WT)
    :rtype: tuple

    .. doctest::

        >>> layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
        >>> pipe_layers(layers, Di_ref=0.660, umass=337.0)
        (5232.900238245189, 0.0491)
    """
    #if (Di is not None) and (Do is not None):
    if len([None for x in [Di_ref, Do_ref] if x is None]) != 1:
        raise ValueError(f"pipe_layers: arguments not correctly specified: Di_ref={Di_ref}, Do_ref={Do_ref}")

    #alayers = np.array(layers, dtype=[('WT', 'f4'), ('density', 'f4')])
    alayers = layers
    #print(alayers)
    if Do_ref:
    #     Di_ref = Do_ref - np.sum(alayers["WT"]) * 2
    #     alayers = alayers[::-1]
        Di_ref = sum([x for x,y in layers])
        alayers = layers[::-1]
    WT_total = 0.0
    equiv_umass = umass
    layer_Di = Di_ref 
    for layer in alayers:
        #print(layer)
        layer_Do = layer_Di + 2*layer[0]
        WT_total += layer[0]
        _csa = np.pi/4 * (np.power(layer_Do,2) - np.power(layer_Di,2))
        equiv_umass += _csa * layer[1]
        layer_Di = layer_Do
    if Do_ref is None:
        Do_ref = Di_ref + 2 * WT_total
    _csa = np.pi/4 * (np.power(Do_ref,2) - np.power(Di_ref,2))
    equiv_ρ = equiv_umass / _csa
    #return (equiv_density, equiv_umass, Do_ref, Di_ref, WT_total)
    if returnDict:
        return {
            "equiv_ρ": equiv_ρ,
            "umass": equiv_umass,
            "Do": Do_ref,
            "Di": Di_ref,
            "WT": WT_total
        }
    else:
        return (equiv_ρ, equiv_umass, Do_ref, Di_ref, WT_total)


# def calc_pipeline_usubwgt(Do, WT, pipe_ρ, coating_layers):
#     Do, Di, WT = calc_pipe_Do_Di_WT(Do=Do, WT=WT)
#     CSA = calc_pipe_CSA(Do, Di)
#     umass = calc_pipe_umass(CSA, pipe_ρ)
#     joint_mass = umass * length
#     uwgt = pdover2t.pipe.calc_pipe_uwgt(umass, g)
#     usubwgt = pdover2t.pipe.calc_pipe_usubwgt(Do, seawater_ρ, g, uwgt=uwgt)
#     joint_subwgt = usubwgt * length
#     layersObj = pdover2t.pipe.calc_pipe_layers(coating_layers, Di_ref=Do, umass=umass)
#     pl_umass = layersObj[1]
#     pl_Do = layersObj[2]
#     pl_uwgt = pdover2t.pipe.calc_pipe_uwgt(pl_umass, g)
#     pl_usubwgt = pdover2t.pipe.calc_pipe_usubwgt(pl_Do, seawater_ρ, g, uwgt=pl_uwgt)
#     return pl_usubwgt



def calc_pipe_props(**kwargs):
    retObj = {}
    Do = kwargs.get("Do", None)
    Di = kwargs.get("Di", None)
    WT = kwargs.get("WT", None)
    Do, Di, WT = dodiwt(Do=Do, Di=Di, WT=WT)
    retObj["Do"] = Do
    retObj["Di"] = Di
    retObj["WT"] = WT
    CSA = dodi2CSA(Do, Di)
    retObj["CSA"] = CSA
    I = dodi2I(Do, Di)
    retObj["I"] = I
    return retObj
