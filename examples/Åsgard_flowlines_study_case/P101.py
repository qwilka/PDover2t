"""

References
«Subsea pipeline design, analysis, and installation» Bai & Bai, 2014 ed, Chapter 23
"""
#import logging

import pdover2t
from pdover2t.pipe import pipe_physical_props

# log_messages = False    # logger messages, turn on (log_messages=True) or off (False)
# log_timestamp = False  # add a timestamp to logger messages

# if log_messages:
#     logger = logging.getLogger()
#     logger.setLevel(logging.WARNING)  # logging.DEBUG  logging.WARNING
#     lh = logging.StreamHandler()
#     # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     log_template = '%(levelname)s: %(name)s.%(message)s'
#     if log_timestamp: log_template += ' «%(asctime)s»'
#     formatter = logging.Formatter(log_template)
#     lh.setFormatter(formatter)
#     logger.addHandler(lh)

# Uncomment the following line to enable extended log messages.
#pdover2t.utilities.turn_on_logging(level="WARNING", timestamp=False) 


pipe_Do = 258.5e-3   # pipe outer diameter (m)
pipe_WT = 15.6e-3   # pipe wall thickness (m)
pipe_ρ = 7850.0     # pipe steel density (kg/m3)
pipe_coat = [(53.e-3, 1190.0)] # [(thickness, density)]
pipe_joint_length = 12.2


seawater_ρ = 1027.0     # seawater density (kg/m3)

ret = pipe_physical_props(rho_pipe=pipe_ρ, Do=pipe_Do, WT=pipe_WT, 
    coating=pipe_coat, rho_water=seawater_ρ)

_, pipe_Di, _ = pdover2t.pipe.pipe_D_WT(Do=pipe_Do, WT=pipe_WT)   # calculate pipe inner diameter 
CSA = pdover2t.pipe.pipe_CSA(Do=pipe_Do, WT=pipe_WT)
pipe_joint_mass = pdover2t.pipe.pipe_mass(pipe_ρ, CSA=CSA, length=pipe_joint_length)

P101 = {
    "pipe_joint_bare": pdover2t.pipe.LinePipe(length=pipe_joint_length, 
        ρ=pipe_ρ, Do=pipe_Do, WT=pipe_WT),      
}

P101["zone2"] = {
    "pipe_joint_coated": pdover2t.pipe.LinePipe(length=pipe_joint_length, 
        ρ=pipe_ρ, Do=pipe_Do, WT=pipe_WT,
        coat_layers=pipe_coat)      
}



