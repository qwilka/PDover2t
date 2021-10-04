"""Analysis of gas pipeline «P-01»
"""
#import logging

import numpy as np

from pdover2t.pipe import *


Di = 617.2 * 1.e-3
WT = 24.22 * 1.e-3

Do = pipe_Do(Di, WT)
CSA = pipe_CSA(Do, Di)



# pipe_length = 12.2

# # p.11
# Do = 0.3229
# coating_layers = [
#     (0.0003, 1300, "FBE"),
#     (0.0003, 900, "adhesive"),
#     (0.0094, 900, "EA165E"),
#     (0.031, 620, "TDF1"),
#     (0.003, 900, "EA165E"),
#     (0.031, 620, "TDF2"),
#     (0.004, 900, "EA165E"),
# ]

# coat_thk, coat_rho, coat_mass = pipe_equivalent_layers(coating_layers, Di_ref=Do)

# print(f"L51 coating thickness={coat_thk} equivalent density={coat_rho}")

# pipe_layers = [
#     (0.0185, 7850, "backing pipe"),
#     (0.003, 7000, "clad layer"),
# ]

# pipe_thk, pipe_rho, pipe_mass = pipe_equivalent_layers(pipe_layers, Do_ref=Do)

# print(f"L51 pipe thickness={pipe_thk} equivalent density={pipe_rho}")

# total_pipe_mass = (pipe_mass + coat_mass) * pipe_length

# print(f"L51 total pipe mass dry={total_pipe_mass} kg")

# pipe_cs_weigth = (pipe_mass + coat_mass) * 9.81

# print(f"L51 pipe cross-section weight dry={pipe_cs_weigth} N/m")
