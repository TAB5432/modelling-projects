from modsim import *
import matplotlib.pyplot as plt
from numpy import log, exp, pi

params = Params(
    mass = 0.0025,
    diameter = 0.019,
    rho = 1.2,
    g = 9.8,
    v_init = 0,
    v_term = 18,
    height = 381,
    t_end = 30,
)

def make_system(params):
    init = State(y=params.height, v=params.v_init)

    area = pi * (params.diameter/2) ** 2

    C_d = (2 *(params.mass * params.g)) / \
        (params.rho * area * params.v_term ** 2)
    
    return System(init=init,
                  area=area,
                  C_d=C_d,
                  mass=params.mass,
                  rho = params.rho,
                  g=params.g,
                  t_end=params.t_end 
                  )

def slope_func(t, state, system):
    y, v = state
    rho, C_d, area = system.rho, system.C_d, system.area
    mass, g = system.mass, system.g

    drag_force = 0.5 * rho * (v ** 2) * C_d * area
    drag_accel = drag_force / mass

    dydt = v
    dvdt = -g + drag_accel

    return dydt, dvdt

def event_func(t, state, system):
    y, v = state
    return y

def error_func(guess, params):
    params = params.set(v_term=guess)
    system = make_system(params)
    results, details = run_solve_ivp(system, slope_func, 
                                     events=event_func)
    t_sidewalk = results.index[-1]
    error = t_sidewalk - params.flight_time
    return error

quarter_params = params.set(
    mass=0.0057,
    diameter=0.024,
    flight_time=19.1
)

quarter_system = make_system(quarter_params)
results, details = run_solve_ivp(quarter_system, slope_func, events=event_func)
root_res = root_scalar(error_func, quarter_params, bracket=[18, 22])

v_term = root_res.root
c_d_estimate = make_system(quarter_params.set(v_term=root_res.root)).C_d
print(c_d_estimate)             