import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
from scipy import signal

G = float
R = float
C = float
k = R*C
R_ratio = float

H1 = signal.lti([1],[-(k/G)**2, (k/G)*R_ratio, 1])
H2 = signal.lti([1,0],[-R_ratio*k/G, 1, R_ratio*G/k])
H3 = signal.lti([1,0,0],[-1, (G/k)*R_ratio, (G/k)**2])

transfer_functions = [H1, H2, H3]

for H in transfer_functions:
    H.poles()
    H.zeros()
    H.impulse()
    H.bode()