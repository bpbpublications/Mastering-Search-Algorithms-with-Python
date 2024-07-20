import streamlit as st
import plotly.graph_objects as go
from collections import deque



class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = {vertex: [] for vertex in range(self.vertices)}
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    def bidirectional_search(self, start, target):
        if start == target:
            return [start]
        visited_from_start = {start}
        visited_from_goal = {target}
        queue_from_start = deque([start])
        queue_from_goal = deque([target])
        # Maintain parent pointers to reconstruct path
        parent_start = {}
        parent_goal = {}
        while queue_from_start and queue_from_goal:
            # Forward search from start
            current_start = queue_from_start.popleft()
            for neighbor in self.graph[current_start]:
                if neighbor in visited_from_goal:
                    path = [neighbor, current_start]
                    while parent_start.get(current_start):
                        current_start = parent_start[current_start]
                        path.insert(1, current_start)
                    current_goal = neighbor
                    while parent_goal.get(current_goal):
                        current_goal = parent_goal[current_goal]
                        path.append(current_goal)
                    return path
                if neighbor not in visited_from_start:
                    visited_from_start.add(neighbor)
                    queue_from_start.append(neighbor)
                    parent_start[neighbor] = current_start
            # Backward search from goal
            current_goal = queue_from_goal.popleft()
            for neighbor in self.graph[current_goal]:
                if neighbor in visited_from_start:
                    path = [neighbor, current_goal]
                    while parent_goal.get(current_goal):
                        current_goal = parent_goal[current_goal]
                        path.append(current_goal)
                    current_start = neighbor
                    while parent_start.get(current_start):
                        current_start = parent_start[current_start]
                        path.insert(0, current_start)
                    return path
                if neighbor not in visited_from_goal:
                    visited_from_goal.add(neighbor)
                    queue_from_goal.append(neighbor)
                    parent_goal[neighbor] = current_goal
        return None

# Create a sample graph
g = Graph(15)
g.addEdge(0, 4)
g.addEdge(1, 4)
g.addEdge(2, 5)
g.addEdge(3, 5)
g.addEdge(4, 6)
g.addEdge(5, 6)
g.addEdge(6, 7)
g.addEdge(7, 8)
g.addEdge(8, 9)
g.addEdge(8, 10)
g.addEdge(9, 11)
g.addEdge(9, 12)
g.addEdge(10, 13)
g.addEdge(10, 14)

# Streamlit app
st.title("Bidirectional Search with Streamlit and Plotly")

start = st.number_input("Enter start node:", min_value=0, max_value=14, value=0, step=1)
goal = st.number_input("Enter goal node:", min_value=0, max_value=14, value=14, step=1)

if st.button("Search"):
    path = g.bidirectional_search(start, goal)
    st.write(f"Found path: {path}")

    edge_x = []
    edge_y = []
    for edge in g.graph.items():
        for end in edge[1]:
            edge_x.extend([edge[0], end, None])
            edge_y.extend([edge[0], end, None])

    node_x = list(g.graph.keys())
    node_y = list(g.graph.keys())

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, line=dict(width=0.5, color="#888"), hoverinfo="none", mode="lines"
    )

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text", hoverinfo="text", marker=dict(showscale=True, colorscale="YlGnBu", size=10, colorbar=dict(thickness=15, title="Node Connections", xanchor="left")),
        text=list(g.graph.keys()), textposition="top center"
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(showlegend=False, hovermode="closest", margin=dict(t=0, b=0, l=0, r=0), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )

    st.plotly_chart(fig)

