"""

Bai, Yong & Xu, Weiping & Ruan, Weidong & Tang, Jiwei. (2014). On-bottom stability of subsea lightweight pipeline (LWP) on sand soil surface. Ships and Offshore Structures. 12. 1-9. 10.1080/17445302.2014.962249.
"""

#import pytest

import numpy as np

from pdover2t.utilities.data import json2globals
from pdover2t.pipe import *
#from pdover2t.pipe.pipe_properties import *


data_filepath = "LWP.json"

mapvars = {
    "pipe_Do": "Do",
    "pipe_WT": "WT",
}
mapvars = None

varnames = json2globals(data_filepath, mapvars)  # import data in JSON file into the current global scope as variables

Do = pipe_Do[0]
WT = pipe_WT[0]
cont_ρ = cont_ρ[0]

# Do = np.array(pipe_Do)
# WT = np.array(pipe_WT)
#cont_ρ = np.array(cont_ρ)

Di = dowt2di(Do, WT)
CSA = dodi2CSA(Do, Di)
I = dodi2I(Do, Di)
umass = pipe_unit_mass(pipe_ρ, CSA, cont_ρ)
uwgt = pipe_unit_wgt(umass, g)
usubwgt = pipe_unit_subwgt(Do, seawater_ρ, umass, g)

