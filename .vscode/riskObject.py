import numpy as np
import random

from graphviz import Graph

class risk:
    def __init__(self, players=6):

        self.players = players

        self.continentList = [[0,1,2,3,4,5,6,7,8], #north america
                        [9,10,11,12], #south america
                        [13,14,15,16,17,18,19], #europe
                        [20,21,22,23,24,25], #africa
                        [26,27,28,29,30,31,32,33,34,35,36,37], #asia
                        [38,39,40,41]] #oceania
        self.borderList = [[1,2,31],[0,2,3,4],[0,1,3,4,5],[1,2,4,6,13],[1,2,3,5,6,7],[2,4,7,8],[3,4,7],[4,5,6,8],[5,7,9], #0-8 north america
                    [8,10,11],[9,11,12,20],[9,10,12],[10,11], #9-12 south america
                    [3,14,15],[13,15,16,18],[13,14,16,17],[14,15,17,18,19],[15,16,19,20],[14,16,19,26,27,28],[16,17,18,20,21,28], #13-19 europe
                    [10,17,19,21,22,23],[19,20,22,28],[20,21,23,24,25,28],[20,22,24],[22,23,25],[22,24], #20-25 africa
                    [18,27,29,35],[18,26,28,35,36],[18,19,21,22,27,36],[26,30,32,34,35],[29,31,32],[0,30,32,33,34],[29,30,31,34],[31,34],[29,31,32,33,35],[26,27,29,34,36,37],[27,28,35,37],[35,36,38], #26-37 asia
                    [37,39],[38,40,41],[39,41],[39,40]] #38-41 oceania
        self.borderMap = np.zeros(((max(max(self.continentList))+1),(max(max(self.continentList)))+1))

        for i in range(len(self.borderList)):
            for j in self.borderList[i]:
                self.borderMap[i,j]=1

        #np.savetxt("borderMap",borderMap,fmt ='%.0f')

        self.ownerList = [None]*len(self.borderList)
        self.troopList = [0]*len(self.borderList)

        self.cardPile = [[None,0],[None,0],[None,0],[33, 2],[35, 3],[18, 1],[20, 1],[23, 3],[27, 1],[28, 3],[9, 2],[19, 1],[16, 2],[3, 2],[37, 2],[32, 3],[36, 2],[2, 3],[21, 2],[31, 3],[17, 1],[38, 1],[30, 3],[12, 1],[41, 2],[22, 1],[41, 3],[25, 2],[18, 1],[4, 3],[8, 1],[10, 1],[1, 2],[11, 2],[24, 3],[5, 3],[6, 3],[15, 1],[14, 1],[34, 2],[26, 1],[13, 2],[7, 3],[39, 2],[0, 3]]

        random.shuffle(self.cardPile)

        self.cardList = [[] for _ in range(players)]

        self.playerTurn = 0

        self.setupMap()

    def setupMap(self):
        troops = [25]*(self.players-1)
        i = 0
        while None in self.ownerList:
            #test = ownerList.index(-1)
            remainingCountries = [j for j, x in enumerate(self.ownerList) if x == None]
            selection = random.choice(remainingCountries)
            self.ownerList[selection] = self.playerTurn
            self.troopList[selection] = 1
            self.playerTurn = self.playerTurn+1
            if self.playerTurn > self.players-1:
                self.playerTurn = 0
            i = i+1

        for i in range(self.players-1):
            for j in range(troops[i]):
                remainingCountries = [j for j, x in enumerate(self.ownerList) if x == i]
                selection = random.choice(remainingCountries)
                self.troopList[selection] = self.troopList[selection] + 1

        self.createMap()

    def dealCard(self):
        self.cardList[self.playerTurn].append(self.cardPile.pop(0))

    def createMap(self):
        worldMap = Graph(graph_attr={'rankdir':'LR'})
        for i in range(len(self.continentList)):
            with worldMap.subgraph(name='cluster'+str(i)) as c:
                for j in self.continentList[i]:
                    c.node(str(j))
        
        worldMapEdges = []
        for i in range(len(self.borderList)):
            for j in self.borderList[i]:
                if str(j)+str(i) not in worldMapEdges:
                    worldMapEdges.append(str(i)+str(j))
                    worldMap.edge(str(i),str(j))

        ownerColour = ['red','green','blue','purple','orange','yellow']

        for i in range(len(self.ownerList)):
            worldMap.node(str(i),style='filled',fillcolor=ownerColour[self.ownerList[i]])

        for i in range(len(self.troopList)):
            worldMap.node(str(i),label='< <b>      '+str(i)+'    </b> <br/>'+str(self.troopList[i])+'>')

        worldMap.save()

game = risk()
game.dealCard()