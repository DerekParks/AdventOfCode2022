#!/usr/bin/env python3

import math
import numpy as np

def min_max(lines, dim):
    min = math.inf
    max = 0
    for line in lines:
        if line[dim] < min:
            min = line[dim]
        if line[dim] > max:
            max = line[dim]
    return min, max

def to_index_cords(lines):
    min_x, max_x = min_max(lines, 0)
    min_y, max_y = min_max(lines, 1)
    min_z, max_z = min_max(lines, 2)

    return [(x - min_x, y - min_y, z - min_z) for x,y,z in lines], (max_x - min_x + 1, max_y - min_y + 1, max_z - min_z + 1)

def possible_neigh(i, j, k):
    return [(i-1, j, k), (i+1, j, k), (i, j-1, k), (i, j+1, k), (i, j, k-1), (i, j, k+1)]

def get_neigh(i, j, k, index_cords_set):
    return filter(lambda ijk: ijk in index_cords_set, possible_neigh(i, j, k))

def get_neigh_inbounds(i, j, k, n_i, n_j, n_k):
    return filter(lambda ijk: ijk[0] >= 0 and ijk[0] < n_i and ijk[1] >= 0 and ijk[1] < n_j and ijk[2] >= 0 and ijk[2] < n_k, possible_neigh(i, j, k))

def get_faces(coords):
    index_coords_set = set(coords)

    faces = 0
    for coord in index_coords_set:
        i,j,k = coord
        faces += 6 - len(list(get_neigh(i, j, k, index_coords_set)))
    return faces

if __name__ == "__main__":

    if False:
        file_name = "day18_test.txt"  
    else:
        file_name = "day18.txt"

    with open(file_name) as f:
        lines_in = f.readlines()

    #lines_in = ["1,1,1", "2,1,1", "3,1,1", "1,1,2"]

    lines = [tuple(map(int,line.strip().split(","))) for line in lines_in]

    index_coords, (n_i, n_j, n_k) = to_index_cords(lines)

    #Part 1
    faces = get_faces(index_coords)
    print(f"Faces: {faces}")

    #Part 2
    arr = np.zeros((n_i, n_j, n_k))
    for i,j,k in index_coords:
         arr[i,j,k] = 1

    q = [(n_i-1, n_j-1, n_k-1)]
    while len(q) > 0:
        i,j,k = q.pop()
        for ijk in get_neigh_inbounds(i, j, k, n_i, n_j, n_k):
            if arr[ijk[0], ijk[1], ijk[2]] == 0:
                arr[ijk[0], ijk[1], ijk[2]] = 1
                q.append(ijk)

    empty_cells = []
    for idx, x in np.ndenumerate(arr):
        if x == 0:
            empty_cells.append(idx)
            print(f"Empty: {idx}")

    hidden_faces = get_faces(empty_cells)

    print(f"Empty cells: {empty_cells}")
    print(f"Hidden faces: {hidden_faces}")
    print(f"Exposed faces: {faces - hidden_faces}")
