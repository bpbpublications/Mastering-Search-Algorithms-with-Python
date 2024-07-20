import streamlit as st

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # Return the index where the target is found
    return -1  # Return -1 if target is not found

def main():
    st.title("Linear Search Visualization")

    # Input elements
    arr = st.text_input("Enter an array (comma-separated)", "34, 12, 45, 67, 23, 9, 56, 89")
    target = st.number_input("Enter target element", value=23)

    arr = [int(x.strip()) for x in arr.split(",")]

    result = linear_search(arr, target)

    # Visualization
    st.write("Array:", arr)
    st.write(f"Target: {target}")

    if result != -1:
        st.write(f"Target {target} found at index {result}")
    else:
        st.write(f"Target {target} not found in the array")

if __name__ == "__main__":
    main()
