from FlowEdge import FlowEdge
import copy


class BaseballElimination:

    def __init__(self, filename):
        self.file = open(filename)
        self.teams = int(self.file.readline())
        c = self.teams
        self.winCount = [0 for x in range(c)]
        self.loseCount = [0 for x in range(c)]
        self.remainingCount = [0 for x in range(c)]
        self.gameGrid = [[0 for x in range(c)] for y in range(c)]
        self.teamToIndex = dict()
        self.indexToTeam = [0 for x in range(c)]
        self.results = dict()
        self.certificates = dict()
        self.graph = dict()
        self.temp_teams = None
        self.cur_team = None
        self.process_file()

        for x in self.indexToTeam:
            self.graph_construction(x)

    def process_file(self):

        c = self.teams

        count = 0
        ti = self.teamToIndex
        it = self.indexToTeam

        for x in range(c):
            line = self.file.readline().split()
            ti[line[0]] = count
            it[count] = line[0]

            self.winCount[count] = int(line[1])
            self.loseCount[count] = int(line[2])
            self.remainingCount[count] = int(line[3])

            for y in range(c):
                self.gameGrid[count][y] = int(line[4+y])
            count += 1

    def number_of_teams(self):
        return self.indextoTeam

    def wins(self, team: str):

        if team in self.teamToIndex:
            return self.winCount[self.teamToIndex[team]]
        else:
            return "Team does not exist"

    def losses(self, team: str):

        if team in self.teamToIndex:
            return self.loseCount[self.teamToIndex[team]]
        else:
            return "Team does not exist"

    def remaining(self, team: str):

        if team in self.teamToIndex:
            return self.remainingCount[self.teamToIndex[team]]
        else:
            return "Team does not exist"

    def against(self, team1: str, team2: str):

        if team1 not in self.teamToIndex:
            return "First team does not exist"

        if team2 not in self.teamToIndex:
            return "Second team does not exist"

        return self.gameGrid[self.teamToIndex[team1]][self.teamToIndex[team2]]

    def print_info(self):

        max_len = 0
        teams = self.indexToTeam
        for x in teams:
            max_len = max(max_len,len(x))

        max_len += 2
        for x in teams:
            temp = [p1.against(x, w) for w in teams]
            ss = ""
            for w in temp:
                ss += str(w) + " "
            sp = " " *(max_len-len(x))
            print(x + sp + str(self.wins(x)) + " " + str(self.losses(x)) + " " + str(self.remaining(x)) + "  " + ss)

    def is_eliminated(self, team: str):

        if team in self.teamToIndex:
            return self.remainingCount[self.teamToIndex[team]]
        else:
            return self.results[team]

    def certificate_of_elimination(self, team: str):

        if team in self.teamToIndex:
            return self.remainingCount[self.teamToIndex[team]]
        else:
            return self.certificates[team]

    def graph_construction(self, team: str):

        self.graph = dict()
        graph = self.graph
        self.cur_team = team
        self.temp_teams = copy.deepcopy(self.indexToTeam)
        temp_teams = self.temp_teams
        temp_teams.pop(self.teamToIndex[team])

        mix = self.wins(team)+self.remaining(team)

        c = self.teams-1

        graph['src'] = dict()
        graph['dest'] = dict()

        for x in temp_teams:
            graph[x] = dict()
            forward = FlowEdge(max(0, mix-self.wins(x)))
            if mix-self.wins(x) < 0:
                self.results[self.cur_team] = True
                self.certificates[self.cur_team] = {x}
                return
            reverse = FlowEdge(0)
            forward.connect(reverse)
            reverse.connect(forward)
            graph[x]['dest'] = forward
            graph['dest'][x] = reverse

        for i in range(c):
            for j in range(i+1, c):
                node = temp_teams[i]+" || "+temp_teams[j]
                graph[node] = dict()

                balance = self.against(temp_teams[i], temp_teams[j])
                forward1 = FlowEdge(balance)
                reverse1 = FlowEdge(0)
                forward1.connect(reverse1)
                reverse1.connect(forward1)
                graph['src'][node] = forward1
                graph[node]['src'] = reverse1

                forward2 = FlowEdge(100000)
                reverse2 = FlowEdge(0)
                forward2.connect(reverse2)
                reverse2.connect(forward2)
                graph[node][temp_teams[i]] = forward2
                graph[temp_teams[i]][node] = reverse2

                forward3 = FlowEdge(100000)
                reverse3 = FlowEdge(0)
                forward3.connect(reverse3)
                reverse3.connect(forward3)
                graph[node][temp_teams[j]] = forward3
                graph[temp_teams[j]][node] = reverse3

        self.ford_fulkerson()

    def ford_fulkerson(self):

        temp_teams = self.temp_teams
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
                            q.append((x, temp_node[1]+";"+x))

            if path != "":
                nodes = path.split(";")
                nodes.pop(0)
                nodes.insert(0, 'src')
                nodes.append('dest')

                r = len(nodes)

                for i in range(r-1):
                    bottleneck = min(bottleneck, graph[nodes[i]][nodes[i+1]].get_capacity())
                for i in range(r-1):
                    graph[nodes[i]][nodes[i + 1]].send_flow(bottleneck)
            else:
                break

        src_adj = graph['src']
        eliminated = False
        r_set = set()
        for x in src_adj:
            if src_adj[x].get_capacity() != 0:
                eliminated = True

        if eliminated:
            visited = dict()

            for x in graph:
                visited[x] = False

            q = list()
            q.append('src')

            while len(q) > 0:
                temp_node = q.pop(0)
                adj = graph[temp_node]
                visited[temp_node] = True

                for x in adj:
                    if adj[x].get_capacity() > 0 and visited[x] == False: q.append(x)

            for x in temp_teams:
                if visited[x]: r_set.add(x)

        self.results[self.cur_team] = eliminated
        self.certificates[self.cur_team] = r_set

    def print_results(self):

        self.print_info()
        print()

        for x in self.indexToTeam:
            if self.results[x]:
                print(x+" is eliminated by the subset R = "+str(self.certificates[x]))
            else:
                print(x+" is not eliminated")


p1 = BaseballElimination("teams54.txt")
p1.print_results()
