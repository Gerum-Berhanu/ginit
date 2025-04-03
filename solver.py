from sympy import symbols, diff, sympify, lambdify
import numpy

def resolve(eqn):
    x = symbols('x')

    try:
        # f_expr = sympify(input("Enter an equation (use 'x' as a variable, e.g., x**3 - 4*x**2 + 1)\n"))
        f_expr = sympify(eqn)
    except Exception as e:
        # print(f"Invalid equation: {e}")
        # exit()
        return [[], f"Invalid equation: {e}"]

    # sympify ensures that "x**3 - 4*x**2 + 1" is treated as a symbolic expression rather than a plain string.
    # f_expr = sympify("x**3 - 4*x**2 + 1")  # This holds x**3 - 4*x**2 + 1
    df_expr = diff(f_expr, x) # This holds 3*x**2 - 8*x

    # Convert symbolic expressions into python functions
    f = lambdify(x, f_expr)
    df = lambdify(x, df_expr)

    search_range = numpy.linspace(-50, 50, 1000)
    potential_guesses = []
    for i in range(len(search_range) - 1):
        x1, x2 = search_range[i], search_range[i + 1]
        if f(x1) * f(x2) <= 0 or df(x1) * df(x2) <= 0:
            midpoint = (x1 + x2) / 2
            potential_guesses.append(midpoint) # midpoint as initial guess

    # print(potential_guesses)
    roots_found = []

    for initial_guess in potential_guesses:
        xn = initial_guess
        for _ in range(100):
            if df(xn) == 0:
                break

            x_next = xn - (f(xn) / df(xn))

            if abs(x_next - xn) <= 1e-5:
                if round(x_next, 5) not in roots_found: roots_found.append(round(x_next, 5))
                break

            xn = x_next

    return [sorted(roots_found), ""]