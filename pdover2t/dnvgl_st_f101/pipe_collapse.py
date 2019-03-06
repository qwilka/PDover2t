#import math

import numpy as np
import scipy.optimize

from . import factor
from .material import char_mat_strength

__all__ = [
    "pipe_ovality",
    "pipe_char_elastic_pressure",
    "pipe_char_plastic_pressure",
    "char_collapse_pressure_num",
    "char_collapse_pressure",
    "pipe_collapse_unity",
    "pipe_collapse_all"
]

# from .pipe_collapse import pipe_char_elastic_pressure
# from .pipe_collapse import pipe_char_plastic_pressure
# from .pipe_collapse import pipe_ovality
# from .pipe_collapse import char_collapse_pressure
# from .pipe_collapse import pipe_collapse_unity

# def pipeCollapse(t,D,P_c,SMYS,nu=0.3,E=207.*10**9, f_o=None):
#     '''DNV-OS-F101:2010 Sec.5 D401, collapse due to external pressure '''
#     P_el = 2*E*(t/D)**3/(1-nu**2)
#     P_p = f_y*alpha_fab*(2*t/D)
#     if not f_o:
#         f_o = (D_max-D_min)/D
#         if f_o<0.005: f_o = 0.005
#     return (P_c-P_el)*(P_c**2-P_p**2) - P_c*P_el*P_p*f_o*D/t


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


def pipe_char_elastic_pressure(t, D, nu=0.3, E=207.*10**9) -> "p_el":
    """Calculate p_el.
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.4.2 eq:5.12 page:96 $p_{el}$
    """
    p_el = 2*E*(t/D)**3/(1-nu**2)
    return p_el

def pipe_char_plastic_pressure(t, D, f_y, alpha_fab) -> "p_p":
    """Calculate characteristic plastic pressure p_p.
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.4.2 eq:5.13 page:96 $p_p$
    """
    p_p = f_y*alpha_fab*(2*t/D)
    return p_p


def p_c_zerofunc(p_c, p_el, p_p, O_0, D, t):
    return (p_c-p_el)*(p_c**2-p_p**2) - p_c*p_el*p_p*O_0*D/t

def p_c_fprime(p_c, p_el, p_p, O_0, D, t):
    return 3*p_c**2 - 2*p_c*p_el - p_p**2 - p_el*p_p**O_0*D/t

def char_collapse_pressure_num(p_el, p_p, O_0, D, t, p_c_0=1.e5) -> "p_c":
    """Calculate p_c numerically using Newton's method.
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.4.2 eq:5.11 page:95 $p_c$
    """
    p_c = scipy.optimize.newton(p_c_zerofunc, p_c_0, p_c_fprime,
        args=(p_el, p_p, O_0, D, t))
    return p_c


def char_collapse_pressure(p_el, p_p, O_0, D, t) -> "p_c":
    """Calculate p_c analytically using solution of cubic equation given
    in DNVGL-ST-F101.
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:13.4.7 eq:13.10 page:299 $p_c$
    """
    b = -p_el
    c = -(p_p**2 + p_el*p_p*O_0*D/t)
    d = p_el * p_p**2
    u = 1/3 * (-1/3 * b**2 + c)
    v = 1/2 * (2/27 * b**3 - 1/3 * b*c + d)
    phi = np.arccos(-v / np.sqrt(-u**3))
    y  = -2 * np.sqrt(-u) * np.cos(phi/3 + 60*np.pi/180)
    p_c = y - 1/3 * b
    return p_c


def pipe_collapse_unity(p_e, p_c, gamma_m, gamma_SCLB, p_min=0
        ) -> "pipe_collapse_uty":
    """Calculate pipe collapse unity value.
    Local buckling – system collapse (external over pressure only).
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.4.1 eq:5.10 page:95 $p_{lt}$
    """ 
    # if gamma_m is None:
    #     gamma_m = factor.gamma_m_map[limit_state]
    # if gamma_SCLB is None:
    #     gamma_SCLB = factor.gamma_SCLB_map[SC]
    pipe_collapse_uty = (p_e - p_min) * gamma_m * gamma_SCLB / p_c 
    return pipe_collapse_uty


def external_pressure(depth, rho_water, g=9.81) -> "p_e":
    p_e = abs(depth) * rho_water * g
    return p_e

def pipe_collapse_all(t, D, E, nu, SMYS, h_l, rho_water,
        gamma_m, alpha_fab, alpha_U, gamma_SCLB, 
        material=None, T=None, f_ytemp=None,  
        D_max=None, D_min=None, p_min=0, g=9.81
        ) -> "{}":
    O_0 = pipe_ovality(D, D_max, D_min)
    p_el = pipe_char_elastic_pressure(t, D, nu, E)
    #_alpha_U = factor.alpha_U_map(alpha_U)
    f_y = char_mat_strength(SMYS, material, T, f_ytemp, alpha_U)
    #_alpha_fab = factor.alpha_fab_map(alpha_fab)
    p_p = pipe_char_plastic_pressure(t, D, f_y, alpha_fab)
    p_c = char_collapse_pressure(p_el, p_p, O_0, D, t)
    p_e = external_pressure(abs(h_l), rho_water, g)
    pipe_collapse_uty = pipe_collapse_unity(p_e, p_c, gamma_m, gamma_SCLB, p_min)
    return {
        "O_0": O_0,
        "p_el": p_el,
        "p_p": p_p,
        "p_c": p_c,
        "p_e": p_e,
        "pipe_collapse_uty": pipe_collapse_uty,
    }



if __name__ == "__main__":
    p_c_0 = 1025*9.81*1
    t = 0.0212
    t_corr = 0.0005
    t_fab = 0.001
    t_1 = t - t_corr - t_fab 
    D = 0.660
    D_max = D
    D_min = D
    SMYS = 450e6
    f_y =  SMYS - 6e6
    alpha_fab = 1.00
    h_l = -410.
    rho_water = 1027.
    p_e = rho_water*9.81*abs(h_l)
    p_el = pipe_char_elastic_pressure(t_1, D, nu=0.3, E=207.*10**9)
    p_p = pipe_char_plastic_pressure(t_1, D, f_y, alpha_fab)
    O_0 = pipe_ovality(D, D_max, D_min)
    p_c = char_collapse_pressure_num(p_el, p_p, O_0, D, t_1, p_c_0=p_c_0)
    print("p_c (numerical)=", p_c)
    pipe_collapse_uty = pipe_collapse_unity(p_e, p_c)
    print("pipe_colpse_uty  (numerical)=", pipe_collapse_uty)
    p_c = char_collapse_pressure(p_el, p_p, O_0, D, t_1)
    print("p_c=", p_c)
    pipe_collapse_uty = pipe_collapse_unity(p_e, p_c)
    print("pipe_colpse_uty=", pipe_collapse_uty)