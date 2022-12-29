#!/usr/bin/env python3

import sys
import re
import heapq
#from more_itertools import set_partitions
from itertools import permutations, product, combinations
from collections import defaultdict
import copy
from dask.distributed import Client, as_completed
import os
import pickle
from pickle import UnpicklingError

def read_input(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

class Valve:
    def __init__(self, name, rate):
        self.rate = rate
        self.name = name
        self.neigh = []

    def add_neigh(self, neigh):
        self.neigh.append(neigh)

    def __repr__(self):
        #return f"{self.name}({self.rate} {[n.name for n in self.neigh]})"
        return f"{self.name}"

    def __lt__(self, other):
        return self.rate < other.rate

def build_graph(inlines):
    graph = {}

    for line in inlines:
        name, rate = re.findall(r'Valve ([A-Z][A-Z]).+=(\d+);', line)[0]
        graph[name] = Valve(name, int(rate))

    for line in inlines:
        name, neighs = re.findall(r'Valve ([A-Z][A-Z]).+valves?\s([A-Z,\s]+)$', line)[0]
        neighs = neighs.split(',')
        graph[name].neigh = sorted([graph[n.strip()] for n in neighs], key=lambda x: x.rate, reverse=False)

    return graph

def shortest_path(f, t):
    heap = []
    seen = set()
    heapq.heappush(heap, (0, (f,)))

    while heap:
        time, path = heapq.heappop(heap)
        node = path[-1]
        if node == t:
            return time, path
        for neigh in node.neigh:
            if neigh not in seen:
                seen.add(neigh)
                heapq.heappush(heap, (time + 1, path + (neigh,)))

def build_shortest_paths(graph):

    shortest_paths = {}
    for f in graph.values():
        f.paths = {}
        f.path_to = {}
        for t in graph.values():
            if f == t:
                continue
            if t.rate == 0:
                continue
            if (t, f) in shortest_paths:
                f.paths[t], f.path_to[t] = shortest_paths[(t, f)]
                f.path_to[t] = tuple(reversed(f.path_to[t]))
            else:
                temp = shortest_path(f, t)
                if temp is None:
                    print(f"no path from {f} to {t} {graph}")
                    return None
                f.paths[t], f.path_to[t] = temp
            shortest_paths[(f, t)] = (f.paths[t], f.path_to[t])
    return shortest_paths

class TraversalState:
    def __init__(self, graph, max_time, path=(), opened=frozenset(), released=[]):
        self.path = path
        self.opened = opened
        self.released = released
        self.graph = graph
        self.max_time = max_time

    def time(self):
        return len(self.path)

    def _update_released(self):
        self.released.append(sum([p.rate for p in self.opened]))

    def _update(self, node, opened):
        new_opened = self.opened.union((node,)) if opened else self.opened
        result = TraversalState(self.graph, self.max_time, self.path + (node,), new_opened, self.released.copy())
        result._update_released()
        return result

    def move_to(self, node):
        return self._update(node, False)

    def open(self):
        return self._update(self.node(), True)

    def no_op(self):
        return self._update(self.node(), False)

    def node(self):
        return self.path[-1]

    def path_name(self):
        return [n.name for n in self.path]

    def __repr__(self):
        return f"{' ' * self.time()} {self.time()} {self.path_name()} {self.opened} {self.released} {sum(self.released)}"

    def __lt__(self, other):
        if self.time() == other.time():
            return self.total_released() >= other.total_released()
        else:
            return self.time() < other.time()

    def total_released(self):
        return sum(self.released)

    def to_see(self):
        return (self.opened, self.time(), self.total_released())


class TraversalState:
    def __init__(self, graph, max_time, path=(), opened=frozenset(), released=[]):
        self.path = path
        self.opened = opened
        self.released = released
        self.graph = graph
        self.max_time = max_time

    def time(self):
        return len(self.path)

    def _update_released(self):
        self.released.append(sum([p.rate for p in self.opened]))

    def _update(self, node, opened):
        new_opened = self.opened.union((node,)) if opened else self.opened
        result = TraversalState(self.graph, self.max_time, self.path + (node,), new_opened, self.released.copy())
        result._update_released()
        return result

    def move_to(self, node):
        return self._update(node, False)

    def open(self):
        return self._update(self.node(), True)

    def no_op(self):
        return self._update(self.node(), False)

    def node(self):
        return self.path[-1]

    def path_name(self):
        return [n.name for n in self.path]

    def __repr__(self):
        return f"{' ' * self.time()} {self.time()} {self.path_name()} {self.opened} {self.released} {sum(self.released)}"

    def __lt__(self, other):
        if self.time() == other.time():
            return self.total_released() >= other.total_released()
        else:
            return self.time() < other.time()

    def total_released(self):
        return sum(self.released)

    def to_see(self):
        return (self.opened, self.time(), self.total_released())


optimal_traversal = ["AA", "DD", "CC", "BB", "AA", "II", "JJ", "II", "AA", "DD", "EE", "FF", "GG", "HH", "GG", "FF", "EE", "DD", "CC"]
time_step =     [  1,    2,    3 ,   4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,   18,   19,   20,   21,   22,   23,   24,   25,   26,   27,   28,   29,   30]
released  =     [  0,    0,    20,  20,   20,   33,   33,   33,   33,   54,   54,   54,   54,   54,   54,   54,   54,   76,   76,   76,   76,   79,   79,   79,   81,   81,   81,   81,   81,   81]
optimal_locs  = ["AA", "DD", "DD", "CC", "BB", "BB", "AA", "II", "JJ", "JJ", "II", "AA", "DD", "EE", "FF", "GG", "HH", "HH", "GG", "FF", "EE", "EE", "DD", "CC", "CC", "CC", "CC", "CC", "CC", "CC"]
optimal_locs2  = ["AA", "DD", "DD", "AA", "BB", "BB", "AA", "II", "JJ", "JJ", "II", "AA", "DD", "EE", "FF", "GG", "HH", "HH", "GG", "FF", "EE", "EE", "DD", "CC", "CC", "CC", "CC", "CC", "CC", "CC"]

force_optimal_path = False

def fts3(graph, max_time=30):
    heap = []
    seen = set()

    max_release = 0
    max_state = None
    count = 0

    open_ables = [n for n in graph.values() if n.rate != 0]

    def add(state):
        state_to_see = state.to_see()
        if state_to_see not in seen:
            heapq.heappush(heap, state)
            seen.add(state_to_see)
        else:
            pass
            #print("Already Seen", state.path, state_to_see)

    add(TraversalState(graph=graph, max_time=max_time).move_to(graph['AA']))

    while heap:
        state = heapq.heappop(heap)
        current = state.node()
        time = state.time()
        count += 1

        path_name = state.path_name()
        if force_optimal_path:
            if path_name == optimal_locs2:
                print(f"{' ' * time}  Optimal path {state.path}")
                return state

            if path_name != optimal_locs2[:len(path_name)]:
                print(f"{' ' * time}  Not on happy path {path_name} {optimal_locs[:len(path_name)]}")
                continue

        unopened = [n for n in open_ables if n not in state.opened]
        #print(f"{' ' * time} {time} {state.to_see()} {state.path} {current} -> {unopened}")

        if len(unopened) == 0 or time > max_time:
            while state.time() < max_time:
                state = state.no_op()

            released = state.total_released()
            if released > max_release:
                max_release = released
                max_state = state
            # print(f"{' ' * time} {time} Max time {state.path}")
            continue

        for node in unopened:
            if node not in current.paths:
                continue

            state_next = state

            cost = current.paths[node] + 1

            next_time = time + cost
            if next_time > max_time:
                while state_next.time() < max_time:
                    state_next = state_next.no_op()
                released = state_next.total_released()
                if released > max_release:
                    max_release = released
                    max_state = state_next
                continue

            #print(f"{current} -> {node} {cost} {next_time} {current.path_to[node][1:]}")
            for node_on_path in current.path_to[node][1:]:
                state_next = state_next.move_to(node_on_path)

            add(state_next.open())

    #print(f"count: {count} {max_release}")
    return max_state

def part1(graph):
    build_shortest_paths(graph)

    state = fts3(graph, 30)

    if state:
        print(state)
        print(state.released)
        print(sum(state.released))
        print(state.path)


if __name__ == "__main__":
    inlines = read_input(sys.argv[1])
    graph = build_graph(inlines)

    #print([(p.name, p.neigh) for p in graph.values()])
    #print([(p.name, p.rate, p.paths) for p in graph.values()])

    part1(graph)
    #part2(graph)