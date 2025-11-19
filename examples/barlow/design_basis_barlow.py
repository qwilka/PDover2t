"""

"""

from pickleshare import *
#from pathlib import Path

import numpy as np
import pandas as pd

project_name = "Barlow-test"
db_path =  "_doc/test-Barlow.db"
comment  = "Test study using Barlow formula"  # description

db = PickleShareDB(db_path)

basecase = {
    "name" : "basecase",
    "comment": "Basecase: 24\" 50bar-150bar ",
    "NPS":  24,                       #"24\"", 
    "D_o": 24 * 25.4 * 1.e-3,  # (m) pipe internal diameter
    "p_d": np.array([50.e5, 150.e5]),  # (Pa) design pressure at reference elevation Z_ref
    "t_nom": 0.0159,  # (m) pipe wall thickness.
    "designf": 0.72,
    "SMYS": 450.e6, # (Pa) pipe steel SMYS
}


design_basis = {
    "name": "Barlow-test",
    "basecase": basecase
}

db[design_basis["name"]] = design_basis


