import numpy as np

def analyze_array(arr):
    print(f"Array: {arr}")
    print(f"Mean: {np.mean(arr)}")
    print(f"Standard Deviation: {np.std(arr)}")
    print(f"Sum: {np.sum(arr)}")
    print(f"Maximum Element: {np.max(arr)}")
    print(f"Minimum Element: {np.min(arr)}")

if __name__ == "__main__":
    # Get user input for the array
    user_input = input("Enter numbers separated by spaces: ")
    arr = np.array([float(num) for num in user_input.split()])
    
    analyze_array(arr)
