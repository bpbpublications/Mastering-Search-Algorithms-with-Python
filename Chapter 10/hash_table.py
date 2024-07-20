import streamlit as st
import networkx as nx
import plotly.graph_objects as go

# Initialize session state for hash table if it doesn't exist
if 'hash_table' not in st.session_state:
    st.session_state['hash_table'] = {}

# Streamlit UI
st.title("Hashing-Based Search Application with Graph Visualization")

# User input for key and value
search_key = st.text_input("Enter a key to search or add:", key="search")
value_to_add = st.text_input("Enter a value to add:", key="value")
add_button = st.button("Add Key-Value Pair")

# Button to perform the search
if st.button("Search"):
    hash_table = st.session_state['hash_table']
    if search_key in hash_table:
        st.write(f"Key '{search_key}' found with value: {hash_table[search_key]}")
    else:
        st.write(f"Key '{search_key}' not found in the hash table.")

# Add key-value pair to the hash table
if add_button:
    if search_key and value_to_add:  # Ensure both key and value are provided
        st.session_state['hash_table'][search_key] = value_to_add
        st.write(f"Added key '{search_key}' with value '{value_to_add}' to the hash table.")

# Visualization of the hash table using NetworkX
st.subheader("Graph Visualization of the Hash Table")
G = nx.Graph()
hash_table = st.session_state['hash_table']
for key, value in hash_table.items():
    G.add_node(key, label=key)
    G.add_node(value, label=value)
    G.add_edge(key, value)  # Connect each key to its value

# Generate positions for each node
pos = nx.spring_layout(G)

# Create edge traces for Plotly
edge_trace = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace.append(go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                                 line=dict(width=0.5, color='#888'),
                                 hoverinfo='none', mode='lines'))

# Create node traces for Plotly
node_trace = []
for node in G.nodes():
    x, y = pos[node]
    node_trace.append(go.Scatter(x=[x], y=[y], mode='markers+text', hoverinfo='text',
                                 marker=dict(showscale=True, colorscale='YlGnBu', size=10),
                                 text=node))

# Draw the graph
fig = go.Figure(data=edge_trace + node_trace,
                layout=go.Layout(showlegend=False, hovermode='closest',
                                 margin=dict(b=0, l=0, r=0, t=0),
                                 xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
st.plotly_chart(fig)
