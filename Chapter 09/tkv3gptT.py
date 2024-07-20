import torch
import streamlit as st
import plotly.graph_objs as go
import networkx as nx

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    StoppingCriteria,
    StoppingCriteriaList,
)

# Choose a model from Hugging Face (examples below)
model_name = "EleutherAI/gpt-neo-125M"  # Smaller, faster model

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
generator = pipeline('text-generation', model=model, tokenizer=tokenizer, device=device)

def generate_sequence(input_sequence):
    """Generates a text sequence using the chosen open-source model."""

    class StopOnTokens(StoppingCriteria):
        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
            for stop_id in [tokenizer.eos_token_id]:  # Stop on end-of-sentence
                if input_ids[0][-1] == stop_id:
                    return True
            return False

    stopping_criteria = StoppingCriteriaList([StopOnTokens()])

    sequence = generator(
        input_sequence, 
        max_length=50, 
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        stopping_criteria=stopping_criteria
    )

    generated_text = sequence[0]["generated_text"]
    return generated_text

def create_tree_graph(input_sequence, generated_sequence):
    """Creates a Plotly tree graph visualization of the token sequences."""
    G = nx.DiGraph()

    # Adding nodes and edges for input sequence
    input_tokens = input_sequence.split()
    for i in range(len(input_tokens) - 1):
        G.add_edge(input_tokens[i], input_tokens[i + 1])
    
    # Adding nodes and edges for generated sequence
    generated_tokens = generated_sequence.split()
    for i in range(len(generated_tokens) - 1):
        G.add_edge(generated_tokens[i], generated_tokens[i + 1])

    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_x.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            size=10,
            color=[],
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Tree Graph of Token Sequences',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Tree graph",
                            showarrow=False,
                            xref="paper", yref="paper")],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    return fig

# Streamlit app
st.title("Token Prediction and Sequence Generation with Tree Graph Visualization (Open Source Model)")
user_input = st.text_area("Enter a sequence:", "The quick brown fox")

if st.button("Generate Sequence"):
    generated_sequence = generate_sequence(user_input)
    st.write(generated_sequence) # Display generated_sequence
    fig = create_tree_graph(user_input, generated_sequence)
    st.plotly_chart(fig)
