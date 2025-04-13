import tkinter as tk

def run_app(solve_equation):
    # Creating the main window
    root = tk.Tk()
    root.title("Equation Solver")
    root.state("zoomed")  # Full-screen on launch
    root.config(bg="#f0f8ff")  # Light background (Alice Blue for a fresh, bright feel)

    # Creating a title label with modern styling
    title_label = tk.Label(
        root, 
        text="Equation Solver", 
        font=("Helvetica", 24, "bold"), 
        bg="#f0f8ff", 
        fg="#333333"  # Dark gray text for contrast
    )
    title_label.pack(pady=20)

    # Creating a frame for input fields for better organization
    input_frame = tk.Frame(root, bg="#f0f8ff")
    input_frame.pack(pady=10)

    # Creating the input fields and labels
    equation_label = tk.Label(
        input_frame, 
        text="Enter equation (in terms of x):", 
        bg="#f0f8ff", 
        fg="#333333", 
        font=("Helvetica", 16)
    )
    equation_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    equation_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 14))
    equation_entry.grid(row=0, column=1, padx=10, pady=10)

    lower_bound_label = tk.Label(
        input_frame, 
        text="Enter lower bound:", 
        bg="#f0f8ff", 
        fg="#333333", 
        font=("Helvetica", 16)
    )
    lower_bound_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    lower_bound_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 14))
    lower_bound_entry.grid(row=1, column=1, padx=10, pady=10)

    upper_bound_label = tk.Label(
        input_frame, 
        text="Enter upper bound:", 
        bg="#f0f8ff", 
        fg="#333333", 
        font=("Helvetica", 16)
    )
    upper_bound_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    upper_bound_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 14))
    upper_bound_entry.grid(row=2, column=1, padx=10, pady=10)

    # Result label with modern styling
    result_label = tk.Label(
        root, 
        text="Solutions will be displayed here.", 
        bg="#f0f8ff", 
        fg="#333333", 
        font=("Helvetica", 14)
    )
    result_label.pack(pady=20)

    # Solve button with cheerful styling
    solve_button = tk.Button(
        root,
        text="Solve Equation",
        command=lambda: solve_equation(equation_entry, lower_bound_entry, upper_bound_entry, result_label),
        font=("Helvetica", 14, "bold"),
        bg="#4CAF50",  # Fresh green for positivity
        fg="#ffffff",
        width=25,
        height=2,
        relief="raised",
        bd=3
    )
    solve_button.pack(pady=20)

    # Run the Tkinter event loop
    root.mainloop()