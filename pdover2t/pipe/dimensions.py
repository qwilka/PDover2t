import math

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


def pipe_Do(Di, WT):
    """Calculate pipe outer diameter, given the pipe inner diamater and wall thickness.
    """
    Do = Di + 2 * WT
    return Do


def pipe_Di(Do, WT):
    """Calculate pipe inner diameter, given the pipe outer diamater and wall thickness.
    """
    Di = Do - 2 * WT
    return Di

def pipe_WT(Do, Di):
    """Calculate pipe wall thickness, given the pipe outer diamater and inner diameter.
    """
    WT = (Do - Di) / 2
    return WT



def pipe_CSA(Do, Di):
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

        >>> pipe_CSA(0.6656, 0.6172)
        0.19522098526377624
    """
    CSA = math.pi * (Do*Do - Di*Di)
    return CSA




# ================================================================

#import inspect
import logging

import numpy as np

# __all__ = [
#     "pipe_dimensions",
#     "pipe_weight",
# ]

logger = logging.getLogger(__name__)


def calc_pipe_Di(Do, WT) -> "Di":
    """Calculate pipe inner diameter from Do and WT.
    """
    return Do - 2*WT


def pipe_D_WT(*, Do=None, Di=None, WT=None, _round=False) -> "('Do', 'Di', 'WT')":
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
        logger.error("pipe_D_WT: arguments incorrectly specified: Do=%s, Di=%s, WT=%s" % (Do,Di,WT))
    return Do, Di, WT




def pipe_CSA(*, Do=None, Di=None, WT=None):
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

        >>> pipe_CSA(Do=0.660, WT=0.05)
        0.09581857593448868
    """
    _Do, _Di, _WT = pipe_D_WT(Do=Do, Di=Di, WT=WT)
    #_csa = np.pi/4 * (_Do**2 - _Di**2)
    _csa = np.pi/4 * (np.power(_Do, 2) - np.power(_Di, 2))
    return _csa


def pipe_mass(ρ, *, Do=None, Di=None, WT=None, CSA=None, length=None):
    """Calculate pipe mass (per unit length)
    """
    if CSA is None:
        CSA = pipe_CSA(Do=Do, Di=Di, WT=WT)
    mass = CSA * ρ
    if length:
        mass *= length
    return mass


def pipe_layers_equivalent(layers, *, Di_ref=None, Do_ref=None):
    """Calculate equivalent properties for pipe coating layers.
    """
    if len([n for n in (Di_ref, Do_ref) if n is None]) != 1:
        logger.error("pipe_layers_equivalent: arguments incorrectly specified: Di_ref=%s, Do_ref=%s" % (Di_ref, Do_ref))
        raise ValueError(f"arguments not correctly specified: Di_ref={Di_ref}, Do_ref={Do_ref}")    
    _do = _di = Di_ref if Di_ref else Do_ref
    mass_total = 0
    wt_total = 0
    csa_total = 0
    for (wt, ρ, *args) in layers:
        if Di_ref:
            layer_Di = _do
            _do = layer_Do = _do + (2 * wt)
        else:
            layer_Do = _di
            _di = layer_Do = _di - (2 * wt) 
        wt_total += wt
        layer_csa = pipe_CSA(Do=layer_Do, Di=layer_Di)
        #_mass = _csa * ρ
        mass_total += layer_csa * ρ
        csa_total += layer_csa
    ρ_equiv = mass_total / csa_total
    return {
        "Di": _di,
        "Do": _do,
        "ρ": ρ_equiv,
        "mass": mass_total
    }


class Cylinder:

    def __init__(self, length=None, Do=None, Di=None, WT=None):
        (self.Do, self.Di, self.WT) = pipe_D_WT(Do=Do, Di=Di, WT=WT)
        self.CSA = pipe_CSA(Do=self.Do, WT=self.WT)
        if length:
            self.volume = self.CSA * length


class LinePipe(Cylinder):

    def __init__(self, length, ρ, Do=None, Di=None, WT=None,
        coat_layers=None):
        super().__init__(length=length, Do=Do, Di=Di, WT=WT)
        #(self.pipe_Do, self.pipe_Di, self.pipe_WT) = pipe_D_WT(Do=Do, Di=Di, WT=WT)
        self.mass = self.volume * ρ
        self.Doa = self.Do
        self.status = {
            "external_coat": False,
            "internal_coat": False,
            "internal_clad": False,
            "internal_liner": False,          
        }
        if coat_layers:
            self.external_coat = {
                "layers": coat_layers,
                "equivalent": pipe_layers_equivalent(coat_layers,
                    Di_ref=self.Do)
            }
            self.Doa = self.external_coat["equivalent"]["Do"]
            self.status["external_coat"] = True







# old versions of functions below -----------------------------------

def pipe_dimensions(D_o=None, D_i=None, WT=None) -> "(D_o, D_i, WT)":
    # if funcname is None:
    #     funcname = inspect.currentframe().f_code.co_name
    if all([isinstance(x, (float, int)) for x in [D_o, D_i, WT]]):
        assert D_i==D_o-2*WT, f"pipe_basic_dims: inconsistent pipe dimensions D_o={D_o} D_i={D_i}, WT={WT}."
    elif D_o is None and all([isinstance(x, (float, int)) for x in [D_i, WT]]):
        D_o = D_i + 2*WT
    elif D_i is None and all([isinstance(x, (float, int)) for x in [D_o, WT]]):
        D_i = D_o - 2*WT
    elif WT is None and all([isinstance(x, (float, int)) for x in [D_o, D_i]]):
        WT = (D_o - D_i)/2
    else:
        logger.error("pipe_basic_dims: incorrectly specified arg: D_o=%s,D_i=%s,WT=%s" % (D_o,D_i,WT))
        return False
    return D_o, D_i, WT


def pipe_cross_sectional_area(D_o=None, D_i=None, WT=None) -> "pipe_CSA":
    D_o, D_i, WT = pipe_dimensions(D_o, D_i, WT)
    _CSA = np.pi/4 * (D_o**2 - D_i**2)
    return _CSA


def pipe_physical_props(rho_pipe, Do=None, Di=None, WT=None, length=None, rho_cont=None,
        coating=None, clad=None, liner=None, rho_water=None, g=9.81) -> "{}":
    Do, Di, WT = pipe_dimensions(Do, Di, WT)
    _CSA = pipe_cross_sectional_area(Do, Di, WT)
    _mass_len = _CSA * rho_pipe
    pp = {
        "pipe_Do": Do,
        "pipe_Di": Di,
        "pipe_WT": WT,
        "pipe_CSA": _CSA,
        "pipe_mass": _mass_len,
        "pj_mass": _mass_len,
        "D_buoy": Do,
        "D_cont": Di,
    }
    # if length:
    #     pp["pipe_len"] = length
    #     pp["pipe_mass"] = _mass_len * length
    if coating is not None:
        _coat_Di = pp["pipe_Do"]
        _coat_mass = 0
        if not isinstance(coating[0], (tuple,list)):
            coating = [coating]
        for ii, (_thick, _density, *args) in enumerate(coating):
            _Do, _Di, _thick = pipe_dimensions(None, _coat_Di, _thick)
            pp[f"coat{ii}_Do"] = _Do
            pp[f"coat{ii}_WT"] = _thick
            pp[f"coat{ii}_mass"] = np.pi/4 * (_Do**2 - _Di**2) * _density
            _coat_mass += pp[f"coat{ii}_mass"]
            _coat_Di +=  _thick * 2
        _mass_len += _coat_mass
        pp["coat_Do"] = _Do
        pp["coat_WT"] = (_Do - pp["pipe_Do"]) / 2
        pp["coat_mass"] = _coat_mass
        pp["coat_rho_eqv"] = _coat_mass / (np.pi/4 * (_Do**2 - pp["pipe_Do"]**2) )
        pp["D_buoy"] = _Do
        pp["pj_mass"] += _coat_mass
    if clad is not None:
        _clad_Do = pp["pipe_Di"]
        _clad_mass = 0
        if not isinstance(clad[0], (tuple,list)):
            clad = [clad]
        for ii, (_thick, _density, *args) in enumerate(clad):
            _Do, _Di, _thick = pipe_dimensions(_clad_Do, None, _thick)
            pp[f"clad{ii}_Di"] = _Di
            pp[f"clad{ii}_WT"] = _thick
            pp[f"clad{ii}_mass"] = np.pi/4 * (_Do**2 - _Di**2) * _density
            _clad_mass += pp[f"clad{ii}_mass"]
            _clad_Do -=  _thick * 2 
        pp["D_cont"] = _Di
        pp["pj_mass"] += _clad_mass
    if liner is not None:
        _liner_Do = pp["D_cont"]
        _liner_mass = 0
        if not isinstance(liner[0], (tuple,list)):
            liner = [liner]
        for _thick, _density, *args in liner:
            _Do, _Di, _thick = pipe_dimensions(_liner_Do, None, _thick)
            pp[f"liner{ii}_Di"] = _Di
            pp[f"liner{ii}_WT"] = _thick
            pp[f"liner{ii}_mass"] = np.pi/4 * (_Do**2 - _Di**2) * _density
            _liner_mass += pp[f"liner{ii}_mass"]
            _liner_Do -=  _thick * 2
        pp["D_cont"] = _Di
        pp["pj_mass"] += _liner_mass
    if rho_cont is not None:
        pp["pj_cont_mass"] = pp["pj_mass"] + np.pi/4 * pp["D_cont"]**2 * rho_cont
    if rho_water is not None:
        pp["pj_flood_mass"] = pp["pj_mass"] + np.pi/4 * pp["D_cont"]**2 * rho_water
        pp["pj_buoyf"] = rho_water * g * np.pi/4 * pp["D_buoy"]**2 
        pp["pj_subw"] = pp["pj_mass"] * g - pp["pj_buoyf"]
        if rho_cont is not None:
            pp["pj_cont_subw"] = pp["pj_cont_mass"] * g - pp["pj_buoyf"]
        pp["pj_flood_subw"] = pp["pj_flood_mass"] * g - pp["pj_buoyf"] 
    return pp

#def pipe_weight(rho_pipe, D_o=None, D_i=None, WT=None, length=None, rho_cont=None, D_buoy=None):



if __name__ == "__main__":
    parameters = {
        "Do": 0.3229,
        "WT": 0.0185,
        "rho_pipe": 7850,
        "clad": (0.003, 8000),
        "coating": [
            (0.0003, 1300),
            (0.0003, 900),
            (0.0094, 900),
            (0.031, 620),
            (0.003, 900),
            (0.031, 620),
            (0.004, 900),            
        ],
        "rho_water": 1027,
        "rho_cont": np.array([10, 860]),
    }
    pp = pipe_physical_props(**parameters)
    