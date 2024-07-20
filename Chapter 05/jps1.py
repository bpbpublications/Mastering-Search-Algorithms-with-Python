import streamlit as st
import plotly.graph_objects as go

class Node:
    def __init__(self, x, y, cost=float('inf'), prev=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.prev = prev
        self.heuristic = 0

    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def heuristic(node, end):
    return abs(node.x - end.x) + abs(node.y - end.y)

def jump_point_search(grid, start, end):
    open_list = [start]
    closed_list = []

    start.cost = 0
    start.heuristic = heuristic(start, end)

    while open_list:
        current = min(open_list, key=lambda x: x.cost + x.heuristic)
        if current == end:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.prev
            return path[::-1]

        open_list.remove(current)
        closed_list.append(current)

        neighbors = get_successors(current, grid)
        for neighbor in neighbors:
            if neighbor in closed_list:
                continue
            tentative_g = current.cost + 1
            if neighbor not in open_list or tentative_g < neighbor.cost:
                neighbor.prev = current
                neighbor.cost = tentative_g
                neighbor.heuristic = heuristic(neighbor, end)
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None  # No path found

def get_successors(node, grid):
    successors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dx, dy in directions:
        next_x, next_y = node.x + dx, node.y + dy
        if is_valid(next_x, next_y, grid):
            successors.append(Node(next_x, next_y))

    return successors

def is_valid(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[y][x] != 1  # 1 represents an obstacle

def visualize_grid(grid, path=[]):
    """Visualize the grid with Plotly."""
    fig = go.Figure()

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            color = 'white'
            if cell == 1:  # obstacle
                color = 'black'
            elif (j, i) in path:  # Notice the inversion for row-col vs x-y
                color = 'blue'
            fig.add_trace(go.Scatter(x=[j], y=[-i], 
                                     marker=dict(size=10, color=color),
                                     mode='markers'))

    fig.update_layout(showlegend=False, 
                      xaxis=dict(range=[-1, len(grid[0])], showgrid=False),
                      yaxis=dict(range=[-len(grid), 1], showgrid=False),
                      plot_bgcolor='rgba(0,0,0,0)')
    st.write(fig)

# Streamlit UI elements
st.title('Jump Point Search Visualization')

# Define grid size
grid_size = st.slider("Select grid size:", 5, 25, 10)
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Let user define obstacles, start, and end points
selected_cells = st.multiselect('Select obstacles (row, column):', 
                                [(i, j) for i in range(grid_size) for j in range(grid_size)])
for cell in selected_cells:
    grid[cell[0]][cell[1]] = 1

start = st.selectbox('Select start point:', [(i, j) for i in range(grid_size) for j in range(grid_size)])
end = st.selectbox('Select end point:', [(i, j) for i in range(grid_size) for j in range(grid_size)], index=1)

if st.button('Execute JPS'):
    start_node = Node(start[1], start[0])  # Notice the inversion for row-col vs x-y
    end_node = Node(end[1], end[0])
    path = jump_point_search(grid, start_node, end_node)
    visualize_grid(grid, path)
else:
    visualize_grid(grid)
