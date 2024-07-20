import streamlit as st
import networkx as nx
import plotly.graph_objects as go

# Dijkstra's algorithm implementation
def dijkstra(graph, start):
    visited = {node: float('infinity') for node in graph.nodes}
    path = {}
    visited[start] = 0
    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if min_node is None or visited[node] < visited[min_node]:
                min_node = node

        if visited[min_node] == float('infinity'):
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges(min_node, data=True):
            weight = current_weight + edge[2]['weight']
            if weight < visited[edge[1]]:
                visited[edge[1]] = weight
                path[edge[1]] = min_node

    return visited, path
# Function to create a graph from user input
def create_graph(edge_list):
    G = nx.DiGraph()
    for edge in edge_list:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    # Assign positions to each node for visualization
    pos = nx.spring_layout(G)  # This line assigns positions using the spring layout
    for node, p in pos.items():
        G.nodes[node]['pos'] = p
    return G

# Function to visualize the graph
# Function to visualize the graph
def plot_graph(graph, path=None):
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = graph.nodes[edge[0]]['pos']
        x1, y1 = graph.nodes[edge[1]]['pos']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = graph.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(showscale=True, colorscale='YlGnBu', size=10))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40)))

    st.plotly_chart(fig, use_container_width=True)

st.title('Dijkstra\'s Algorithm Visualization')

# User input for edges and weights
user_input = st.text_area("Enter the graph edges and weights (format: node1,node2,weight):", 
                          "A,B,4\nB,C,1\nA,C,2\nC,D,4\nB,D,5")

# Parsing user input to create edges
edges = []
for line in user_input.split('\n'):
    if line:
        node1, node2, weight = line.split(',')
        edges.append((node1.strip(), node2.strip(), int(weight)))

# Proceed only if edges are provided
if edges:
    # Start and end nodes for path finding
    start_node = st.text_input("Enter the start node:", "A")
    end_node = st.text_input("Enter the end node:", "D")

    # Creating the graph
    graph = create_graph(edges)

    # Visualize the graph
    plot_graph(graph)

    if st.button('Calculate Shortest Path'):
        distances, paths = dijkstra(graph, start_node)
        st.write(f"Shortest distance from {start_node} to {end_node}: {distances[end_node]}")
        st.write(f"Path: {paths[end_node]}")

        # Complexity information
        st.markdown("### Asymptotic Complexity of Dijkstra's Algorithm:")
        st.markdown("""
            - **Time Complexity**: O(V^2), but can be improved to O(V + E log V) with a min-priority queue.
            - **Space Complexity**: O(V)
            - **V**: Number of vertices, **E**: Number of edges
            - **Explanation**: The algorithm iteratively explores vertices, updating distances.
        """)
