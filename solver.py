from sympy import symbols, sympify, diff, lambdify, S, Interval, Union
from sympy.calculus.util import continuous_domain
import numpy

def resolve(eqn, lower_bound = -100, upper_bound = 100):
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
    f = lambdify(x, f_expr)
    df = lambdify(x, df_expr)

    potential_guesses = []
    roots_found = []
    
    if isinstance(search_interval, Union):
        intervals = list(search_interval.args)
    else:
        intervals = [search_interval]

    for interval in intervals:
        start = float(interval.start)
        end = float(interval.end)
        samples = numpy.linspace(start, end, 100)
        
        for i in range(len(samples) - 1):
            x1, x2 = samples[i], samples[i + 1]
            # the below condition ensures values too close to the boundaries are not mistakenly approximated to the boundaries
            if i == 0:
                x1 += 1e-10
                x2 += 1e-10
            if i == len(samples) - 2:
                x1 -= 1e-10
                x2 -= 1e-10
                
            f1, f2 = f(x1), f(x2)
            if f1 == 0 or f2 == 0:
                if f1 == 0:
                    roots_found.append(float(x1))
                if f2 == 0:
                    roots_found.append(float(x2))
                continue

            midpoint = float((x1 + x2) / 2)

            if f(x1) * f(x2) <= 0:
                potential_guesses.append(midpoint) # midpoint as initial guess
                
            if x1 in df_domain and x2 in df_domain:
                df1, df2 = df(x1), df(x2)
                if df1 * df2 <= 0:
                    potential_guesses.append(midpoint)

    for initial_guess in potential_guesses:
        xn = initial_guess
        for _ in range(100):
            if df(xn) == 0:
                break
            
            x_next = float(xn - (f(xn) / df(xn)))

            if abs(x_next - xn) <= 1e-5:
                root = round(x_next, 5)
                roots_found.append(root)
                break

            xn = x_next

    return [sorted(list(set(roots_found))), ""]

if __name__ == "__main__":
    eqn_str = input("Enter an equation (use 'x' as a variable, e.g., x^3 - 4*x^2 + 1)\n>>> ")
    lower_bound = float(input("Enter lower bound (default: -100): ") or -100)
    upper_bound = float(input("Enter upper bound (default: 100): ") or 100)
    answer, message = resolve(eqn_str)
    if message:
        print(message)
    else:
        print(answer)