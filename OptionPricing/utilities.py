# Import Python packages
import numpy as np  # Load Numpy package and call it 'np'
from scipy.stats import norm
from scipy.optimize import fsolve

def bsVanilla(K,T,pc,S0,r,c,v):
    vsqrt = v * np.sqrt(T + 1e-60)
    d1 = (np.log(S0/K) + (r-c)*T)/vsqrt + vsqrt/2
    d2 = d1 - vsqrt
    dfd = np.exp(-r*T)
    dff = np.exp(-c*T)
    Nd1 = norm.cdf(pc*d1)
    Nd2 = norm.cdf(pc*d2)
    price = pc * (dff*S0*Nd1 - dfd*K*Nd2)
    return price

def bsDigital(K,T,pc,S0,r,c,v):
    vsqrt = v * np.sqrt(T + 1e-60)
    d1 = (np.log(S0/K) + (r-c)*T)/vsqrt + vsqrt/2
    d2 = d1 - vsqrt
    dfd = np.exp(-r*T)
    Nd2 = norm.cdf(pc*d2)
    price = dfd * Nd2
    return price

def bsimpvol(K,T,pc,S0,r,c,price):
    def bsprice(v,K,T,pc,S0,r,c,price):
        vsqrt = v * np.sqrt(T + 1e-60)
        d1 = (np.log(S0/K) + (r-c)*T)/vsqrt + vsqrt/2
        d2 = d1 - vsqrt
        dfd = np.exp(-r*T)
        dff = np.exp(-c*T)
        Nd1 = norm.cdf(pc*d1)
        Nd2 = norm.cdf(pc*d2)
        y = pc * (dff*S0*Nd1 - dfd*K*Nd2)
        return y - price
        
    x = np.zeros(K.shape)
    for i in range(0,K.size):
        x[i] = fsolve(bsprice, 0.1, (K[i],T,pc,S0,r,c,price[i]))
    
    return x

def sabrVolatility(S,K,r,c,alpha,beta,rho,nu,T):
    f = S * np.exp((r-c)*T)
    z = nu/alpha * (f*K)**(0.5-beta/2.0) * np.log(f/K) + 1e-20
    chi = np.log( (np.sqrt(1 - 2.0*rho*z + z**2) + z - rho)/(1-rho)) + 1e-20
    vol = ( alpha * (f*K)**(beta/2.0-0.5) 
        /(1+ (1-beta)**2 / 24 * np.log(f/K)**2 + (1.0-beta)**4/1920*np.log(f/K)**4)
        *z/chi
        *(1 + ((1-beta)**2 / 24 *alpha**2 *(f*K)**(beta-1.0) + rho*beta*nu*alpha/4*(f*K)**(beta/2.0 - 0.5) + (2-3*rho**2)/24*nu**2)*T) )
    return vol

def sabr2LocalVol(S,K,r,c,alpha,beta,rho,nu,T):
    sig = sabrVolatility(S,K,r,c,alpha,beta,rho,nu,T)
    dk = 0.001
    sig_Kup = sabrVolatility(S,K*(1+dk),r,c,alpha,beta,rho,nu,T)
    sig_Kdn = sabrVolatility(S,K*(1-dk),r,c,alpha,beta,rho,nu,T)
    dsig_dK = (sig_Kup - sig_Kdn)/(2*dk*K)
    d2sig_dK2 = (sig_Kup -2*sig + sig_Kdn)/(dk*K)**2
    dT = 0.001
    sig_Tup = sabrVolatility(S,K,r,c,alpha,beta,rho,nu,T*(1+dT))
    sig_Tdn = sabrVolatility(S,K,r,c,alpha,beta,rho,nu,T*(1-dT))
    dsig_dT = (sig_Tup - sig_Tdn)/(2*dT*(T + 1e-20))
    
    vsqrt = sig*np.sqrt(T + 1e-20)
    d1 = (np.log(S/K) + (r-c)*T)/vsqrt + vsqrt/2
    d2 = d1 - vsqrt
    vol2 = (sig**2 + 2*T*sig*(dsig_dT + (r-c)*K*dsig_dK)) \
        / (1+ 2*np.sqrt(T)*d1*K*dsig_dK + T*K**2 * (d1*d2*dsig_dK**2 + sig*d2sig_dK2))
    vol = np.sqrt(vol2)
    return vol
    
    
    vol = 0
    return vol
    