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

fig, ax = plt.subplots(3, 3)

bode_mag_lines = []
bode_phase_lines = []
for i, H in enumerate(bode(init_G, init_R, init_C, init_R_ratio)):
    w, mag, phase = H
    line, = ax[0,i].plot(w, mag)
    ax[0,i].grid()
    ax[0,i].set_title(f'H{i+1}(s) Bode Mag')
    bode_mag_lines.append(line)

    line, = ax[1,i].plot(w, phase)
    ax[1,i].grid()
    ax[1,i].set_title(f'H{i+1}(s) Bode Phase')
    bode_phase_lines.append(line)

impulse_lines = []
for i, H in enumerate(impulse(init_G, init_R, init_C, init_R_ratio)):
    t, y = H
    line, = ax[2,i].plot(t, y)
    ax[2,i].grid()
    ax[2,i].set_title(f'H{i+1}(s) Impulse')
    impulse_lines.append(line)

fig.subplots_adjust(
    top=0.975,
    bottom=0.25,
    left=0.02,
    right=0.99,
    hspace=0.2,
    wspace=0.2)

ax_G = fig.add_axes([0.05, 0.05, 0.9, 0.03])
G_slider = Slider(
    ax=ax_G,
    label='G',
    valmin=1,
    valmax=10e7,
    valinit=init_G,
)
ax_R = fig.add_axes([0.05, 0.1, 0.9, 0.03])
R_slider = Slider(
    ax=ax_R,
    label='R',
    valmin=1,
    valmax=10e7,
    valinit=init_R,
)
ax_C = fig.add_axes([0.05, 0.15, 0.9, 0.03])
C_slider = Slider(
    ax=ax_C,
    label='C',
    valmin=10e-11,
    valmax=10e-5,
    valinit=init_C,
)
ax_Ratio = fig.add_axes([0.05, 0.2, 0.9, 0.03])
ratio_slider = Slider(
    ax=ax_Ratio,
    label='R2/R3',
    valmin=10e-7,
    valmax=10e7,
    valinit=init_R_ratio,
)

def update(event):
    for i, H in enumerate(bode(G_slider.val, R_slider.val, C_slider.val, ratio_slider.val)):
        w, mag, phase = H
        print(f'Bode H({i+1}): {H}')
        bode_mag_lines[i].set_data(w, mag)
        bode_phase_lines[i].set_data(w, phase)

    for i, H in enumerate(impulse(G_slider.val, R_slider.val, C_slider.val, ratio_slider.val)):
        print(f'Impulse H({i+1}): {H}')
        t, y = H
        impulse_lines[i].set_data(t, y)

    fig.canvas.draw_idle()

resetax = fig.add_axes([0.8, 0.025, 0.1, 0.02])
button = Button(resetax, 'Update', hovercolor='0.975')

button.on_clicked(update)

plt.show()