import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.widgets import Button, Slider
import numpy as np
import scipy.signal as scs
import scipy.fft as scfft

signal_freq = 5e3 #Hz
signal_amp = 1 #V

noise_freq = 20e3 #Hz
noise_amp = 1 #V

samp_freq = 16e3+1 #Hz

passband_drop = 3 #dB
stopband_drop = 10 #dB

passband_f = 8e3 #dB
stopband_f = 11e3 #dB

def sin_wave(freq, amp, t):
    return amp * np.sin(freq * 2 * np.pi * t)

fig, ax = plt.subplots(2)

fig.subplots_adjust(
    top=0.989,
    bottom=0.249,
    left=0.023,
    right=0.994,
    hspace=0.2,
    wspace=0.2)

ax_samp = fig.add_axes([0.05, 0.05, 0.9, 0.03])
samp_slider = Slider(
    ax=ax_samp,
    label='Samp f',
    valmin=16e3,
    valmax=1e5,
    valinit=samp_freq,
)

ax_t = fig.add_axes([0.05, 0.1, 0.9, 0.03])
t_slider = Slider(
    ax=ax_t,
    label='t',
    valmin=1e-10,
    valmax=1,
    valinit=1e-5,
)

def update(event):
    plot()

def plot():
    ax[0].clear()
    ax[1].clear()

    t = np.linspace(0, 1, int(samp_slider.val), False)

    signal = sin_wave(signal_freq, signal_amp, t)
    noise = sin_wave(noise_freq, noise_amp, t)
    in_sig = signal + noise

    #n, wn = scs.cheb1ord(samp_slider.val / (2 * passband_f), samp_slider.val / (2 * stopband_f), passband_drop, stopband_drop, fs=samp_slider.val)
    sos = scs.cheby1(30, passband_drop, passband_f, 'lp', fs=samp_slider.val, output='sos')
    filtered = scs.sosfilt(sos, in_sig)

    in_sig_fft = scfft.fft(in_sig)
    filtered_fft = scfft.fft(filtered)

    ax[0].plot(t, signal, alpha=0.5, label='signal')
    ax[0].plot(t, noise, alpha=0.3, label='noise')
    ax[0].plot(t, in_sig, alpha=0.4, label='filter in')
    ax[0].plot(t, filtered, label='filter out')

    ax[0].set_xlim(0, t_slider.val)
    ax[0].set_ylim(-2, 2)
    ax[0].legend(loc='upper right')

    ax[1].plot(in_sig_fft, alpha=0.6, label='filter in')
    ax[1].plot(filtered_fft, label='filtered_fft')
    
    ax[1].legend(loc='upper right')

samp_slider.on_changed(update)
t_slider.on_changed(update)
plot()
plt.show()