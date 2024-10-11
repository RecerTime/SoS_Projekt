import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy import signal

def transfer_functions(G, R, C, R_ratio):
    k = R*C

    H1 = signal.lti([-1],[(k/G)**2, (k/G)*R_ratio, 1])
    H2 = signal.lti([-1,0],[R_ratio*k/G, 1, R_ratio*G/k])
    H3 = signal.lti([-1,0,0],[-1, (G/k)*R_ratio, (G/k)**2])
    #H3 = signal.lti([1,0,0],[1, R_ratio, -G/k])

    return H1, H2, H3

def impulse(G, R, C, R_ratio):
    return [fs.impulse() for fs in transfer_functions(G, R, C, R_ratio)]
def bode(G, R, C, R_ratio):
    return [fs.bode() for fs in transfer_functions(G, R, C, R_ratio)]

init_G = -1
init_R = 1
init_C = 1
init_R_ratio = 1

fig, axes = plt.subplots(4, 3)

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

for i, H in enumerate(transfer_functions(init_G, init_R, init_C, init_R_ratio)):
    ax = axes[3,i]
    print(f'H{i+1} Poles: {H.poles}')
    print(f'H{i+1} Zeros: {H.zeros}')

    ax.scatter(np.real(H.poles), np.imag(H.poles), marker='x', color='red', s=25)
    ax.scatter(np.real(H.zeros), np.imag(H.zeros), marker='o', color='blue', s=25)
    ax.set_aspect('equal')

    circle = plt.Circle((0, 0), 1, fill=False, color='green', linestyle='--')
    ax.add_artist(circle)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)

    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Pole-Zero Plot')

    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

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
    valmin=-10e2,
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
        #ax.set_ylim(min(y.min(), -10e10), max(y.max(), -9e10))

    for i, H in enumerate(transfer_functions(G_slider.val, R_slider.val, C_slider.val, ratio_slider.val)):
        ax = axes[3,i]

        ax.clear()

        print(f'H{i+1} Poles: {H.poles}')
        print(f'H{i+1} Zeros: {H.zeros}')

        ax.scatter(np.real(H.poles), np.imag(H.poles), marker='x', color='red', s=25)
        ax.scatter(np.real(H.zeros), np.imag(H.zeros), marker='o', color='blue', s=25)
        ax.set_aspect('equal')

        circle = plt.Circle((0, 0), 1, fill=False, color='green', linestyle='--')
        ax.add_artist(circle)

        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)

        ax.set_xlabel('Real')
        ax.set_ylabel('Imaginary')
        ax.set_title('Pole-Zero Plot')

        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    
    fig.canvas.draw_idle()

G_slider.on_changed(update)
R_slider.on_changed(update)
C_slider.on_changed(update)
ratio_slider.on_changed(update)

plt.show()