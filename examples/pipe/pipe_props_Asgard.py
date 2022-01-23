"""
References
«Subsea pipeline design, analysis, and installation» Bai & Bai, 2014 ed, Chapter 23
"""

from pdover2t.pipe import calc_pipe_props

# P101
P101 = {
    "Do": 258.8e-3,
    "WT": 15.6e-3,
    "ρ_pipe":  7850.0,
    "coat": [(53.e-3, 1190.0)],
    "length": 12.2,
    "ρ_content": 0,
    "ρ_seawater": 1027.0,
}

ret = calc_pipe_props(**P101)
