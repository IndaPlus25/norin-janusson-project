from classes import TPMSsensor
import datetime as dt

def to_coocurence_matrix(sensors: list[TPMSsensor]):
    sensor_count = len(sensors)
    coocurence_matrix = [[0 for j in range(sensor_count)] for i in range(sensor_count)]

    for i in range(0, sensor_count):
        sensor = sensors.pop()
        for key in sensor.observations.keys():
            for i2 in range(0, len(sensors)):
                matches = count_matches(sensors[i2].observations[key], sensor.observations[key])
                coocurence_matrix[i][i2] = coocurence_matrix[i][i2]+matches
                coocurence_matrix[i2][i] = coocurence_matrix[i][i2]
    return coocurence_matrix

def count_matches(arr1: list[dt.datetime], arr2: list[dt.datetime]):
    count = 0
    for dt1 in arr1:
        for dt2 in arr2:
            if abs((dt1 - dt2).total_seconds()) <= 60:
                count += 1
    return count
    

def normalize():
    
    return 