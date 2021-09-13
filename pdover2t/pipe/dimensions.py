import math

def pipe_Do_Di_WT(*, Do=None, Di=None, WT=None):
    """Calculate pipe wall thickness / outer diameter / inner diameter.
    """
    if Do is not None and Di is not None and WT is not None:
        assert Do==Di+2*WT, f"pipe_D_WT: inconsistent pipe dimensions Do={Do} Di={Di} WT={WT}."
    elif WT is None:
        WT = (Do - Di) / 2
    elif Di is None:
        Di = Do - 2 * WT
    elif Do is None:
        Do = Di + 2 * WT
    else:
        return False
    return Do, Di, WT


def pipe_Do(Di, WT):
    """Calculate pipe outer diameter, given the pipe inner diamater and wall thickness.
    """
    Do = Di + 2 * WT
    return Do


def pipe_Di(Do, WT):
    """Calculate pipe inner diameter, given the pipe outer diamater and wall thickness.
    """
    Di = Do - 2 * WT
    return Di

def pipe_WT(Do, Di):
    """Calculate pipe wall thickness, given the pipe outer diamater and inner diameter.
    """
    WT = (Do - Di) / 2
    return WT



def pipe_CSA(Do, Di):
    """Calculate pipe cross sectional area, given the pipe outer diamater and inner diameter.

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :returns: pipe cross sectional area
    :rtype: float

    .. math::
        A =  \frac{\pi}{4} \left( D_o^2 - D_i^2   \right)  

    .. doctest::

        >>> pipe_CSA(0.6656, 0.6172)
        0.19522098526377624
    """
    CSA = math.pi * (Do*Do - Di*Di)
    return CSA
