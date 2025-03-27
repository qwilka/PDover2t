"""
"""
from collections import namedtuple
#import sys

from ..config import use_numpy

if use_numpy:
    from numpy import abs as _abs
else:
    _abs = abs



def external_water_pressure(ρ_xwater, g=9.80665, *, h_l=None, LAT=None):
    """Water pressure, external to pipe.
    """
    if h_l is None:
        h_l = -_abs(LAT)
    p_e = _abs(h_l) * ρ_xwater * g
    return p_e


def still_water_level(WL, WL_ref="MWL", tide_t1=0.0, tide_t2=0.0, storm_surge_pos=0.0, storm_surge_neg=0.0, fsurge=1.0):
    r"""
    :param WL: water depth/level corresponding to WL_ref=LAT/MWL/HAT, (specify +ve value)
    :type WL: float
    :param WL_ref: reference water level, one of LAT/MWL/MSL/HAT :math:`(WL_ref)`
    :type WL_ref: str
    :param tide_t1: tide at t1, see DNV-RP-C205 f:4.2
    :type tide_t1: float
    :param tide_t2: tide at t2 (specify +ve value), see DNV-RP-C205 f:4.2 
    :type tide_t2: float
    :param storm_surge_pos: positive storm surge, see DNV-RP-C205 f:4.2 
    :type storm_surge_pos: float
    :param storm_surge_neg: negative storm surge (specify +ve value), see DNV-RP-C205 f:4.2 
    :type storm_surge_neg: float
    :param fsurge: factor applied to storm_surge values to calculate LAT/HAT, recommend fsurge=0.5|1.0, note that DNV-RP-C205 f:4.2 implies fsurge=0.5
    :type fsurge: float
    :returns: LAT, MWL, HAT
    :rtype: tuple
    
    Reference:
        DNV-RP-C205 (2021-09) f:4.2 sec:4.2.4 page:90

    Notes:
        h_l = -abs(WL)
        hl defined in DNV-ST-F101: the elevation of the local pressure point (positive upwards)
    """
    match WL_ref:
        case "LAT":
            LAT = abs(WL)
            MWL = LAT + abs(tide_t2) + abs(storm_surge_neg)*fsurge
            HAT = MWL + abs(tide_t1) + abs(storm_surge_pos)*fsurge 
        case "MSL" | "MWL":
            MWL = abs(WL)
            LAT = MWL - abs(tide_t2) - abs(storm_surge_neg)*fsurge
            HAT = MWL + abs(tide_t1) + abs(storm_surge_pos)*fsurge 
        case "HAT":
            HAT = abs(WL)
            MWL = HAT - abs(tide_t2) - abs(storm_surge_neg)*fsurge
            LAT = MWL - abs(tide_t1) - abs(storm_surge_pos)*fsurge 

    retTuple = namedtuple('StillWaterLevel', 'LAT MWL HAT')
    return retTuple(LAT, MWL, HAT)


if __name__=="__main__":
    retTuple = still_water_level(55.0, WL_ref="MWL", tide_t1=1.0, tide_t2=1.0, storm_surge_pos=0.0, storm_surge_neg=0.0, fsurge=1.0)
    print(retTuple)
    LAT, MWL, HAT = retTuple

