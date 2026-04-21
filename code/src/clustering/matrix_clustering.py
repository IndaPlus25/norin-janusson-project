from collections import defaultdict
import hdbscan
from scipy.sparse.csgraph import laplacian
from numpy.linalg import eigh
from numpy import diff, argmax
from sklearn.cluster import SpectralClustering


def apply_HDBSCAN(
    euclidian_matrix: list[list[float]],
) -> tuple[list[int], list[list[int]], list[list[int]]]:
    clusterer = hdbscan.HDBSCAN(metric="precomputed", min_cluster_size=2)
    labels = clusterer.fit_predict(euclidian_matrix)
    noise: list[int] = []
    clusters = defaultdict(list)
    labels_count = len(labels)
    for i in range(0, labels_count):
        placeholder = labels[i]
        if placeholder == -1:
            noise.append(i)
        else:
            clusters[placeholder].append(i)
    clusters = []
    clusters_to_partition = []
    for _, value in clusters.items():
        if len(value) > 4:
            clusters_to_partition.append(value)
        else:
            clusters.append(value)
    return noise, clusters, clusters_to_partition


def partition_cluster(
    affinity_matrix: list[list[float]], size: int
) -> tuple[list[list[int]], list[int]]:
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
    affinity_matrix: list[list[float]], min_size: int, max_size: int
) -> int:
    laplacian_matrix = laplacian(affinity_matrix, normed=True)
    eigenvalues, _ = eigh(laplacian_matrix)
    eigengaps = diff(eigenvalues)
    return int(argmax(eigengaps[min_size - 1 : max_size])) + min_size
