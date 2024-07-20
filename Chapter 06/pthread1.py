import streamlit as st
import plotly.graph_objects as go
import multiprocessing
import networkx as nx
import matplotlib.pyplot as plt

# Search function for each process
def search_in_range(args):
    start, end, value_to_find, G = args
    for i in range(start, end):
        if G.nodes[i]['value'] == value_to_find:
            return True
    return False

# Streamlit App
st.title("Parallel Search Visualization with NetworkX")

# User input
array_size = st.slider("Size of array", min_value=10, max_value=1000, value=100, step=10)
value_to_find = st.slider("Value to search for", min_value=0, max_value=array_size - 1, value=10, step=1)
num_processes = st.slider("Number of processes", min_value=1, max_value=8, value=4, step=1)  # New input for processes

# Generate a linear graph based on user input
G = nx.path_graph(array_size)
for i in range(array_size):
    G.nodes[i]['value'] = i

# Button to initiate search
if st.button("Start Search"):
    
    # Use multiprocessing for parallel search
    num_processes = 4
    pool = multiprocessing.Pool(processes=num_processes)
    step = array_size // num_processes
    ranges = [(i * step, (i + 1) * step if i != num_processes - 1 else array_size, value_to_find, G) for i in range(num_processes)]
    results = pool.map(search_in_range, ranges)
    
    # Check if the value was found
    if any(results):
        st.write("Value found!")
    else:
        st.write("Value not found.")
    
    # Visualize the graph and highlight searched nodes
    colors = []
    for i in range(array_size):
        if any(start <= i < end for start, end, _, _ in ranges):
            colors.append('red')  # Searched nodes
        else:
            colors.append('blue')
    
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, alpha=0.6)
    
    st.pyplot(plt.gcf())

