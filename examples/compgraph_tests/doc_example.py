"""
https://graphtik.readthedocs.io/en/latest/
"""

from graphtik import compose, operation
from operator import mul, sub

@operation(name="abs qubed", needs=["α-α×β"], provides=["|α-α×β|³"])
def abs_qubed(a):
    return abs(a) ** 3


graphop = compose("graphop", 
    operation(mul, needs=["α", "β"], provides=["α×β"]),
    operation(sub, needs=["α", "α×β"], provides=["α-α×β"]),
    abs_qubed)


sol = graphop(**{'α': 2, 'β': 5})

sol2 = graphop.compute({'α': 2, 'β': 5}, outputs=["α-α×β"])

