# ... [Required imports and the modified Node class here] ...
import streamlit as st
import plotly.graph_objects as go
import heapq
class Node:
    def __init__(self, position: tuple, parent: 'Node' = None):
        self.position = position
        self.parent = parent

        self.g = 0  # Cost from start to this node
        self.h = 0  # Heuristic cost from this node to goal
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"({self.position}, g={self.g}, h={self.h}, f={self.f})"

def manhattan_distance_3d(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2])

#def a_star_tree_search_3d(grid, start, end):
    # ... [The same A* logic, but modified for 3D space] ...

def a_star_tree_search_3d(grid, start, end):
    start_node = Node(start)
    start_node.g = 0
    start_node.h = manhattan_distance_3d(start, end)
    start_node.f = start_node.g + start_node.h
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

        for new_position in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]:
            node_position = (
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1],
                current_node.position[2] + new_position[2]
            )

            if not (0 <= node_position[0] < len(grid)) or not (0 <= node_position[1] < len(grid[0])) or not (0 <= node_position[2] < len(grid[0][0])):
                continue

            if grid[node_position[0]][node_position[1]][node_position[2]] == 1:
                continue

            new_node = Node(node_position, current_node)
            children.append(new_node)

        for child in children:
            child.g = current_node.g + 1
            child.h = manhattan_distance_3d(child.position, end_node.position)
            child.f = child.g + child.h
            heapq.heappush(open_list, child)

    return None


def visualize_grid_3d(grid, path=None):
    fig = go.Figure()

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for z in range(len(grid[0][0])):
                if grid[x][y][z] == 1:
                    fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', marker=dict(color='black', size=10)))

    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        path_z = [p[2] for p in path]
        fig.add_trace(go.Scatter3d(x=path_x, y=path_y, z=path_z, mode='lines+markers', line=dict(color='blue')))

    fig.update_layout(title="A* Tree Search Path in 3D")
    return fig

# ... [The Streamlit interface for 3D input] ...

# ... [Required imports, Node class, a_star_tree_search_3d, and visualize_grid_3d functions from the previous sections] ...

st.title("A* Tree Search Visualization in 3D")

# Let users define the grid size for each dimension
grid_width = st.slider("Grid Width", 5, 10, 5)
grid_height = st.slider("Grid Height", 5, 10, 5)
grid_depth = st.slider("Grid Depth", 5, 10, 5)

start = (0, 0, 0)
end = (grid_width-1, grid_height-1, grid_depth-1)

# Create an empty 3D grid (a cube)
grid = [[[0 for _ in range(grid_depth)] for _ in range(grid_height)] for _ in range(grid_width)]

# Allow users to add obstacles to the grid in 3D space
obstacle_positions = st.multiselect(
    "Select Obstacle Positions (x, y, z)",
    [(x, y, z) for x in range(grid_width) for y in range(grid_height) for z in range(grid_depth)],
    default=[]
)

for pos in obstacle_positions:
    grid[pos[0]][pos[1]][pos[2]] = 1

# Search for a path in the 3D grid
path = a_star_tree_search_3d(grid, start, end)

# Visualize in 3D
st.plotly_chart(visualize_grid_3d(grid, path))
