import math

import numpy as np
import scipy.optimize

from . import factor
#from .material import char_mat_strength


# def pipeCollapse(t,D,P_c,SMYS,nu=0.3,E=207.*10**9, f_o=None):
#     '''DNV-OS-F101:2010 Sec.5 D401, collapse due to external pressure '''
#     P_el = 2*E*(t/D)**3/(1-nu**2)
#     P_p = f_y*alpha_fab*(2*t/D)
#     if not f_o:
#         f_o = (D_max-D_min)/D
#         if f_o<0.005: f_o = 0.005
#     return (P_c-P_el)*(P_c**2-P_p**2) - P_c*P_el*P_p*f_o*D/t


def pipe_ovality(D, D_max, D_min) -> "O_0":
    """Calculate pipe ovality.
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.4.2 eq:5.14 page:96 $O_0$
    """
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
    """Calculate p_el.
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

def char_collapse_pressure(p_c_0, p_el, p_p, O_0, D, t) -> "p_c":
    p_c = scipy.optimize.newton(p_c_zerofunc, p_c_0, p_c_fprime,
        args=(p_el, p_p, O_0, D, t))
    return p_c



def pipe_collapse_unity(p_e, p_c, 
        gamma_m=None, limit_state="ULS", gamma_SCLB=None, SC="medium",
        p_min=0) -> "pipe_collapse_uty":
    """Calculate pipe collapse unity value.
    Local buckling – system collapse (external over pressure only).
    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.4.1 eq:5.10 page:95 $p_{lt}$
    """
    if gamma_m is None:
        gamma_m = factor.gamma_m_map[limit_state]
    if gamma_SCLB is None:
        gamma_SCLB = factor.gamma_SCLB_map[SC]
    pipe_collapse_uty = p_c / (gamma_m * gamma_SCLB) / (p_e - p_min)
    return pipe_collapse_uty




if __name__ == "__main__":
    p_c_0 = 1025*9.81*10
    D = D_max = D_min = 10 * 0.0254
    t = 0.0254
    f_y = 450e6
    alpha_fab = 1.00
    p_el = pipe_char_elastic_pressure(t, D, nu=0.3, E=207.*10**9)
    p_p = pipe_char_plastic_pressure(t, D, f_y, alpha_fab)
    O_0 = pipe_ovality(D, D_max, D_min)
    p_c = char_collapse_pressure(p_c_0, p_el, p_p, O_0, D, t)
    print("p_c=", p_c)