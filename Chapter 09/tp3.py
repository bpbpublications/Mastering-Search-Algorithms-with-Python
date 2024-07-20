import os
import torch
os.environ["BITSANDBYTES_NOWELCOME"] = "1"
os.environ["BITSANDBYTES_FORCE_FP16_MIXED_PREC"] = "0"
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

# Model Selection 
model_name = "EleutherAI/gpt-neo-125M" 

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


def generate_sequence(input_sequence):
    """Generates a text sequence using the chosen model."""
    
    class StopOnTokens(StoppingCriteria):
        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
            return input_ids[0][-1] in [tokenizer.eos_token_id]  # Stop on EOS

    stopping_criteria = StoppingCriteriaList([StopOnTokens()])

    input_ids = tokenizer(input_sequence, return_tensors="pt").input_ids.to(device)
    output = model.generate(
        input_ids=input_ids,
        max_length=50,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        stopping_criteria=stopping_criteria,
        return_dict_in_generate=True,  # Return detailed output dictionary
        output_scores=True,            # Get raw token scores
    )

    generated_text = tokenizer.decode(output.sequences[0], skip_special_tokens=True)  # Use output.sequences

    # Extract token scores using logits and softmax
    token_scores = []
    for logits in output.scores:
        probs = torch.nn.functional.softmax(logits, dim=-1)
        chosen_token_prob = probs[0, output.sequences[0][len(token_scores)]].item()
        token_scores.append(chosen_token_prob)

    return generated_text, token_scores




def create_tree_graph(input_sequence, generated_sequence, token_scores):
    """Creates a Plotly tree graph visualization of the token sequences with scores."""
    G = nx.DiGraph()

    for tokens in [input_sequence.split(), generated_sequence.split()]:
        for i in range(len(tokens) - 1):
            G.add_edge(tokens[i], tokens[i + 1])

    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])  
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

    node_labels = {}
    for i, node in enumerate(G.nodes()):
        token_index = generated_sequence.split().index(node) if node in generated_sequence.split() else None
        # Remove .item() as token_scores is a list of floats
        score = token_scores[token_index] if token_index is not None else 0
        node_labels[node] = f"{node} ({score:.3f})"

    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        text=[node_labels[node] for node in G.nodes()],
        textposition="top center",
        hoverinfo='text',
        marker=dict(size=10, color=[], line_width=2),
    )

    # Explicitly create a Figure object and then pass it to st.plotly_chart
    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        title='Tree Graph of Token Sequences',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    ))

    return fig  # Return the Figure object

# --- Streamlit App ---
st.title("Token Prediction and Sequence Generation with Tree Graph Visualization (Open Source Model)")
user_input = st.text_area("Enter a sequence:", "The quick brown fox")

if st.button("Generate Sequence"):
    with st.spinner("Generating..."):
        generated_sequence, token_scores = generate_sequence(user_input)

        st.subheader("Generated Sequence:")
        st.write(generated_sequence)

        st.subheader("Tree Graph:")
        fig = create_tree_graph(user_input, generated_sequence, token_scores)
        st.plotly_chart(fig)  # Pass the Figure object directly
