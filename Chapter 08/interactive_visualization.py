import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def binary_search(arr, x):
    left, right = 0, len(arr) - 1
    steps = []  # To track the steps for visualization
    while left <= right:
        mid = left + (right - left) // 2
        steps.append((left, right, mid))
        if arr[mid] == x:
            return mid, steps
        elif arr[mid] < x:
            left = mid + 1
        else:
            right = mid - 1
    return -1, steps

def visualize_steps(steps, arr, target):
    for left, right, mid in steps:
        st.write(f"Checking between indexes {left} and {right}, Middle: {mid}, Value: {arr[mid]}")
        if arr[mid] == target:
            st.success(f"Found {target} at index {mid}!")
            break
        else:
            st.warning("Searching...")

def plot_complexity(n):
    x = np.arange(1, n+1)
    y = np.log2(x)
    plt.plot(x, y, label='O(log n)')
    plt.xlabel('Input size (n)')
    plt.ylabel('Steps')
    plt.title('Binary Search Time Complexity')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

st.title("Binary Search Visualization with Complexity")

# User input for list and target value
user_list = st.text_input("Enter a sorted list (comma-separated):")
user_number = st.number_input("Enter the number to search for:", step=1)

if user_list and user_number:
    user_list = [int(i.strip()) for i in user_list.split(',')]
    index, steps = binary_search(user_list, user_number)
    if index != -1:
        visualize_steps(steps, user_list, user_number)
        plot_complexity(len(user_list))
        st.markdown("### Complexity Analysis:")
        st.markdown("""
            * **Time Complexity**: O(log n)
            * **Explanation**: In binary search, the search space is halved in each step. 
              Therefore, the maximum number of steps is proportional to the logarithm of the input size.
        """)
    else:
        st.error("Number not found in the list.")
