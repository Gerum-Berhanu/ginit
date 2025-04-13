from sympy import symbols, lambdify, S, Interval, Union
from decimal import Decimal
from scripts import *

def resolve(eqn, lower_bound, upper_bound, to_plot):
    if lower_bound >= upper_bound:
        return [[], f"Invalid lower and/or upper bound."]
    
    x = symbols('x')
    eqn = replace_logs(eqn)

    funcs, msg = set_funcs(eqn)
    if msg:
        return [[], msg]
    f_expr, df_expr, f_domain, df_domain = funcs

    full_range = Interval(lower_bound, upper_bound)
    search_interval = f_domain.intersect(full_range)
    if search_interval is S.EmptySet:
        return [[], f"No real root found in the interval {lower_bound} to {upper_bound}."]

    # Convert symbolic expressions into python functions
    f_raw = lambdify(x, f_expr)
    df_raw = lambdify(x, df_expr)

    # Wrapper functions: take Decimal or float, return Decimal
    f = lambda x: Decimal(str(f_raw(float(x))))
    df = lambda x: Decimal(str(df_raw(float(x))))

    # Solve with inverse method if the equation holds x^(1/n), tan(x) or cot(x)
    inv_ans, inv_msg = inverse_method(f_expr)
    if inv_ans is not None or inv_msg is not None:
        return [inv_ans, inv_msg]
    
    # If the inverse method returns [None, None], which means there is no x^(1/n), tan(x) and cot(x) found in the equation, then the following code continues
    
    if isinstance(search_interval, Union):
        intervals = list(search_interval.args)
    else:
        intervals = [search_interval]

    # Have the best initial guesses with bisection method
    roots_found = []
    potential_guesses = bisection_method(intervals, f, f_expr, df, df_expr)
    if not potential_guesses:
        return [[], f"No real root found in the interval {lower_bound} to {upper_bound}."]
    
    # Solve with newton's method only if the equation doesn't hold x^(1/n), tan(x) and cot(x)
    for initial_guess in potential_guesses:
        root = newtons_method(initial_guess, eqn, f, df, to_plot)
        to_plot = False
        if root is None:
            continue
        roots_found.append(root)

    roots_found = sorted(list(set(roots_found)))
    return [[ans for ans in roots_found], ""]

if __name__ == "__main__":
    eqn_str = input("Enter an equation (use 'x' as a variable, e.g., x^3 - 4*x^2 + 1)\n>>> ")
    lower_bound = Decimal(input("Enter lower bound (default: -100): ") or -100)
    upper_bound = Decimal(input("Enter upper bound (default: 100): ") or 100)

    answer, message = resolve(eqn_str, lower_bound, upper_bound, True)
    if message:
        print(message)
    else:
        print(answer)