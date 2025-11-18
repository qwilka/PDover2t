"""
for testing calculate pressure containment using Barlow formula with a design factor
"""
import numpy as np


def hoop_stress_barlow(t, P, D):
    return P*D/(2.0 * t)


def WT_barlow(hoop, P, D):
    return P*D/(2.0 * hoop)


def hoop_stress_unity(hoop, SMYS, Df):
    return hoop/(SMYS * Df)


if __name__ == "__main__":
    P = 150.e5
    D = 24 * 25.4 * 1.e-3
    t = 15.9 * 1.e-3
    t = np.linspace(5.0,20.0, 21) * 1.e-3
    SMYS = 450.e6
    Df = 1.0 #0.72
    hoop = hoop_stress_barlow(t, P, D)
    unity = hoop_stress_unity(hoop, SMYS, Df)
    hoop_MPa = hoop * 1.e-6
    print(f"{hoop_MPa=} MPa {unity=}")
    t_opt = np.interp(0, t, unity)
    # try:
    #     t_opt = t_opt.item()  # conver np.float to float
    # except:
    #     pass
    # print(f"{t_opt=}")
    # hoop = hoop_stress_barlow(t_opt, P, D)
    # unity = hoop_stress_unity(hoop, SMYS, Df)
    # print(f"{t_opt=} {hoop=} MPa {unity=}")

    from scipy import interpolate
    f = interpolate.interp1d(unity, t)
    t_0 = f(1.0)
    hoop_0 = hoop_stress_barlow(t_0, P, D)
    unity_0 = hoop_stress_unity(hoop_0, SMYS, Df)
    wt_barlow_0 = WT_barlow(hoop_0, P, D )
    check_0 = t_0 - wt_barlow_0
    print(f"{t_0=} {hoop_0=} {unity_0=} {wt_barlow_0=} {check_0=}")

