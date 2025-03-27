"""
for testing calculate pressure containment using Barlow formula with a design factor
"""
from ...util.named_tuple import make_return_namedtuple



def hoop_stress_barlow(t_nom, p_d, D_o):
    σ_hoop = p_d*D_o/(2.0 * t_nom)
    return σ_hoop


def WT_barlow(σ_hoop, p_d, D_o):
    return p_d*D_o/(2.0 * σ_hoop)


def pressure_contain_unity(σ_hoop, SMYS, Df):
    pc_unity = σ_hoop/(SMYS * Df)
    return pc_unity


def pressure_containment(*,
    t_nom, p_d, D_o,
    SMYS, Df,
    **kwargs):
    σ_hoop = hoop_stress_barlow(t_nom, p_d, D_o)
    pc_unity = pressure_contain_unity(σ_hoop, SMYS, Df)
    return make_return_namedtuple("""σ_hoop, pc_unity""") 


if __name__ == "__main__":
    premise = {
        "p_d": 150.e5,
        "D_o": 24 * 25.4 * 1.e-3,
        "t_nom": 15.9 * 1.e-3,
        "SMYS": 450.e6,
        "Df": 0.72
    }
    pc = pressure_containment(**premise)

