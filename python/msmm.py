import numpy as np
import scipy as sp
from scipy.integrate import ode

g = 1.
gamma = .05
r_a = .916
z_c = 5.5

def odes(t, y, p):
    m = p[0]
    k = p[1]
    v_0 = p[2]
    v = y[1]
    a = g - k * y[0] / m - gamma * y[1] / m - (np.pi * r_a**2. * v_0 * (y[1] - v_0)) / m
    return np.array((v, a))

def get_k(m) -> float:
    return 0. if m >= 4.61 else -11.4 * m + 52.5

def solve(v_0, h=.01, t_end=1000.):
    data = np.zeros((int(t_end/h), 7))
    data[:,0] = np.arange(0., t_end, h)
    data[0,1] = 2. # z
    data[0,2] = v_0 # v
    data[0,3] = 4.61 # m
    data[0,4] = get_k(data[0,3]) # k
    data[:,5] = v_0 # v_0
    data[:,6] = 0. # break?

    solver = ode(odes).set_integrator("dopri5", nsteps=10000)
    solver.set_initial_value(data[0,1:3])
    solver.set_f_params(data[0,3:])

    i = 1
    for t in data[:-1,0]:
        solver.integrate(t+h)
        data[i,1:3] = solver.y 
        data[i,3] = data[i-1,3] + np.pi * r_a**2. * v_0 * h # m
        data[i,4] = get_k(data[i,3]) # k

        if solver.y[0] >= z_c:
            solver.y[0] = 2.
            solver.y[1] = 0.
            data[i,1] = 2.
            data[i,2] = 0.
            data[i,3] = .2 * data[i,3] + .3
            data[i,6] = 1.
        solver.set_f_params(data[i,3:])
        i += 1
    return data
