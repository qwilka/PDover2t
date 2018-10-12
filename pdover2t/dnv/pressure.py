



# parameters
# P_h  mill hydrostatic test pressure, page 66

# grav_acc [g]  gravity acceleration
# dens_cont [\rho_cont]

# http://www.sphinx-doc.org/en/master/ext/math.html

def local_incidental_pressure(p_inc: float, dens_cont: float,
        h_l: float, h_ref: float, grav_acc: float = 9.81) -> float:
    r'''Calculate local incidental pressure.
    DNVGL-ST-F101 (2017) sec:4.2.2.2 eq:4.1 page:67
    
    .. math::
        p_{li} = p_{inc} - \rho_{cont} \cdot g \cdot \left( h_l - h_{ref} \right)

    :param p_inc: $p_{inc}$ incidental reference pressure at ref elevation       
    :param dens_cont: $\rho_{cont}$ density of pipeline contents
    :param h_l: $h_l$ elevation of the local pressure point (positive upwards)
    :param h_ref: $h_{ref}$ elevation of the reference point
    :param grav_acc: $g$ gravitational acceleration
    :returns: p_li: $h_{ref}$ local incidental pressure
    
    Examples:    
    >>> local_incidental_pressure(100.e-5, 1025, -125, 30)
    1558563.751
    '''
    p_li = p_inc - dens_cont * grav_acc * (h_l - h_ref)
    return p_li



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)