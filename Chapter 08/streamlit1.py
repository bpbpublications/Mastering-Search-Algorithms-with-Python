import streamlit as st
# Title of the app
st.title('Streamlit Layout and Widgets Demo')
# Sidebar
st.sidebar.header('Sidebar')
sidebar_option = st.sidebar.selectbox("Choose an option", ['Option 1', 'Option 2', 'Option 3'])
# Displaying selected option
st.write(f"You selected: {sidebar_option}")
# Columns for layout
col1, col2 = st.columns(2)
with col1:
    st.header("Column 1")
    st.write("This is column 1.")
    st.button("Click me!")
with col2:
    st.header("Column 2")
    st.write("This is column 2.")
    number = st.slider("Select a number", 1, 10)
st.write(f"You selected number {number} in column 2.")
# Expander
with st.expander("See explanation"):
    st.write("""
        The Streamlit layout and widgets are simple yet powerful tools to create interactive apps.
        - The sidebar allows for adding controls and filters.
        - Columns help in organizing content side by side.
        - The expander is useful for optional detailed information.
    """)
