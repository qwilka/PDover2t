"""

Bai, Yong & Xu, Weiping & Ruan, Weidong & Tang, Jiwei. (2014). On-bottom stability of subsea lightweight pipeline (LWP) on sand soil surface. Ships and Offshore Structures. 12. 1-9. 10.1080/17445302.2014.962249.
"""

import pytest

from pdover2t.utilities.data import json2globals
#from pdover2t.pipe import *
from pdover2t.pipe.pipe_properties import *


data_filepath = "P01.json"

json2globals(data_filepath)  # import data in JSON file into the current global scope as variables

Di = dowt2di(Do, WT)
CSA = dodi2CSA(Do, Di)
I = dodi2I(Do, Di)
umass = pipe_unit_mass(ρ_pipe, CSA)
uwgt = pipe_unit_wgt(umass, g)
#uwgt = umass * g

