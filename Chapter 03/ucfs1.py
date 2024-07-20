import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import heapq

# Uniform Cost Search function
def ucs(graph, start, goal):
    visited = set()
    priority_queue = [(0, start, [start])]  # (cumulative cost, current node, path)

    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)
        if node in visited:
            continue

        visited.add(node)
        if node == goal:
            return cost, path

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + weight, neighbor, path + [neighbor]))

    return float('inf'), []  # Goal not reachable

# Streamlit app
def main():
    st.title("Uniform Cost Search Visualization")

    user_input = st.text_input("Enter your graph (e.g. A-B-1,C-3;B-D-4,E-2;C-F-5;D;E;F):")

    graph = {}
    if user_input:
        pairs = user_input.split(';')
        for pair in pairs:
            node_connections = pair.split('-')
            node = node_connections[0]
            graph[node] = []

            # Handling nodes with neighbors
            if len(node_connections) > 1:
                neighbor_connections = node_connections[1:]
                combined_neighbors = '-'.join(neighbor_connections)
                neighbors = combined_neighbors.split(',')

                for neighbor in neighbors:
                    if '-' in neighbor:
                        neighbor_node, weight = neighbor.split('-')
                        graph[node].append((neighbor_node, int(weight)))
                    else:
                        # Handling isolated nodes or nodes without specified edges
                        graph[node].append((neighbor, 0))  # Assuming a default weight, e.g., 0

        # Dropdown for use cases
        use_case = st.selectbox("Select Use Case", ["Find Shortest Path", "Find Path Cost"])

        if use_case and user_input:
            start_node = st.selectbox("Choose a start node", list(graph.keys()))
            end_node = st.selectbox("Choose an end node", list(graph.keys()))

            if st.button("Run UCS"):
                cost, path = ucs(graph, start_node, end_node)

                # Using NetworkX to create a graph object
                G = nx.DiGraph()
                for node, neighbors in graph.items():
                    for neighbor, weight in neighbors:
                        G.add_edge(node, neighbor, weight=weight)

                # Plotting using Plotly
                pos = nx.spring_layout(G)
                edge_x = []
                edge_y = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])

                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='none',
                    mode='lines')

                node_x = []
                node_y = []
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)

                node_trace = go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    text=list(G.nodes()),
                    marker=dict(
                        showscale=True,
                        colorscale='YlGnBu',
                        size=10,
                        color=list(range(len(G.nodes()))),
                        colorbar=dict(
                            thickness=15,
                            title='Node Connections',
                            xanchor='left',
                            titleside='right'
                        ),
                        line_width=2))

                fig = go.Figure(data=[edge_trace, node_trace],
                                layout=go.Layout(
                                    title=f'{use_case} using UCS: Path: {" -> ".join(path)}, Cost: {cost}',
                                    showlegend=False,
                                    hovermode='closest',
                                    margin=dict(b=0, l=0, r=0, t=0),
                                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

                st.plotly_chart(fig)

if __name__ == '__main__':
    main()
