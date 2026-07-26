from modsim import *
import matplotlib.pyplot as plt

def make_system(T_init, volume, r, t_end):
    return System(T_init=T_init,volume=volume,r=r,t_end=t_end,T_env=22,t_0=0,dt=1)

def change_func(t, T, system):
    r, T_env, dt = system.r, system.T_env, system.dt
    return -r * (T-T_env) * dt

def run_sim(system, change_func):
    t_array = linrange(system.t_0, system.t_end, system.dt)
    n = len(t_array)

    series = TimeSeries(index=t_array)
    series.iloc[0] = system.T_init

    for i in range(n-1):
        t = t_array[i]
        T = series.iloc[i]
        series.iloc[i+1] = T + change_func(t, T, system)
    
    system.T_final = series.iloc[-1]
    return series

def get_error(r, system):
    system.r = r
    results = run_sim(system, change_func)
    return system.T_final - 70


def get_error_m(r, system):
    system.r = r
    results = run_sim(system, change_func)
    return system.T_final - 20



"""
MILK SYSTEM & FIND R
milk = make_system(T_init=5, volume=50, r=0.12, t_end=15)
milk.r = root_scalar(get_error_m, milk, bracket=[0.1,0.2]).root
results = run_sim(milk, change_func)

results.plot()
plt.show()
"""

"""
COFFEE SYSTEM & FIND R
coffee = make_system(T_init=90, volume=300, r=0.01, t_end=30)
coffee.r = root_scalar(get_error, coffee, bracket=[0.01,0.02]).root
results = run_sim(coffee, change_func)

results.plot()
plt.show()
"""


