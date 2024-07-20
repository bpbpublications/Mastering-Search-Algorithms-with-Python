import streamlit as st
import plotly.graph_objects as go

# Greedy function for Activity Selection Problem
def activity_selection(start, finish):
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    n = len(activities)
    i = 0
    selected = [i]

    for j in range(1, n):
        if activities[j][0] >= activities[i][1]:
            selected.append(j)
            i = j
            
    return selected, activities

st.title("Greedy Algorithm - Activity Selection Problem")

# Input for start and finish times
start = st.sidebar.text_input("Start times (comma separated)", "1, 3, 0, 5, 8, 5")
finish = st.sidebar.text_input("Finish times (comma separated)", "2, 4, 6, 7, 9, 9")

start = [int(s.strip()) for s in start.split(",")]
finish = [int(f.strip()) for f in finish.split(",")]

selected, activities = activity_selection(start, finish)

# Plotly Visualization
fig = go.Figure()

for idx, (s, f) in enumerate(activities):
    color = "blue" if idx in selected else "red"
    fig.add_shape(type="rect", x0=s, x1=f, y0=idx-0.4, y1=idx+0.4, line=dict(color=color), fillcolor=color)
    fig.add_trace(go.Scatter(x=[(s+f)/2], y=[idx], text=f"Activity {idx}", mode="text"))

fig.update_layout(title="Activity Selection", xaxis_title="Time", yaxis_title="Activities", showlegend=False)
st.plotly_chart(fig)
