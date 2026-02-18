"""
DNV Rules 1976 (1980)
"""
from ..pipe.environment import external_water_pressure
from ..util.named_tuple import make_return_namedtuple


def barlow_hoop_stress(*, D_o, t_nom, p_i, p_e, **kwargs):
    """DNV Rules 1976 (1980) sec. 4.2.2.2
    """
    σ_y = (p_i - p_e) * D_o / (2.0 * t_nom)
    return σ_y


def allowable_hoop_stress(*, σ_f, Dfactor=0.72, k_t=1.0, **kwargs):
    """DNV Rules 1976 (1980) sec. 4.2.2.1
    Permissible/allowable hoop stress.
    σ_f  SMYS
    """
    σ_yp = Dfactor * σ_f * k_t
    return σ_yp


def pressure_contain_unity(σ_y, σ_yp):
    """
    """
    pc_unity = σ_y / σ_yp 
    return pc_unity




def pressure_containment(*,
    t_nom, p_d, D_o,
    SMYS, Df=0.72, k_t=1.0, h_l, ρ_xwater,
    **kwargs):
    p_e = external_water_pressure(h_l=h_l, ρ_xwater=ρ_xwater)
    σ_hoop = barlow_hoop_stress(D_o=D_o, t_nom=t_nom, p_i=p_d, p_e=p_e)
    σ_yp = allowable_hoop_stress(σ_f=SMYS, Dfactor=Df, k_t=k_t)
    unity = pressure_contain_unity(σ_hoop, σ_yp)
    return make_return_namedtuple("""σ_hoop, unity""") 


if __name__ == "__main__":
    premise = {
        "p_d": 207.9.e5,
        "D_o": 323.9 * 1.e-3,
        "t_nom": 19.1 * 1.e-3,
        "SMYS": 358.e6,
        "Df": 0.72
    }
    pc = pressure_containment(**premise)
