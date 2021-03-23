import math
import numpy
import csv

def load_data(filepath):
    data = []
    with open(filepath) as file:
        reader = csv.DictReader(file)
        for row in reader:
            dict = {}
            del row['Lat']
            del row['Long']
            for i in row:
                dict[i] = row[i]
            data.append(dict)
    return data

def calculate_all(data):
    X = []
    for i in data:
        X.append(calculate_x_y(i))
    return X

def calculate_x_y(time_series):
    data = time_series.copy()
    del data['Province/State']
    del data['Country/Region']

    april = list(time_series.items())[-1][1]
    cases_num = int(april)
    today = len(data) - 1

    if cases_num != 0:
        case_day = 0
        ten = cases_num / 10
        day_i = 0
        x = math.nan
        for value in data.values():
            var = int(value)
            if var <= ten and day_i >= case_day:
                case_day = day_i
                x = today - day_i
            day_i = day_i + 1

        day = 0
        hundred = cases_num / 100
        day_i = 0
        y = math.nan
        for value in data.values():
            var = int(value)
            if var <= hundred and day_i >= day:
                day = day_i
                y = case_day - day_i
            day_i = day_i + 1
    else:
        x = math.nan
        y = math.nan
    return x, y

def hac(dataset):
    data = []
    for x, y in dataset:
        if math.isfinite(x) and math.isfinite(y):
            data.append((x, y))
    cluster_dict = {}
    for i in range(len(data)):
        cluster_dict[i] = [data[i]]

    cluster_list = []
    line = 0
    length = len(cluster_dict)

    while len(cluster_dict) > 1:
        cluster_1 = 0
        cluster_2 = 0
        min_dist = math.inf
        for x in cluster_dict.keys():
            for y in cluster_dict.keys():
                if x == y:
                    continue
                dist = math.inf
                for x1, y1 in cluster_dict[x]:
                    for x2, y2 in cluster_dict[y]:
                        curr_dist = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
                        dist = min(dist, curr_dist)
                if dist < min_dist:
                    if x < y:
                        cluster_1, cluster_2 = (x, y)
                    else:
                        cluster_1, cluster_2 = (x, y)
                    min_dist = dist

        index = length + line
        pts = len(cluster_dict[cluster_1]) + len(cluster_dict[cluster_2])
        cluster_list.append([cluster_1, cluster_2, min_dist, pts])

        cluster_dict[index] = cluster_dict[cluster_1] + cluster_dict[cluster_2]
        del cluster_dict[cluster_1]
        del cluster_dict[cluster_2]
        line = line + 1

    cluster_list = numpy.asmatrix(cluster_list)
    return cluster_list

if __name__ == "__main__":
    data = load_data('time_series_covid19_confirmed_global.csv')
    list = calculate_all(data)
    print(hac(list))
