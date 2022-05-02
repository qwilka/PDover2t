"""

Bai, Yong & Xu, Weiping & Ruan, Weidong & Tang, Jiwei. (2014). On-bottom stability of subsea lightweight pipeline (LWP) on sand soil surface. Ships and Offshore Structures. 12. 1-9. 10.1080/17445302.2014.962249.
"""

#import pytest

import numpy as np

from pdover2t.utilities.data import json2globals
from pdover2t.pipe import *
#from pdover2t.pipe.pipe_properties import *


data_filepath = "Choi2013.json"

# mapvars = {
#     "pipe_Do": "Do",
#     "pipe_WT": "WT",
# }
mapvars = None

# import data in JSON file into the current global scope as variables
meta = json2globals(data_filepath, mapvars)  

# Do = pipe_Do[0]
# WT = pipe_WT[0]
# cont_ρ = cont_ρ[0]

# Do = np.array(pipe_Do)
# WT = np.array(pipe_WT)
#cont_ρ = np.array(cont_ρ)

pipe_Di = dowt2di(pipe_Do, pipe_WT)
#CSA = dodi2CSA(Do, Di)
#I = dodi2I(Do, Di)

pipe_wgt = pipe_weight(pipe_ρ, pipe_Do=pipe_Do, pipe_Di=pipe_Di, g=g)
cont_wgt = pipe_content_weight(cont_ρ, pipe_Di=pipe_Di, g=g)
coat_wgt, coat_WT, coat_ρ_eqv = pipe_coat_weight(pipe_Do, pipe_coat, g, eqv_props=True)
PL_wgt = pipe_wgt + cont_wgt + coat_wgt
PL_buoy_Do = pipe_Do + 2.0 * coat_WT
PL_buoy = pipe_buoyancy(seawater_ρ, buoy_Do=PL_buoy_Do, g=g)
PL_subwgt =  PL_wgt - PL_buoy



# umass = pipe_unit_mass(pipe_ρ, CSA, cont_ρ)
# uwgt = pipe_unit_wgt(umass, g)
# usubwgt = pipe_unit_subwgt(Do, seawater_ρ, umass, g)

