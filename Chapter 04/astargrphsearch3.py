import streamlit as st
import plotly.graph_objects as go
from queue import PriorityQueue

# ... [Your A* implementation goes here] ...

import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


def get_neighbors(node, grid):
    neighbors = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        node_position = (node.position[0] + new_position[0], node.position[1] + new_position[1])
        if 0 <= node_position[0] < len(grid) and 0 <= node_position[1] < len(grid[0]) and grid[node_position[0]][node_position[1]] == 0:
            neighbors.append(Node(node_position))
    return neighbors


def heuristic(node, end_node):
    return abs(node.position[0] - end_node.position[0]) + abs(node.position[1] - end_node.position[1])


def a_star_search(grid, start, end):
    start_node = Node(start)
    end_node = Node(end)

    open_list = []
    closed_list = []

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        neighbors = get_neighbors(current_node, grid)

        for neighbor in neighbors:
            if neighbor in closed_list:
                continue
            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor, end_node)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.parent = current_node

            if neighbor in open_list:
                for node in open_list:
                    if node == neighbor and node.g > neighbor.g:
                        node.g = neighbor.g
                        node.f = node.g + node.h
                        node.parent = current_node
            else:
                heapq.heappush(open_list, neighbor)

    return None



def visualize(grid, start, end, path=None):
    # Create a blank plotly figure
    fig = go.Figure()

    # Draw the grid, start and end points, obstacles, and the path
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                fig.add_shape(type="rect", x0=i, y0=j, x1=i+1, y1=j+1, fillcolor="blue")
            elif (i, j) == start:
                fig.add_shape(type="circle", x0=i, y0=j, x1=i+1, y1=j+1, fillcolor="green")
            elif (i, j) == end:
                fig.add_shape(type="circle", x0=i, y0=j, x1=i+1, y1=j+1, fillcolor="red")

    if path:
        for node in path:
            fig.add_shape(type="circle", x0=node[0], y0=node[1], x1=node[0]+1, y1=node[1]+1, fillcolor="yellow")

    st.plotly_chart(fig)


st.title("A* Graph Search Visualization")

# Choose grid size
size = st.slider("Choose grid size", 5, 50, 10)

# Allow the user to select start, end, and obstacles
start = st.selectbox("Select Start Point", [(i, j) for i in range(size) for j in range(size)])
end = st.selectbox("Select End Point", [(i, j) for i in range(size) for j in range(size)], index=size*size-1)

# Run the A* algorithm
if st.button("Run A*"):
    grid = [[0 for _ in range(size)] for _ in range(size)]
    path = a_star_search(grid, start, end)
    visualize(grid, start, end, path)
