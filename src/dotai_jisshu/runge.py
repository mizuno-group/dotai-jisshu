import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import ode

def runge_kutta(func, param_list, name):
    # param_list : list of parameter set of tuple.
    # name : list of title of parameter set. length is same as length of param_list.
    for x in range(len(param_list)):
        if len(param_list[x]) != 18:
          raise IndexError("!! 初期値の数が足りません! !!")
  
    v0 = np.array([0, 0, 0, 0, 0, 0])
    tmax = 1000
    step = 1
    t = np.arange(0, tmax+step, step)
    sols = []
    solver = ode(func)
    for v in param_list:
        solver.set_integrator("dopri5")
        solver.set_initial_value(v0, 0)
        solver.set_f_params(v)

        sol = np.empty((int((1000/ step) + 1), 6))
        sol[0] = v0

        k = 1
        while solver.successful() and solver.t < tmax:
            solver.integrate(t[k])
            sol[k] = solver.y 
            k += 1
        sols.append(sol)

    all_sol = pd.DataFrame({'Time': t})
 
    for v,w in zip(sols, name):
        plt.plot(t, v[:,0], label=w)
        all_sol[f"{w}_artery"] = v[:, 0]
    plt.xlabel("Time (min)", fontsize=12)
    plt.ylabel("Conc. (nmol/mL)", fontsize=12)
    plt.grid(axis="both", lw=0.5, ls="--")
    plt.legend(loc="lower right")
    plt.title("Concentration in artery", fontsize=15)
    plt.show()

    for v, w in zip(sols, name):
        plt.plot(t, v[:,-1], label=w)
        all_sol[f"{w}_liver"] = v[:, -1]
    plt.xlabel("Time (min)", fontsize=12)
    plt.ylabel("Conc. (nmol/mL)", fontsize=12)
    plt.grid(axis="both", lw=0.5, ls="--")
    plt.legend(loc="lower right")
    plt.title("Concentration in liver tissue", fontsize=15)
    plt.show()

    for v, w, x in zip(sols, name, param_list):
        plt.plot(t, v[:,-1]*x[10]*x[16], label=w)
        all_sol[f"{w}_bile_rate"] = v[:, -1] * x[10] * x[16]
    plt.xlabel("Time (min)", fontsize=12)
    plt.ylabel("Rate (nmol/min/kg)", fontsize=12)
    plt.grid(axis="both", lw=0.5, ls="--")
    plt.legend(loc="lower right")
    plt.title("Bile excretion rate", fontsize=15)
    plt.show()