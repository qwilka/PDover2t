# engineering/subsea_pipeline/mechanics/freespans_VIV
# 2011_thesis_VIV_506763.pdf
# p 16
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

def wave_velocity(H, T, depth, z, grav_acc=9.81):   
    omega = 2*np.pi/T
    print("omega=", omega)
    k = omega**2/grav_acc
    print("k=", k)
    _lambda = 2*np.pi/k
    print("lambda=", _lambda)
    u_w =  np.pi*H/T * np.cosh(k*(z+depth))/np.sinh(k*depth)
    return u_w

def phillips_constant(H_s, omega_p, gamma, grav_acc=9.81):
    phillips = 5/16 * H_s**2 * omega_p**4 / grav_acc**2 *(1-0.287*np.log(gamma))
    return phillips

def JONSWAP(omega, H_s, T_p, grav_acc=9.81, gamma=None):
    omega_p = 2*np.pi/T_p
    sigma = np.full(omega.shape, 0.09)
    sigma[omega<=omega_p] = 0.07
    phi = T_p / np.sqrt(H_s)
    if not gamma:
        if phi<=3.6:
            gamma = 5
        elif 3.6<phi<5:
            gamma = np.exp(5.75-1.15*phi)
        else:
            gamma = 1
    phillips = ( 5/16 * H_s**2 * 
                omega_p**4 / grav_acc**2 * 
                (1-0.287*np.log(gamma)) )
    S_etaeta = ( phillips * grav_acc**2 * omega**-5 * 
                np.exp(-5/4 * (omega/omega_p)**-4 ) *
                gamma**np.exp(-0.5*((omega-omega_p)/(sigma*omega_p))**2 ) )
    return S_etaeta

def find_wavelen_func(_lambda, T, depth, grav_acc=9.81):
    # DNVGL-RP-C205_2017 3.2.2.3 page 46 not working...
    #return T**2 - (grav_acc/(2*np.pi*_lambda))*np.tanh(2*np.pi*depth/_lambda)
    # DNVGL-RP-C205_2017 page 61 / lwt_new_2000_Part_A.pdf page 31
    return T**2 - 2*np.pi*_lambda/grav_acc / np.tanh(2*np.pi*depth/_lambda)

def calc_wave_length(T, depth, grav_acc=9.81):
    if isinstance(T, np.ndarray):
        wavelen = np.zeros_like(T)
        for ii, _T in enumerate(T):
            try:
                wavelen[ii] = scipy.optimize.bisect(find_wavelen_func,  
                                        0.1, 1000, args=(_T, depth))
            except ValueError as err:
                wavelen[ii] = np.NaN
    else:
        wavelen = scipy.optimize.bisect(find_wavelen_func, 0.1, 1000, 
                                    args=(T, depth))
    return wavelen

def wave_no_func(k, omg, depth, grav_acc=9.81):
    return omg**2/grav_acc - k*np.tanh(k*depth)

def wave_number(omega, depth, grav_acc=9.81):
    # DNVGL-RP-F109_2017-05 page 17 eq. 3.10
    # cannot solve this for k, 
    # dependency between omega and k seems to be the problem..
    k = np.zeros_like(omega)
    #T = 2*np.pi/omega
    for ii, _omg in enumerate(omega):
        # wavelen = calc_wave_length(T[ii], depth)
        # k[ii] = 2*np.pi/wavelen
        k[ii] = scipy.optimize.bisect(wave_no_func, 0, 100, args=(_omg, depth))
    return k

def JONSWAP_transformed(omega, S_etaeta, depth, D=0, e=0, grav_acc=9.81):
    #k = wave_number(omega, depth)
    T = 2*np.pi/omega 
    wavelen = calc_wave_length(T, depth)
    k = 2*np.pi/wavelen
    #G = omega*np.cosh(k*(D+e))/np.sinh(k*depth)
    G = omega*np.cosh(k*(D+e))/np.sinh(k*depth)
    S_uu = G**2 * S_etaeta
    return S_uu, G


if __name__=="__main__":
    if False:
        T = 10 # wave period 10 s
        H = 2 # wave height 2m
        depth = 100
        z = -100
        print(wave_velocity(H, T, depth, z)) 
    if False:
        omega = np.linspace(0.01, 2.0, 100)
        S_etaeta = JONSWAP(omega, H_s=10, T_p=15)
        print(S_etaeta)
        plt.plot(omega, S_etaeta)
    if False:
        # DNVGL-RP-N103 (2017) Figure 2-2 (page 22)
        gam1 = JONSWAP(omega, H_s=4, T_p=8, gamma=1)
        gam2 = JONSWAP(omega, H_s=4, T_p=8, gamma=2)
        gam5 = JONSWAP(omega, H_s=4, T_p=8, gamma=5)
        plt.plot(omega, gam1, 'r', omega, gam2, 'g', omega, gam5, 'b')
        plt.show()
    if False:
        omega = np.linspace(0.01, 2.0, 100)
        k = wave_number(omega, depth=100)
        print(k)
        plt.plot(omega, k)
        plt.show()
    if False:
        k1 = 2*np.pi/100
        k2 = 2*np.pi/1
        k = np.linspace(k1, k2, 10)
        _func1 = wave_no_func(k, omg=0.1, depth=90)
        _func2 = wave_no_func(k, omg=0.5, depth=90)
        _func3 = wave_no_func(k, omg=1.0, depth=90)
        _func4 = wave_no_func(k, omg=2.0, depth=90)
        plt.plot(k, _func1, '-r', label='omg=0.1')
        plt.plot(k, _func2, '-g', label='omg=0.5')
        plt.plot(k, _func3, '-b', label='omg=1.0')
        plt.plot(k, _func4, '-c', label='omg=2.0')
        plt.legend(loc='best')
        plt.show()
    if False:
        # lwt_new_2000_Part_A.pdf, page 19, exercise 5.2
        T=10; depth=2000
        wavelen = calc_wave_length(T, depth)
        print(f"wave length={wavelen:.3f}; T={T}, depth={depth}")
        T=10; depth=1
        wavelen = calc_wave_length(T, depth)
        print(f"wave length={wavelen:.3f}; T={T}, depth={depth}")
        T=15; depth=90
        wavelen = calc_wave_length(T, depth)
        print(f"wave length={wavelen:.3f}; T={T}, depth={depth}")
        wavelen = np.linspace(0.1, 500, 40)
        # _func1 = find_wavelen_func(wavelen, T=10, depth=2000)
        # _func2 = find_wavelen_func(wavelen, T=10, depth=1)
        _func3 = find_wavelen_func(wavelen, T=15, depth=90)
        plt.plot(wavelen, _func3, '-g', label='T=10, depth=1')
        plt.legend(loc='best')
        plt.show()
    if False:
        T_p=15; depth=90; H_s=10
        wavelen = calc_wave_length(T_p, depth)
        print(f"wave length={wavelen:.3f}; T={T_p}, depth={depth}")
        omega = np.linspace(0.1, 2.0, 100)
        S_etaeta = JONSWAP(omega, H_s=H_s, T_p=T_p)
        S_uu, G = JONSWAP_transformed(omega, S_etaeta, D=0, depth=depth)
        #print(S_etaeta)
        plt.plot(omega, S_etaeta, omega, S_uu, omega, G)
        #plt.plot(omega, S_uu)
        plt.show()
    if True:
        T_p=15; depth=50; H_s=10
        wavelen = calc_wave_length(T_p, depth)
        print(f"wave length={wavelen:.3f}; T={T_p}, depth={depth}")
        omega = np.linspace(0.1, 2.0, 100)
        S_etaeta = JONSWAP(omega, H_s=H_s, T_p=T_p)
        S_uu, G = JONSWAP_transformed(omega, S_etaeta, D=0, depth=depth)
        #print(S_etaeta)
        plt.plot(omega, S_etaeta, omega, S_uu, omega, G)
        #plt.plot(omega, S_uu)
        plt.show()