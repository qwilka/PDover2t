"""
12 inch water injection pipeline

to run:
python 
"""


import numpy as np
import pandas as pd

from pdover2t.utilities.data import json2globals
#from pdover2t.pipe import *



data_filepath = "12in_WI.json"

mapvars = None

# import data in JSON file into the current global scope as variables
meta = json2globals(data_filepath, mapvars)  

pro = pd.DataFrame.from_dict(profiles)


# https://realpython.com/pandas-plot-python/
# import matplotlib.pyplot as plt
# pro.plot(x="KP", y=["T_op", "P_i"])
# plt.show()
