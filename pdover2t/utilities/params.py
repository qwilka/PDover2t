"""
"""
import numpy as np
import pandas as pd


def paramater_grid(*paramlists, table=False, dataframe=False):
    "Create a grid-search/parameter sweep grid from parameter lists"
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




if __name__ == "__main__":
    a = [1.0,2.0,3.0,4.0]
    b = np.array([11,12,13])
    c = ("a","b")
    pars = paramater_grid(a, b, c)
    print(pars)
