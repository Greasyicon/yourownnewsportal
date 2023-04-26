import pandas as pd
import time
import numpy as np
from numba import njit, prange
from multiprocessing import Pool, cpu_count

# Generate a dataset of random 3D points
num_points = 5000
points = np.random.rand(num_points, 3)

# Function to compute Euclidean distance between two points
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# Numba-optimized Euclidean distance function
@njit
def euclidean_distance_numba(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# Sequential approach for calculating distance matrix
def calculate_distances_sequential(points):
    num_points = len(points)
    distances = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(i + 1, num_points):
            distances[i, j] = euclidean_distance(points[i], points[j])
            distances[j, i] = distances[i, j]
    return distances

# Wrapper function for multiprocessing, accepting arguments as a tuple
def wrapper(args):
    points, i, j = args
    return i, j, euclidean_distance(points[i], points[j])

# Multiprocessing approach using Pool.map
def calculate_distances_multiprocessing_map(points):
    num_points = len(points)
    distances = np.zeros((num_points, num_points))
    indices = [(points, i, j) for i in range(num_points) for j in range(i + 1, num_points)]

    num_cores = cpu_count()
    print(f"Number of available CPU cores: {num_cores}")
    with Pool(num_cores) as pool:
        results = pool.map(wrapper, indices)

    for i, j, distance in results:
        distances[i, j] = distance
        distances[j, i] = distance

    return distances

# Numba parallel approach
@njit(parallel=True)
def calculate_distances_numba(points):
    num_points = len(points)
    distances = np.zeros((num_points, num_points))
    for i in prange(num_points):
        for j in prange(i + 1, num_points):
            distances[i, j] = euclidean_distance_numba(points[i], points[j])
            distances[j, i] = distances[i, j]
    return distances

# Time measurement for each approach
if __name__ == '__main__':

    # Time measurement for each approach
    start = time.time()
    distances_sequential = calculate_distances_sequential(points)
    print(f"Sequential processing time: {time.time() - start:.2f} seconds")

    start = time.time()
    distances_multiprocessing_map = calculate_distances_multiprocessing_map(points)
    print(f"Multiprocessing (Pool.map) processing time: {time.time() - start:.2f} seconds")

    start = time.time()
    distances_numba = calculate_distances_numba(points)
    print(f"Numba parallel processing time: {time.time() - start:.2f} seconds")


    print(np.shape(distances_sequential))
    print(np.sum(distances_sequential))
    print(np.shape(distances_multiprocessing_map))
    print(np.sum(distances_multiprocessing_map))
    print(np.shape(distances_numba))
    print(np.sum(distances_numba))


    ## The following code will fail with Numba, as it does not fully support dataframes and dictionaries.
    ## Numba does not support pandas DataFrame operations.
    # @njit
    # def process_dict(d):
    #     return {k: v * 2 for k, v in
    #             d.items()}
    #
    #
    # data = {'a': 1, 'b': 2, 'c': 3}
    # process_dict(data)

    ## Numba does not support dictionaries either.
    # @njit
    # def process_dataframe(df):
    #     return df['a'] * 2  # Numba does not support pandas DataFrame operations.
    #
    #
    # data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
    # df = pd.DataFrame(data)
    # process_dataframe(df)