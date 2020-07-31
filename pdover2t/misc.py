

# def water_depth_press(wd: "h_l", rho_water, g=9.81) -> "p_e":
#     p_e = rho_water * g * abs(wd)
#     return p_e

def symbol(desc):
    _desc = desc.strip(" \/")
    if _desc == "alpha" or len(desc)==1 and desc=="a":
        return "α"
    if _desc == "lambda" or len(desc)==1 and desc=="l":
        return "λ"
    if _desc == "nu" or len(desc)==1 and desc=="n":
        return "ν"
    if _desc == "rho" or len(desc)==1 and desc=="r":
        return "ρ"
    if _desc == "sigma" or len(desc)==1 and desc=="s":
        return "σ"


