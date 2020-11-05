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
    for i in range(min([len(attackerDice),len(defenderDice)])):
        if defenderDice[i] >= attackerDice[i]:
            attackerLoss = attackerLoss - 1
        else:
            defenderLoss = defenderLoss - 1
    print(attackerLoss,defenderLoss)
    return attackerLoss, defenderLoss, attackerDiceNo

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

ownerList = [None]*len(borderList)
troopList = [0]*len(borderList)

#print(ownerList)

#troopList = []

#random start map
players = 6-1
troops = [25]*players
turn = 0
i = 0
while None in ownerList:
    #test = ownerList.index(-1)
    remainingCountries = [j for j, x in enumerate(ownerList) if x == None]
    selection = random.choice(remainingCountries)
    ownerList[selection] = turn
    troopList[selection] = 1
    turn = turn+1
    if turn > players:
        turn = 0
    i = i+1

for i in range(players):
    for j in range(troops[i]):
        remainingCountries = [j for j, x in enumerate(ownerList) if x == i]
        selection = random.choice(remainingCountries)
        troopList[selection] = troopList[selection] + 1
    

#for i in range(0,(max(max(continentList))+1)):
#    n = random.randint(1,5)
#    troopList.append(n)
#print(troopList)

createMap(continentList,borderList,ownerList,troopList)

#attackerDiceNo = 2
#defenderDiceNo = 2
#attackerLoss, defenderLoss = rollDice(attackerDiceNo,defenderDiceNo)

#print(attackerLoss,defenderLoss)

attackerCountry = 0
defenderCountry = 1
def reinforce(ownerList,troopList,reinforceCountry,baseCountry=-1,troops=1):
    if not baseCountry == -1:
        troopList[baseCountry] = troopList[baseCountry]-troops
    troopList[reinforceCountry] = troopList[reinforceCountry]+troops
    return ownerList, troopList


def battle(attackerCountry,defenderCountry,ownerList,troopList):

    print(attackerCountry, defenderCountry)

    while troopList[attackerCountry]>1:
        if troopList[attackerCountry]>3:
            attackerDiceNo = 3
        else:
            attackerDiceNo = troopList[attackerCountry]-1

        if troopList[defenderCountry]>1:
            defenderDiceNo = 2
        else:
            defenderDiceNo = 1

        attackerLoss, defenderLoss, attackerDiceNo = rollDice(attackerDiceNo,defenderDiceNo)

        troopList[attackerCountry] = troopList[attackerCountry]+attackerLoss
        troopList[defenderCountry] = troopList[defenderCountry]+defenderLoss

        if troopList[defenderCountry]<=0:
            ownerList[defenderCountry]=ownerList[attackerCountry]
            break
    return ownerList, troopList
input("Press Enter to continue...")
ownerList, troopList = battle(attackerCountry,defenderCountry,ownerList,troopList)

createMap(continentList, borderList, ownerList, troopList)