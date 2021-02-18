"""Residual curvature installation of subsea pipelines.



References
==========
ANALYTICAL FORMULAE FOR THE LATERAL BUCKLING BEHAVIOUR OF PIPELINES
INSTALLED WITH RESIDUAL CURVATURE, Teigen, Ibrahim, OMAE2020-18261
"""
import numpy as np

from pdover2t.utilities import turn_on_logging
turn_on_logging(template='%(levelname)s: %(message)s')

from pdover2t.pipe import (pipe_umass, pipe_layers, pipe_usubwgt, 
    pipe_uwgt, pipe_Do_Di_WT)


# Table 1 common properties
common_props = {
    "WD": 360.0,
    "material": "CMn",
    "pipe_ρ": 7930.0,
    "E": 207.0*10**9,
    'ν': 0.3,
    "SMYS": 450.e6,
    "SMTS": 535.e6,    
    'α': 1.17e-5,
    "ρ_cont": 903.0,
    "coat_WT": 62.e-3,
    "coat_ρ": 661.0,
}
WD = 360.0
material = "CMn"
pipe_ρ = 7930.0
E = 207.0*10**9
ν = 0.3
SMYS = 450.e6
SMTS = 535.e6
α = 1.17e-5
ρ_cont = 903.0
coat_WT = 62.e-3
coat_ρ = 661.0
seawater_ρ = 1025.0
g = 9.81

# Table 2 case specific
Do = np.array([203.2, 254.0, 304.8, 355.6, 406.4, 457.2]) * 1.e-3
WT = 22.2 * 1.e-3

Do, Di, WT = pipe_Do_Di_WT(Do=Do, WT=WT)



# empty pipeline
umass = pipe_umass(pipe_ρ, Do=Do, WT=WT)

_, pl_umass, pl_Do, _ , _ = pipe_layers([(coat_WT, coat_ρ)], Di_ref=Do, umass=umass)

cont_umass = pipe_umass(ρ_cont, Do=Di, Di=0)
pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT, 
                umass=(pl_umass+cont_umass))
