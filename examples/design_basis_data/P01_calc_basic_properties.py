"""
"""
from pdover2t.pipe import *
from pdover2t.utilities.data import json2globals

data_filepath = "P01.json"

json2globals(data_filepath)  # import data in JSON file into the current global scope as variables

Di = dowt2di(Do, WT)
CSA = dodi2CSA(Do, Di)
I = dodi2I(Do, Di)
umass = pipe_unit_mass(ρ_pipe, CSA)
uwgt = pipe_unit_wgt(umass, g)
