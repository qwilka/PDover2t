
import numpy as np

#from . import factor
from ..pipe_properties import pipe_physical_props

__all__ = [
    "floatation_stability"
]


def floatation_stability(W_sub, b, gamma_w=1.1) -> "float_stab_uty":
    """Floatation stability unity check. 
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.5.5.3, eq:5.42, page:113 
    DNVGL-RP-F109 (2017-05) 
        sec:3.2, eq:3.1, page:12 
    """
    float_stab_uty = gamma_w * b / (W_sub + b)
    return float_stab_uty



if __name__ == "__main__":
    D = 0.3229
    t_nom = 0.0185
    parameters = {
        "Do": D,
        "WT": t_nom,
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
        "rho_cont": 10,
    }
    pp = pipe_physical_props(**parameters)
    W_sub = pp["pj_cont_subw"]
    b = pp["pj_buoyf"]
    float_stab_uty = floatation_stability(W_sub, b, gamma_w=1.1)