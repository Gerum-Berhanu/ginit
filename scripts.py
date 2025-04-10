from sympy import symbols, sqrt, Pow, Add, Mul, Rational, sympify, solve, lambdify, preorder_traversal, S
from sympy.core.expr import Expr
from sympy.calculus.util import continuous_domain
import re

def replace_logs(input_string):
    # Replace log(expr) with log(expr, 10) only if there is no second argument (base)
    updated_string = re.sub(r"log\(([^,]+)\)", r"log(\1, 10)", input_string)
    # Replace ln(expr) with log(expr, exp(1))
    updated_string = re.sub(r"ln\(([^)]+)\)", r"log(\1, exp(1))", updated_string)
    return updated_string

def solve_inverse(expr) -> float:
    x, y = symbols('x y')

    try:
        i_list = solve(expr - y, x) # expr - y is your equation, and you are asking SymPy to solve this equation for the symbol x
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
        return [[], f"Unable to solve the equation {expr}"]
    except Exception as e:
        return [[], f"An unexpected error occurred: {str(e)}"]


def is_expr_only_square_roots(expr: Expr) -> bool:
    """
    Checks if the expression is made only of square roots (Pow with exp=1/2),
    connected by +, -, *, or /.
    Allows any expression inside the square root (not just symbols).
    """
    # It must contain at least one square root
    if not expr.has(Pow) or not any(isinstance(e, Pow) and e.exp == Rational(1, 2) for e in preorder_traversal(expr)):
        return False

    for sub in preorder_traversal(expr):
        # Atoms like x, numbers, etc. are allowed
        if sub.is_Atom:
            continue

        # Allow only sqrt: Pow with exponent 1/2
        if isinstance(sub, Pow):
            if sub.exp != Rational(1, 2):
                return False
            continue

        # Allow only +, -, *, /
        if isinstance(sub, (Add, Mul)):
            continue

        # If it's not Add/Mul/Pow or Atom — reject
        return False

    return True