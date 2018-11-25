from . import factor


def abs_stability(Fstar_Y, Fstar_Z, F_R, mu, w_s, 
                   gamma_SC=None, SC="high", soil_type="clay" ) -> "abs_stab":
    """stability unity check. 
    Reference:
    DNVGL-RP-F109 (2017-05) 
        sec:3.6.2, eq:3.38, page:31 
    """
    if gamma_SC is None:
        gamma_SC = factor.gamma_SC_lookup(SC, soil_type)
    abs_stab = gamma_SC * (Fstar_Y + mu*Fstar_Z) / (mu*w_s + F_R)
    return abs_stab


if __name__ == "__main__":
    pass