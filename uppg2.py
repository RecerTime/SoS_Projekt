import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.widgets import Button, Slider
import numpy as np
import scipy.signal as scs
import scipy.fft as fft

signal_freq = 5e3 #Hz
signal_amp = 1 #V

noise_freq = 15e3 #Hz
noise_amp = 1 #V

samp_freq = 24e3 #Hz

passband_drop = 3 #dB
stopband_drop = 60 #dB

passband_f = 8.5e3 #dB
stopband_f = 10e3 #dB

def sin_wave(freq, amp, t):
    return amp * np.sin(freq * 2 * np.pi * t)

fig, ax = plt.subplots(3)

fig.subplots_adjust(
    top=0.989,
    bottom=0.249,
    left=0.023,
    right=0.994,
    hspace=0.2,
    wspace=0.2)

ax_pb_f = fig.add_axes([0.05, 0.05, 0.9, 0.03])
pb_f_slider = Slider(
    ax=ax_pb_f,
    label='pb f',
    valmin=8e3,
    valmax=15e3,
    valinit=8150,
)
ax_sb_f = fig.add_axes([0.05, 0.1, 0.9, 0.03])
sb_f_slider = Slider(
    ax=ax_sb_f,
    label='sb f',
    valmin=8e3,
    valmax=20e3,
    valinit=11e3,
)
ax_pb_d = fig.add_axes([0.05, 0.15, 0.9, 0.03])
pb_d_slider = Slider(
    ax=ax_pb_d,
    label='pb d',
    valmin=0,
    valmax=15,
    valinit=1,
)
ax_sb_d = fig.add_axes([0.05, 0.2, 0.9, 0.03])
sb_d_slider = Slider(
    ax=ax_sb_d,
    label='sb d',
    valmin=0,
    valmax=100,
    valinit=71.5,
)
def update(event):
    plot()

def plot():
    ax[0].clear()
    ax[1].clear()

    t = np.linspace(0, 1, int(samp_freq*10), False)

    signal = sin_wave(signal_freq, signal_amp, t)
    noise = sin_wave(noise_freq, noise_amp, t)
    in_sig = signal + noise

    n, wn = scs.cheb1ord(2*np.pi*pb_f_slider.val, 2*np.pi*sb_f_slider.val, pb_d_slider.val, sb_d_slider.val, analog=True)
    ba = scs.cheby1(n, pb_d_slider.val, wn, 'lp', analog=True)
    tout, yout, xout = scs.lsim(ba, in_sig[10 - 1::10], t[10 - 1::10])

    ax[0].plot(t, signal, alpha=0.5, label='signal')
    ax[0].plot(t, noise, alpha=0.3, label='noise')
    ax[0].plot(t, in_sig, alpha=0.4, label='filter in')
    ax[0].plot(tout, yout, label=f'filter out n={n}')

    ax[0].set_xlim(0, 5e-3)
    ax[0].set_ylim(-2, 2)
    ax[0].legend(loc='upper right')

    b, a = ba
    w, h = scs.freqs(b, a)
    ax[1].semilogx(w/(2*np.pi), 20 * np.log10(abs(h)))
    ax[1].set_xlim(5e3, 12e3)
    ax[1].set_ylim(20*np.log10(0.5/2**11), 3)
    ax[1].grid(which='both', axis='both')
    ax[1].axvline(11e3, color='green') # cutoff frequency
    ax[1].axvline(8e3, color='yellow') # cutoff frequency
    ax[1].axhline(-3, color='yellow') # rp

    fft_result = fft.fft(signal, norm='forward')
    fft_freq = fft.fftfreq(len(t), 1/(samp_freq*10))
    ax[2].plot(fft_freq[:len(fft_freq)//2]/1e3, np.abs(fft_result[:len(fft_result)//2]), label=f'signal ({np.abs(fft_freq[np.argmax(fft_result)])} Hz)')

    fft_result = fft.fft(yout, norm='forward')
    fft_freq = fft.fftfreq(len(tout), 1/(samp_freq))
    ax[2].plot(fft_freq[:len(fft_freq)//2]/1e3, np.abs(fft_result[:len(fft_result)//2]), label=f'filter out ({np.abs(fft_freq[np.argmax(fft_result)])} Hz)')

    ax[2].set_xlim(0, 24)
    ax[2].set_ylim(0, 0.8)
    ax[2].legend(loc='upper right')

pb_f_slider.on_changed(update)
sb_f_slider.on_changed(update)
pb_d_slider.on_changed(update)
sb_d_slider.on_changed(update)

plot()
plt.show()