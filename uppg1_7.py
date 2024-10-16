import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy import signal

n = 10e3
f = 50
samp = 10e3

kG = 1/(300*2*np.pi)
R_ratio = 1/np.sqrt(10)

H = signal.lti([-1],[(kG)**2, (kG)*R_ratio, 1])

def fourier_series(t, f, n_terms):
    n_terms = int(n_terms)
    result = 0
    for n in range(1, n_terms + 1):
        result += 2*(np.sin(n * f * t) / n)
    return result

# Generate t values
t = np.linspace(0, 2*np.pi, int(samp))
fs = fourier_series(t, f, n)

tout, yout, xout = signal.lsim(system=H, U=fs, T=t)
w, mag, phase = H.bode()

# Create the plot
fig, ax = plt.subplots(2)
ax[0].plot(t, fs, label='In Signal')
ax[0].plot(tout, yout, label='Filtered Signal')

ax[0].set_ylim(-5, 4)
ax[0].legend(loc='upper right')
ax[0].grid(which='both', axis='both')


ax[1].semilogx(w/(2*np.pi), mag, label=f'{np.max(mag)} dB')

twin1 = ax[1].twinx()
twin1.semilogx(w/(2*np.pi), phase, color='orange', label='Phase (deg)')

twin1.legend(loc='upper right')

ax[1].axvline(300, color='green')
ax[1].axhline(10, color='green')
ax[1].legend(loc='lower left')
ax[1].grid(which='both', axis='both')


plt.show()