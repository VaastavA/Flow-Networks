class BaseballElimination:
    def __init__(self,filenme):
        self.file = open(filenme)
        self.teams = int(self.file.readline())
        self.processFile()

    def processFile(self):

        c = self.teams
        self.wins = [0 for x in range(c)]
        self.loses = [0 for x in range(c)]
        self.remaining = [0 for x in range(c)]
        self.gameGrid = [[0 for x in range(c)] for y in range(c)]

        count = 0
        self.teamToIndex = dict()
        self.indextoTeam = [0 for x in range(c)]
        ti = self.teamToIndex
        it = self.indextoTeam

        for x in range(c):
            line = self.file.readline().split()
            ti[line[0]] = line[0]
            it[count] = [0 for x in range(c)]

            self.wins[count] = int(line[1])
            self.loses[count] = int(line[2])
            self.remaining[count] = int(line[3])

            for y in range(c):
                self.gameGrid[count][y] = int(line[4+y])
            count += 1

p1 = BaseballElimination("team4")
print(p1.gameGrid)