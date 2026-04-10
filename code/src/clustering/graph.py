from collections import defaultdict
from sklearn.cluster import SpectralClustering
import datetime as dt
import hdbscan
from data.classes import TPMSsensorFormatted


def to_coocurence_matrix(sensors: list[TPMSsensorFormatted]):
    sensor_count = len(sensors)
    coocurence_matrix = [[0 for j in range(sensor_count)] for i in range(sensor_count)]

    for i in range(0, sensor_count):
        sensor = sensors[i]
        for key in sensor.observations.keys():
            for i2 in range(0, len(sensors)):
                matches = count_matches(
                    sensors[i2].observations[key], sensor.observations[key]
                )
                coocurence_matrix[i][i2] = coocurence_matrix[i][i2] + matches
                coocurence_matrix[i2][i] = coocurence_matrix[i][i2]
    return coocurence_matrix


def count_matches(arr1: list[dt.datetime], arr2: list[dt.datetime]):
    count = 0
    for dt1 in arr1:
        for dt2 in arr2:
            if abs((dt1 - dt2).total_seconds()) <= 60:
                count += 1
    return count


def apply_HDBSCAN(euclidian_matrix: list[list[float]]):
    clusterer = hdbscan.HDBSCAN(metric="precomputed", min_cluster_size=5)
    labels = clusterer.fit_predict(euclidian_matrix)
    noise = []
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
    return (noise, clusters, clusters_to_partition)


def apply_spectralClustering(euclidian_matrix: list[list[float]]):
    spectral_clustering = SpectralClustering(
        n_clusters=2, affinity="rbf", gamma=1.0, random_state=42
    )
    return


def affinity_to_euclidian(affinity_matrix: list[list[float]]):
    return 1 - affinity_matrix
