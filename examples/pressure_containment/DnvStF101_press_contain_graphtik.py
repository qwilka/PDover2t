
"""
Pipeline pressure containment according to DNVGL-ST-F101 (2017-12)
refs:
https://graphtik.readthedocs.io/en/latest/

Notes:


to run:
python DnvStF101_pressure_containment.py 
"""

from graphtik import compose, operation
from pdover2t.DnvStF101 import *

#from operator import mul, sub

# @operation(name="abs qubed", needs=["α-α×β"], provides=["|α-α×β|³"])
# def abs_qubed(a):
#     return abs(a) ** 3


# graphop = compose("graphop", 
#     operation(mul, needs=["α", "β"], provides=["α×β"]),
#     operation(sub, needs=["α", "α×β"], provides=["α-α×β"]),
#     abs_qubed)


# sol = graphop(**{'α': 2, 'β': 5})

# sol2 = graphop.compute({'α': 2, 'β': 5}, outputs=["α-α×β"])

# Gas Export (0-0.3 km) location class II, 60°C max. Temp. 340-370m depth
p_d = 240.e5  # (Pa) design pressure at reference elevation Z_ref
h_ref = 30.0  # (m) reference elevation for pressure (LAT=0m)
ρ_cont = 275. # (kg/m3) density of pipeline contents



γ_inc = 1.10  # incidental to design pressure ratio
α_spt = 1.05  # DNVGL-ST-F101 (2017-12) p94


#p_inc = p_incid_ref(p_d, γ_inc)
#p_t = p_system_test_ref(p_d,  γ_inc, α_spt)
#p_li = p_incid_loc(p_d, ρ_cont, h_ref, h_ref, γ_inc)  # h_l=h_ref

p_inc_OP = operation(p_incid_ref, needs=["p_d", "γ_inc"], provides=["p_inc"])
p_t_OP = operation(p_system_test_ref, needs=["p_d", "γ_inc", "α_spt"], 
            provides=["p_t"])
p_li_OP = operation(p_incid_loc, needs=["p_d", "ρ_cont", "h_l", "h_ref", "γ_inc", "g"], 
            provides=["p_li"])

