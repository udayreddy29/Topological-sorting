# Python program to print topological sorting of a DAG
from collections import defaultdict
from collections import OrderedDict
# Class to represent a graph
from operator import getitem
import time


class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)  # dictionary containing adjacency List
        self.V = vertices  # No. of vertices
        self.dic = dict()
        self.time = 0
        self.t = time.time()
        # self.pred = 0

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        for val in [u, v]:
            # if val not in self.dic.keys():
            if val not in list(self.dic):
                self.dic[val] = {
                    'color': 'white',
                    'd': 0,
                    'f': 0,
                    'P': None,
                    # 'pred': 0,
                }

    def addEdgeByPath(self, path):
        file1 = open(path, 'r')
        Lines = file1.readlines()
        for line in Lines:
            line = line.strip()
            lineArray = line.split(' ')
            self.addEdge(lineArray[0], lineArray[1])

    def DFS(self):
        # for val in self.graph.keys():
        for val in list(self.graph):
            # self.graph.l = self.graph
            # self.dic[val]['l'] = self.dic[self.dic[val]['p']]['l'] + 1
            # print('val is', val)
            if self.dic[val]['color'] == 'white':
                self.DFS_VISIT(val)

    def DFS_VISIT(self, u):
        self.time += 1
        self.dic[u]['d'] = self.time
        self.dic[u]['color'] = 'grey'
        for i in self.graph[u]:
            if self.dic[i]['color'] == 'white':
                self.dic[i]['P'] = u
                self.DFS_VISIT(i)
        self.dic[u]['color'] = 'black'
        self.time = self.time + 1
        self.dic[u]['f'] = self.time

    def longestPath(self):
        res = OrderedDict(sorted(self.dic.items(),
                                 key=lambda x: getitem(x[1], 'f'), reverse=True))
        dp = [0] * len(list(res))
        sortedArray = list(res)
        for i, element in enumerate(sortedArray):
            if self.dic[element]['P'] is None:
                dp[i] = 0
            else:
                dp[i] = dp[sortedArray.index(self.dic[element]['P'])] + 1

        print('longest distance is', max(dp))
        currNode = sortedArray[dp.index(max(dp))]
        path = []
        # print('current Node is', currNode)
        while currNode:
            path.append(currNode)
            currNode = self.dic[currNode]['P']
        print('longest path is', path[::-1])
        t2 = time.time()
        print('time taken to sovle is', round((t2 - self.t) * 1000,2) , 'ms')

    def finalData(self):
        res = OrderedDict(sorted(self.dic.items(),
                                 key=lambda x: getitem(x[1], 'f'), reverse=True))
        print('tropological order is', list(res))


g = Graph(50)
g.addEdgeByPath('/Users/udayreddy/Desktop/adListData.txt')

# #
# g.addEdge('A1', 'B1');
# g.addEdge('B1', 'A2');
# g.addEdge('A1', 'C1');
# g.addEdge('C1', 'B2');
# g.addEdge('C2', 'B2');

# g.iterateLoop()
g.DFS()
g.finalData()
g.longestPath()
