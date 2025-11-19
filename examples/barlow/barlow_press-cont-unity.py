"""
for testing calculate pressure containment using Barlow formula with a design factor
"""

from pdover2t.utilities.named_tuple import make_return_namedtuple as rnt


def hoop_stress_barlow(t, P, D):
    hoop_stress = P*D/(2.0 * t)
    return hoop_stress


def WT_barlow(hoop, P, D):
    return P*D/(2.0 * hoop)


def pressure_contain_unity(hoop, SMYS, Df):
    unity = hoop/(SMYS * Df)
    return unity

def pressure_containment_bursting(*,
    t, P, D,
    SMYS, Df,
    **kwargs):
    hoop_stress = hoop_stress_barlow(t, P, D)
    unity = pressure_contain_unity(hoop_stress, SMYS, Df)
    return rnt("""hoop_stress, unity""") 


if __name__ == "__main__":
    premise = {
        "P": 150.e5,
        "D": 24 * 25.4 * 1.e-3,
        "t": 15.9 * 1.e-3,
        "SMYS": 450.e6,
        "Df": 0.72
    }
    pc = pressure_containment_bursting(**premise)

