import numpy as np
import scipy.signal as scs
from matplotlib import pyplot as plt

wp = np.linspace(1e3, 15e3, 30)
ws = np.linspace(5e3, 30e3, 30)
gpass = np.logspace(1e-4, 10, 30)
gstop = np.linspace(50, 200, 30)
rp = np.logspace(1e-4, 10, 30)

#wp, ws, gpass, gstop = 8150, 11e3, 1, 71.5
#wp, ws, gpass, gstop = 4368.421052631579, 16000.0, 15.0, 100.0

high_lim = 20*np.log10(0.5/2**11)
high_lim_f = 11e3

low_lim = -3
low_lim_f = 8e3

def filter_test(wp, ws, gpass, gstop, rp):
    n, wn = scs.cheb1ord(2*np.pi*wp, 2*np.pi*ws, gpass, gstop, analog=True)
    b, a = scs.cheby1(n, rp, wn, 'lp', analog=True)
    w, h = scs.freqs(b, a)

    f = w/(2*np.pi)
    db = 20 * np.log10(abs(h))

    #plt.semilogx(f, db)

    #print(db[np.where(f >= high_lim_f)[0][0]-1])
    #print(f[np.where(f >= high_lim_f)[0][0]-1])
    #print(db[np.where(f <= low_lim_f)[0]])
    #print(f[np.where(f <= low_lim_f)[0]])

    if db[np.where(f >= high_lim_f)[0][0]-1] >= high_lim:
        #print(f'Highlim error: {f[np.where(f >= high_lim_f)[0][0]-1]} Hz at {db[np.where(f >= high_lim_f)[0][0]-1]} dB')
        return False
    
    if len(np.where(db[np.where(f <= low_lim_f)[0]] <= low_lim)[0]) > 0:
        #print(f'Lowlim error')
        return False
    
    return n, [wp, ws, gpass, gstop, rp]

def loop(wp, ws, gpass, gstop, rp):
    res_dict = {}

    for w_p in wp:
        print(f'wp: {w_p}')
        if len(res_dict.keys()) > 0:
            lowest_n = min(res_dict.keys())
            print(f'{lowest_n}: {res_dict[lowest_n]}')
        for w_s in ws:
            for g_pass in gpass:
                for g_stop in gstop:
                    for r_p in rp:
                        try:
                            res = filter_test(w_p, w_s, g_pass, g_stop, r_p)
                            if res != False:
                                n, lst = res
                                res_dict[n] = lst
                        except:
                            break
    return res_dict

#print(filter_test(wp, ws, gpass, gstop))

if __name__ == '__main__':
    #print(high_lim)
    res_dict = loop(wp, ws, gpass, gstop, rp)
    #lowest_n = min(res_dict.keys())
    #print(f'{lowest_n}: {res_dict[lowest_n]}')
    print(res_dict)
    #plt.show()
    