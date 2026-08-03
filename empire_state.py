from modsim import *
import matplotlib.pyplot as plt
from numpy import log, exp

init = State(y=381, v=0)
system = System(init=init, g=9.8, t_end=10)

def slope_func(t, state, system):
    y, v = state
    dydt = v
    dvdt = -system.g

    return dydt, dvdt

def event_func(t, state, system):
    y, v = state
    return y

results, details = run_solve_ivp(system, slope_func, events=event_func)

results.y.plot()
decorate(xlabel="Time", ylabel="Position/m")
plt.show()

print(results.iloc[-1])