from sympy import symbols, sympify, diff, lambdify, S, Interval, Union
from sympy.calculus.util import continuous_domain
from decimal import Decimal
import numpy

def resolve(eqn, lower_bound = -100.0, upper_bound = 100.0):
    if lower_bound >= upper_bound:
        return [[], f"Invalid lower and/or upper bound."]
    
    x = symbols('x')

    try:
        f_expr = sympify(eqn)
    except Exception as e:
        return [[], f"Invalid equation: {e}"]

    df_expr = diff(f_expr, x)

    f_domain = continuous_domain(f_expr, x, S.Reals)
    if f_domain is S.EmptySet:
        return [[], "Function is not defined over the set of real numbers."]
    df_domain = continuous_domain(df_expr, x, S.Reals)
    if df_domain is S.EmptySet:
        return [[], "Derivative of the function is not defined over the set of real numbers."]

    full_range = Interval(lower_bound, upper_bound)
    search_interval = f_domain.intersect(full_range)
    if search_interval is S.EmptySet:
        return [[], f"No real roots found in range {lower_bound} to {upper_bound}."]

    # convert symbolic expressions into python functions
    f_raw = lambdify(x, f_expr)
    df_raw = lambdify(x, df_expr)

    # wrapper functions: take Decimal or float, return Decimal
    f = lambda x: Decimal(str(f_raw(float(x))))
    df = lambda x: Decimal(str(df_raw(float(x))))

    potential_guesses = []
    roots_found = []
    
    if isinstance(search_interval, Union):
        intervals = list(search_interval.args)
    else:
        intervals = [search_interval]

    for interval in intervals:
        start = Decimal(str(interval.start))
        end = Decimal(str(interval.end))
        if interval.left_open:
            start += Decimal(str("1e-8"))
        if interval.right_open:
            end -= Decimal(str("1e-8"))
        samples = numpy.linspace(start, end, 100)
        
        for i in range(len(samples) - 1):
            x1, x2 = Decimal(str(samples[i])), Decimal(str(samples[i + 1]))

            midpoint = Decimal(str((x1 + x2) / 2))
            # midpoint = round(float((x1 + x2) / 2), 10)

            if f(x1) * f(x2) <= 0:
                potential_guesses.append(midpoint) # midpoint as initial guess
                
            if x1 in df_domain and x2 in df_domain:
                df1, df2 = df(x1), df(x2)
                if df1 * df2 <= 0:
                    potential_guesses.append(midpoint)

    for initial_guess in potential_guesses:
        count = 0
        xn = initial_guess
        if df(xn) == 0:
            continue
        x_next = Decimal(str(xn - (f(xn) / df(xn))))
        while abs(x_next - xn) > 1e-5:
            count += 1
            xn = x_next
            x_next = Decimal(str(x_next - (f(x_next) / df(x_next))))
        root = round(float(x_next), 10)
        roots_found.append(root)

    return [[ans for ans in sorted(list(set(roots_found)))], ""]

if __name__ == "__main__":
    eqn_str = input("Enter an equation (use 'x' as a variable, e.g., x^3 - 4*x^2 + 1)\n>>> ")
    lower_bound = Decimal(input("Enter lower bound (default: -100): ") or -100)
    upper_bound = Decimal(input("Enter upper bound (default: 100): ") or 100)
    answer, message = resolve(eqn_str)
    if message:
        print(message)
    else:
        print(answer)