import streamlit as st
import plotly.graph_objects as go
from queue import PriorityQueue
# ... [A* code from above] ...
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

def visualize(grid, start, end, visited=None, path=None):
    fig = go.Figure()

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            color = "white"
            if grid[i][j] == 1:
                color = "blue"
            elif visited and (i, j) in visited:
                color = "lightyellow"
            elif path and (i, j) in path:
                color = "yellow"
            elif (i, j) == start:
                color = "green"
            elif (i, j) == end:
                color = "red"
            
            fig.add_shape(type="rect", x0=j, x1=j+1, y0=i, y1=i+1, line=dict(width=0.5), fillcolor=color)

    fig.update_layout(width=600, height=600, showlegend=False)
    st.plotly_chart(fig)

# Let's use a cache so that grid is retained across runs
@st.cache(allow_output_mutation=True)
def get_grid(size):
    return [[0 for _ in range(size)] for _ in range(size)]

size = st.slider("Choose grid size", 5, 50, 10)
grid = get_grid(size)
start = (0, 0)
end = (size-1, size-1)

# Handle obstacle drawing
click_data = st.session_state.get("click_data", None)
if click_data:
    row, col = int(click_data["points"][0]["y"]), int(click_data["points"][0]["x"])
    grid[row][col] = 1 - grid[row][col]  # Toggle between obstacle and free cell

visualize(grid, start, end)

# Store click data from user for obstacle placement
if st.session_state.get("click_data") is None:
    st.session_state.click_data = None
st.session_state.click_data = st.plotly_click("plotly_chart")

# Run A* and animate
if st.button("Run A*"):
    path = a_star_search(grid, start, end)
    for i in range(1, len(path)+1):
        visualize(grid, start, end, path[:i])
        st.sleep(0.1)
