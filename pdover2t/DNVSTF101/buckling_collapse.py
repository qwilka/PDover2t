"""
"""
#import sys

# Note: if using numpy, it _must_ be imported before PDover2t modules are imported
from ..config import use_numpy

#use_numpy = False
if use_numpy:
    import numpy as np
    from numpy import sqrt, pi, abs as _abs, cos, acos
    from scipy.optimize import newton
else:
    from math import sqrt, pi, cos, acos
    _abs = abs

from ..util.named_tuple import make_return_namedtuple
from ..pipe.environment import external_water_pressure
from ..pipe.material import characteristic_material_strength
from ..pipe.pipe import characteristic_WT




def pipe_ovality(D, D_max=None, D_min=None) -> "O_0":
    """Calculate pipe ovality.
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.4.2 eq:5.14 page:96 $O_0$
    """
    if D_max is None:
        D_max = D
    if D_min is None:
        D_min = D
    O_0 = (D_max - D_min) / D
    if O_0 < 0.005:
        O_0 = 0.005
    return O_0



def elastic_collapse_pressure(D_o, t_nom, E, ν=0.3):
    """elastic collapse pressure
    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.4.2 eq:5.14 page:93 $p_{el}$
    """
    p_el = 2.0 * E * (t_nom/D_o)**3 / (1-ν**2)
    return p_el


def plastic_collapse_pressure(D_o, t_nom, f_y, α_fab):
    """Calculate characteristic plastic pressure p_p.
    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.4.2 eq:5.15 page:93 $p_p$
    """
    p_p = f_y * α_fab * 2.0*t_nom/D_o
    return p_p





def characteristic_collapse_pressure(D_o, t_nom, p_el, p_p, O_0, p_c_0=10.e5):
    """Calculate p_c numerically using Newton's method.
    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.4.2 eq:5.11 page:95 $p_c$
    """

    def p_c_func(p_c, p_el, p_p, O_0, D_o, t_nom):
        return (p_c-p_el)*(p_c**2-p_p**2) - p_c*p_el*p_p*O_0*D_o/t_nom

    def p_c_func_deriv(p_c, p_el, p_p, O_0, D_o, t_nom):
        return 3*p_c**2 - 2*p_c*p_el - p_p**2 - p_el*p_p**O_0*D_o/t_nom

    p_c = newton(p_c_func, p_c_0, p_c_func_deriv, args=(p_el, p_p, O_0, D_o, t_nom))
    return p_c


def characteristic_collapse_pressure_analytic(D_o, t_nom, p_el, p_p, O_0):
    """Calculate p_c analytically using solution of cubic equation given
    in DNV-ST-F101.
    Reference:
    DNV-ST-F101 (2021-08) 
        sec:13.4.7 eq:13.10 page:292 $p_c$
    """
    b = -p_el
    c = -(p_p**2 + p_el*p_p*O_0*D_o/t_nom)
    d = p_el * p_p**2
    u = 1/3 * (-1/3 * b**2 + c)
    v = 1/2 * (2/27 * b**3 - 1/3 * b*c + d)
    phi = acos(-v / sqrt(-u**3))    # np.arccos
    y  = -2 * sqrt(-u) * cos(phi/3 + 60*pi/180)
    p_c = y - 1/3 * b
    return p_c


def local_buckling_collapse_unity(p_e, p_min, p_c, γ_m, γ_SCLB):
    """Local buckling collapse unity check.

    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.4.1 eq:5.12 p:92 

    (press_contain_resis_unity)
    """
    lbuck_collapse_uty =  (p_e - p_min) * γ_m * γ_SCLB / p_c  
    return lbuck_collapse_uty






def local_buckling_collapse_all(*,
    t_nom, D_o, ν, E, O_0, t_fab, t_corr, t_ero,
    SMYS, f_ytemp,
    ρ_xwater, h_l, p_min=0.0, 
    α_U, α_fab, γ_m, γ_SCLB,
    **kwargs ):
    """
    """

    t_1, _ = characteristic_WT(t_nom, t_fab, t_corr, t_ero)
    _t = t_1
    p_el = elastic_collapse_pressure(D_o, _t, E, ν)
    f_y = characteristic_material_strength(SMYS, α_U, f_ytemp=f_ytemp)
    p_p = plastic_collapse_pressure(D_o, _t, f_y, α_fab)
    try:
        p_c = characteristic_collapse_pressure(D_o, _t, p_el, p_p, O_0, p_c_0=p_p)
    except NameError:   # NameError: name 'newton' is not defined (if not using numpy/scipy)
        p_c = characteristic_collapse_pressure_analytic(D_o, _t, p_el, p_p, O_0)

    p_e   = external_water_pressure(ρ_xwater, h_l=h_l)
    lb_collapse_uty = local_buckling_collapse_unity(p_e, p_min, p_c, γ_m, γ_SCLB)
    lb_collapse_check = (p_e - p_min) <= p_c / (γ_m * γ_SCLB)  # DNV-ST-F101 eq:5.12 

    return make_return_namedtuple("""p_el, f_y, p_p, p_c, p_e, lb_collapse_uty, lb_collapse_check""")



