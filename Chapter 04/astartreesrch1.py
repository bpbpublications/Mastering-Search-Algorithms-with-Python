import streamlit as st
import plotly.graph_objects as go
import heapq

# ... [Insert the Node class and a_star_tree_search function from the previous example here] ...

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])



def a_star_tree_search(grid, start, end):
    start_node = Node(start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(end)

    open_list = []
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == end_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1]
            )

            if not (0 <= node_position[0] < len(grid)) or not (0 <= node_position[1] < len(grid[0])):
                continue

            if grid[node_position[0]][node_position[1]] == 1:
                continue

            new_node = Node(node_position, current_node)
            children.append(new_node)

        for child in children:
            child.g = current_node.g + 1
            child.h = manhattan_distance(child.position, end_node.position)
            child.f = child.g + child.h
            heapq.heappush(open_list, child)

    return None


def visualize_grid(grid, path=None):
    fig = go.Figure()
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                fig.add_trace(go.Scatter(x=[col], y=[row], marker=dict(color='black', size=20), mode='markers'))

    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        fig.add_trace(go.Scatter(x=path_x, y=path_y, mode='lines+markers', name='Path', line=dict(color='blue')))

    fig.update_layout(title="A* Tree Search Path", xaxis=dict(range=[-1, len(grid[0])]), yaxis=dict(range=[-1, len(grid)]), yaxis_autorange="reversed")
    return fig

st.title("A* Tree Search Visualization")

# Let users define the grid size
grid_size = st.slider("Grid Size", 5, 20, 10)
start = (0, 0)
end = (grid_size-1, grid_size-1)

# Create an empty grid
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Allow users to add obstacles to the grid
obstacle_positions = st.multiselect(
    "Select Obstacle Positions (row, col)",
    [(row, col) for row in range(grid_size) for col in range(grid_size)],
    default=[]
)

for pos in obstacle_positions:
    grid[pos[0]][pos[1]] = 1

# Search for a path
path = a_star_tree_search(grid, start, end)

# Visualize
st.plotly_chart(visualize_grid(grid, path))
