import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Function to simulate Gradient Descent on a 2D function
def gradient_descent(starting_point, learning_rate, num_iterations):
    # Example function: f(x) = x^2
    # Derivative: f'(x) = 2x
    x = starting_point
    history = [x]

    for _ in range(num_iterations):
        grad = 2 * x  # Derivative of x^2
        x = x - learning_rate * grad
        history.append(x)

    return np.array(history)

def main():
    st.title("Gradient Descent Visualization")

    # Sidebar inputs
    st.sidebar.header("Settings")
    starting_point = st.sidebar.number_input("Starting Point", value=0.0, format="%.2f")
    learning_rate = st.sidebar.number_input("Learning Rate", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    num_iterations = st.sidebar.slider("Number of Iterations", 1, 100, 10)

    # Run gradient descent
    history = gradient_descent(starting_point, learning_rate, num_iterations)

    # Visualization
    # ... (This will be added in the next steps)

    # Inside main function, after calculating 'history'

# Function data
    x_range = np.linspace(-10, 10, 400)
    y_range = x_range**2  # Example function: f(x) = x^2

# Gradient descent path
    gd_x = history
    gd_y = gd_x**2

# Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', name='Function'))
    fig.add_trace(go.Scatter(x=gd_x, y=gd_y, mode='markers+lines', name='Gradient Descent Path'))

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
