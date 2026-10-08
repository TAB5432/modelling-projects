from modsim import *
import matplotlib.pyplot as plt
from numpy import log, exp, pi

params = Params(
    mass = 0.0025,      # kg
    diameter = 0.019,   # m
    rho = 1.2,          # kg/m^3
    g = 9.8,            # m/s^2
    v_init = 0,         # m/s
    v_term = 18,        # m/s
    height = 381,       # m
    t_end = 30          # s
)

def compute_C_d(m, g, rho, v_term, A):
    return (2*m*g) / (rho * (v_term**2) * A)
    
def make_system(params):
    init = State(y=params.height, v=params.v_init)

    area = pi * (params.diameter/2) ** 2

    C_d = compute_C_d(params.mass,params.g, params.rho, params.v_term, area)

    return System(init=init, area=area, 
                  C_d=C_d, mass=params.mass, 
                  rho=params.rho, g=params.g, 
                  t_end=params.t_end)


def slope_func(t, state, system):
    y, v = state
    rho = system.rho
    C_d = system.C_d
    A = system.area
    m = system.mass
    g = system.g

    f_d = 0.5 * rho * (v**2) * C_d * A
    a_d = f_d / m

    dydt = v
    dvdt = -g + a_d

    return dydt, dvdt

def event_func(t, state, system):
    y, v = state
    return y

system = make_system(params)

results, details = run_solve_ivp(system, slope_func, events=event_func)

results.v.plot(color="C2", label="v")
decorate(xlabel="Time /s", ylabel = "Velocity /ms^-1")
plt.show()

#quarter
params_q = params.set(
    mass = 0.0057,
    diameter = 0.024,
    flight_time = 19.1
)

def error_func(guess, params):
    #Error func for flight time
    params = params.set(v_term=guess)
    system = make_system(params)
    results, details = run_solve_ivp(system, slope_func, events=event_func)
    t_total = results.index[-1]
    error = t_total - params.flight_time
    return error

res = root_scalar(error_func, params_q, bracket=[18, 22])
v_term = res.root

system_q = make_system(params_q.set(v_term=v_term))
print(system_q.C_d)

