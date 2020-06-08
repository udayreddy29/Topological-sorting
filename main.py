import argparse
import collections
import sys


class Node:
    def __init__(self, index=0, color='white', pred=None, d=0, f=0):
        self.index = index
        self.color = color
        self.pred = pred
        self.d = d
        self.f = f


class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.time = 0
        self.idx_vertex_map = collections.defaultdict()
        self.sorted_arr = []

    def add_edge(self, u, v):
        self.adj_matrix[u][v] = 1

    def map_index_vertex(self, index, node):
        self.idx_vertex_map[index] = node

    def __repr__(self):
        text = ''
        for i in range(self.size):
            text += str(self.adj_matrix[i]) + '\n'
        return text

    def dfs_visit(self, node, vertices):
        self.time += 1
        vertices[node].d = self.time
        vertices[node].color = 'gray'
        for idx, neighbor in enumerate(self.adj_matrix[vertices[node].index]):
            next_node = self.idx_vertex_map[idx]
            if neighbor == 1 and vertices[next_node].color == 'white':
                vertices[next_node].pred = vertices[node]
                self.dfs_visit(next_node, vertices)
        vertices[node].color = 'black'
        self.time += 1
        vertices[node].f = self.time
        self.sorted_arr.append(vertices[node])

    def dfs(self, vertices):
        self.time = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.adj_matrix[row][col] == 1 and vertices[self.idx_vertex_map[row]].color == 'white':
                    self.dfs_visit(self.idx_vertex_map[row], vertices)

    def topological_sort(self, vertices):
        self.dfs(vertices)
        return list(reversed(self.sorted_arr))


def main(ARGS):
    file_name = ''
    if ARGS.graph01:
        file_name = 'graph01.txt'
    elif ARGS.graph02:
        file_name = 'graph02.txt'
    elif ARGS.biggraph:
        file_name = 'biggraph.txt'
    else:
        file_name = 'test_case1.txt'

    num_of_vertices = 0
    vertices = collections.defaultdict(list)
    edges = []
    with open(file_name) as f:
        # Get number of nodes
        num_of_vertices = int(f.readline())

        # Skip #
        f.readline()

        # Get vertices
        line = f.readline().strip()
        i = 0
        vertices[line] = Node(i)
        while True:
            line = f.readline().strip()
            if line == '#':
                break
            i += 1
            vertices[line] = Node(i)

        # Get edges
        line = f.readline().strip()
        edges.append(line.split())

        while True:
            line = f.readline().strip()
            if not line:
                break
            edges.append(line.split())

    # create graph
    g = Graph(num_of_vertices)
    for edge in edges:
        g.add_edge(vertices[edge[0]].index, vertices[edge[1]].index)

    if ARGS.debug:
        print(format('Adjacency matrix', '*^100s'))
        print(g)

    for k, v in vertices.items():
        g.map_index_vertex(v.index, k)

    if ARGS.debug:
        print(format('Topological Sort', '*^100s'))
    sorted_g = g.topological_sort(vertices)
    if ARGS.debug:
        for k, v in vertices.items():
            print('node={} predecessor={} d={} f={}'.format(
                k, [g.idx_vertex_map[v.pred.index] if v.pred else None], v.d, v.f))

    print('\nTopological sort:')
    print('{:20s}'.format('Node: '), end=' ')
    for x in sorted_g:
        print('{:3s}'.format(g.idx_vertex_map[x.index]), end=' ')
    print('\n')
    print('{:20s}'.format('Finishing Time: '), end=' ')
    for x in sorted_g:
        print('{:3s}'.format(str(x.f)), end=' ')
    print('\n')

    if ARGS.debug:
        print(format('The number of hops (semesters) on the longest path', '*^100s'))
    dp = [0] * len(sorted_g)
    for i, vertex in enumerate(sorted_g):
        if vertex.pred is None:
            dp[i] = 0
        else:
            dp[i] = dp[sorted_g.index(vertex.pred)] + 1

    print('Length of the longest path:')
    print(max(dp))
    print('A longest path:')
    curr = sorted_g[dp.index(max(dp))]
    path = []
    while curr:
        path.append(g.idx_vertex_map[curr.index])
        curr = curr.pred
    for x in reversed(path):
        print(x, end=' ')

    print('\n')

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Project 1: Graduation Time')
    PARSER.add_argument('-d', '--debug', action='store_true')
    GROUP = PARSER.add_mutually_exclusive_group()

    GROUP.add_argument('-1', '--graph01', action='store_true')
    GROUP.add_argument('-2', '--graph02', action='store_true')
    GROUP.add_argument('-3', '--biggraph', action='store_true')
    GROUP.add_argument('-4', '--test_case1', action='store_true')

    ARGS = PARSER.parse_args()
    if not any([ARGS.graph01, ARGS.graph02, ARGS.biggraph, ARGS.test_case1, ARGS.debug]):
        PARSER.print_help()
        exit(0)
    main(ARGS)
