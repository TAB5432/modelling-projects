from modsim import *
import matplotlib.pyplot as plt
from numpy import log, exp

def make_system(T_init, volume, r, t_end):
    return System(T_init=T_init,T_final=T_init,volume=volume,r=r,t_end=t_end,T_env=22,t_0=0,dt=1)

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

def mix(system1, system2):
    V1, V2 = system1.volume, system2.volume
    T1, T2 = system1.T_final, system2.T_final

    V_mix = V1 + V2
    T_mix = (V1 * T1 + V2 * T2) / V_mix

    return make_system(T_init=T_mix, volume = V_mix, r = system1.r, t_end=30)

def run_and_mix(t_add, t_total):
    coffee.t_end = t_add
    milk.t_end = t_add
    run_sim(coffee, change_func)
    run_sim(milk, change_func)

    mixture = mix(coffee, milk)
    mixture.t_end = t_total - t_add
    run_sim(mixture, change_func)

    return mixture.T_final

def compute_r(system):
    return (1/system.t_end) * log((system.T_init - system.T_env) / (system.T_final - system.T_env))

def run_analysis(system):
    t_array = linrange(system.t_0, system.t_end, system.dt)
    T_array = system.T_env + (system.T_init - system.T_env) * exp(-system.r * t_array)
    system.T_final = T_array[-1]

    return make_series(t_array, T_array)

"""
ANALYTICAL RESULTS MILK

milk = make_system(T_init=5, volume=50, r=0, t_end=15)
milk.T_final = 5
r_milk = compute_r(milk)
milk.r = r_milk
print(r_milk)

results = run_analysis(milk)
print(milk.T_final)
"""

"""
ANALYTICAL RESULTS COFFEE

coffee = make_system(T_init=90, volume=300, r=0, t_end=30)
coffee.T_final = 70
r_coffee = compute_r(coffee)
coffee.r = r_coffee

results = run_analysis(coffee)
print(coffee.T_final)
"""

"""
GRAPH OPTIMAL TIMES

r_coffee = 0.0115
coffee = make_system(T_init=90, volume=300, r=r_coffee, t_end=30)

r_milk = 0.133
milk = make_system(T_init=5, volume=50, r=r_milk, t_end=15)

sweep = SweepSeries()
for t_add in linspace(0, 30, 15):
    sweep[t_add] = run_and_mix(t_add, 30)

sweep.plot(label="Mixture")
decorate(xlabel="Time Until Mixing", ylabel = "Final temp")
plt.show()
"""

"""
MILK LAST

r_coffee = 0.0115
coffee = make_system(T_init=90, volume=300, r=r_coffee, t_end=30)

r_milk = 0.133
milk = make_system(T_init=5, volume=50, r=r_milk, t_end=15)

run_sim(coffee, change_func)
run_sim(milk, change_func)
mix_last = mix(coffee, milk)
print(mix_last.T_final)
"""

"""
MIX FIRST
r_coffee = 0.0115
coffee = make_system(T_init=90, volume=300, r=r_coffee, t_end=30)

r_milk = 0.133
milk = make_system(T_init=5, volume=50, r=r_milk, t_end=15)

mix_first = mix(coffee, milk)
series = run_sim(mix_first, change_func)
print(mix_first.T_final)
"""




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


