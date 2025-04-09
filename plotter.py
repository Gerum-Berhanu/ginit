from sympy import symbols, sympify, lambdify, diff
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np

x = None
f = None
df = None

def prepare_functions(eqn):
    global x, f, df
    x = symbols("x")

    try:
        f_expr = sympify(eqn)
    except Exception as e:
        print(f"Invalid equation: {e}")
        return None

    df_expr = diff(f_expr, x)

    f = lambdify(x, f_expr)
    df = lambdify(x, df_expr)
    return 0

    
def line_expr(a):
    global x, f, df
    a = float(a)
    return df(a) * (x - a) + f(a)

def prepare_line(a):
    global x, f, df
    a = float(a)
    return lambdify(x, line_expr(a))

def plot_graph(expr_data, line1, line2):
    global f, df
    x_ax = np.linspace(-10, 10, 100)
    y1 = f(x_ax)
    l1 = line1(x_ax)
    l2 = line2(x_ax)

    plt.plot(x_ax, y1, label=f"f(x) = {expr_data["equation"]}", color="blue")
    plt.plot(x_ax, l1, label=f"Tangent at x = {expr_data["line_pt1"]}", color="green")
    plt.plot(x_ax, l2, label=f"Tangent at x = {expr_data["line_pt2"]}", color="red")

    plt.scatter(expr_data["line_pt1"], 0, label=f"Initial guess ({expr_data["line_pt1"]}, 0)", color="green")
    plt.scatter(expr_data["line_pt2"], 0, label=f"Second guess ({expr_data["line_pt2"]}, 0)", color="red")

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Demonstration of Plotting")

    # Bold the x=0 and y=0 lines
    plt.axhline(0, color='black', linewidth=2)  # y=0 (horizontal line at y=0)
    plt.axvline(0, color='black', linewidth=2)  # x=0 (vertical line at x=0)

    plt.xlim(-10, 10)
    plt.ylim(-5, 10)

    plt.grid(True)
    plt.legend(loc="upper left")
    plt.show()

def prepare_plot(equation, line_pt1, line_pt2):
    result = prepare_functions(equation)
    if result == None:
        return None
    line1 = prepare_line(line_pt1)
    line2 = prepare_line(line_pt2)
    expr_data = {
        "equation": equation,
        "line_pt1": line_pt1,
        "line_pt2": line_pt2
    }
    plot_graph(expr_data, line1, line2)
    return 0