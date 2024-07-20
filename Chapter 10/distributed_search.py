import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random

# Create a distributed network graph
def create_distributed_network(num_nodes):
    G = nx.Graph()
    for node in range(num_nodes):
        G.add_node(node, label=f"Node {node}")
    for _ in range(num_nodes * 2):
        source = random.randint(0, num_nodes - 1)
        target = random.randint(0, num_nodes - 1)
        G.add_edge(source, target)
    return G

# Distributed search algorithm
def distributed_search(graph, start_node, target_node):
    visited_nodes = set()
    queue = [(start_node, None)]

    while queue:
        current_node, parent = queue.pop(0)
        visited_nodes.add(current_node)

        if current_node == target_node:
            return visited_nodes

        neighbors = list(graph.neighbors(current_node))
        for neighbor in neighbors:
            if neighbor != parent and neighbor not in visited_nodes:
                queue.append((neighbor, current_node))

    return visited_nodes

# Streamlit UI
st.title("Distributed Search Algorithm")

num_nodes = st.slider("Number of Nodes", 5, 20, 10)
target_node = st.slider("Target Node", 0, num_nodes - 1, 5)

G = create_distributed_network(num_nodes)

if st.button("Start Search"):
    st.write("Searching for Target Node...")
    visited_nodes = distributed_search(G, 0, target_node)

    # Visualize the network and search path
    pos = nx.spring_layout(G)
    edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(x=[], y=[], mode='markers', hoverinfo='text', marker=dict(showscale=True, colorscale='YlGnBu', size=10))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)

    st.plotly_chart(go.Figure(data=[edge_trace, node_trace], layout=go.Layout(showlegend=False, hovermode='closest', margin=dict(b=0, l=0, r=0, t=0), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))))
    
    st.write(f"Visited Nodes: {list(visited_nodes)}")
    if target_node in visited_nodes:
        st.success(f"Target Node {target_node} Found!")
    else:
        st.error(f"Target Node {target_node} Not Found!")

