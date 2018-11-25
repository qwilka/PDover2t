import logging
import math

logger = logging.getLogger(__name__)

# # Reference: DNVGL-ST-F101 (2017-12) table:5.1 sec:5.3.2.3 page:87
# gamma_m_map = {
#     "SLS": 1.15,
#     "ULS": 1.15,
#     "ALS": 1.15,
#     "FLS": 1.00,
# }

# # Reference: DNVGL-ST-F101 (2017-12) table:5.2 sec:5.3.2.4 page:88
# gamma_SCPC_map = {
#     "low": 1.046,
#     "medium": 1.138,
#     "high": 1.308,
# }
# gamma_SCLB_map = {
#     "low": 1.04,
#     "medium": 1.14,
#     "high": 1.26,
# }

# # Reference: DNVGL-ST-F101 (2017-12) table:5.3 sec:5.3.3.6 page:90
# alpha_U_map = {
#     "normal": 1.00,
#     "U": 1.00,
#     "other": 0.96,
# }

# # Reference: DNVGL-ST-F101 (2017-12) table:5.8 sec:5.4.2.1 page:94
# alpha_mpt_map = {
#     "low": 1.000,
#     "medium": 1.088,
#     "high": 1.251,
# }
# alpha_spt_map = {
#     "low": 1.03,
#     "medium": 1.05,
#     "high": 1.05,
# }
# def calc_alpha_mpt(gamma_m, gamma_SCPC):
#     """Calculate pressure test factor alpha_mpt using DNVGL-ST-F101 formula.

#     Reference:
#     DNVGL-ST-F101 (2017-12) 
#         table:5.8 sec:5.4.2.1 page:94
#     """
#     return gamma_m * gamma_SCPC * 0.96 *(math.sqrt(3)/2)


def gamma_SC_lookup(SC, soil_type, region="north sea", cyclonic=False):
    """lookup gamma_SC for on-bottom stability check.

    Reference:
    DNVGL-RP-F109 (2017-05) 
        table:3.5 sec:3.6.3 page:31 (only North Sea for now....)
    """
    gamma_SC = None
    if soil_type.lower() in ["sand", "rock", "gravel", "sand and rock"]:
        gamma_SC = {"low": 0.98, 
                    "normal": 1.32, 
                    "high": 1.67}.get(SC.lower(), None)
    elif soil_type.lower() in ["clay"]:
        gamma_SC = {"low": 1.00, 
                    "normal": 1.40, 
                    "high": 1.83}.get(SC.lower(), None)
    if gamma_SC is None:
        logger.error("stab_gamma_SC_lookup: cannot resolve args «SC»=«%s» «soil_type»=«%s»" % (SC, soil_type))
    return gamma_SC