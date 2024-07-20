import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import numpy as np
import random

# Define the Ant class
class Ant:
    def __init__(self, start_node):
        self.current_node = start_node
        self.path = [start_node]

    def move_to(self, node):
        self.path.append(node)
        self.current_node = node

    def get_path_length(self, graph):
        length = 0
        for i in range(1, len(self.path)):
            length += graph[self.path[i-1]][self.path[i]]['weight']
        return length

# ACO algorithm
def ant_colony_optimization(graph, n_ants, n_iterations, alpha, beta, evaporation_rate):
    all_paths = []
    for _ in range(n_iterations):
        ants = [Ant(start_node=random.choice(list(graph.nodes))) for _ in range(n_ants)]
        for ant in ants:
            for _ in range(len(graph.nodes) - 1):
                next_node = choose_next_node(graph, ant.current_node, alpha, beta)
                ant.move_to(next_node)

            all_paths.append((ant.path, ant.get_path_length(graph)))

        update_pheromones(graph, all_paths, evaporation_rate)
    return min(all_paths, key=lambda x: x[1])

def choose_next_node(graph, current_node, alpha, beta):
    neighbors = list(graph.neighbors(current_node))
    probabilities = [transition_probability(graph, current_node, neighbor, alpha, beta) for neighbor in neighbors]
    return random.choices(neighbors, weights=probabilities)[0]

def transition_probability(graph, current_node, next_node, alpha, beta):
    pheromone = graph[current_node][next_node]['pheromone']
    weight = graph[current_node][next_node]['weight']
    return (pheromone ** alpha) * ((1 / weight) ** beta)

def update_pheromones(graph, all_paths, evaporation_rate):
    for edge in graph.edges:
        graph[edge[0]][edge[1]]['pheromone'] *= (1 - evaporation_rate)

    for path, length in all_paths:
        for i in range(len(path) - 1):
            graph[path[i]][path[i+1]]['pheromone'] += 1 / length

# Initialize Graph
def create_graph():
    G = nx.Graph()
    G.add_edge('A', 'B', weight=2, pheromone=1)
    G.add_edge('B', 'C', weight=2, pheromone=1)
    G.add_edge('C', 'D', weight=2, pheromone=1)
    G.add_edge('A', 'D', weight=3, pheromone=1)
    G.add_edge('B', 'D', weight=1, pheromone=1)

    # Define positions
    pos = {
        'A': (0, 0),
        'B': (1, 1),
        'C': (2, 0),
        'D': (1, -1)
    }

    # Set positions in the graph
    for node in G.nodes:
        G.nodes[node]['pos'] = pos[node]

    return G


# Streamlit UI
st.title("Ant Colony Optimization Demo")

n_ants = st.slider("Number of Ants", 1, 100, 10)
n_iterations = st.slider("Number of Iterations", 1, 100, 20)
alpha = st.slider("Alpha", 0.1, 5.0, 1.0)
beta = st.slider("Beta", 0.1, 5.0, 1.0)
evaporation_rate = st.slider("Evaporation Rate", 0.01, 0.99, 0.5)

graph = create_graph()

if st.button("Run Ant Colony Optimization"):
    best_path, best_length = ant_colony_optimization(graph, n_ants, n_iterations, alpha, beta, evaporation_rate)
    st.write(f"Best path: {best_path} with length {best_length}")

    # Visualize the graph
    fig = go.Figure()

    for edge in graph.edges():
        x0, y0 = graph.nodes[edge[0]]['pos']
        x1, y1 = graph.nodes[edge[1]]['pos']
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines+markers', name=f"Edge {edge}"))

    st.plotly_chart(fig)
