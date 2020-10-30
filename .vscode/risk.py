import numpy as np
import random

def rollDice(attackerDiceNo=3,defenderDiceNo=2):
    attackerDice = []
    defenderDice = []

    for i in range(attackerDiceNo):
        attackerDice.append(random.randint(1,6))
    attackerDice.sort(reverse=True)

    print(attackerDice)


    for i in range(defenderDiceNo):
        defenderDice.append(random.randint(1,6))
    defenderDice.sort(reverse=True)

    print(defenderDice)

    attackerLoss = 0
    defenderLoss = 0
    for i in range(len(defenderDice)):
        if defenderDice[i] >= attackerDice[i]:
            attackerLoss = attackerLoss - 1
        else:
            defenderLoss = defenderLoss - 1
    return attackerLoss, defenderLoss

def createMap(continentList,borderList,ownerList,troopList):
    from graphviz import Graph

    worldMap = Graph()#(graph_attr={'rankdir':'LR'})
    for i in range(len(continentList)):
        #print(i)
        with worldMap.subgraph(name='cluster'+str(i)) as c:
            for j in continentList[i]:
                #print(j)
                c.node(str(j))
    
    worldMapEdges = []
    for i in range(len(borderList)):
        for j in borderList[i]:
            if str(j)+str(i) not in worldMapEdges:
                worldMapEdges.append(str(i)+str(j))
                worldMap.edge(str(i),str(j))
    worldMap.save()  

    ownerColour = ['red','green','blue','purple','orange','yellow']

    for i in range(len(ownerList)):
        worldMap.node(str(i),style='filled',fillcolor=ownerColour[ownerList[i]])

    for i in range(len(troopList)):
        worldMap.node(str(i),label='< <b>      '+str(i)+'    </b> <br/>'+str(troopList[i])+'>')
    worldMap.save()

continentList = [[0,1,2,3,4,5,6,7,8], #north america
                [9,10,11,12], #south america
                [13,14,15,16,17,18,19], #europe
                [20,21,22,23,24,25], #africa
                [26,27,28,29,30,31,32,33,34,35,36,37], #asia
                [38,39,40,41]] #oceania
borderList = [[1,2,31],[0,2,3,4],[0,1,4,5],[1,2,4,6],[1,2,3,5,6,7],[2,4,7,8],[3,4,7],[4,5,6,8],[5,7,9], #0-8 north america
            [8,10,11],[9,11,12,20],[9,10,12],[10,11], #9-12 south america
            [3,14,15],[13,15,16,18],[13,14,16,17],[14,15,17,18,19],[15,16,19,20],[14,16,19,26,27,28],[16,17,18,20,21,28], #13-19 europe
            [10,17,19,21,22,23],[19,20,22,28],[20,21,23,24,25,28],[20,22,24],[22,23,25],[22,24], #20-25 africa
            [18,27,29,35],[18,26,28,35,36],[18,19,21,22,27,36],[26,30,32,34,35],[29,31,32],[0,30,32,33,34],[29,30,31,34],[31,34],[29,31,32,33,35],[26,27,29,34,36,37],[27,28,35,37],[35,36,38], #26-37 asia
            [37,39],[38,40,41],[39,41],[39,40]] #38-41 oceania
borderMap = np.zeros(((max(max(continentList))+1),(max(max(continentList)))+1))

#print(borderMap.shape)

for i in range(len(borderList)):
    for j in borderList[i]:
        borderMap[i,j]=1

#np.savetxt("borderMap",borderMap,fmt ='%.0f')

ownerList = []
for i in range(0,(max(max(continentList))+1)):
    n = random.randint(0,5)
    ownerList.append(n)
#print(ownerList)

troopList = []
for i in range(0,(max(max(continentList))+1)):
    n = random.randint(0,5)
    troopList.append(n)
#print(troopList)

createMap(continentList,borderList,ownerList,troopList)

attackerDiceNo = 2
defenderDiceNo = 2
print(rollDice(attackerDiceNo,defenderDiceNo))