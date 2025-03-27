"""

"""

from ..config import use_numpy

#use_numpy = False
if use_numpy:
    from numpy import exp
else:
    from math import exp

from ..util.named_tuple import make_return_namedtuple
from ..pipe.pipe import characteristic_WT
from ..pipe.material import characteristic_material_strength
from ..pipe.environment import external_water_pressure






def propagating_pressure(D, t, f_y, α_fab):
    """Pipe propagating buckle characteristic pressure. 
    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.5.1 eq:5.21 p:94 
    """
    p_pr = 35.0 * f_y * α_fab * (t/D)**2.5
    return p_pr


def local_buckling_propagation_unity(p_e, p_min, p_pr, γ_m, γ_SCLB):
    """Local buckling collapse unity check.

    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.4.1 eq:5.12 p:92 

    (press_contain_resis_unity)
    """
    lbuck_collapse_uty =  (p_e - p_min) * γ_m * γ_SCLB / p_pr  
    return lbuck_collapse_uty




def local_buckling_propagation_all(*, 
    D_o, t_nom, t_fab, t_corr, t_ero,
    SMYS, SMTS, α_U, f_ytemp=0.0, f_utemp=0.0,
    α_fab, ρ_xwater, h_l, p_min=0.0, 
    γ_m, γ_SCLB,
    **kwargs ):
    """

    Reference:
        DNV-ST-F101 (2021-08) 
        sec:5.4.4.1 eq:5.12 p:92 
    """
    _, t_2 = characteristic_WT(t_nom, t_fab, t_corr, t_ero)
    f_y = characteristic_material_strength(SMYS, α_U, f_ytemp=f_ytemp)
    # D_over_t_check = 15.0 < D_o/t_2 <= 45.0  # The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    D_over_t_check = (15.0 < D_o/t_2) & (D_o/t_2 <= 45.0)
    p_pr = propagating_pressure(D_o, t_2, f_y, α_fab)
    p_e   = external_water_pressure(ρ_xwater, h_l=h_l)
    lb_prop_uty = local_buckling_propagation_unity(p_e, p_min, p_pr, γ_m, γ_SCLB)
    lb_prop_check = (p_e - p_min) <= p_pr / (γ_m * γ_SCLB)  # DNV-ST-F101 eq:5.21 

    return make_return_namedtuple("""D_over_t_check, p_pr, p_e, lb_prop_uty, lb_prop_check""")



def crossover_pressure(p_pr, p_prBA, D, t_2, L_BA):
    """
    Reference:
        DNV-ST-F101 (2021-08) 
        sec:5.4.5.3 eq:5.23 p:95 
    """
    p_x = p_pr + (p_prBA-p_pr) * (1.0 - exp(-20*t_2*L_BA/D**2))
    return p_x


def buckle_arrestor_unity(p_e, p_x,
        gamma_m=None, limit_state="ULS", gamma_SCLB=None, SC="medium"
        ):
    """
    Reference:
        DNV-ST-F101 (2021-08) 
        sec:5.4.5.3 eq:5.22 p:95 
    """    
    if gamma_m is None:
        gamma_m = factor.gamma_m_map[limit_state]
    if gamma_SCLB is None:
        gamma_SCLB = factor.gamma_SCLB_map[SC]
    propbuck_arrestor_uty = p_e * 1.1 * gamma_m * gamma_SCLB / p_x
    return propbuck_arrestor_uty

