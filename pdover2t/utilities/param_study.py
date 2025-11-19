import numbers

import numpy as np
import pandas as pd


def param_sweep(*paramlists, table=False, dataframe=False):
    "Create a grid-search/parameter sweep from parameter lists"
    # https://peps.python.org/pep-3102/#specification
    op = []
    for ii, li in enumerate(paramlists):
        if len(li)==0:
            raise ValueError(f"Empty list not allowed.")
        li = np.array(li)
        if ii<len(paramlists)-1:
            #print(paramlists[ii+1:])
            flen = 1
            for li2 in paramlists[ii+1:]:
                flen = flen*len(li2)
            li = np.repeat(li, flen)
        if ii>0:
            rlen = 1
            for li2 in paramlists[:ii]:
                rlen = rlen*len(li2)    
            li = np.tile(li, rlen)        
        li = np.array(li)
        op.append(li)
    if table:  # NOTE np.array has a single type
        op = np.array(op).T
        return op
    if dataframe:
        # op = np.array(op).T
        # op = pd.DataFrame(op)
        op_dict = {}
        for ii, arr in enumerate(op):
            op_dict[ii] = arr
        op = pd.DataFrame(op_dict)
        return op
    return tuple(op)


def ttest(a):
    a = np.array(a)
    print(f"ttest: type of a {type(a)}")
    return None

def axial_friction(phi_s, r_soil_pipe, check_radians=True):
    """Return axial friction coefficient."""
    if check_radians:
        _phi = phi_s if isinstance(phi_s, numbers.Number) else phi_s[0]
        if _phi > np.pi/2:
            phi_s = phi_s*np.pi/180.0
    mu_seabed = r_soil_pipe * np.tan(phi_s)
    return mu_seabed


# def typeframe(*lists):
#     typstr = ""
#     for ii, li in enumerate(lists):
#         li = np.array(li)
#         if ii>0:
#             typstr += "+"


if __name__ == "__main__":
    a = [1.0,2.0,3.0,4.0]
    b = np.array([11,12,13])
    c = ("a","b")
    pars = param_sweep(a, b, c)
    print(pars)
    #ttest(a)
    r_soil_pipe = [0.7, 0.8, 0.9]
    phi_s = [35.0, 42.0, 46.0]
    #phi_s = np.array(phi_s)*np.pi/180.
    vphi_s, vr_soil_pipe = param_sweep(phi_s, r_soil_pipe)
    mu_s = axial_friction(vphi_s, vr_soil_pipe)
    df = pd.DataFrame({"phi":vphi_s, "r_soil_pipe": vr_soil_pipe, "mu_s":mu_s})

