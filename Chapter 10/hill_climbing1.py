import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import random

# Function to optimize (example: quadratic function)
def objective_function(x):
    return -(x-5)**2 + 25  # A simple inverted parabola

# Hill Climbing algorithm
def hill_climbing(start):
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

# User input for the starting point
start_point = st.number_input("Enter a starting point:", value=0, step=1)

# Button to start the algorithm
if st.button("Start Hill Climbing"):
    solution, path = hill_climbing(start_point)
    st.write(f"Solution found: x = {solution}, f(x) = {objective_function(solution)}")

    # Plotly for Visualization
    fig = go.Figure()

    # Plot the function
    x_values = list(range(0, 10))
    y_values = [objective_function(x) for x in x_values]
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='Objective Function'))

    # NetworkX graph for the path
    G = nx.Graph()
    for i in range(len(path)-1):
        G.add_edge(path[i], path[i+1])

    # Add path to the plot
    path_x = [x for x in path]
    path_y = [objective_function(x) for x in path]
    fig.add_trace(go.Scatter(x=path_x, y=path_y, mode='markers+lines', name='Path', marker=dict(color='red')))

    # Show the plot
    st.plotly_chart(fig)

# Run this script using: streamlit run script_name.py
