from sympy import symbols, sympify, diff, Pow, solve, lambdify, S, Function, tan, cot
from sympy.calculus.util import continuous_domain
from decimal import Decimal
from plotter import prepare_plot
import re
import numpy

def set_funcs(eqn : str):
    x = symbols('x')

    try:
        f_expr = sympify(eqn)
    except Exception as e:
        return [[], f"Invalid equation: {e}"]
    df_expr = diff(f_expr, x)

    f_domain = find_domain(f_expr)
    if f_domain is None:
        return [[], "Function is not defined over the set of real numbers."]
    df_domain = find_domain(df_expr)
    if df_domain is None:
        return [[], "Derivative of the function is not defined over the set of real numbers."]
    
    return [[f_expr, df_expr, f_domain, df_domain], ""]

def replace_logs(input_string):
    # Replace log(expr) with log(expr, 10) only if there is no second argument (base)
    updated_string = re.sub(r"log\(([^,]+)\)", r"log(\1, 10)", input_string)
    # Replace ln(expr) with log(expr, exp(1))
    updated_string = re.sub(r"ln\(([^)]+)\)", r"log(\1, exp(1))", updated_string)
    return updated_string

def find_domain(expr : str, sym = symbols('x'), domain = S.Reals):
    expr_domain = continuous_domain(expr, sym, domain)
    if expr_domain is S.EmptySet:
        return None
    return expr_domain

def inverse_method(f_expr):
    has_sqrt = any(
        isinstance(arg, Pow) 
        and arg.exp.q != 1 # means exponent is a rational (1/n) and not an integer
        and arg.exp.p == 1 # numerator of exponent must be 1
        for arg in f_expr.atoms(Pow)
    )
    has_tan_cot = any(
        isinstance(arg, Function)
        and (arg.func == tan or arg.func == cot) # checks if the function is tan or cot
        for arg in f_expr.atoms(Function)
    )
    
    if not has_sqrt and not has_tan_cot:
        return [None, None]
    
    x, y = symbols('x y')

    try:
        i_list = solve(f_expr - y, x) # f_expr - y is your equation, and you are asking SymPy to solve this equation for the symbol x
        if not i_list:
            return [[], "No inverse found."]

        solutions = []
        for i_expr in i_list:
            i_domain = continuous_domain(i_expr, y, S.Reals)

            if i_domain is S.EmptySet:
                return [[], "Inverse of the function is not defined over the set of real numbers."]

            if 0 not in i_domain:
                return [[], "Zero is not part of the domain of the inverse function."]

            i = lambdify(y, i_expr)
            val = i(0)
            if isinstance(val, complex):
                if val.imag != 0:
                    continue  # skip imaginary roots
                val = val.real  # if complex with zero imaginary part

            solutions.append(float(val))
        return [solutions, ""]
    
    except NotImplementedError:
        return [[], f"Unable to solve the equation {f_expr}"]
    except Exception as e:
        return [[], f"An unexpected error occurred: {str(e)}"]
    
def bisection_method(intervals : list, f, f_expr, df, df_expr, gap : float = 1000):
    f_domain = find_domain(f_expr)
    df_domain = find_domain(df_expr)

    potential_guesses = []

    for interval in intervals:
        start = Decimal(str(interval.start))
        end = Decimal(str(interval.end))

        if interval.left_open:
            start += Decimal(str("1e-8"))
        if interval.right_open:
            end -= Decimal(str("1e-8"))

        samples = numpy.linspace(start, end, gap)
        
        for i in range(len(samples) - 1):
            x1, x2 = Decimal(str(samples[i])), Decimal(str(samples[i + 1]))

            midpoint = Decimal(str((x1 + x2) / 2))

            if f(x1) * f(x2) <= 0:
                potential_guesses.append(midpoint)
                
            if x1 in df_domain and x2 in df_domain:
                df1, df2 = df(x1), df(x2)
                if df1 * df2 <= 0:
                    potential_guesses.append(midpoint)

    return potential_guesses

def newtons_method(x_i : Decimal, eqn : str, f, df, plot : bool):
    if f(x_i) == 0:
        root = round(float(x_i), 8)
        return root
    if df(x_i) == 0:
        return None

    x_n = Decimal(str(x_i - (f(x_i) / df(x_i))))

    if plot:
        prepare_plot(eqn, x_i, x_n)

    while abs(x_n - x_i) > 1e-5:
        x_i = x_n
        x_n = Decimal(str(x_i - (f(x_i) / df(x_i))))

    root = round(float(x_n), 8)
    return root