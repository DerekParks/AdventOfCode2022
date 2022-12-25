#!/usr/bin/env python3
import sys
import re
from pyspark.sql import SparkSession

def read_input(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

def to_coords_input(line):
    coords_str = re.findall(r'(-?\d+)', line)
    coords = [int(x) for x in coords_str]
    return (coords[0], coords[1]), (coords[2], coords[3])

def intersection(s, b, y):
    s_x, s_y = s
    b_x, b_y = b
    dist = abs(s[0] - b[0]) + abs(s[1] - b[1])

    if y >= s_y - dist and y <= s_y + dist:
        n_x_in_range = dist - abs(s_y - y)
        return s_x-n_x_in_range, s_x+n_x_in_range+1
    else:
        return None

def merge_ranges(ranges):
    merged = []
    for r in sorted(ranges):
        if merged and r[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], r[1]))
        else:
            merged.append(r)
    return merged


def build_row(row_of_interest: int, coords: list[tuple[tuple[int, int], tuple[int, int]]]) -> list[tuple[int, int]]:
    to_filter = [intersection(coord[0], coord[1], row_of_interest) for coord in coords]

    to_merge = [x for x in to_filter if x is not None]

    return merge_ranges(to_merge)

def run_single_row(row_of_interest, coords):
    merged = build_row(row_of_interest, coords)

    result = sum([x[1] - x[0] for x in merged])

    coords_on_row = set([(x[0][0],x[0][1]) for x in coords if x[0][1] == row_of_interest] + [(x[1][0], x[1][1]) for x in coords if x[1][1] == row_of_interest])

    beacon_overlaps = 0
    for beacon in coords_on_row:
        for m in merged:
            if beacon[0] >= m[0] and beacon[0] <= m[1]:
                beacon_overlaps += 1

    return result - beacon_overlaps

def to_freq(x, y):
    return x * 4000000 + y

def part1(filename):
    row_of_interest = 10 if "test" in filename else 2000000
    return run_single_row(row_of_interest)

def part2(filename, coords):
    max_x, max_y = (21, 20) if "test" in filename else (4000001, 4000000)

    beacons_sensors = set([(x[0][0], x[0][1]) for x in coords] + [(x[1][0], x[1][1]) for x in coords])

    def process_row(y):
        row = build_row(y, coords)
        row = [(max(0, x[0]), min(max_x, x[1])) for x in row]
        if len(row) == 1 and row[0][0] == 0 and row[0][1] == max_x:
            return None

        for x in range(max_x):
            if (x, y) not in beacons_sensors and not any([x >= r[0] and x < r[1] for r in row]):
                return to_freq(x, y)

    sc = SparkSession.builder.master("local[8]").appName('Day15').getOrCreate().sparkContext
    result = sc.parallelize(range(max_y)).map(process_row).filter(lambda x: x is not None).take(1)
    print(result)
    return result
if __name__ == "__main__":
    filename = sys.argv[1]
    lines = read_input(filename)
    coords = list(map(to_coords_input, lines))

    #result = part1(filename)

    result = part2(filename, coords)
    print(result)