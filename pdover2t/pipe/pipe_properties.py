import logging
import math

import numpy as np

logger = logging.getLogger(__name__)


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



def dodi2CSA(Do, Di=0):
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


def dodi2I(Do, Di=0):
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


def pipe_weight(pipe_ρ, pipe_Do=None, pipe_Di=0.0, CSA=None, g=9.806650, weight=True, length=None):
    """Calculate pipe weight (default) or mass. 


    """
    _g = g if weight else 1.0
    _length = length if length else 1.0
    if CSA is None and pipe_Do is not None:
        CSA = dodi2CSA(pipe_Do, pipe_Di)
    pipe_wgt = CSA * pipe_ρ * _length * _g
    return pipe_wgt


def pipe_content_weight(cont_ρ, pipe_Di=None, CSA=None, g=9.806650, weight=True, length=None):
    """Calculate pipe content weight (default) or mass. 


    """
    _g = g if weight else 1.0
    _length = length if length else 1.0
    if CSA is None and pipe_Di is not None:
        CSA = dodi2CSA(pipe_Di)
    cont_wgt = CSA * cont_ρ * _length * _g
    return cont_wgt


def pipe_coat_weight(pipe_Do, layers, g=9.806650, eqv_props=False, weight=True, length=None):
    """Calculate pipe coating weight (default) or mass.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param layers: list of layer properties, each element is
    a tuple consisting of (layer_thickness, layer_mass_density), in order
    starting with the innermost coating layer. 
    :type layers: list, tuple
    :returns: tuple with equivalent properties (WT_coat, ρ_coat_equiv, umass_coat)
    :rtype: tuple

    .. doctest::

        >>> layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
        >>> pipe_layers(layers, Di_ref=0.660, umass=337.0)
        (5232.900238245189, 0.0491)
    """
    _g = g if weight else 1.0
    _length = length if length else 1.0
    layer_Di = pipe_Do
    coat_wgt = 0.0
    for (layer_WT, layer_ρ) in layers:
        layer_Do = layer_Di + 2.0 * layer_WT
        CSA = dodi2CSA(layer_Do, layer_Di)
        coat_wgt += CSA * layer_ρ * _length * _g
        layer_Di = layer_Do
    if eqv_props:
        coat_WT = (layer_Do - pipe_Do) / 2.0
        CSA = dodi2CSA(layer_Do, pipe_Do)
        coat_ρ_eqv = coat_wgt / (CSA * _length * _g)
        return coat_wgt, coat_WT, coat_ρ_eqv
    else:
        return coat_wgt


def pipe_buoyancy(seawater_ρ, buoy_Do=None, CSA=None, g=9.806650, weight=True, length=None):
    """Calculate pipe buoyancy weight (default) or mass. 


    """
    _g = g if weight else 1.0
    _length = length if length else 1.0
    if CSA is None and buoy_Do is not None:
        CSA = dodi2CSA(buoy_Do)
    buoy = CSA * seawater_ρ * _length * _g
    return buoy


# ---------------------------------------------------




# def pipe_unit_mass(ρ, CSA, cont_ρ=None, length=None):
#     """Calculate pipe mass. Returns pipe mass if length 
#     is specified, otherwise returns pipe unit mass (mass/length). 
#     """
#     _length = length if length else 1.0
#     umass = CSA * ρ * _length
#     if cont_ρ is not None:
#         umass += CSA * cont_ρ * _length
#     return umass



# def pipe_unit_wgt(umass, g=9.806650):
#     """Calculate pipe unit weight (weight/length).
#     """
#     # if umass is None:
#     #     umass = calc_pipe_umass(pipe_ρ, Do=Do, Di=Di, WT=WT)
#     return umass * g


# def pipe_unit_subwgt(Do_buoy, ρ_seawater, umass, g=9.806650):
#     """Calculate pipe unit submerged weight (weight/length).
#     """
#     # if uwgt is None:
#     #     uwgt = calc_pipe_uwgt(g, Do=Do, Di=Di, WT=WT, umass=umass, pipe_ρ=pipe_ρ)
#     usubwgt = (umass - np.pi/4*Do_buoy**2 * ρ_seawater) * g
#     return usubwgt


# def pipe_equiv_coating(Do, coating):
#     Di_layer = Do
#     for (thk, density, *_) in coating:
#         Do_layer = Di_layer + 2 * thk
#         CSA = dodi2CSA(Do_layer, Di_layer)


# def pipe_equiv_coating(Do, layers):
#     """Calculate equivalent properties for pipe coating layers.

#     :param Do: pipe outer diameter :math:`(D_o)`
#     :type p_d: float
#     :param layers: list of layer properties, each element is
#     a tuple consisting of (layer_thickness, layer_mass_density), in order
#     starting with the innermost coating layer. 
#     :type layers: list, tuple
#     :returns: tuple with equivalent properties (WT_coat, ρ_coat_equiv, umass_coat)
#     :rtype: tuple

#     .. doctest::

#         >>> layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
#         >>> pipe_layers(layers, Di_ref=0.660, umass=337.0)
#         (5232.900238245189, 0.0491)
#     """
#     Di_layer = Do
#     umass_coat = 0
#     CSA_coat = 0
#     for (WT_layer, density_layer) in layers:
#         Do_layer = Di_layer + 2 * WT_layer
#         CSA_layer = dodi2CSA(Do_layer, Di_layer)
#         umass_coat += CSA_layer * density_layer
#         CSA_coat += CSA_layer
#         Di_layer = Do_layer
#     WT_coat = (Do_layer - Do) / 2
#     ρ_coat_equiv = umass_coat / CSA_coat
#     return WT_coat, ρ_coat_equiv, umass_coat


# def calc_basic_pipe_properties(Do, WT, ρ_pipe, coat_layers,
#     ρ_seawater, g=9.806650):
#     """
#     """
#     Di = Do - 2 * WT
#     CSA_pipe = dodi2CSA(Do, Di)
#     umass_pipe = pipe_unit_mass(ρ_pipe, CSA_pipe)
#     WT_coat, ρ_coat_equiv, umass_coat = pipe_equiv_coating(Do, coat_layers)
#     umass_pipe_coat = umass_pipe + umass_coat
#     Do_buoy = Do + 2 * WT_coat
#     umass_pl_empty = umass_pipe_coat
#     usubwgt_pl_empty = pipe_unit_subwgt(Do_buoy, ρ_seawater, umass_pl_empty, g)
#     return {
#         "umass_pipe": umass_pipe,
#         "umass_pipe_coat": umass_pipe_coat,
#         "umass_pl_empty": umass_pl_empty,
#         "usubwgt_pl_empty": usubwgt_pl_empty,
#     }




# =====================================================================

# def pipe_equiv_layers(layers, *, Di_ref=None, Do_ref=None, umass=0,
#         returnDict=False):
#     """DEPR calculate equivalent properties for stacked pipe layers.

#     :param layers: list of layer properties, each element is
#     a tuple consisting of (layer_thickness, layer_mass_density)
#     The first layer is the layer at Do_ref|Di_ref. Subsequent layers
#     are ordered outwards (increasing D) when Di_ref is reference diameter. 
#     Layers are ordered inwards when Do_ref is reference diameter (decreasing D).
#     :type layers: list, tuple
#     :returns: tuple with equivalent properties (density, umass, Do, Di, WT)
#     :rtype: tuple

#     .. doctest::

#         >>> layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
#         >>> pipe_layers(layers, Di_ref=0.660, umass=337.0)
#         (5232.900238245189, 0.0491)
#     """
#     #if (Di is not None) and (Do is not None):
#     if len([None for x in [Di_ref, Do_ref] if x is None]) != 1:
#         raise ValueError(f"pipe_layers: arguments not correctly specified: Di_ref={Di_ref}, Do_ref={Do_ref}")

#     #alayers = np.array(layers, dtype=[('WT', 'f4'), ('density', 'f4')])
#     alayers = layers
#     #print(alayers)
#     if Do_ref:
#     #     Di_ref = Do_ref - np.sum(alayers["WT"]) * 2
#     #     alayers = alayers[::-1]
#         Di_ref = sum([x for x,y in layers])
#         alayers = layers[::-1]
#     WT_total = 0.0
#     equiv_umass = umass
#     layer_Di = Di_ref 
#     for layer in alayers:
#         #print(layer)
#         layer_Do = layer_Di + 2*layer[0]
#         WT_total += layer[0]
#         _csa = np.pi/4 * (np.power(layer_Do,2) - np.power(layer_Di,2))
#         equiv_umass += _csa * layer[1]
#         layer_Di = layer_Do
#     if Do_ref is None:
#         Do_ref = Di_ref + 2 * WT_total
#     _csa = np.pi/4 * (np.power(Do_ref,2) - np.power(Di_ref,2))
#     equiv_ρ = equiv_umass / _csa
#     #return (equiv_density, equiv_umass, Do_ref, Di_ref, WT_total)
#     if returnDict:
#         return {
#             "equiv_ρ": equiv_ρ,
#             "umass": equiv_umass,
#             "Do": Do_ref,
#             "Di": Di_ref,
#             "WT": WT_total
#         }
#     else:
#         return (equiv_ρ, equiv_umass, Do_ref, Di_ref, WT_total)


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


# def pipe_joint_props(*, Do=None, Di=None, WT=None):
#     try:
#         Do, Di, WT = dodiwt(Do=Do, Di=Di, WT=WT)
#     except TypeError:
#         logger.error("pipe_joint_props: pipe diameter/wall thickness not correctly specified.") 
#         return None
#     CSA = dodi2CSA(Do, Di)
#     I = dodi2I(Do, Di)


# def calc_pipe_props(**kwargs):
#     """[summary]

#     additional inputs:
#     length - pipe length

#     Returns:
#         [type]: [description]
#     """
#     retObj = {}
#     Do = kwargs.get("Do", None)
#     Di = kwargs.get("Di", None)
#     WT = kwargs.get("WT", None)
#     CSA = I = None
#     try:
#         Do, Di, WT = dodiwt(Do=Do, Di=Di, WT=WT)
#     except TypeError:
#         logger.warning("calc_pipe_props: pipe diameter/wall thickness not correctly specified.")
#     else:
#         retObj["Do"] = Do
#         retObj["Di"] = Di
#         retObj["WT"] = WT
#         retObj["D_buoy"] = Do_buoy = Do
#         CSA = dodi2CSA(Do, Di)
#         retObj["CSA"] = CSA
#         I = dodi2I(Do, Di)
#         retObj["I"] = I
#     # pipe unit mass (mass/length) «umass», and mass if pipe length is specified
#     umass = None
#     ρ_pipe = kwargs.get("ρ_pipe", None)
#     length = kwargs.get("length", None)
#     try:
#         umass = pipe_unit_mass(ρ_pipe, CSA)
#     except TypeError:
#         logger.warning("calc_pipe_props: umass not calculated, check pipe density «ρ».")
#     else:
#         retObj["umass_pipe"] = umass
#         if length: retObj["mass_pipe"] = umass * length
#     # pipe unit weight «uwgt»
#     uwgt = None
#     ip = {"umass": umass}  # dict for function inputs as keyword arguments 
#     g = kwargs.get("ρ", None)  
#     if g:
#         ip["g"] = g   # only include g in function input dict if specified
#     try:
#         uwgt = pipe_unit_wgt(**ip)
#     except TypeError:
#         logger.warning("calc_pipe_props: uwgt not calculated.")
#     else:
#         retObj["uwgt"] = uwgt
#     # coating
#     coat_layers = kwargs.get("coat", None)
#     ip = {"Di_ref": Do, "umass": umass} 
#     try:
#         _ret = pipe_equiv_layers(coat_layers, **ip)
#         ##print("pipe_equiv_layers: ", _ret)
#         _, umass, Do_coat, _, WT_coat = _ret
#     except TypeError as err:
#         logger.warning("calc_pipe_props: coating not calculated.  %s"  % (err,))
#     else:
#         retObj["Do_coat"] = Do_coat
#         retObj["umass_coat"] = umass
#         if length: retObj["mass_coat"] = umass * length
#         retObj["D_buoy"] = Do_buoy = Do_coat
#     # submerged weight empty pipeline
#     ρ_seawater = kwargs.get("ρ_seawater", None)
#     ip = {"Do_buoy": Do_buoy, "ρ_seawater": ρ_seawater, "umass": umass}
#     g = kwargs.get("ρ", None)  
#     if g: ip["g"] = g   # only include g in function input dict if specified
#     try:
#         usubwgt_empty = pipe_unit_subwgt(**ip)
#     except TypeError as err:
#         logger.warning("calc_pipe_props: usubwgt_empty not calculated.  %s"  % (err,))
#     else:
#         retObj["usubwgt_empty"] = usubwgt_empty
#     # pipeline  umass with internal content   
#     ρ_content = kwargs.get("ρ_content", None)
#     try:
#         umass_content = dodi2CSA(Di) * ρ_content
#     except TypeError as err:
#         logger.warning("calc_pipe_props: pipeline contents not calculated.  %s"  % (err,))
#     else:
#         umass += umass_content
#         #retObj["umass_content"] = umass
#         #if length: retObj["mass_content"] = umass * length  
#     # pipeline submerged weight with internal content filled
#     ρ_seawater = kwargs.get("ρ_seawater", None)
#     ip = {"Do_buoy": Do_buoy, "ρ_seawater": ρ_seawater, "umass": umass}
#     g = kwargs.get("ρ", None)  
#     if g: ip["g"] = g   # only include g in function input dict if specified
#     try:
#         usubwgt_content = pipe_unit_subwgt(**ip)
#     except TypeError as err:
#         logger.warning("calc_pipe_props: usubwgt_content not calculated.  %s"  % (err,))
#     else:
#         retObj["usubwgt_content"] = usubwgt_content
#     # pipeline submerged weight with seawater filed  
#     ρ_seawater = kwargs.get("ρ_seawater", None)
#     umass_seawater = dodi2CSA(Di) * ρ_seawater + retObj["umass_coat"]
#     ip = {"Do_buoy": Do_buoy, "ρ_seawater": ρ_seawater, "umass": umass_seawater}
#     g = kwargs.get("ρ", None)  
#     if g: ip["g"] = g   # only include g in function input dict if specified
#     try:
#         usubwgt_seawater = pipe_unit_subwgt(**ip)
#     except TypeError as err:
#         logger.warning("calc_pipe_props: usubwgt_seawater not calculated.  %s"  % (err,))
#     else:
#         retObj["usubwgt_seawater"] = usubwgt_seawater
#     return retObj
