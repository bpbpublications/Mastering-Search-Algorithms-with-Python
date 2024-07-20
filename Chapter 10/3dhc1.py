import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random

# Different objective functions
def quadratic_function(x):
    return -(x-5)**2 + 25

def sine_function(x):
    return 10 + np.sin(x)

def polynomial_function(x):
    return -0.1 * x**4 + 2 * x**3 - 10 * x**2 + 5 * x + 20

# Hill Climbing algorithm
def hill_climbing(start, objective_function):
    current = start
    path = [start]
    while True:
        neighbor = current + random.choice([-1, 1])  # Generate a neighbor
        if objective_function(neighbor) <= objective_function(current):
            return current, path
        current = neighbor
        path.append(current)

# Streamlit interface
st.title("Hill Climbing Algorithm Demo")

# User selects objective function
function_choice = st.selectbox("Select an objective function:", 
                               ("Quadratic", "Sine", "Polynomial"))

# Map user choice to function
if function_choice == "Quadratic":
    objective_function = quadratic_function
elif function_choice == "Sine":
    objective_function = sine_function
else:
    objective_function = polynomial_function

# User input for the starting point
start_point = st.number_input("Enter a starting point:", value=0, step=1)

# Button to start the algorithm
if st.button("Start Hill Climbing"):
    solution, path = hill_climbing(start_point, objective_function)
    st.write(f"Solution found: x = {solution}, f(x) = {objective_function(solution)}")

    # Plotly for Visualization
    fig = go.Figure()

    # Generate values for 3D plot
    x_values = np.linspace(-10, 10, 400)
    y_values = [objective_function(x) for x in x_values]

    # 3D Plot
    fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=[0]*len(x_values), mode='lines', name='Objective Function'))

    # Add path to the plot
    path_x = [x for x in path]
    path_y = [objective_function(x) for x in path]
    fig.add_trace(go.Scatter3d(x=path_x, y=path_y, z=[0]*len(path_x), mode='markers+lines', name='Path', marker=dict(color='red')))

    # Show the plot
    st.plotly_chart(fig)
