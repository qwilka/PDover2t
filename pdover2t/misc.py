

def water_depth_press(wd: "h_l", rho_water, g=9.81) -> "p_e":
    p_e = rho_water * g * abs(wd)
    return p_e
