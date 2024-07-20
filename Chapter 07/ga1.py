import streamlit as st
import plotly.graph_objs as go
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

#import random

def initialize_population(population_size, network_structure):
    population = []
    for _ in range(population_size):
        network = {'layers': random.choice(network_structure),
                   'learning_rate': random.uniform(0.001, 0.1)}
        population.append(network)
    return population

def evaluate_networks(population):
    for network in population:
        network['fitness'] = random.uniform(0, 1)  # Simulated fitness

def select_parents(population, num_parents):
    population.sort(key=lambda x: x['fitness'], reverse=True)
    return population[:num_parents]

def crossover(parents, num_children):
    children = []
    while len(children) < num_children:
        parent1, parent2 = random.sample(parents, 2)
        child = {'layers': random.choice([parent1['layers'], parent2['layers']]),
                 'learning_rate': (parent1['learning_rate'] + parent2['learning_rate']) / 2}
        children.append(child)
    return children

def mutate(network):
    mutation_rate = 0.1
    if random.uniform(0, 1) < mutation_rate:
        # Mutate each layer size in the network
        network['layers'] = [max(1, size + random.choice([-1, 1])) for size in network['layers']]
        network['learning_rate'] += random.uniform(-0.01, 0.01)

        # Ensure learning rate remains within a reasonable range
        network['learning_rate'] = min(max(network['learning_rate'], 0.001), 1.0)

def plot_network(network):
    G = nx.DiGraph()
    layer_sizes = network['layers']
    
    # Adding nodes for each layer
    prev_layer_size, node_count = 0, 0
    for i, size in enumerate(layer_sizes):
        for j in range(size):
            node_id = f'Layer {i+1}_Neuron {j+1}'
            G.add_node(node_id)
            if i > 0:
                for k in range(prev_layer_size):
                    G.add_edge(f'Layer {i}_Neuron {k+1}', node_id)
            node_count += 1
        prev_layer_size = size

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()



def genetic_algorithm(population_size, num_generations, network_structure):
    population = initialize_population(population_size, network_structure)

    for _ in range(num_generations):
        evaluate_networks(population)
        parents = select_parents(population, num_parents=2)
        # Ensure that the number of children matches the population size
        children = crossover(parents, num_children=population_size - len(parents))
        for child in children:
            mutate(child)

        # Combine parents and children for the next generation
        population = parents + children

    return population

def main():
    st.title("Neural Network Optimization using Genetic Algorithms")

    population_size = st.sidebar.number_input('Population Size', min_value=1, value=10)
    num_generations = st.sidebar.number_input('Number of Generations', min_value=1, value=10)
    network_structure = [[2, 2], [3, 2], [2, 2, 1]]

    if st.button('Run Genetic Algorithm'):
        final_population = genetic_algorithm(population_size, num_generations, network_structure)
        if final_population:
            best_network = max(final_population, key=lambda x: x.get('fitness', 0))
            st.write("Best network configuration:", best_network)

            # Plotting the best network
            st.write("Visualizing the Best Network Structure:")
            plot_network(best_network)
            st.pyplot(plt)
        else:
            st.write("No network configurations were generated.")

if __name__ == "__main__":
    main()
