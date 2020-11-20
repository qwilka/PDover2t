import logging

import numpy as np

from ..utilities.function_tools import func_call_exception_trap

logger = logging.getLogger(__name__)

#π = np.pi


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


@func_call_exception_trap
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


@func_call_exception_trap
def pipe_CSA(Do=None, Di=None, WT=None):
    """Calculate pipe cross sectional area.
    """
    if Do is None or Di is None:
        Do, Di, WT = pipe_Do_Di_WT(Do=Do, Di=Di, WT=WT)
    CSA = np.pi / 4 * (Do**2 - Di**2)
    return CSA


@func_call_exception_trap
def pipe_umass(pipe_ρ, *, CSA=None, Do=None, Di=None, WT=None):
    """Calculate pipe unit mass (mass/length).
    """
    if CSA is None:
        CSA = pipe_CSA(Do=Do, Di=Di, WT=WT)
    umass = CSA * pipe_ρ
    return umass


@func_call_exception_trap
def pipe_uwgt(g=9.806650, *, umass=None, Do=None, Di=None, WT=None, pipe_ρ=None):
    """Calculate pipe unit weight (weight/length).
    """
    if umass is None:
        umass = pipe_umass(pipe_ρ, Do=Do, Di=Di, WT=WT)
    uwgt = umass * g
    return uwgt


@func_call_exception_trap
def pipe_usubwgt(Dbuoy, seawater_ρ, g=9.806650, *, uwgt=None, 
        Do=None, Di=None, WT=None, umass=None, pipe_ρ=None):
    """Calculate pipe unit submerged weight (weight/length).
    """
    if uwgt is None:
        uwgt = pipe_uwgt(g, Do=Do, Di=Di, WT=WT, umass=umass, pipe_ρ=pipe_ρ)
    usubwgt = uwgt - np.pi/4*Dbuoy**2 * seawater_ρ * g
    return usubwgt


@func_call_exception_trap
def pipe_layers(layers, *, Di_ref=None, Do_ref=None, umass=0,
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
        return (equiv_ρ, WT_total)


if __name__ == "__main__":
    """ To run doctests:
    $ python -m pdover2t.pipe.pipe
    """
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    # if True:
    #     Do = 0.660
    #     WT = 0.0214
    #     coating_layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
    # else:
    #     Do = np.array([0.660, 0.6656])
    #     WT = np.array([0.0214, 0.0242])
    #     # coating_layers = [ (np.array([0.0003, 0.0003]), np.array([1450., 1450.])), 
    #     #     (np.array([0.0038, 0.0038]), np.array([960., 960.]) ), 
    #     #     (np.array([0.045, 0.045]), np.array([2250., 1900.]) )]
    #     coating_layers = [ (0.0003, 1450.), (0.0038, 960. ), 
    #         (0.045, np.array([2250., 1900.]) )]
    # length = 12.2
    # pipe_ρ = 7850.    
    # seawater_ρ = 1027.0
    # g = 9.81

    # # Do, Di, WT = pipe_Do_Di_WT(Do=Do, WT=WT)
    # # CSA = pipe_CSA(Do, Di)
    # # umass = pipe_umass(CSA, pipe_ρ)
    # # joint_mass = umass * length
    # # uwgt = pipe_uwgt(umass, g)
    # # usubwgt = pipe_usubwgt(Do, seawater_ρ, g, Do=Do, WT=WT)
    # # joint_subwgt = usubwgt * length

    # umass = pipe_umass(pipe_ρ, Do=Do, WT=WT)
    # layersObj = pipe_layers(coating_layers, Di_ref=Do, umass=umass, returnDict=True)
    # pl_umass = layersObj["umass"]
    # pl_Do = layersObj["Do"]
    # #pl_uwgt = pipe_uwgt(pl_umass, g)
    # #pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT, umass=pl_umass)
    # pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT)
