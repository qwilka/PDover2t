
#import inspect
import logging

import numpy as np

# __all__ = [
#     "pipe_basic_dims",
#     "pipe_weight",
# ]

logger = logging.getLogger(__name__)


def pipe_basic_dims(D_o=None, D_i=None, WT=None) -> "(D_o, D_i, WT)":
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
    return D_o, D_i, WT

def pipe_cross_section_area(D_o=None, D_i=None, WT=None) -> "pipe_CSA":
    D_o, D_i, WT = pipe_basic_dims(D_o, D_i, WT)
    pipe_CSA = np.pi/4 * (D_o**2 - D_i**2)
    return pipe_CSA

def pipe_physical_props(rho_pipe, Do=None, Di=None, WT=None, length=None, rho_cont=None,
        coating=None, clad=None, liner=None, rho_water=None, g=9.81) -> "{}":
    Do, Di, WT = pipe_basic_dims(Do, Di, WT)
    _CSA = pipe_cross_section_area(Do, Di, WT)
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
            _Do, _Di, _thick = pipe_basic_dims(None, _coat_Di, _thick)
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
            _Do, _Di, _thick = pipe_basic_dims(_clad_Do, None, _thick)
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
            _Do, _Di, _thick = pipe_basic_dims(_liner_Do, None, _thick)
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