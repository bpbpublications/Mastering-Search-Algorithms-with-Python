import streamlit as st
import plotly.graph_objects as go
from queue import PriorityQueue

class Node:
    def __init__(self, index_seq1, index_seq2, g, h, prev_node=None):
        self.index_seq1 = index_seq1
        self.index_seq2 = index_seq2
        self.g = g
        self.h = h
        self.f = g + h
        self.prev_node = prev_node

    def __lt__(self, other):
        return self.f < other.f

def heuristic(seq1_idx, seq2_idx, seq1, seq2):
    remaining_seq1 = len(seq1) - seq1_idx
    remaining_seq2 = len(seq2) - seq2_idx
    return abs(remaining_seq1 - remaining_seq2)

def a_star_rna_alignment(seq1, seq2, match_score=1, mismatch_score=-1, gap_score=-1):
    open_nodes = PriorityQueue()

    start_node = Node(0, 0, 0, heuristic(0, 0, seq1, seq2))
    open_nodes.put(start_node)
    closed_nodes = []

    while not open_nodes.empty():
        current_node = open_nodes.get()

        # Check for goal state
        if current_node.index_seq1 == len(seq1) and current_node.index_seq2 == len(seq2):
            # Reconstruct path
            path = []
            while current_node:
                path.append((current_node.index_seq1, current_node.index_seq2))
                current_node = current_node.prev_node
            return path[::-1]

        closed_nodes.append(current_node)

        for dx, dy in [(0, 1), (1, 0), (1, 1)]:
            new_seq1_idx = current_node.index_seq1 + dx
            new_seq2_idx = current_node.index_seq2 + dy

            if 0 <= new_seq1_idx <= len(seq1) and 0 <= new_seq2_idx <= len(seq2):
                if dx == dy == 1:
                    cost = match_score if seq1[new_seq1_idx - 1] == seq2[new_seq2_idx - 1] else mismatch_score
                else:
                    cost = gap_score

                new_node = Node(new_seq1_idx, new_seq2_idx, current_node.g + cost, heuristic(new_seq1_idx, new_seq2_idx, seq1, seq2), current_node)
                if new_node not in closed_nodes:
                    open_nodes.put(new_node)

    return None

def visualize_alignment(seq1, seq2, alignment):
    z = []
    for i in range(len(seq1) + 1):
        row = []
        for j in range(len(seq2) + 1):
            if (i, j) in alignment:
                if i == 0 or j == 0:
                    row.append(0.5)  # gray
                elif seq1[i - 1] == seq2[j - 1]:
                    row.append(1)  # green for match
                else:
                    row.append(0)  # red for mismatch
            else:
                row.append(None)
        z.append(row)

    fig = go.Figure(data=go.Heatmap(z=z,
                                    colorscale=[[0, 'red'], [0.5, 'gray'], [1, 'green']],
                                    hoverongaps=False))
    fig.update_layout(title="RNA Sequence Alignment")
    return fig


st.title("RNA Sequence Alignment using A*")

seq1 = st.text_input("Enter the first RNA sequence:")
seq2 = st.text_input("Enter the second RNA sequence:")

if st.button("Align Sequences"):
    alignment = a_star_rna_alignment(seq1, seq2)
    if alignment:
        st.write("Sequences Aligned!")
        st.plotly_chart(visualize_alignment(seq1, seq2, alignment))
    else:
        st.write("Failed to align the sequences.")

