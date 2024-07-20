import streamlit as st
import plotly.graph_objs as go
import networkx as nx
import numpy as np
import time

def create_network_graph(layer_sizes):
    G = nx.DiGraph()
    total_nodes = sum(layer_sizes)
    current_node = 0

    # Create nodes for each neuron in each layer
    for i, size in enumerate(layer_sizes):
        for j in range(size):
            G.add_node(current_node, layer=i)
            current_node += 1

    # Connect nodes between layers
    current_node = 0
    for i in range(len(layer_sizes) - 1):
        for j in range(layer_sizes[i]):
            for k in range(layer_sizes[i + 1]):
                target_node = sum(layer_sizes[:i + 1]) + k
                G.add_edge(current_node, target_node)
            current_node += 1

    return G



def update_plotly_graph(fig, num_iterations, num_layers):
    for iteration in range(num_iterations):
        # Simulate a training step update
        new_y = np.random.random(100) * num_layers
        fig.data[0].y = new_y
        time.sleep(0.1)  # Simulate training time delay
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("Neural Network Optimization Visualization")

    # Sidebar for user inputs
    st.sidebar.header("Network Configuration")
    learning_rate = st.sidebar.slider('Learning Rate', 0.01, 0.1, 0.01)
    num_layers = st.sidebar.selectbox('Number of Layers', [1, 2, 3, 4, 5])
    num_iterations = st.sidebar.slider('Training Iterations', 1, 100, 10)

    # NetworkX Graph Visualization
    # NetworkX Graph Visualization
    layer_sizes = [4, 6, 4, 1]  # Example layer sizes
    G = create_network_graph(layer_sizes)
    pos = nx.spring_layout(G)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', hoverinfo='text', marker=dict(showscale=True, colorscale='YlGnBu', size=10))

    fig = go.Figure(data=[edge_trace, node_trace])
    st.plotly_chart(fig, use_container_width=True)


    # Plotly Graph for Training Visualization
    data_x = np.linspace(1, 10, 100)
    data_y = np.random.random(100) * num_layers
    fig = go.Figure(data=[go.Scatter(x=data_x, y=data_y, mode='markers')])
    fig.update_layout(title='Neural Network Training Progress',
                      xaxis_title='X',
                      yaxis_title='Y')

    # Start Training Button
    if st.button('Start Training'):
        update_plotly_graph(fig, num_iterations, num_layers)

if __name__ == "__main__":
    main()