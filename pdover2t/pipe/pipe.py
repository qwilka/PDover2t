from collections import namedtuple
import logging

from ..config import use_numpy
if use_numpy:
    from numpy import pi
else:
    from math import pi

from ..util.named_tuple import make_return_namedtuple, isinstance_namedtuple

logger = logging.getLogger(__name__)


pipeCoatLayer = namedtuple("PipeCoatLayer", ["thickness", "density", "name"])


class PipeCoat:
    def __init__(self, layers):
        self.layers = layers


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


def tubular_CSA(Do, WT):
    Di = Do - 2*WT
    return pi / 4.0 *(Do*Do - Di*Di)


def tubular_linear_mass(CSA, ρ):
    return CSA * ρ


def tubular_properties(Do, WT, ρ, length=None, ρ_xwater=None):
    """
    https://en.wikipedia.org/wiki/Linear_density
    """
    CSA = tubular_CSA(Do, WT)
    mass_ld = tubular_linear_mass(CSA, ρ)  # mass linear density unit mass
    if length is None:
        mass = None
    else:
        mass = mass_ld * length
    # if ρ_xwater is not None:
    #     linear_buoyancy = Do*Do / 4.0 * pi * ρ_xwater
    #     sub_linear_ρ = linear_ρ - linear_buoyancy
    # else:
    #     linear_buoyancy = None
    #     sub_linear_ρ = None
    return make_return_namedtuple("""CSA, mass_ld, mass""")




def linepipe_properties(*, D_o, t_nom, ρ_pipe, joint_length=12.2, ρ_xwater, retInputs=False, **kwargs):
    retItems = ["D_o", "t_nom", "ρ_pipe"] if retInputs else []
    CSA, mass_ld, mass = tubular_properties(D_o, t_nom, ρ_pipe, joint_length, ρ_xwater)
    retItems.extend(["CSA", "mass_ld", "mass"])  # """CSA, mass_ld, mass"""
    return make_return_namedtuple(retItems)


def pipeline_properties(*, coat=None, D_o=None, mass_ld=None, lp_props=None, ρ_xwater, **kwargs):
    """
    """
    # if lp_props and isinstance_namedtuple(lp_props, "linepipe_properties"):
    #     for varname, value in lp_props._asdict():
    #         exec(f"{varname} = {value}")  # ???
    if lp_props and isinstance_namedtuple(lp_props, "linepipe_properties"):
        if D_o is None and "D_o" in lp_props._fields: D_o = lp_props.D_o
        if mass_ld is None and "mass_ld" in lp_props._fields: mass_ld = lp_props.mass_ld
    #_do = D_o
    if coat:
        if isinstance(coat, (list, tuple)) and isinstance_namedtuple(coat[0], typename="PipeCoatLayer"):
            _coat = coat
        elif isinstance(coat, PipeCoat):
            _coat = coat.layers
        # elif isinstance_namedtuple(coat[0][0], typename="PipeCoatLayer"):
        #     _coat = coat[0]
        for thk, density, _ in _coat:
            _di = D_o
            D_o = _di + 2.0 * thk
            _CSA, _massld, _ = tubular_properties(D_o, thk, density)
            mass_ld +=  _massld
    D_buoy = D_o
    buoy_ld = pi / 4.0 *D_buoy*D_buoy * ρ_xwater
    submass_ld = mass_ld - buoy_ld
    return make_return_namedtuple(["D_o","mass_ld", "D_buoy", "buoy_ld", "submass_ld"])





def characteristic_WT(t_nom, t_fab, t_corr, t_ero, operation=True):
    """Pipe characteristic wall thickness.


    Notes:
        for t2, set t_fab=t_corr=t_ero=0.0
        for pre-operation set t_corr=t_ero=0.0

    Reference:
    DNV-ST-F101 (2021-08) 
        s:5.3.4.1 p:89 t:5-5 
    """
    if operation:
        t_1  = t_nom - t_fab - t_corr - t_ero
        t_2  = t_nom - t_corr - t_ero
    else:  # prior to operation
        t_1  = t_nom - t_fab 
        t_2  = t_nom 
    return t_1, t_2
