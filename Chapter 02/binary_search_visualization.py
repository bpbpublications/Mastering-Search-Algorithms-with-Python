import streamlit as st

def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

def main():
    st.title("Binary Search Visualization with Streamlit")

    # Input elements
    arr = st.text_input("Enter a sorted array (comma-separated)", "9, 12, 23, 34, 45, 56, 67, 89")
    target = st.number_input("Enter target element", value=23)

    arr = [int(x.strip()) for x in arr.split(",")]

    result = binary_search(arr, target)

    # Visualization
    st.write("Array:", arr)
    st.write(f"Target: {target}")

    if result != -1:
        st.write(f"Target {target} found at index {result}")
    else:
        st.write(f"Target {target} not found in the array")

if __name__ == "__main__":
    main()

