from collections import defaultdict

import hdbscan
import numpy as np
from numpy.typing import NDArray
from numpy.linalg import eigh
from scipy.sparse.csgraph import laplacian
from sklearn.cluster import SpectralClustering


def apply_HDBSCAN(
    euclidian_matrix: NDArray[np.float64],
) -> tuple[list[int], list[list[int]], list[list[int]]]:
    if euclidian_matrix.size == 0:
        return ([], [], [])

    clusterer = hdbscan.HDBSCAN(metric="precomputed", min_cluster_size=2)
    labels = clusterer.fit_predict(euclidian_matrix)
    noise: list[int] = []
    buckets: dict[int, list[int]] = defaultdict(list)
    for i, label in enumerate(labels):
        if label == -1:
            noise.append(i)
        else:
            buckets[label].append(i)
    clusters: list[list[int]] = []
    clusters_to_partition: list[list[int]] = []
    for value in buckets.values():
        if len(value) > 4:
            clusters_to_partition.append(value)
        else:
            clusters.append(value)
    return noise, clusters, clusters_to_partition


def partition_cluster(
    affinity_matrix: NDArray[np.float64], size: int
) -> tuple[list[list[int]], list[int]]:
    if affinity_matrix.size == 0 or size <= 0:
        return ([], [])

    partitioner = SpectralClustering(
        n_clusters=size, affinity="precomputed", random_state=42
    )
    labels = partitioner.fit_predict(affinity_matrix)

    result_dict: dict[int, list[int]] = {}
    for node, label in enumerate(labels):
        if label not in result_dict:
            result_dict[label] = []
        result_dict[label].append(node)

    noise: list[int] = []
    clusters: list[list[int]] = []
    for partitions in result_dict.values():
        if len(partitions) == 1:
            noise.append(partitions[0])
        else:
            clusters.append(partitions)

    return (clusters, noise)


def get_best_cluster_size(
    affinity_matrix: NDArray[np.float64], min_size: int, max_size: int
) -> int:
    if affinity_matrix.size == 0:
        return max(min_size, 1)

    laplacian_matrix = laplacian(affinity_matrix, normed=True)
    eigenvalues, _ = eigh(laplacian_matrix)
    eigengaps = np.diff(eigenvalues)
    return int(np.argmax(eigengaps[min_size - 1 : max_size])) + min_size
