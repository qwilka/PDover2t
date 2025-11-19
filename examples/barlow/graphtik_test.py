"""

networkx version issue
https://github.com/pygraphkit/graphtik/issues/10  Exception with the latest versions of networkx
"""
import importlib

from graphtik import compose, operation    #, keyword

barlow = importlib.import_module("barlow_press-cont-unity")
#from barlow import hoop_stress_barlow, pressure_contain_unity



cgraph = compose("hoop-stress", 
    operation(barlow.hoop_stress_barlow, name="Barlow", 
              needs=["t_nom", "p_d", "D_o"], 
              provides=["hoop_stress"]),
    operation(barlow.pressure_contain_unity, name="unity", 
              needs=["hoop_stress", "SMYS", "Df"], 
              provides=["hoop_unity"]),
)

try:
    cgraph.plot("barlow-graph.svg")
except:
    print(f"error: cgraph.plot")


if __name__ == "__main__":
    premise = {
        "p_d": 150.e5,
        "D_o": 24 * 25.4 * 1.e-3,
        "t_nom": 15.9 * 1.e-3,
        "SMYS": 450.e6,
        "Df": 0.72
    }
    result = cgraph.compute(premise)
    result.plot("barlow-result.svg")

    