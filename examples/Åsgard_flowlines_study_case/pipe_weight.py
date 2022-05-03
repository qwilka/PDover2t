"""


to run:
python pipe_weight_test.py 
"""


import numpy as np

from pdover2t.utilities.data import json2globals
from pdover2t.pipe import *



data_filepath = "P101.json"
data_filepath = "S101.json"

mapvars = None

# import data in JSON file into the current global scope as variables
meta = json2globals(data_filepath, mapvars)  



pipe_Di = dowt2di(pipe_Do, pipe_WT)


pipe_wgt = pipe_weight(pipe_ρ, pipe_Do=pipe_Do, pipe_Di=pipe_Di, g=g)
cont_wgt = pipe_content_weight(cont_ρ, pipe_Di=pipe_Di, g=g)
coat_wgt, coat_WT, coat_ρ_eqv = pipe_coat_weight(pipe_Do, pipe_coat, g, eqv_props=True)
PL_wgt = pipe_wgt + cont_wgt + coat_wgt
PL_buoy_Do = pipe_Do + 2.0 * coat_WT
PL_buoy = pipe_buoyancy(seawater_ρ, buoy_Do=PL_buoy_Do, g=g)
PL_subwgt =  PL_wgt - PL_buoy



