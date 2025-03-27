"""

"""
from collections import namedtuple
#import sys

# https://stackoverflow.com/questions/30483246/how-can-i-check-if-a-module-has-been-imported
# use_numpy = False
# if use_numpy:
#if use_numpy and "numpy" in sys.modules:
#from .. import use_numpy

from ..config import use_numpy
#print(f"{__name__} {use_numpy=}")

if use_numpy:
    import numpy as np
    from numpy import sqrt, abs as _abs
    #_abs = np.abs
else:
    from math import sqrt
    _abs = abs

from ..pipe.pipe import pipe_Do_Di_WT, characteristic_WT
from ..pipe.material import characteristic_material_strength
from ..util.utils import min_nums_vectors
from ..util.named_tuple import make_return_namedtuple






# long-name function aliases
# incidental_reference_pressure = p_incid_ref
# system_test_pressure = p_system_test_ref
# local_incidental_pressure = p_incid_loc
# local_test_pressure = p_test_loc
# local_test_pressure_unity = p_test_loc_uty
# mill_test_pressure = p_mill_test
# mill_test_pressure_unity = p_mill_test_uty
# pressure_containment_resistance = p_contain_resist
# pressure_containment_resistance_unity = p_contain_resist_uty
# pressure_containment_unity = p_contain_uty


def pressure_containment_resistance(D, t, f_y, f_u=None):
    """Pressure containment resistance in accordance with DNV-ST-F101.

    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.2.3 eq:5.9 p:91 $p_{b}(t)$

    """
    if f_u is None:
        f_cb = f_y
    else:
        #f_cb = min(f_y, f_u/1.15)
        f_cb = min_nums_vectors([f_y, f_u/1.15])
    p_b = (2.0*t/(D-t) * f_cb * 2.0/sqrt(3.0))
    return p_b


def incidental_reference_pressure(p_d, γ_inc):
    r"""Calculate DNV-ST-F101 «incidental reference pressure». 

    p_inc : the incidental reference pressure at the reference elevation

    :param p_d: design pressure :math:`(p_d)`
    :type p_d: float
    :param γ_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type γ_inc: float
    :returns: p_inc incidental reference pressure :math:`(p_{inc})`
    :rtype: float

    Reference:
    DNV-ST-F101 (2021-08) 
        eq:4.3 sec:4.2.2.2 page:64 :math:`(p_{inc})`

    .. doctest:: 

        >>> p_incid_ref(100e5, 1.1)
        11000000.0
    """
    p_inc = p_d * γ_inc
    return p_inc


def local_incidental_pressure(p_inc, ρ_cont, h_l, h_ref, g=9.80665):
    r'''Calculate local incidental pressure. 

    :param p_inc: incidental reference pressure :math:`(p_inc)`
    :type p_d: float
    :param ρ_cont: density of pipeline fluid content :math:`(\rho_{cont})`
    :type ρ_cont: float
    :param h_l: elevation of the local pressure point :math:`(h_l)`
    :type h_l: float
    :param h_ref: elevation of the reference point :math:`(h_{ref})`
    :type h_ref: float
    :param g: gravitational acceleration :math:`(g)`
    :type g: float
    :returns: p_li local incidental pressure :math:`(p_{li})`
    :rtype: float

    Notes:
        γ_inc=1.0 for local system test pressure :math:`(p_{lt})`.

    .. math::
        p_{li} = p_{inc} - \rho_{cont} \cdot g \cdot \left( h_l - h_{ref} \right)

    Reference:
    DNV-ST-F101 (2021-08) 
        | sec:4.2.2.2 eq:4.1 p:64 :math:`(p_{li})`

    .. doctest::

        >>> p_incid_loc(100.e-5, 810., -125.0, 30.0, 1.1)
        1231224.9086
    '''
    p_li = p_inc - ρ_cont * g * (h_l - h_ref) 
    return p_li


def external_water_pressure(h_l, ρ_xwater, g=9.80665):
    """Water pressure, external to pipe.
    """
    p_e = _abs(h_l) * ρ_xwater * g
    return p_e


def pressure_containment_resistance_unity(p_li, p_e, p_b, γ_m, γ_SCPC):
    """Pressure containment resistance unity check.

    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.2.1 eq:5.7 p:90 

    (press_contain_resis_unity)
    """
    p_cont_res_uty =  (p_li - p_e) * γ_m * γ_SCPC / p_b  # convert eq:5.7 to a unity check
    return p_cont_res_uty


def system_test_pressure(p_d, γ_inc, α_spt):
    r"""Calculate DNV-ST-F101 «system test pressure». 

    p_t : the system test reference pressure at the reference elevation

    :param p_d: design pressure :math:`(p_d)`
    :type p_d: float
    :param γ_inc: incidental to design pressure ratio :math:`(\gamma_{inc})`
    :type γ_inc: float
    :param α_spt: system pressure test factor :math:`(\alpha_{spt})`
    :type α_spt: float
    :returns: p_t system test pressure :math:`(p_t)`
    :rtype: float

    Reference:
    DNVGL-ST-F101 (2017-12)  
        | eq:4.3 sec:4.2.2.2 p:67 :math:`p_{inc}`  
        | table:5.8 sec:5.4.2.1 p:94 :math:`\alpha_{spt}`  
        | sec:5.2.2.1 p:84  

    .. doctest::    
    
        >>> p_system_test_ref(100e5, 1.1, 1.05)
        11550000.0
    """
    p_t = p_d * γ_inc * α_spt
    return p_t


def local_test_pressure(p_t, ρ_t, h_l, h_ref, g=9.80665):
    """Calculate local test pressure.  
    
    Reference:
    DNV-ST-F101 (2021-08) 
        sec:4.2.2.2 eq:4.2 p:64 $p_{lt}$

    """
    p_lt = p_t - ρ_t * g * (h_l - h_ref)
    return p_lt


def local_test_pressure_unity(p_lt, p_li, α_spt):
    """Local test pressure unity check.

    Reference:
    DNV-ST-F101 (2021-08) 
        sec:5.4.2.1 eq:5.7 p:90 

    (local_test_press_unity)
    """
    p_lt_uty = p_li / p_lt * α_spt 
    return p_lt_uty


def mill_test_pressure(D, t_min, SMYS, SMTS, α_U=None, α_mpt=None, k=1.15):
    """Mill test pressure

    Reference:
    DNV-ST-F101 (2021-08) 
        sec:7.5.1.2 eq:7.3 p:172 $p_{mpt}$
    (mill_test_press)
    see also p93.
    """
    #p_mpt = k * (2*t_min)/(D-t_min) * min(SMYS*0.96, SMTS*0.84)
    #breakpoint()
    #print(f"{t_min=} {D=} {SMYS=} {SMYS=}")
    p_mpt = k * (2*t_min)/(D-t_min) * min_nums_vectors([SMYS*0.96, SMYS*0.84])
    #if α_U and α_mpt:  # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    if α_U is not None and α_mpt is not None:
        p_mpt = p_mpt * α_U / α_mpt
    return p_mpt


def p_contain_uty2(p_cont_res_uty, p_mpt_uty, p_lt_uty=None):
    """Pressure containment (bursting) unity check.

    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 

    (press_contain_unity)
    """
    p_cont_uty = min_nums_vectors([p_cont_res_uty, p_mpt_uty])
    if p_lt_uty is not None:
        p_cont_uty = min_nums_vectors([p_lt_uty, p_cont_uty])
    return p_cont_uty


def mill_test_pressure_unity(p_li, p_e, p_mpt):
    """Mill test pressure unity


    Reference:
    DNVGL-ST-F101 (2017-12) 
        sec:5.4.2.1 eq:5.6 p:93 
    (mill_test_press_unity)
    """
    p_mpt_uty = (p_li - p_e) / p_mpt
    return p_mpt_uty



def pressure_containment_bursting(*,
    D_o, t_nom, t_fab, t_corr, t_ero,
    SMYS, SMTS, α_U, f_ytemp=0.0, f_utemp=0.0,
    p_d, γ_inc, α_spt, α_mpt, γ_m, γ_SCPC, 
    ρ_cont_d, ρ_t, h_l, h_ref, LAT=None, ρ_xwater,
    **kwargs
):
    """DNVSTF101_pressure_containment
    """
    t_1, _ = characteristic_WT(t_nom, t_fab, t_corr, t_ero)
    f_y = characteristic_material_strength(SMYS, α_U, f_ytemp=f_ytemp)
    f_u = characteristic_material_strength(SMTS, α_U, f_ytemp=f_utemp)
    p_b = pressure_containment_resistance(D_o, t_1, f_y, f_u)

    # if LAT:
    #     min_water_depth = LAT
    # else:
    #     min_water_depth = h_l
    p_e   = external_water_pressure(h_l, ρ_xwater)
    p_inc = incidental_reference_pressure(p_d, γ_inc)
    p_li  = local_incidental_pressure(p_inc, ρ_cont_d, h_l, h_ref)
    p_cont_res_uty = pressure_containment_resistance_unity(p_li, p_e,  p_b, γ_m, γ_SCPC)

    p_t   = system_test_pressure(p_d,  γ_inc, α_spt)
    p_lt  = local_test_pressure(p_t, ρ_t, h_l, h_ref)
    p_lt_uty = local_test_pressure_unity(p_lt, p_li, α_spt)

    t_min_mill_test, _ = characteristic_WT(t_nom, t_fab, t_corr=0.0, t_ero=0.0)
    p_mpt = mill_test_pressure(D_o, t_min_mill_test, SMYS, SMTS, α_U, α_mpt, k=1.15)
    p_mpt_uty = mill_test_pressure_unity(p_li, p_e, p_mpt)

    return make_return_namedtuple("""t_1, f_y, f_u, p_b, p_e, p_inc, p_li, p_mpt, p_t, p_lt, p_lt_uty, p_mpt_uty, p_cont_res_uty""")


def pressure_containment_bursting_check(*, p_e, p_li, p_b, p_lt, p_mpt, γ_m, γ_SCPC, α_spt, α_U, α_mpt, **kwargs):
    """ Pressure containment bursting p_li check

    Reference:
        DNV-ST-F101 (2021-08) 
        sec:5.4.2.1 eq:5.7 eq:5.8 p:90
    
    """
    # DNV-ST-F101 eq:5.7
    delta_p_li  = p_li - p_e
    limit_p_b   = p_b / (γ_m * γ_SCPC)
    limit_p_lt  = p_lt / α_spt - p_e
    limit_p_mpt = p_mpt * α_U / α_mpt
    limits_p_li = (limit_p_b, limit_p_lt, limit_p_mpt)
    # if "numpy" in sys.modules:
    #     min_p_li = np.min( np.column_stack( np.broadcast_arrays(*limits_p_li) ), axis=1)
    # else:
    #     min_p_li = min(limits_p_li)
    min_p_li = min_nums_vectors(limits_p_li)
    check_p_li  = delta_p_li <= min_p_li  # DNV-ST-F101 eq:5.7
    try:
        idx_p_li = limits_p_li.index(min_p_li)
        governing_p_li = ("p_b", "p_lt", "p_mpt")[idx_p_li]
    except ValueError:
        governing_p_li = []
        for ii, val in enumerate(min_p_li):
            try:
                lim_p_b = limit_p_b[ii]
            except TypeError:
                lim_p_b = limit_p_b
            try:
                lim_p_lt = limit_p_lt[ii]
            except (TypeError, IndexError):
                lim_p_lt = limit_p_lt
            try:
                lim_p_mpt = limit_p_mpt[ii]
            except TypeError:
                lim_p_mpt = limit_p_mpt
            idx_p_lt = [lim_p_b, lim_p_lt, lim_p_mpt].index(val)
            governing_p_li.append(("p_b", "p_lt", "p_mpt")[idx_p_lt])

    # DNV-ST-F101 eq:5.8
    delta_p_lt  = p_lt - p_e
    limits_p_lt = (limit_p_b, p_mpt)
    #min_p_lt = minimum(limits_p_lt)
    # if "numpy" in sys.modules:
    #     min_p_lt = np.min( np.column_stack( np.broadcast_arrays(*limits_p_lt) ), axis=1)
    # else:
    #     min_p_lt = min(limits_p_lt)
    min_p_lt = min_nums_vectors(limits_p_lt)
    # print(f"{min_p_lt=}")
    # print(f"{limits_p_lt=}")
    check_p_lt  = delta_p_lt <= min_p_lt  # DNV-ST-F101 eq:5.8
    try:
        idx_p_lt = limits_p_lt.index(min_p_lt)
        governing_p_lt = ("p_b", "p_mpt")[idx_p_lt]
    except ValueError:
        governing_p_lt = []
        for ii, val in enumerate(min_p_lt):
            try:
                lim_p_b = limit_p_b[ii]
            except TypeError:
                lim_p_b = limit_p_b
            try:
                lim_p_mpt = p_mpt[ii]
            except TypeError:
                lim_p_mpt = p_mpt
            idx_p_lt = [lim_p_b, lim_p_mpt].index(val)
            governing_p_lt.append(("p_b", "p_mpt")[idx_p_lt])
        #governing_p_lt = [limits_p_lt.index(x) for x in min_p_lt]

    return make_return_namedtuple("""delta_p_li, limit_p_b, limit_p_lt, limit_p_mpt, check_p_li, governing_p_li, delta_p_lt, check_p_lt, governing_p_lt""")

    # retTuple = namedtuple('DNVSTF101PressureContainment', 't_1, f_y, f_u, p_inc, p_li')
    # return retTuple(t_1, f_y, f_u, p_inc, p_li)

    # return {
    #     "t_1": t_1,
    #     "f_y": f_y,
    #     "f_u": f_u,
    #     "p_inc": p_inc,
    #     "p_li": p_li,
    # }


if __name__ == "__main__":
    from environment import still_water_level
    # use_numpy = use_numpy
    # if use_numpy:
    #     from numpy import array
    MSL = 55.0  # mean sea level/water depth 
    tide = 1.0
    LAT, MWL, HAT = still_water_level(MSL, WL_ref="MSL", tide_t1=tide, tide_t2=tide, storm_surge_pos=0.0, storm_surge_neg=0.0, fsurge=1.0)
    h_l = -MSL
    basecase = {
        "name" : "basecase",
        "comment": "Basecase: 24\" 50bar-150bar ",
        "NPS":  24,                       #"24\"", 
        "D_o": 24 * 25.4 * 1.e-3,  # (m) pipe internal diameter
        "p_d": 50.e5,  #np.array([50.e5, 150.e5]),  # (Pa) design pressure at reference elevation Z_ref
        "t_nom": 0.0159,  # (m) pipe wall thickness
        "t_corr": 0.0, # (m) corrosion allowance
        "t_ero": 0.0, # (m) erosion allowance
        "t_fab": 0.001, # (m) thickness negative fabrication tolerance

        "SMYS": 450.e6, # (Pa) pipe steel SMYS
        "f_ytemp": 35.e6, # (Pa) steel yield strength temperature de-rating
        "SMTS": 535.e6, # (Pa) pipe steel SMTS
        "f_utemp": 0.e6, # (Pa) steel ultimate strength temperature de-rating
        "α_U": 0.96, # material strength factor
        "α_U_spt": 1.0, # material strength factor for system pressure test cacls
        "γ_m": 1.15,  # material resistance factor
        "α_fab": 0.93, 
        "E": 207.0*10**9,
        "ν": 0.3,

        "γ_inc": 1.10 , # incidental to design pressure ratio
        "ρ_cont_d": 20., # (kg/m3) density of pipeline design fluid content
        "ρ_t": 1025. ,  # test fluid density

        "ρ_xwater": 1025., # (kg/m3) density of seawater

        "α_spt": 1.05,  # DNVGL-ST-F101 (2017-12) p94gamma
        "α_mpt": 1.088,  # p94
        "α_spt": 1.05,  # p94
        "γ_SCPC": 1.138,  # safety class resistance factor for pressure containment
        "γ_SCPC_pt": 1.046,  # safety class resistance factor for hydrotest

        "mill_test_k": 1.0,   # k parameter used for calculating mill test pressure
        "t_corr_mill_test": 0.0,

        "h_ref": 0.0 , # (m) reference elevation for pressure (MSL=0m)
        "h_l": h_l,
        "LAT": LAT,
    }
    use_numpy = True
    if use_numpy:
        import numpy as np
        basecase["p_d"] = np.array([50.e5, 150.e5])
    pc = pressure_containment_bursting(**basecase)
    check = pressure_containment_bursting_check(**basecase,**pc._asdict())
