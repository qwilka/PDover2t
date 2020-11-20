"""
Pipeline Submerged Weight 

to run:
python pipe_weight_test.py 
"""
import argparse
import numpy as np

from pdover2t.utilities import turn_on_logging
turn_on_logging(template='%(levelname)s: %(message)s')

from pdover2t.pipe import (pipe_umass, pipe_layers, pipe_usubwgt, 
    pipe_uwgt, pipe_Do_Di_WT)

aparser = argparse.ArgumentParser(description="Testing pdover2t module.")
aparser.add_argument("case", help="Specify a test case to run.", 
    nargs='?', default="scalar",
    choices=["scalar", "array", "error"])
args = aparser.parse_args()


eqs = "="*30
print(f"{eqs}\nRunning test case «{args.case}»\n{eqs}")
if args.case.lower() in ["scalar", "error"]:
    Do = 0.660
    WT = 0.0214
    coating_layers = [(0.0003, 1450.), (0.0038, 960.), (0.045, 2250.)]
elif args.case.lower()=="array":
    Do = np.array([0.660, 0.6656])
    WT = np.array([0.0214, 0.0242])
    # coating_layers = [ (np.array([0.0003, 0.0003]), np.array([1450., 1450.])), 
    #     (np.array([0.0038, 0.0038]), np.array([960., 960.]) ), 
    #     (np.array([0.045, 0.045]), np.array([2250., 1900.]) )]
    coating_layers = [ (0.0003, 1450.), (0.0038, 960. ), 
        (0.045, np.array([2250., 1900.]) )]
length = 12.2
pipe_ρ = 7850.    
seawater_ρ = 1027.0
gas_ρ = 215.0
g = 9.81

# Do, Di, WT = pipe_Do_Di_WT(Do=Do, WT=WT)
# CSA = pipe_CSA(Do, Di)
# umass = pipe_umass(CSA, pipe_ρ)
# joint_mass = umass * length
# uwgt = pipe_uwgt(umass, g)
# usubwgt = pipe_usubwgt(Do, seawater_ρ, g, Do=Do, WT=WT)
# joint_subwgt = usubwgt * length

# empty pipeline
umass = pipe_umass(pipe_ρ, Do=Do, WT=WT)
layersObj = pipe_layers(coating_layers, Di_ref=Do, umass=umass, returnDict=True)
pl_umass = layersObj["umass"]
pl_Do = layersObj["Do"]
#pl_uwgt = pipe_uwgt(pl_umass, g)
if args.case.lower()=="error":
    pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT)
else:
    pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT, 
                        umass=pl_umass)
#pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT)
print(f"empty pl_usubwgt={pl_usubwgt}")

# water filled pipeline
Do, Di, WT = pipe_Do_Di_WT(Do=Do, WT=WT)
waterfill_umass = pipe_umass(seawater_ρ, Do=Di, Di=0)
waterfill_pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT, 
                umass=(pl_umass+waterfill_umass))
print(f"waterfill pl_usubwgt={waterfill_pl_usubwgt}")

# gas filled pipeline
gasfill_umass = pipe_umass(gas_ρ, Do=Di, Di=0)
gasfill_pl_usubwgt = pipe_usubwgt(pl_Do, seawater_ρ, g, Do=Do, WT=WT, 
                umass=(pl_umass+gasfill_umass))
print(f"gasfill pl_usubwgt={gasfill_pl_usubwgt}")

