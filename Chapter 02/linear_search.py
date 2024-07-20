def linear_search(arr, target):
	for i in range(len(arr)):
	    if arr[i] == target:
	        return i  # Target found, return the index
	return -1  # Target not found, return -1
	
# Example usage:
my_array = [34, 12, 45, 67, 23, 9, 56, 89]
target_number = 23
result = linear_search(my_array, target_number)
	
if result != -1:
	print(f"Target {target_number} found at index {result}")
else:
	print(f"Target {target_number} not found in the array")