import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy import signal

n = 10e3
f = 50
samp = 10e3

R = 1
C = 1
G = 1
R_ratio = 0.3206


H1 = signal.lti([1],[-(k/G)**2, (k/G)*R_ratio, 1])


def fourier_series(t, f, n_terms):
    n_terms = int(n_terms)
    result = 0
    for n in range(1, n_terms + 1):
        result += 2*(np.sin(n * f * t) / n)
    return result

# Generate t values
t = np.linspace(0, 2*np.pi, int(samp))

# Create the plot
plt.figure(figsize=(12, 8))
plt.plot(t, fourier_series(t, f, n))

plt.show()