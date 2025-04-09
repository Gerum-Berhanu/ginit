import tkinter as tk

def run_app(solve_equation):
    # Creating the main window
    root = tk.Tk()
    root.title("Equation Solver")
    root.geometry("400x300")  # Set the window size
    root.config(bg="#f5f5f5")  # Set background color

    # Creating a title label for better clarity
    title_label = tk.Label(root, text="Solve Your Equation", font=("Helvetica", 16, "bold"), bg="#f5f5f5")
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Creating the input fields and labels
    equation_label = tk.Label(root, text="Enter equation (in terms of x):", bg="#f5f5f5")
    equation_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    equation_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
    equation_entry.grid(row=1, column=1, padx=10, pady=5)

    lower_bound_label = tk.Label(root, text="Enter lower bound:", bg="#f5f5f5")
    lower_bound_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    lower_bound_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
    lower_bound_entry.grid(row=2, column=1, padx=10, pady=5)

    upper_bound_label = tk.Label(root, text="Enter upper bound:", bg="#f5f5f5")
    upper_bound_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    upper_bound_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
    upper_bound_entry.grid(row=3, column=1, padx=10, pady=5)

    # Result label
    result_label = tk.Label(root, text="Solutions will be shown here.", bg="#f5f5f5", font=("Helvetica", 12))
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

    # Solve button with a more modern look
    solve_button = tk.Button(
        root, 
        text="Solve", 
        command=lambda: solve_equation(equation_entry, lower_bound_entry, upper_bound_entry, result_label),
        font=("Helvetica", 12, "bold"), 
        bg="#4CAF50", 
        fg="white", 
        width=20,
        height=2,
        relief="raised",
        bd=2
    )
    solve_button.grid(row=5, column=0, columnspan=2, pady=20)

    # Start the Tkinter event loop
    root.mainloop()
