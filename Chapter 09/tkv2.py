import torch
import streamlit as st
import plotly.graph_objs as go
import networkx as nx
from transformers import GPT2Tokenizer, GPT2LMHeadModel
#from transformers import GPT2TokenizerFast


# Load pre-trained model tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def generate_sequence(input_sequence):
    # Encode the input text, adding the attention mask
    inputs = tokenizer.encode_plus(input_sequence, return_tensors='pt', add_special_tokens=True)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']

    # Generate text using the model
    generated_output = model.generate(
        input_ids, 
        attention_mask=attention_mask, 
        max_length=50, 
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode the generated text
    generated_text = tokenizer.decode(generated_output[0], skip_special_tokens=True)
    return generated_text


def create_tree_graph(input_sequence, generated_sequence):
    # Create a directed graph
    G = nx.DiGraph()

    # Split sequences into tokens
    input_tokens = tokenizer.tokenize(input_sequence)
    generated_tokens = tokenizer.tokenize(generated_sequence)

    # Add nodes and edges for the input tokens
    for i in range(len(input_tokens)):
        G.add_node(input_tokens[i])
        if i > 0:
            G.add_edge(input_tokens[i-1], input_tokens[i])

    # Add nodes and edges for the generated tokens
    prev_token = input_tokens[-1] if input_tokens else None
    for token in generated_tokens:
        G.add_node(token)
        if prev_token:
            G.add_edge(prev_token, token)
        prev_token = token

    # Position nodes using a tree layout
    pos = nx.spring_layout(G, seed=42)

    # Create trace for nodes
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        text=[node for node in G.nodes()],
        textposition="top center",
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='blue',
            size=10,
            line_width=2))

    # Create trace for edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create the plot
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig

# Streamlit app
st.title("Token Prediction and Sequence Generation with Tree Graph Visualization")

user_input = st.text_area("Enter a sequence:", "The quick brown fox")

if st.button("Generate Sequence"):
    generated_sequence = generate_sequence(user_input)
    st.write(generated_sequence)

    # Create and display the tree graph
    fig = create_tree_graph(user_input, generated_sequence)
    st.plotly_chart(fig)
