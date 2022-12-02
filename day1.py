#!/usr/bin/env python3

import sys
import heapq

def read_next_input():
    for line in sys.stdin:
        if line.strip() == '':
            return
        yield int(line.rstrip())

def read_all_inputs():
    while True:
        s = sum(read_next_input())

        if s == 0:
            break
        yield s

def sum_top_n(n):
    return sum(heapq.nlargest(n, list(read_all_inputs())))

def main():
    print(sum_top_n(3))

if __name__ == '__main__':
    main()