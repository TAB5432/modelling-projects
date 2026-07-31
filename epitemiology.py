from modsim import *
import matplotlib.pyplot as plt
from numpy import log

tc = 4
tr = 2
beta = 1/tc
gamma = 1/tr

def make_system(beta, gamma, t_end):
    init = State(s=89, i=1, r=0)
    init /= init.sum()

    return System(init=init, t_end=t_end, beta=beta, gamma=gamma)

def add_immunity(system, fraction):
    system.init.s -= fraction
    system.init.r += fraction

    return system

def update(t, state, system):
    s, i, r = state.s, state.i, state.r

    infected = system.beta * i * s
    recovered = system.gamma * i

    s-= infected
    i += infected - recovered
    r += recovered 

    return State(s=s, i=i, r=r)

def run_sim(system, update_func):
    frame = TimeFrame(columns=system.init.index)
    #set first row to current values
    frame.loc[0] = system.init

    for t in range(0, system.t_end):
        frame.loc[t+1] = update_func(t, frame.loc[t], system)
    
    return frame

def plot_results(S, I, R):
    S.plot(style ="--", label = "Susceptible")
    I.plot(style ="-", label = "Infected")
    R.plot(style =":", label = "Recovered")
    decorate(xlabel = "Time in Days", ylabel = "Fraction of population")

def calc_total_infected(results, system):
    return results.s[0] - results.s[system.t_end]

def sweep_immunity(fraction_arr):
    sweep = SweepSeries()

    for fraction in fraction_arr:
        system = make_system(beta, gamma, 7*14)
        add_immunity(system, fraction)
        results = run_sim(system, update)
        sweep[fraction] = calc_total_infected(results, system)
    
    return sweep

def sweep_beta(beta_arr, gamma):
    sweep = SweepSeries()

    for beta in beta_arr:
        system = make_system(beta, gamma, 7*14)
        results = run_sim(system, update)
        sweep[beta] = calc_total_infected(results, system)
    
    return sweep

def sweep_beta_max_i(beta_arr, gamma):
    sweep = SweepSeries()

    for beta in beta_arr:
        system = make_system(beta, gamma, 7*14)
        results = run_sim(system, update)
        sweep[beta] = results.i.max()
    
    return sweep

def sweep_parameters(beta_arr, gamma_arr):
    frame = SweepFrame(columns = gamma_arr)

    for gamma in gamma_arr:
        frame[gamma] = sweep_beta(beta_arr, gamma)
    
    return frame

def plot_sweep_frame(frame):
    for gamma in frame.columns:
        column = frame[gamma]
        for beta in column.index:
            metric = column[beta]
            plt.plot(beta/gamma, metric, ".")

def plot_sweep_frame_diff(frame):
    for gamma in frame.columns:
        column = frame[gamma]
        for beta in column.index:
            metric = column[beta]
            plt.plot(beta - gamma, metric, ".")

system = make_system(beta, gamma, 7*14)
beta_arr = linspace(0.1, 1.1, 11)
gamma_arr = linspace(0.1, 0.7, 4)



frame = SweepFrame(columns = gamma_arr)
for gamma in gamma_arr:
    frame[gamma] = sweep_beta_max_i(beta_arr, gamma)

plot_sweep_frame(frame)
plt.show()


"""
BETA - GAMMA vs FRACTION INFECTED

sweep_frame = sweep_parameters(beta_arr, gamma_arr)
plot_sweep_frame_diff(sweep_frame)
decorate(xlabel = "beta - gamma", ylabel = "fraction infected")
plt.show()
"""

"""
ANALYSIS OF C vs REAL RESULTS OF C

beta_arr = linspace(0.1, 1.1, 11)
gamma_arr = linspace(0.1, 0.7, 4)

sweep_frame = sweep_parameters(beta_arr, gamma_arr)

s_inf_arr = linspace(0.003, 0.99, 50)
c_arr = log(s_inf_arr) / (s_inf_arr - 1)
frac_infected = 1 - s_inf_arr
frac_infected_series = make_series(c_arr, frac_infected)

plot_sweep_frame(sweep_frame)
frac_infected_series.plot(label="Analysis")
decorate(xlabel = "Contact number", ylabel = "fraction infected")
plt.show()
"""