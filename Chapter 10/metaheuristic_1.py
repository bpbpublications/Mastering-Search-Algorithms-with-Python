import streamlit as st
import plotly.graph_objects as go
import random

# Objective function to optimize (example: quadratic function)
def objective_function(x):
    return -(x-5)**2 + 25  # Inverted parabola

# Simple Evolutionary Algorithm
def evolutionary_algorithm(start_population, generations, mutation_factor):
    population = start_population
    best_individual = None
    best_score = float('-inf')

    for _ in range(generations):
        # Mutation step
        mutated_population = [x + random.choice([-mutation_factor, mutation_factor]) for x in population]

        # Selection step
        scored_population = [(x, objective_function(x)) for x in mutated_population]
        best_individual, best_score = max(scored_population, key=lambda x: x[1])
        population = [best_individual] * len(population)  # Elitism: all population becomes the best individual

    return best_individual, best_score

# Streamlit interface
st.title("Evolutionary Algorithm Demo")

# User input for the parameters
start_population = st.slider("Start Population Size", 1, 10, 5)
generations = st.slider("Number of Generations", 1, 100, 20)
mutation_factor = st.slider("Mutation Factor", 1, 5, 2)

# Button to start the algorithm
if st.button("Start Evolutionary Algorithm"):
    best_individual, best_score = evolutionary_algorithm([random.randint(0, 10) for _ in range(start_population)], generations, mutation_factor)
    st.write(f"Best solution found: x = {best_individual}, f(x) = {best_score}")

    # Plotly for Visualization
    fig = go.Figure()

    # Plot the function
    x_values = list(range(0, 10))
    y_values = [objective_function(x) for x in x_values]
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='Objective Function'))

    # Show the plot
    st.plotly_chart(fig)

# Run this script using: streamlit run script_name.py
