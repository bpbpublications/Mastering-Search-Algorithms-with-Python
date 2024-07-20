import streamlit as st
import plotly.express as px
import pandas as pd  # Import pandas for creating DataFrame

def linear_search(arr, target):
    steps = []  # To store data for visualization

    for i in range(len(arr)):
        steps.append((i, arr[i], target == arr[i]))  # Save step data

        if arr[i] == target:
            return i, steps  # Return index and steps data
    return -1, steps  # Return -1 if target is not found

def main():
    st.title("Linear Search Visualization with Plotly")

    # Input elements
    arr = st.text_input("Enter an array (comma-separated)", "34, 12, 45, 67, 23, 9, 56, 89, 95, 112, 117, 94")
    target = st.number_input("Enter target element", value=23)

    arr = [int(x.strip()) for x in arr.split(",")]

    result, steps = linear_search(arr, target)

    # Convert steps data to a DataFrame
    steps_df = pd.DataFrame(steps, columns=["Index", "Value", "Match"])

    # Visualization
    fig = px.bar(
        steps_df,
        x="Index",
        y="Value",
        color="Match",
        title="Linear Search Visualization",
        labels={"Match": "Is Target"},
    )
    st.plotly_chart(fig)

    if result != -1:
        st.write(f"Target {target} found at index {result}")
    else:
        st.write(f"Target {target} not found in the array")

if __name__ == "__main__":
    main()
