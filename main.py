import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.widgets import Button, Slider
import numpy as np
from scipy import signal

def transfer_functions(G, R, C, R_ratio):
    k = R*C

    H1 = signal.lti([1],[-(k/G)**2, (k/G)*R_ratio, 1])
    H2 = signal.lti([1,0],[-R_ratio*k/G, 1, R_ratio*G/k])
    H3 = signal.lti([1,0,0],[-1, (G/k)*R_ratio, (G/k)**2])

    return H1, H2, H3


def poles(G, R, C, R_ratio):
    return [fs.poles() for fs in transfer_functions(G, R, C, R_ratio)]
def zeros(G, R, C, R_ratio):
    return [fs.zeros() for fs in transfer_functions(G, R, C, R_ratio)]
def impulse(G, R, C, R_ratio):
    return [fs.impulse() for fs in transfer_functions(G, R, C, R_ratio)]
def bode(G, R, C, R_ratio):
    return [fs.bode() for fs in transfer_functions(G, R, C, R_ratio)]

init_G = 1
init_R = 1
init_C = 1
init_R_ratio = 1

fig, axes = plt.subplots(3, 3)

bode_mag_lines = []
bode_phase_lines = []

for i, H in enumerate(bode(init_G, init_R, init_C, init_R_ratio)):
    w, mag, phase = H
    ax = axes[0,i]
    line, = ax.semilogx(w, mag)
    ax.grid()
    ax.set_title(f'H{i+1}(s) Bode Mag')
    ax.set_xlabel("f (Hz)")
    ax.set_ylabel("Mag (dB)")
    bode_mag_lines.append((line, ax))

    ax = axes[1,i]
    line, = ax.semilogx(w, phase)
    ax.grid()
    ax.set_title(f'H{i+1}(s) Bode Phase')
    ax.set_xlabel("f (Hz)")
    ax.set_ylabel("Phase (deg)")
    bode_phase_lines.append((line, ax))

impulse_lines = []
for i, H in enumerate(impulse(init_G, init_R, init_C, init_R_ratio)):
    t, y = H
    ax = axes[2,i]
    line, = ax.plot(t, y)
    ax.grid()
    ax.set_title(f'H{i+1}(s) Impulse')
    impulse_lines.append((line, ax))

fig.subplots_adjust(
    top=0.975,
    bottom=0.25,
    left=0.035,
    right=0.99,
    hspace=0.4,
    wspace=0.2)

ax_G = fig.add_axes([0.05, 0.05, 0.9, 0.03])
G_slider = Slider(
    ax=ax_G,
    label='G',
    valmin=10e-2,
    valmax=10e2,
    valinit=init_G,
)
ax_R = fig.add_axes([0.05, 0.1, 0.9, 0.03])
R_slider = Slider(
    ax=ax_R,
    label='R',
    valmin=10e-2,
    valmax=10e2,
    valinit=init_R,
)
ax_C = fig.add_axes([0.05, 0.15, 0.9, 0.03])
C_slider = Slider(
    ax=ax_C,
    label='C',
    valmin=10e-2,
    valmax=10e2,
    valinit=init_C,
)
ax_Ratio = fig.add_axes([0.05, 0.2, 0.9, 0.03])
ratio_slider = Slider(
    ax=ax_Ratio,
    label='R2/R3',
    valmin=10e-2,
    valmax=10e2,
    valinit=init_R_ratio,
)

def update(event):
    for i, H in enumerate(bode(G_slider.val, R_slider.val, C_slider.val, ratio_slider.val)):
        w, mag, phase = H
        line, ax = bode_mag_lines[i]
        line.set_data(w, mag)
        ax.set_xlim(np.min(w), np.max(w)+1)
        ax.set_ylim(np.min(mag)-1, np.max(mag)+1)

        line, ax = bode_phase_lines[i]
        line.set_data(w, phase)
        ax.set_xlim(np.min(w), np.max(w)+1)
        ax.set_ylim(np.min(phase)-1, np.max(phase)+1)

    for i, H in enumerate(impulse(G_slider.val, R_slider.val, C_slider.val, ratio_slider.val)):
        t, y = H
        line, ax = impulse_lines[i]
        line.set_data(t, y)
        ax.set_xlim(np.min(t)-1, np.max(t)+1)
        ax.set_ylim(min(y.min(), -10e10), max(y.max(), -9e10))

    fig.canvas.draw_idle()

G_slider.on_changed(update)
R_slider.on_changed(update)
C_slider.on_changed(update)
ratio_slider.on_changed(update)

plt.show()