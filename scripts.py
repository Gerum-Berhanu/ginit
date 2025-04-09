import re

def replace_logs(input_string):
    # Replace log(expr) with log(expr, 10)
    updated_string = re.sub(r"log\(([^)]+)\)", r"log(\1, 10)", input_string)

    # Replace ln(expr) with log(expr, expr(1))
    updated_string = re.sub(r"ln\(([^)]+)\)", r"log(\1, exp(1))", updated_string)

    return updated_string