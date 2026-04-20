from collections import defaultdict
import hdbscan


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


# TODO: implement
def partition_cluster(euclidian_matrix: list[list[int]]) -> list[list[int]]:
    return
