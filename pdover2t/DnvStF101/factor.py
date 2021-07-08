import logging
import math

logger = logging.getLogger(__name__)

# Reference: DNVGL-ST-F101 (2017-12) table:5.1 sec:5.3.2.3 page:87
def gamma_m_map(gamma_m="default") -> "gamma_m":
    """Map value for material resistance factor, $\gamma_m$
    Reference: DNVGL-ST-F101 (2017-12) table:5.1 sec:5.3.2.3 page:87
    """
    if isinstance(gamma_m, (float, int)):
        if not 1.00<=gamma_m<=1.15:
            logger.warning("gamma_m_map: check argument «gamma_m»=%d non-standard value!" % (gamma_m, ))
        return gamma_m
    elif gamma_m.upper() in ["SLS", "ULS", "ALS"]:
        return 1.15
    elif gamma_m.upper() == "FLS":
        return 1.00
    else:
        return 1.00
# gamma_m_map = {
#     "SLS": 1.15,
#     "ULS": 1.15,
#     "ALS": 1.15,
#     "FLS": 1.00,
# }

# Reference: DNVGL-ST-F101 (2017-12) table:5.2 sec:5.3.2.4 page:88
def gamma_SCPC_map(gamma_SCPC="default") -> "gamma_SCPC":
    """Map value for safety class resistance factor for 
    pressure containment, $\gamma_{SC,PC}$
    Reference: DNVGL-ST-F101 (2017-12) table:5.2 sec:5.3.2.4 page:88
    """
    if isinstance(gamma_SCPC, (float, int)):
        if not 1.046<=gamma_SCPC<=1.308:
            logger.warning("gamma_SCPC_map: check argument «gamma_SCPC»=%d non-standard value!" % (gamma_SCPC, ))
        return gamma_SCPC
    elif gamma_SCPC.upper() == "HIGH":
        return 1.308
    elif gamma_SCPC.upper() == "MEDIUM":
        return 1.138
    elif gamma_SCPC.upper() == "LOW":
        return 1.046
    else:
        return 1.308
# gamma_SCPC_map = {
#     "low": 1.046,
#     "medium": 1.138,
#     "high": 1.308,
# }
def gamma_SCLB_map(gamma_SCLB="default") -> "gamma_SCLB":
    """Map value for safety class resistance factor for 
    local buckling, collapse and load controlled, $\gamma_{SC,LB}$
    Reference: DNVGL-ST-F101 (2017-12) table:5.2 sec:5.3.2.4 page:88
    """
    if isinstance(gamma_SCLB, (float, int)):
        if not 1.04<=gamma_SCLB<=1.26:
            logger.warning("gamma_SCLB_map: check argument «gamma_SCLB»=%d non-standard value!" % (gamma_SCLB, ))
        return gamma_SCLB
    elif gamma_SCLB.upper() == "HIGH":
        return 1.26
    elif gamma_SCLB.upper() == "MEDIUM":
        return 1.14
    elif gamma_SCLB.upper() == "LOW":
        return 1.04
    else:
        return 1.26
# gamma_SCLB_map = {
#     "low": 1.04,
#     "medium": 1.14,
#     "high": 1.26,
# }

# Reference: DNVGL-ST-F101 (2017-12) table:5.3 sec:5.3.3.6 page:90
def alpha_U_map(alpha_U="default", system_pressure_test=False,
                    supplementary_requirement=None):
    """Map value for material strength factor, $\alpha_U$
    Reference: DNVGL-ST-F101 (2017-12) table:5.3 sec:5.3.3.6 page:90
    """
    if isinstance(alpha_U, (float, int)):
        if not 0.96<=alpha_U<=1.0:
            logger.warning("alpha_U_map: check argument «alpha_U»=%d non-standard value!" % (alpha_U, ))
        return alpha_U
    elif system_pressure_test or supplementary_requirement.upper() in ["P", "U"]:
        return 1.00
    else:
        return 0.96
# alpha_U_map = {
#     "normal": 1.00,
#     "U": 1.00,
#     "other": 0.96,
#     "default": 0.96,
# }

# Reference: DNVGL-ST-F101 (2017-12) table:5.8 sec:5.4.2.1 page:94
def alpha_mpt_map(alpha_mpt="default", gamma_m=None, gamma_SCPC=None) -> "alpha_mpt":
    """Map value for pressure test factor for
    mill test pressure, $\alpha_{mpt}$
    Reference: DNVGL-ST-F101 (2017-12) table:5.8 sec:5.4.2.1 page:94
    """
    if isinstance(alpha_mpt, (float, int)):
        if not 1.000<=alpha_mpt<=1.251:
            logger.warning("alpha_mpt_map: check argument «alpha_mpt»=%d non-standard value!" % (alpha_mpt, ))
        return alpha_mpt
    elif gamma_m and gamma_SCPC:
        alpha_mpt = gamma_m * gamma_SCPC * 0.96 *(math.sqrt(3)/2)
        logger.warning("alpha_mpt_map: calculating «alpha_mpt»=%d " % (alpha_mpt, ))
        return alpha_mpt
    elif alpha_mpt.upper() == "HIGH":
        return 1.251
    elif alpha_mpt.upper() == "MEDIUM":
        return 1.088
    elif alpha_mpt.upper() == "LOW":
        return 1.000
    else:
        return 1.251
# alpha_mpt_map = {
#     "low": 1.000,
#     "medium": 1.088,
#     "high": 1.251,
# }
# def calc_alpha_mpt(gamma_m, gamma_SCPC):
#     """Calculate pressure test factor alpha_mpt using DNVGL-ST-F101 formula.
#     Reference:
#     DNVGL-ST-F101 (2017-12) 
#         table:5.8 sec:5.4.2.1 page:94
#     """
#     return gamma_m * gamma_SCPC * 0.96 *(math.sqrt(3)/2)

def alpha_spt_map(alpha_spt="default") -> "alpha_spt":
    """Map value for pressure test factor for
    system pressure test, $\alpha_{spt}$
    Reference: DNVGL-ST-F101 (2017-12) table:5.8 sec:5.4.2.1 page:94
    """
    if isinstance(alpha_spt, (float, int)):
        if not 1.03<=alpha_spt<=1.05:
            logger.warning("alpha_spt_map: check argument «alpha_spt»=%d non-standard value!" % (alpha_spt, ))
        return alpha_spt
    elif alpha_spt.upper() == "HIGH":
        return 1.05
    elif alpha_spt.upper() == "MEDIUM":
        return 1.05
    elif alpha_spt.upper() == "LOW":
        return 1.03
    else:
        return 1.05
# alpha_spt_map = {
#     "low": 1.03,
#     "medium": 1.05,
#     "high": 1.05,
# }

# Reference: DNVGL-ST-F101 (2017-12) table:5.4 sec:5.3.3.7 page:91
def alpha_fab_map(alpha_fab="default"):
    """Reference: DNVGL-ST-F101 (2017-12) table:5.4 sec:5.3.3.7 page:91
    """
    if isinstance(alpha_fab, (float, int)):
        if not 0.85<=alpha_fab<=1.0:
            logger.warning("alpha_fab_map: check argument «alpha_fab»=%d non-standard value!" % (alpha_fab, ))
        return alpha_fab
    elif alpha_fab.upper() == "SEAMLESS":
        return 1.0
    elif alpha_fab.upper() in ["UO", "TRB", "ERW", "HFW"]:
        return 0.93
    elif alpha_fab.upper() == "UOE":
        return 0.85
    else:
        return 0.85
    
# alpha_fab_map = {
#     "seamless": 1.0,
#     "UO": 0.93,
#     "TRB": 0.93,
#     "ERW": 0.93,
#     "HFW": 0.93,
#     "UOE": 0.85,
#     "default": 0.85,
# }

# def stab_gamma_SC_lookup(SC, soil_type):
#     """lookup gamma_SC for on-bottom stability check.

#     Reference:
#     DNVGL-RP-F109 (2017-05) 
#         table:3.5 sec:3.6.3 page:31
#     """
#     gamma_SC = None
#     if soil_type.lower() in ["sand", "rock", "gravel", "sand and rock"]:
#         gamma_SC = {"low": 0.98, 
#                     "normal": 1.32, 
#                     "high": 1.67}.get(SC.lower(), None)
#     elif soil_type.lower() in ["clay"]:
#         gamma_SC = {"low": 1.00, 
#                     "normal": 1.40, 
#                     "high": 1.83}.get(SC.lower(), None)
#     if gamma_SC is None:
#         logger.error("stab_gamma_SC_lookup: cannot resolve args «SC»=«%s» «soil_type»=«%s»" % (SC, soil_type))
#     return gamma_SC