def binary_search_recursive(arr, target, left, right):
    if left <= right:
        mid = left + (right - left) // 2  # Calculate mid index to prevent overflow
        if arr[mid] == target:
            return mid  # Found target
        elif arr[mid] < target:
            return binary_search_recursive(arr, target, mid + 1, right)  # Search the right half
        else:
            return binary_search_recursive(arr, target, left, mid - 1)  # Search the left half
    return -1  # Target not found

# Example usage
my_array = [9, 12, 23, 34, 45, 56, 67, 89]
target_number = 23
result = binary_search_recursive(my_array, target_number, 0, len(my_array) - 1)

if result != -1:
    print(f"Target {target_number} found at index {result}")
else:
    print(f"Target {target_number} not found in the array")

