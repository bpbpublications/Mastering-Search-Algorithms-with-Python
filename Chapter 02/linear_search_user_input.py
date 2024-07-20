def linear_search(arr, target):
	for i in range(len(arr)):
	    if arr[i] == target:
	        return i  # Target found, return the index
	return -1  # Target not found, return -1
	
# User input for array and target element
user_array = input("Enter an array (comma-separated values): ")
user_target = int(input("Enter the target element: "))
user_array = [int(x.strip()) for x in user_array.split(",")]
	
result = linear_search(user_array, user_target)
	
if result != -1:
	print(f"Target {user_target} found at index {result}")
else:
	print(f"Target {user_target} not found in the array")
