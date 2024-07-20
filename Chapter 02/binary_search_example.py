def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Calculate mid index to prevent overflow

        if arr[mid] == target:
            return mid  # Found target
        elif arr[mid] < target:
            left = mid + 1  # Search the right half
        else:
            right = mid - 1  # Search the left half

    return -1  # Target not found

# Example usage
my_array = [9, 12, 23, 34, 45, 56, 67, 89]
target_number = 23

result = binary_search(my_array, target_number)

if result != -1:
    print(f"Target {target_number} found at index {result}")
else:
    print(f"Target {target_number} not found in the array")
