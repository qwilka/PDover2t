"""
"""

from graphtik import compose, operation    #, keyword

from pressure_containment_barlow import hoop_stress_barlow, hoop_stress_unity



cgraph= compose("hoop-stress", 
    operation(hoop_stress_barlow, name="Barlow", needs=["p_d", "D_o", "t_nom", provides=["hoop_stress"]),
    operation(hoop_stress_barlow, name="Barlow", needs=["p_d", "D_o", "t_nom", provides=["hoop_unity"]),
)