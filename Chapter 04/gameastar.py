import streamlit as st
import plotly.graph_objects as go
from heapq import heappush, heappop

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to this node
        self.h = 0  # Heuristic cost estimate to end
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, end_node):
    return abs(node.position[0] - end_node.position[0]) + abs(node.position[1] - end_node.position[1])

def get_neighbors(node, grid):
    neighbors = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
        node_position = (node.position[0] + new_position[0], node.position[1] + new_position[1])
        if 0 <= node_position[0] < len(grid) and 0 <= node_position[1] < len(grid[0]) and grid[node_position[0]][node_position[1]] == 0:
            neighbors.append(Node(node_position))
    return neighbors

def a_star_search(grid, start, end):
    start_node = Node(start)
    end_node = Node(end)
    open_list = []
    heappush(open_list, start_node)
    closed_list = set()

    while open_list:
        current_node = heappop(open_list)
        closed_list.add(current_node)

        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for neighbor in get_neighbors(current_node, grid):
            if neighbor in closed_list:
                continue

            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor, end_node)
            neighbor.f = neighbor.g + neighbor.h

            if any(neighbor == open_node and neighbor.g > open_node.g for open_node in open_list):
                continue

            heappush(open_list, neighbor)

    return None

def visualize(grid, start, end, path=None):
    fig = go.Figure()

    # Draw the grid
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            color = 'white'
            if grid[row][col] == 1:
                color = 'black'  # Obstacle color
            elif (row, col) == start:
                color = 'green'  # Start color
            elif (row, col) == end:
                color = 'red'    # End color
            fig.add_shape(type='rect', x0=col, y0=row, x1=col+1, y1=row+1, line=dict(color=color), fillcolor=color)

    # Draw the path
    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        fig.add_trace(go.Scatter(x=path_x, y=path_y, mode='lines', name='Path', line=dict(color='blue', width=2)))

    fig.update_layout(title_text='A* Pathfinding', xaxis_showgrid=False, yaxis_showgrid=False,
                      xaxis_zeroline=False, yaxis_zeroline=False, yaxis_autorange='reversed')
    st.plotly_chart(fig, use_container_width=True)

# Streamlit app:
st.title("A* Pathfinding Simulation")

size = st.slider("Choose grid size", 5, 50, 10)
start = st.selectbox("Select Start Point", [(i, j) for i in range(size) for j in range(size)])
end = st.selectbox("Select End Point", [(i, j) for i in range(size) for j in range(size)], index=size*size-1)

# Allow the user to add obstacles:
obstacles = st.multiselect("Select Obstacles", [(i, j) for i in range(size) for j in range(size) if (i, j) != start and (i, j) != end])

if st.button("Run A*"):
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for obstacle in obstacles:
        grid[obstacle[0]][obstacle[1]] = 1
    path = a_star_search(grid, start, end)
    visualize(grid, start, end, path)
