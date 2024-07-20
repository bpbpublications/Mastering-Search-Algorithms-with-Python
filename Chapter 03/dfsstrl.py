import streamlit as st
import plotly.graph_objects as go
import networkx as nx

# DFS logic
def dfs(graph, node, visited=None):
    if visited is None:
        visited = []
    if node not in visited:
        visited.append(node)
        for neighbor in graph[node]:
            dfs(graph, neighbor, visited)
    return visited




# Streamlit app
def main():
    st.title("Depth First Search Visualization")

    # Sample input format: A-B,C;B-D,E;C-F
    user_input = st.text_input("Enter your graph (e.g. A-B,C;B-D,E;C-F):")
    
    # Parsing user input to adjacency list
    # Initialize an empty graph
    graph = {}

    # Parsing user input to adjacency list
    if user_input:
        pairs = user_input.split(';')
        nodes = set()  # Set to hold all unique nodes

        # First, gather all nodes
        for pair in pairs:
            node, neighbors_str = pair.split('-')
            neighbors = neighbors_str.split(',')
            nodes.add(node)
            nodes.update(neighbors)

        # Initialize each node in the graph
        for node in nodes:
            graph[node] = []

        # Now, process the connections
        for pair in pairs:
            node, neighbors_str = pair.split('-')
            neighbors = neighbors_str.split(',')
            graph[node].extend(neighbors)

        start_node = st.selectbox("Choose a start node for DFS", list(graph.keys()))
        if st.button("Run DFS"):
            visited_order = dfs(graph, start_node)

            # Using networkx to create a graph object
            G = nx.Graph()
            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    G.add_edge(node, neighbor)
            
            # Plotting using plotly
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
                    colorbar=dict(
                        thickness=15,
                        title='Node Connections',
                        xanchor='left',
                        titleside='right'
                    ),
                    line_width=2))

            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title='DFS Traversal Order: ' + ' -> '.join(visited_order),
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=0, l=0, r=0, t=40),
                                annotations=[
                                    dict(
                                        showarrow=False,
                                        xref="paper", yref="paper",
                                        x=0.005, y=-0.002)
                                ],
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                            )
            st.plotly_chart(fig)

if __name__ == '__main__':
    main()
