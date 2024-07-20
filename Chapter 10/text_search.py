import streamlit as st

# Sample text document
sample_text = """
Text search algorithms are fundamental in information retrieval, text analysis, and text processing tasks. They enable us to quickly locate and extract relevant information from large volumes of textual data, making them an essential component of many software systems and applications. Let us explore some common text search algorithms.
"""

# Streamlit UI
st.title("Text Search Application")

# User input for search query
search_query = st.text_input("Enter a word to search:")

# Button to perform the search
if st.button("Search"):
    # Split the text into words
    words = sample_text.split()

    # Perform the search and find occurrences
    search_results = [i for i, word in enumerate(words) if search_query.lower() in word.lower()]

    # Display the search results
    if search_results:
        st.write(f"Word '{search_query}' found at positions: {', '.join(map(str, search_results))}")
    else:
        st.write(f"Word '{search_query}' not found in the text.")
