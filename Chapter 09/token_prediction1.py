import torch
import streamlit as st
import plotly.express as px
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load pre-trained model tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def generate_sequence_with_logits(input_sequence):
    # Encode the input text
    input_ids = tokenizer.encode(input_sequence, return_tensors='pt')

    # Get model output including logits
    outputs = model(input_ids, return_dict=True)
    logits = outputs.logits

    # Generate text using the model
    generated_output = model.generate(input_ids, max_length=50, num_return_sequences=1)

    # Decode the generated text
    generated_text = tokenizer.decode(generated_output[0], skip_special_tokens=True)

    return generated_text, logits

def visualize_token_probabilities(logits, input_sequence):
    # Extract the logits for the last token and apply softmax to get probabilities
    last_token_logits = logits[0, -1, :]
    probabilities = torch.nn.functional.softmax(last_token_logits, dim=0).detach().numpy()

    # Get the most probable next tokens
    top_tokens = torch.topk(last_token_logits, 10, dim=0).indices.numpy()
    labels = [tokenizer.decode([token]) for token in top_tokens]

    # Create a bar chart
    fig = px.bar(x=labels, y=probabilities[top_tokens], labels={'x': 'Next Token', 'y': 'Probability'})
    return fig

# Streamlit app
st.title("Token Prediction and Sequence Generation Demo")

user_input = st.text_area("Enter a sequence:", "The quick brown fox")

if st.button("Generate Sequence"):
    generated_sequence, logits = generate_sequence_with_logits(user_input)
    st.write(generated_sequence)

    # Visualize token probabilities
    fig = visualize_token_probabilities(logits, user_input)
    st.plotly_chart(fig)
