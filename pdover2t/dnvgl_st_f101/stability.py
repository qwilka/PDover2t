
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


def absolute_lateral_stability(F_y, F_z, F_R, mu, W_sub, gamma_SC) -> "abs_lat_stab_uty":
    """Absolute lateral stability unity check. 
    Reference:
    DNVGL-RP-F109 (2017-05) 
        sec:3.6.1, eq:3.38, page:31 
    """
    abs_lat_stab_uty = gamma_SC * (F_y + mu*F_z) / (mu*W_sub + F_R)
    return abs_lat_stab_uty


def absolute_vertical_stability(F_z, W_sub, gamma_SC) -> "abs_vert_stab_uty":
    """Absolute vertical stability unity check. 
    Reference:
    DNVGL-RP-F109 (2017-05) 
        sec:3.6.1, eq:3.39, page:31 
    """
    abs_vert_stab_uty = gamma_SC * F_z / W_sub
    return abs_vert_stab_uty

def peak_horizontal_load(r_toty, rho_w, D, C_y, U, V) -> "F_y":
    """Peak horizontal load for on-bottom stability check. 
    Reference:
    DNVGL-RP-F109 (2017-05) 
        sec:3.6.4, eq:3.40, page:32 
    """
    F_y = r_toty * 0.5 * rho_w * D * C_y * (U + V)**2
    return F_y



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