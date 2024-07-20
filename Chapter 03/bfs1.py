import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from collections import deque

def bfs(graph, start, end=None):
    visited = set()
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node in visited:
            continue
        if node in graph:  # Check if node is in graph
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor == end:
                    return new_path
        visited.add(node)
    return None if end else visited

def main():
    st.title("Breadth First Search Visualization")

    # Sample input format: A-B,C;B-D,E;C-F
    user_input = st.text_input("Enter your graph (e.g. A-B,C;B-D,E;C-F):")
    
    graph = {}
    if user_input:
        pairs = user_input.split(';')
        nodes = set()
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

        st.sidebar.title("BFS Options")
        start_node = st.sidebar.selectbox("Choose a start node", list(graph.keys()))
        bfs_type = st.sidebar.selectbox("Select BFS Type", ["Traversal", "Shortest Path"])
        end_node = None
        if bfs_type == "Shortest Path":
            end_node = st.sidebar.selectbox("Choose an end node", [node for node in graph.keys() if node != start_node])

        if st.sidebar.button("Run BFS"):
            result = bfs(graph, start_node, end_node)

            G = nx.Graph()
            for node, neighbors in graph.items():
                for neighbor in neighbors:
                    G.add_edge(node, neighbor)

            # Visualization
            pos = nx.spring_layout(G)
            edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.5, color='#888'), mode='lines')
            node_trace = go.Scatter(x=[], y=[], mode='markers+text', text=[], marker=dict(showscale=True, colorscale='YlGnBu', size=10, colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right'), line_width=2))

            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_trace['x'] += tuple([x0, x1, None])
                edge_trace['y'] += tuple([y0, y1, None])

            for node in G.nodes():
                x, y = pos[node]
                node_trace['x'] += tuple([x])
                node_trace['y'] += tuple([y])
                node_trace['text'] += tuple([node])

            fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(showlegend=False, hovermode='closest', margin=dict(b=0, l=0, r=0, t=40), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

            if bfs_type == "Traversal":
                fig.update_layout(title_text="BFS Traversal Order: " + ' -> '.join(result))
            else:
                fig.update_layout(title_text="Shortest Path using BFS: " + ' -> '.join(result) if result else "No path found!")

            st.plotly_chart(fig)

if __name__ == '__main__':
    main()
