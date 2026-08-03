from modsim import *
import matplotlib.pyplot as plt
from numpy import log, exp

r0 = 149597870700
r_sun = 6.96e8
r_earth = 6.37e6
r_final = r_sun + r_earth

t_end = 1e7

init = State(r=r0, v=0)
system = System(init=init, G=6.67e-11, m1 = 1.989e30, m2 = 5.972e24, r_final=r_final, t_end=t_end)

def compute_gravity(state, system):
    r, v = state
    m1, m2, G = system.m1, system.m2, system.G

    return (G * m1 * m2) / r ** 2

def slope_func(t, state, system):
    r, v = state

    force = compute_gravity(state, system)
    dydt = v
    dvdt = -force / system.m2

    return dydt, dvdt

def event_func(t, state, system):
    r, v = state
    return r - system.r_final

results, details = run_solve_ivp(system, slope_func, events=event_func)
results.index /= 60 * 60 * 24

results.r.plot()
decorate(xlabel="Time (days)", ylabel="Distance from sun")
plt.show()