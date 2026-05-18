import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def fitting(func, data, init_params, method):
    """
    func: function of nonlinear model
    data: input data whose columns is sample name
    init_params: list of initial parameters in function
    method: "two_compartment" or "Ki_predict"
    """
    x = np.array(data.index)
    assert len(data.columns) == 2, "指示した箇所以外のコードが書き換わっています。TAに確認してもらってください。"
    for col in data.columns:
        y = data[col].values
        if method == "two_compartment":
            col = col.replace(" (nmol/mL)", "")
        elif method == "Ki_predict":
            col = col.replace(" (% of control)", "")
        params, cov = curve_fit(func, x, y, p0=init_params[col], sigma=y)
        optim_y = []
        for t in x:
            optim_y.append(func(t, *params))

        print(f"===== {col}のフィッティング結果 =====")
        
        if method == "two_compartment":
            plt.plot(data.index, optim_y, marker="", label="fitting")
            plt.scatter(data.index, y, marker="o", label="observed")
            plt.xlabel("Time (min)", fontsize=12)
            plt.ylabel("plasma conc. (μM)", fontsize=12)
            plt.yscale("log")
            plt.title(col, fontsize=15)
            plt.grid(which="both", axis="both", lw=0.5, ls="--")
            plt.legend()
            plt.show()
            
            result_param(params, method)

        elif method == "Ki_predict":
            plt.plot(data.index, optim_y,marker="", label="fitting")
            plt.scatter(data.index, y, marker="o", label="observed")
            plt.xlabel("RIF conc. (μM)", fontsize=12)
            plt.ylabel("%CL", fontsize=12)
            plt.xscale("log")
            plt.title(col, fontsize=15)
            plt.grid(which="both", axis="both", lw=0.5, ls="--")
            plt.legend()
            plt.show()
            
            result_param(params, method)

def result_param(param, method):
  if method == "two_compartment":
    print(f"p_A = {param[0]}")
    print(f"p_a = {param[1]}")
    print(f"p_B = {param[2]}")
    print(f"p_b = {param[3]}")

  elif method == "Ki_predict":
    print(f"p_pdif = {param[1]}")
    print(f"p_ki = {param[0]}")