import streamlit as st
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch
from transformers import Trainer
# Function to update Streamlit interface during training
def update_streamlit_progress(epoch, loss):
    st.write(f"Epoch {epoch}: Loss - {loss:.4f}")
    progress_bar.progress(epoch / total_epochs)

# Custom Trainer class to incorporate Streamlit updates
class StreamlitTrainer(Trainer):
    def training_step(self, model, inputs):
        # Call the original training_step method and get its output
        result = super().training_step(model, inputs)

        # The loss is typically found in result.loss
        if hasattr(result, "loss"):
            loss = result.loss.item()  # Get the loss value as a Python float
            logs = {"loss": loss}
            # Update progress in Streamlit
            if self.state.global_step % self.args.logging_steps == 0:
                update_streamlit_progress(self.state.epoch, logs["loss"])

        return result

# Streamlit app interface
st.title("LLM Fine-Tuning Demo with Training Process")

# Load model, tokenizer, and dataset
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Preprocess function for the dataset
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, padding=True, max_length=512)

# Load and preprocess the dataset
raw_dataset = load_dataset("imdb", split='train[:1%]')
dataset = raw_dataset.map(preprocess_function, batched=True)

# User input for testing
user_input = st.text_area("Input Text for Sentiment Analysis", "I loved this movie!")

total_epochs = 1
if st.button("Fine-tune Model"):
    st.write("Fine-tuning in progress...")

    # Progress bar
    progress_bar = st.progress(0)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        num_train_epochs=total_epochs
    )

    # Initialize our custom trainer
    trainer = StreamlitTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    # Start fine-tuning
    trainer.train()

    st.write("Model fine-tuned!")

# Testing the model before and after fine-tuning
def test_model():
    inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    prediction = 'Positive' if logits.argmax(-1).item() == 1 else 'Negative'
    st.write(f"Sentiment: {prediction}")

if st.button("Test Before Fine-tuning"):
    test_model()

if st.button("Test After Fine-tuning"):
    test_model()
