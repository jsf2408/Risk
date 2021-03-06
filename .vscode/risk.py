import numpy as np
import random
from graphviz import Graph

print("RISK")

def dealCard(cardPile,cardList,playerTurn=0):
    cardList[playerTurn].append(cardPile.pop(0))
    return cardPile, cardList

def tradeInCards(cardPile,cardList,tradeList,playerTurn=0):
    bonusUnits = 0
    bonusCountry = cardList[playerTurn][tradeList[0]][0]

    troopValues = []
    for i in tradeList:
        troopValues.append(cardList[playerTurn][i][1])

    print(troopValues)
    troopValues = set(troopValues)
    if troopValues == set(1,2,3):
        bonusUnits = 10
    elif troopValues == set(3,3,3): #set ignores duplicates
        bonusUnits = 8
    elif troopValues == set(2,2,2):
        bonusUnits = 6
    elif troopValues == set(1,1,1):
        bonusUnits = 4
        
    return bonusUnits, cardPile, cardList

def rollDice(attackerDiceNo=3,defenderDiceNo=2):
    attackerDice = []
    defenderDice = []

    for i in range(attackerDiceNo):
        attackerDice.append(random.randint(1,6))
    attackerDice.sort(reverse=True)

    for i in range(defenderDiceNo):
        defenderDice.append(random.randint(1,6))
    defenderDice.sort(reverse=True)

    attackerLoss = 0
    defenderLoss = 0
    for i in range(min([len(attackerDice),len(defenderDice)])):
        if defenderDice[i] >= attackerDice[i]:
            attackerLoss = attackerLoss - 1
        else:
            defenderLoss = defenderLoss - 1
    if attackerDiceNo == 3:
        tabString = "\t"
    else:
        tabString = "\t\t"
    if defenderDiceNo == 2:
        tabString2 = "\t"
    else:
        tabString2 = "\t\t"
    print(attackerDice,tabString,defenderDice,tabString2,attackerLoss,"\t",defenderLoss)
    return attackerLoss, defenderLoss, attackerDiceNo

def createMap(continentList,borderList,ownerList,troopList):
    worldMap = Graph()#graph_attr={'rankdir':'LR'})
    for i in range(len(continentList)):
        with worldMap.subgraph(name='cluster'+str(i)) as c:
            for j in continentList[i]:
                c.node(str(j))
    
    worldMapEdges = []
    for i in range(len(borderList)):
        for j in borderList[i]:
            if str(j)+str(i) not in worldMapEdges:
                worldMapEdges.append(str(i)+str(j))
                worldMap.edge(str(i),str(j))

    ownerColour = ['red','green','blue','purple','orange','yellow']

    for i in range(len(ownerList)):
        worldMap.node(str(i),style='filled',fillcolor=ownerColour[ownerList[i]])

    for i in range(len(troopList)):
        worldMap.node(str(i),label='< <b>      '+str(i)+'    </b> <br/>'+str(troopList[i])+'>')
    worldMap.save()

def setupMap(ownerList,troopList,players=6):
    players = players-1
    troops = [25]*(players)
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
    createMap(continentList,borderList,ownerList,troopList)
    return ownerList,troopList,turn

def calcUnits(ownerList, continentList, playerTurn = 0):
    countryBonus = ownerList.count(playerTurn)//3
    if countryBonus < 3:
        countryBonus = 3
    
    #calc continentBonus
    continentOwner = continentList.copy()
    for i in continentOwner:
        for j in i:
            i = ownerList[j]

    totalBonus = countryBonus#+continentBonus
    return totalBonus

def pathCheck(ownerList,troopList,seedCountry,targetCountry, playerTurn = 0):
    borderCountries = []
    borderCountries.append(seedCountry)
    newBorders = []
    while True:
        for z in borderCountries:
            for i in borderList[z]:
                newBorders.append(i)

        removeCountries = []
        for i in newBorders:
            if ownerList[i] != playerTurn:
                removeCountries.append(i)

        for i in newBorders:
            for j in borderCountries:
                if i==j:
                    removeCountries.append(i)

        for i in removeCountries:
            while i in newBorders: 
                newBorders.remove(i)

        newBorders = list(dict.fromkeys(newBorders))

        if len(newBorders) > 0:
            for i in newBorders:
                borderCountries.append(i)
        else:
            break

    if targetCountry in borderCountries:
        return True
    else:
        return False

def reinforce(ownerList,troopList,reinforceCountry,baseCountry=-1,troops=0):
    if not baseCountry == -1:
        troopList[baseCountry] = troopList[baseCountry]-troops
    troopList[reinforceCountry] = troopList[reinforceCountry]+troops
    return ownerList, troopList

def battle(attackerCountry,defenderCountry,ownerList,troopList,style='blitz'):
    if style == 'blitz':
        while troopList[attackerCountry]>1 and troopList[defenderCountry]>0:
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
    else:
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
        print("Victory!")
        victory = True
        ownerList[defenderCountry]=ownerList[attackerCountry]
        ownerList,troopList=reinforce(ownerList,troopList,defenderCountry,attackerCountry,attackerDiceNo)
    else:
        victory = False
    return ownerList, troopList, victory

def draftPhase(ownerList, troopList, continentList, playerTurn = 0):
    print("Starting draft phase...")
    reinforcements = calcUnits(ownerList, continentList, playerTurn)
    while reinforcements > 0:
        print("You have "+str(reinforcements)+" units remaining.")
        while True:
            reinforceCountry = input("Which country would you like to reinforce? ")
            try:
                reinforceCountry = int(reinforceCountry)
            except:
                continue
            if playerTurn == ownerList[reinforceCountry]: break
        
        while True:
            reinforceUnit = input("How many units would you like to send? ")
            try:
                reinforceUnit = int(reinforceUnit)
            except:
                continue
            if reinforceUnit <= reinforcements and reinforceUnit > 0: break
        
        ownerList, troopList = reinforce(ownerList, troopList, reinforceCountry, troops=reinforceUnit)
        reinforcements = reinforcements-reinforceUnit
        createMap(continentList, borderList, ownerList, troopList)
    print("Ending draft phase...")
    return ownerList, troopList

def attackPhase(ownerList, troopList, borderlist, playerTurn = 0):
    print("Starting attack phase...")
    attackOrder = None
    attackEnd = None
    battleWon = False

    while attackEnd != "y":
        attackOrder = input("Would you like to attack a country? ")
        if not (attackOrder == "n" or attackOrder == "y"): continue
        if attackOrder == "n":
            while True:
                attackEnd = input("Are you sure? ")
                if (attackEnd == "n" or attackEnd == "y"): break
            continue
        while True:
            attackerCountry = input("Which country would you like to attack from? ")
            try:
                attackerCountry = int(attackerCountry)
            except:
                continue
            if playerTurn == ownerList[attackerCountry] and troopList[attackerCountry]>1: break
        while True:
            defenderCountry = int(input("Which country would you like to attack? "))
            try:
                defenderCountry = int(defenderCountry)
            except:
                continue
            if defenderCountry in borderList[attackerCountry] and ownerList[defenderCountry]!=ownerList[attackerCountry]: break
        while True:
            attackConfirmation = input("Confirm order?: "+str(attackerCountry)+"->"+str(defenderCountry)+" ")
            if (attackConfirmation == "n" or attackConfirmation == "y"): break
        if attackConfirmation == "y":
            ownerList, troopList, victory = battle(attackerCountry,defenderCountry,ownerList,troopList)
            createMap(continentList,borderList,ownerList,troopList)
            if victory:
                battleWon = True
                while True:
                    reinforceUnits = input("How many additional units would you like to send? ")
                    try:
                        reinforceUnits = int(reinforceUnits)
                    except:
                        continue
                    if reinforceUnits >= 0 and reinforceUnits < troopList[attackerCountry]: break
                ownerList, troopList = reinforce(ownerList,troopList,defenderCountry,attackerCountry,reinforceUnits)
                createMap(continentList,borderList,ownerList,troopList)
        continue
    print("Ending attack phase...")
    return ownerList, troopList

def fortifyPhase(ownerList,troopList,borderList, playerTurn = 0):
    print("Starting fortify phase...")
    fortifyEnd = None
    while fortifyEnd != "y":
        while True:
            fortifyOrder = input("Would you like to fortify? ")
            if (fortifyOrder == "n" or fortifyOrder == "y"): break
        if fortifyOrder == "n":
            while True:
                fortifyEnd = input("Are you sure? ")
                if (fortifyEnd == "n" or fortifyEnd == "y"): break
            continue
        while True:
            baseCountry = input("Which country would you like to fortify from? ")
            try:
                baseCountry = int(baseCountry)
            except:
                continue
            if playerTurn == ownerList[baseCountry] and troopList[baseCountry]>1: break
        while True:
            reinforceCountry = int(input("Which country would you like to fortify? "))
            try:
                reinforceCountry = int(reinforceCountry)
            except:
                continue
            if ownerList[reinforceCountry] == playerTurn and pathCheck(ownerList,troopList,baseCountry,reinforceCountry): break
        while True:
            reinforceTroops = int(input("How many troops would you like to move? "))
            try:
                reinforceTroops = int(reinforceTroops)
            except:
                continue
            if reinforceTroops < troopList[baseCountry] and reinforceTroops > 0: break
        while True:
            fortifyEnd = input("Confirm order?: "+str(baseCountry)+"->"+str(reinforceTroops)+"->"+str(reinforceCountry)+" ")
            if (fortifyEnd == "n" or fortifyEnd == "y"): break
        try:
            ownerList, troopList = reinforce(ownerList,troopList,reinforceCountry,baseCountry,reinforceTroops)
        except:
            continue
    createMap(continentList,borderList,ownerList,troopList)
    print("Ending fortify phase...")
    return ownerList, troopList


continentList = [[0,1,2,3,4,5,6,7,8], #north america
                [9,10,11,12], #south america
                [13,14,15,16,17,18,19], #europe
                [20,21,22,23,24,25], #africa
                [26,27,28,29,30,31,32,33,34,35,36,37], #asia
                [38,39,40,41]] #oceania
borderList = [[1,2,31],[0,2,3,4],[0,1,3,4,5],[1,2,4,6,13],[1,2,3,5,6,7],[2,4,7,8],[3,4,7],[4,5,6,8],[5,7,9], #0-8 north america
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

players = 6

ownerList = [None]*len(borderList)
troopList = [0]*len(borderList)

players = 6

cardPile = [[None,0],[None,0],[None,0],[33, 2],[35, 3],[18, 1],[20, 1],[23, 3],[27, 1],[28, 3],[9, 2],[19, 1],[16, 2],[3, 2],[37, 2],[32, 3],[36, 2],[2, 3],[21, 2],[31, 3],[17, 1],[38, 1],[30, 3],[12, 1],[41, 2],[22, 1],[41, 3],[25, 2],[18, 1],[4, 3],[8, 1],[10, 1],[1, 2],[11, 2],[24, 3],[5, 3],[6, 3],[15, 1],[14, 1],[34, 2],[26, 1],[13, 2],[7, 3],[39, 2],[0, 3]]

cardList = [[] for _ in range(players)]

ownerList, troopList, turn = setupMap(ownerList, troopList, players)



random.shuffle(cardPile)

cardPile, cardList = dealCard(cardPile,cardList)
cardPile, cardList = dealCard(cardPile,cardList)
cardPile, cardList = dealCard(cardPile,cardList)
cardPile, cardList = dealCard(cardPile,cardList)
cardPile, cardList = dealCard(cardPile,cardList)

tradeList = [0,1,2]

#bonusUnits, cardPile, cardList = tradeInCards(cardPile,cardList,tradeList)


calcUnits(ownerList, continentList)

ownerList, troopList = draftPhase(ownerList, troopList, continentList)
ownerList, troopList = attackPhase(ownerList, troopList, borderList)
ownerList, troopList = fortifyPhase(ownerList, troopList, borderList)    

print(elem == ownerList[0] for elem in ownerList)

while all(elem == ownerList[0] for elem in ownerList):
    if playerTurn not in ownerList:
        continue
    ownerList, troopList = draftPhase(ownerList, troopList, continentList, playerTurn)
    ownerList, troopList = attackPhase(ownerList, troopList, borderList, playerTurn)
    ownerList, troopList = fortifyPhase(ownerList, troopList, borderList, playerTurn)
    playerTurn = playerTurn+1
    if playerTurn > players:
        playerTurn = 0

print('Player ', playerTurn, 'has won!')