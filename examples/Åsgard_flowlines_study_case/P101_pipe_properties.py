"""
References
«Subsea pipeline design, analysis, and installation» Bai & Bai, 2014 ed, Chapter 23

"""
import logging
import unittest

import numpy as np
import pdover2t
from pdover2t.pipe.pipe_properties2 import calc_pipe_props, calc_basic_pipe_properties


# p.544 Table 23.2 Installation Analysis Results for Phase I Flowlines
# array order: zone-1, zone-2
ipObj = {
    "lpipe_Do": np.array([0.2588, 0.2518]), 
    "lpipe_WT": np.array([0.0156, 0.0116]),
    "lpipe_ρ": 7760.0,    # 7850,
    "coat_layers": [(0.053, 1190)],
    "content_ρ": 0,
    "seawater_ρ": 1027,
}

#ipObj["lpipe_Do"] = np.array([0.423, 0.5])


# Calculate pipe inner diameter
#plObj = pdover2t.pipe.calc_pipeline_props(**ipObj)
plObj = calc_pipe_props(**ipObj)

