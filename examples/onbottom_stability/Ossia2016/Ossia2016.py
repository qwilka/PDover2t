"""

Bai, Yong & Xu, Weiping & Ruan, Weidong & Tang, Jiwei. (2014). On-bottom stability of subsea lightweight pipeline (LWP) on sand soil surface. Ships and Offshore Structures. 12. 1-9. 10.1080/17445302.2014.962249.
"""

#import pytest

import numpy as np

from pdover2t.utilities.data import json2globals
from pdover2t.pipe import *
#from pdover2t.pipe.pipe_properties import *


data_filepath = "Ossia2016.json"

json2globals(data_filepath)  # import data in JSON file into the current global scope as variables

# Do = pipe_Do[0]
# WT = pipe_WT[0]
# cont_ρ = pipe_WT[cont_ρ]

# Do = np.array(pipe_Do)
# WT = np.array(pipe_WT)
# cont_ρ = np.array(cont_ρ)

Di = dowt2di(Do, WT)
#pipe_CSA = dodi2CSA(Do, Di)
#cont_CSA = dodi2CSA(Di)
I = dodi2I(Do, Di)

pipe_wgt = pipe_weight(pipe_ρ, pipe_Do=pipe_Do, pipe_Di=pipe_Di, g=g)
cont_wgt = pipe_content_weight(cont_ρ, pipe_Di=pipe_Di, g=g)
coat_wgt, coat_WT, coat_ρ_eqv = pipe_coat_weight(pipe_Do, pipe_coat, g, eqv_props=True)
PL_wgt = pipe_wgt + cont_wgt + coat_wgt
PL_buoy_Do = pipe_Do + 2.0 * coat_WT
PL_buoy = pipe_content_weight(seawater_ρ, buoy_Do=PL_buoy_Do, g=g)
PL_subwgt =  PL_wgt - PL_buoy



