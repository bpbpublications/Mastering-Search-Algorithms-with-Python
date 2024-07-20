import streamlit as st
import matplotlib.pyplot as plt

# Linear Search Function
def linear_search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

# Binary Search Function
def binary_search(arr, x):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Function to plot the search process
def plot_search_process(arr, index, search_type):
    plt.figure(figsize=(10, 1))
    colors = ['blue' if i == index else 'gray' for i in range(len(arr))]
    plt.bar(range(len(arr)), arr, color=colors)
    plt.title(f"{search_type} Search - Found at Index: {index}")
    st.pyplot(plt)

# Streamlit User Interface
st.title('Search Algorithms Demonstration')

user_list = st.text_input("Enter a list of sorted numbers (comma-separated):")
user_number = st.number_input("Enter the number to search for:", step=1)

if user_list and user_number:
    user_list = [int(i.strip()) for i in user_list.split(',')]
    user_number = int(user_number)

    # Perform Linear Search
    lin_index = linear_search(user_list, user_number)
    if lin_index != -1:
        plot_search_process(user_list, lin_index, "Linear")
    else:
        st.write("Number not found using Linear Search.")

    # Perform Binary Search
    bin_index = binary_search(user_list, user_number)
    if bin_index != -1:
        plot_search_process(user_list, bin_index, "Binary")
    else:
        st.write("Number not found using Binary Search.")
