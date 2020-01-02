

#import inspect
import logging

#import numpy as np

# __all__ = [
#     "pipe_basic_dims",
#     "pipe_weight",
# ]

logger = logging.getLogger(__name__)



def Do_from_pipe_Di(Di, WT):
    """Calculate pipe outer diameter (Do), given a reference inner diameter (Di)
    and a wall thickness dimension (WT). WT can be a list or tuple of wall
    thicknesses for compound section pipes.

    .. math::
        D_o = D_i + 2 * WT

    :param Di: pipe inner diameter :math:`(D_i)`
    :type p_d: float
    :param WT: pipe wall thickness, or list/tuple of wall thicknesses
    :type WT: float, list, tuple
    :returns: pipe outer diameter :math:`(D_o)`
    :rtype: float

    .. doctest:: 

    >>> Do_from_pipe_Di(0.660, 0.045)
    0.75
    >>> Do_from_pipe_Di(203.2, [3, 45, 5])
    309.2
    """
    if isinstance(WT, (list, tuple)):
        _wt_list = WT
    else:
        _wt_list = [WT]
    Do = Di
    for _wt in _wt_list:
        Do = Do + 2 * _wt
    return Do


def Di_from_pipe_Do(Do, WT):
    """Calculate pipe inner diameter (Di), given a reference outer diameter (Do)
    and a wall thickness dimension (WT). WT can be a list or tuple of wall
    thicknesses for compound section pipes.

    .. math::
        D_i = D_o - 2 * WT

    :param Do: pipe outer diameter :math:`(D_o)`
    :type p_d: float
    :param WT: pipe wall thickness, or list/tuple of wall thicknesses
    :type WT: float, list, tuple
    :returns: pipe inner diameter :math:`(D_i)`
    :rtype: float

    .. doctest:: 

    >>> Di_from_pipe_Do(203.2, 3.0)
    197.2
    """
    if isinstance(WT, (list, tuple)):
        _wt_list = WT
    else:
        _wt_list = [WT]
    Di = Do
    for _wt in _wt_list:
        Di = Di - 2 * _wt
    return Di


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)





