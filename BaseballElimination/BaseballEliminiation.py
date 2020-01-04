class BaseballElimination:
    def __init__(self,filename):
        self.file = open(filename)
        self.teams = int(self.file.readline())
        self.processFile()

    def processFile(self):

        c = self.teams
        self.winCount = [0 for x in range(c)]
        self.loseCount = [0 for x in range(c)]
        self.remainingCount = [0 for x in range(c)]
        self.gameGrid = [[0 for x in range(c)] for y in range(c)]

        count = 0
        self.teamToIndex = dict()
        self.indextoTeam = [0 for x in range(c)]
        ti = self.teamToIndex
        it = self.indextoTeam

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

    def numberOfTeams(self):
        return self.indextoTeam

    def wins(self,team: str):
        if team in self.teamToIndex:
            return self.winCount[self.teamToIndex[team]]
        else:
            return "Team does not exist"

    def losses(self,team: str):
        if team in self.teamToIndex:
            return self.loseCount[self.teamToIndex[team]]
        else:
            return "Team does not exist"

    def remaining(self,team: str):
        if team in self.teamToIndex:
            return self.remainingCount[self.teamToIndex[team]]
        else:
            return "Team does not exist"

    def against(self,team1:str, team2:str):

        if team1 not in self.teamToIndex:
            return "First team does not exist"

        if team2 not in self.teamToIndex:
            return "Second team does not exist"

        return self.gameGrid[self.teamToIndex[team1]][self.teamToIndex[team2]]

    def printInfo(self):

        maxlen = 0
        teams = self.indextoTeam
        for x in teams:
            maxlen = max(maxlen,len(x))

        maxlen+= 2
        for x in teams:
            temp = [p1.against(x, w) for w in teams]
            ss = ""
            for w in temp:
                ss += str(w) + " "
            sp = " " *(maxlen-len(x))
            print(x + sp + str(p1.wins(x)) + " " + str(p1.losses(x)) + " " + str(p1.remaining(x)) + "  " + ss)


p1 = BaseballElimination("team4")
p1.printInfo()
