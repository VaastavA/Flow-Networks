from FlowEdge import FlowEdge


class CustomError(Exception):
    pass


class BipartiteMatching:

    def __init__(self, filename: str):
        self.file = open(filename)
        self.leftSize, self.rightSize = 0, 0
        self.leftSet,self.rightSet = list(), list()
        self.matchingMatrix = []
        self.graph = dict()
        self.matching = list()
        self.left_unmatched,self.right_unmatched = list(), list()
        self.process_file()
        self.graph_construction()

    def process_file(self):
        file = self.file
        self.leftSize, self.rightSize = list(map(int, file.readline().split(" ")))

        for x in range(self.leftSize):
            self.leftSet.append(file.readline().split("\n")[0])
        for x in range(self.rightSize):
            self.rightSet.append(file.readline().split("\n")[0])

        for x in range(self.leftSize):
            self.matchingMatrix.append(list(map(int, file.readline().split(" "))))

    def graph_construction(self):

        graph = self.graph

        graph['src'] = dict()
        graph['dest'] = dict()

        for x in self.leftSet:
            graph[x] = dict()
            forward = FlowEdge(1)
            reverse = FlowEdge(0)
            forward.connect(reverse)
            reverse.connect(forward)
            graph['src'][x] = forward
            graph[x]['src'] = reverse

        for x in self.rightSet:
            graph[x] = dict()
            forward = FlowEdge(1)
            reverse = FlowEdge(0)
            forward.connect(reverse)
            reverse.connect(forward)
            graph[x]['dest'] = forward
            graph['dest'][x] = reverse

        for x in range(self.leftSize):
            for y in range(self.rightSize):
                if self.matchingMatrix[x][y] == 1:
                    forward = FlowEdge(100)
                    reverse = FlowEdge(0)
                    forward.connect(reverse)
                    reverse.connect(forward)
                    graph[self.leftSet[x]][self.rightSet[y]] = forward
                    graph[self.rightSet[y]][self.leftSet[x]] = reverse

        self.ford_fulkerson()

    def ford_fulkerson(self):

        graph = self.graph

        while True:
            visited = dict()

            for x in graph:
                visited[x] = False

            path = ""
            bottleneck = 100001
            q = list()
            q.append(('src', ""))

            while len(q) > 0 and path == "":
                temp_node = q.pop(0)
                adj = graph[temp_node[0]]
                visited[temp_node[0]] = True

                for x in adj:
                    if adj[x].get_capacity() > 0 and visited[x] == False:
                        if x == 'dest':
                            path = temp_node[1]
                            break
                        else:
                            q.append((x, temp_node[1] + ";" + x))

            if path != "":
                nodes = path.split(";")
                nodes.pop(0)
                nodes.insert(0, 'src')
                nodes.append('dest')

                r = len(nodes)

                for i in range(r - 1):
                    bottleneck = min(bottleneck, graph[nodes[i]][nodes[i + 1]].get_capacity())
                for i in range(r - 1):
                    graph[nodes[i]][nodes[i + 1]].send_flow(bottleneck)
            else:
                break

        x = 0
        while x < self.leftSize:
            try:
                for y in range(self.rightSize):
                    if self.matchingMatrix[x][y] == 1 and graph[self.leftSet[x]][self.rightSet[y]].get_capacity() == 99:
                        self.matching.append((self.leftSet[x], self.rightSet[y]))
                        x += 1
                        raise CustomError
                x += 1
            except CustomError:
                pass

        

    def print_results(self):

        print("Format: [Element in left set] has been matched with [Element in right set")
        print()

        for x in self.matching:
            print(x[0]+" has been matched with "+x[1])
        print()
        print("Elements remaining unmatched in left set:  "+str(self.left_unmatched))
        print("Elements remaining unmatched in right set:  "+str(self.right_unmatched))


p1 = BipartiteMatching("data1.txt")
p1.print_results()

