import numpy as np
import random

from graphviz import Graph

class risk:
    def __init__(self, players=6):
        print('RISK')

        if players < 2 or players > 6:
            players = 6

        self.players = players

        self.continentBonus = [5,2,5,3,7,2]

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

        #np.savetxt('borderMap',borderMap,fmt ='%.0f')

        self.ownerList = [None]*len(self.borderList)
        self.unitList = [0]*len(self.borderList)

        self.cardPile = [[None,0],[None,0],[33, 2],[35, 3],[18, 1],[20, 1],[23, 3],[27, 1],[28, 3],[9, 2],[19, 1],[16, 2],[3, 2],[37, 2],[32, 3],[36, 2],[2, 3],[21, 2],[31, 3],[17, 1],[38, 1],[30, 3],[12, 1],[41, 2],[22, 1],[41, 3],[25, 2],[18, 1],[4, 3],[8, 1],[10, 1],[1, 2],[11, 2],[24, 3],[5, 3],[6, 3],[15, 1],[14, 1],[34, 2],[26, 1],[13, 2],[7, 3],[39, 2],[0, 3]]

        random.shuffle(self.cardPile)

        self.cardList = [[] for _ in range(players)]

        self.earnCard = False

        self.tradeList = []

        self.playerTurn = 0

        self.setupMap()

    def setupMap(self):
        starterUnits = [40,35,30,25,20]

        units = [starterUnits[self.players-2]]*(self.players)
        i = 0

        while None in self.ownerList:
            remainingCountries = [j for j, x in enumerate(self.ownerList) if x == None]
            selection = random.choice(remainingCountries)
            self.ownerList[selection] = self.playerTurn
            self.unitList[selection] = 1
            self.playerTurn = self.playerTurn+1
            if self.playerTurn > self.players-1:
                self.playerTurn = 0
            i = i+1

        for i in range(self.players):
            for j in range(units[i]):
                remainingCountries = [j for j, x in enumerate(self.ownerList) if x == i]
                selection = random.choice(remainingCountries)
                self.unitList[selection] = self.unitList[selection] + 1

        self.createMap()

    def dealCard(self):
        self.cardList[self.playerTurn].append(self.cardPile.pop(0))

    def tradeCards(self,tradeList):
        bonusUnits = 0
        bonusCountry = self.cardList[self.playerTurn][tradeList[0]][0]
        
        if self.ownerList[bonusCountry] == self.playerTurn:
            self.reinforce(targetCountry=bonusCountry, units=2)


        unitValues = []
        for i in tradeList:
            unitValues.append(self.cardList[self.playerTurn][i][1])
            self.createMap()

        tradeList.sort()

        unitValues2 = set(unitValues.copy())
        if unitValues2 == set([1,2,3]):
            bonusUnits = 10
        elif unitValues2 == set([3,3,3]): #set ignores duplicates
            bonusUnits = 8
        elif unitValues2 == set([2,2,2]):
            bonusUnits = 6
        elif unitValues2 == set([1,1,1]):
            bonusUnits = 4
        
        j = 0
        for i in tradeList:
            self.cardPile.append(self.cardList[self.playerTurn].pop(i-j))
            j = j+1

        return bonusUnits

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

        for i in range(len(self.unitList)):
            worldMap.node(str(i),label='< <b>      '+str(i)+'    </b> <br/>'+str(self.unitList[i])+'>')

        worldMap.save()
    
    def rollDice(self,attackerDiceNo=3,defenderDiceNo=2):
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
            tabString = '\t'
        else:
            tabString = '\t\t'
        if defenderDiceNo == 2:
            tabString2 = '\t'
        else:
            tabString2 = '\t\t'
        print(attackerDice,tabString,defenderDice,tabString2,attackerLoss,'\t',defenderLoss)
        return attackerLoss, defenderLoss, attackerDiceNo

    def calcUnits(self):
        countryBonus = self.ownerList.count(self.playerTurn)//3
        if countryBonus < 3:
            countryBonus = 3
        
        continentCountryOwner = [[] for i in range(len(self.continentList))]

        continentCountryOwner[0].append(1)

        for i in range(len(self.continentList)):
            for j in range(len(self.continentList[i])):
                if self.ownerList[self.continentList[i][j]] == self.playerTurn:
                    continentCountryOwner[i].append(1)
                else:
                    continentCountryOwner[i].append(0)

        continentOwner = []

        for i in range(len(self.continentBonus)):
            continentOwner.append(min(continentCountryOwner[i]))

        contBonus = []

        for x, y in zip(continentOwner,self.continentBonus):
            contBonus.append(x*y)

        contBonus = sum(contBonus)

        totalBonus = countryBonus+contBonus
        return totalBonus

    def pathCheck(self,targetCountry,seedCountry):
        borderCountries = []
        borderCountries.append(seedCountry)
        newBorders = []
        while True:
            for z in borderCountries:
                for i in self.borderList[z]:
                    newBorders.append(i)

            removeCountries = []
            for i in newBorders:
                if self.ownerList[i] != self.playerTurn:
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

    def reinforce(self,targetCountry,seedCountry=-1,units=0):
        if not seedCountry == -1:
            self.unitList[seedCountry] = self.unitList[seedCountry]-units
        self.unitList[targetCountry] = self.unitList[targetCountry]+units

    def battle(self,attackerCountry,defenderCountry,style='blitz'):
        if style == 'blitz':
            while self.unitList[attackerCountry]>1 and self.unitList[defenderCountry]>0:
                if self.unitList[attackerCountry]>3:
                    attackerDiceNo = 3
                else:
                    attackerDiceNo = self.unitList[attackerCountry]-1

                if self.unitList[defenderCountry]>1:
                    defenderDiceNo = 2
                else:
                    defenderDiceNo = 1

                attackerLoss, defenderLoss, attackerDiceNo = self.rollDice(attackerDiceNo,defenderDiceNo)

                self.unitList[attackerCountry] = self.unitList[attackerCountry]+attackerLoss
                self.unitList[defenderCountry] = self.unitList[defenderCountry]+defenderLoss
        elif style == 'classic':
            if self.unitList[attackerCountry]>3:
                attackerDiceNo = 3
            else:
                attackerDiceNo = self.unitList[attackerCountry]-1

            if self.unitList[defenderCountry]>1:
                defenderDiceNo = 2
            else:
                defenderDiceNo = 1

            attackerLoss, defenderLoss, attackerDiceNo = rollDice(attackerDiceNo,defenderDiceNo)

            self.unitList[attackerCountry] = self.unitList[attackerCountry]+attackerLoss
            self.unitList[defenderCountry] = self.unitList[defenderCountry]+defenderLoss
        if self.unitList[defenderCountry]<=0:
            print('Victory!')
            victory = True
            self.earnCard = True
            self.ownerList[defenderCountry]=self.ownerList[attackerCountry]
            self.reinforce(defenderCountry,attackerCountry,attackerDiceNo)
        else:
            print('Defeat...')
            victory = False
        return victory

    def draftPhase(self):
        print('Starting draft phase...')
        
        reinforcements = self.calcUnits()
        tradeEnd = 'n'
        tradeList = []
        while tradeEnd == 'n' and len(self.cardList[self.playerTurn]) >= 3:
            print('You have',reinforcements,'units.\n')
            
            print('Risk cards:',self.cardList[self.playerTurn],'\n')
            tradeOrder = input('Would you like to trade in cards? ')
            if not (tradeOrder == 'n' or tradeOrder == 'y'): continue
            if tradeOrder == 'n':
                while True:
                    tradeEnd = input('Are you sure? ')
                    if (tradeEnd == 'n' or tradeEnd == 'y'): break
                continue
            while True:
                tradeList.append(int(input('Which card would you like to trade in? (Country bonus first) ')))
                tradeList.append(int(input('Which card would you like to trade in? ')))
                tradeList.append(int(input('Which card would you like to trade in? ')))

                if len(tradeList)==len(set(tradeList)) and max(tradeList)<=len(self.cardList[self.playerTurn]): 
                    reinforcements = reinforcements + self.tradeCards(tradeList)
                    break
                tradeList = []
        
        while reinforcements > 0:
            print('You have '+str(reinforcements)+' units remaining.')
            while True:
                reinforceCountry = input('Which country would you like to reinforce? ')
                try:
                    reinforceCountry = int(reinforceCountry)
                except:
                    continue
                if self.playerTurn == self.ownerList[reinforceCountry]: break
            
            while True:
                reinforceUnit = input('How many units would you like to send? ')
                try:
                    reinforceUnit = int(reinforceUnit)
                except:
                    continue
                if reinforceUnit <= reinforcements and reinforceUnit > 0: break
            
            self.reinforce(targetCountry=reinforceCountry, units=reinforceUnit)
            reinforcements = reinforcements-reinforceUnit
            self.createMap()
        print('Ending draft phase...')

    def attackPhase(self):
        print('Starting attack phase...')
        attackOrder = None
        attackEnd = None
        battleWon = False

        while attackEnd != 'y':
            attackOrder = input('Would you like to attack a country? ')
            if not (attackOrder == 'n' or attackOrder == 'y'): continue
            if attackOrder == 'n':
                while True:
                    attackEnd = input('Are you sure? ')
                    if (attackEnd == 'n' or attackEnd == 'y'): break
                continue
            while True:
                attackerCountry = input('Which country would you like to attack from? ')
                try:
                    attackerCountry = int(attackerCountry)
                except:
                    continue
                if self.playerTurn == self.ownerList[attackerCountry] and self.unitList[attackerCountry]>1: break
            while True:
                defenderCountry = int(input('Which country would you like to attack? '))
                try:
                    defenderCountry = int(defenderCountry)
                except:
                    continue
                if defenderCountry in self.borderList[attackerCountry] and self.ownerList[defenderCountry]!=self.ownerList[attackerCountry]: break
            while True:
                attackConfirmation = input('Confirm order?: '+str(attackerCountry)+'->'+str(defenderCountry)+' ')
                if (attackConfirmation == 'n' or attackConfirmation == 'y'): break
            if attackConfirmation == 'y':
                victory = self.battle(attackerCountry,defenderCountry)
                self.createMap()
                if victory:
                    battleWon = True
                    while True:
                        reinforceUnits = input('How many additional units would you like to send? ')
                        try:
                            reinforceUnits = int(reinforceUnits)
                        except:
                            continue
                        if reinforceUnits >= 0 and reinforceUnits < self.unitList[attackerCountry]: break
                    self.reinforce(defenderCountry,attackerCountry,reinforceUnits)
                    self.createMap()
            continue
        print('Ending attack phase...')
        return self.ownerList, self.unitList

    def fortifyPhase(self):
        print('Starting fortify phase...')
        fortifyEnd = None
        while fortifyEnd != 'y':
            while True:
                fortifyOrder = input('Would you like to fortify? ')
                if (fortifyOrder == 'n' or fortifyOrder == 'y'): break
            if fortifyOrder == 'n':
                while True:
                    fortifyEnd = input('Are you sure? ')
                    if (fortifyEnd == 'n' or fortifyEnd == 'y'): break
                continue
            while True:
                baseCountry = input('Which country would you like to fortify from? ')
                try:
                    baseCountry = int(baseCountry)
                except:
                    continue
                if self.playerTurn == self.ownerList[baseCountry] and self.unitList[baseCountry]>1: break
            while True:
                reinforceCountry = int(input('Which country would you like to fortify? '))
                try:
                    reinforceCountry = int(reinforceCountry)
                except:
                    continue
                if self.ownerList[reinforceCountry] == self.playerTurn and self.pathCheck(reinforceCountry,baseCountry): break
            while True:
                reinforceunits = int(input('How many units would you like to move? '))
                try:
                    reinforceunits = int(reinforceunits)
                except:
                    continue
                if reinforceunits < self.unitList[baseCountry] and reinforceunits > 0: break
            while True:
                fortifyEnd = input('Confirm order?: '+str(baseCountry)+'->'+str(reinforceunits)+'->'+str(reinforceCountry)+' ')
                if (fortifyEnd == 'n' or fortifyEnd == 'y'): break
            try:
                self.reinforce(reinforceCountry,baseCountry,reinforceunits)
            except:
                continue
        if self.earnCard == True:
            print('Dealing card...')
            self.dealCard()
        self.earnCard = False
        self.createMap()
        print('Ending fortify phase...')

    def playGame(self):
        while not all(elem == self.ownerList[0] for elem in self.ownerList):
            print('\nStarting player', self.playerTurn, 'turn...')
            if self.playerTurn not in self.ownerList:
                continue
            self.draftPhase()
            self.attackPhase()
            self.fortifyPhase()
            self.playerTurn = self.playerTurn+1
            if self.playerTurn > self.players-1:
                self.playerTurn = 0

        print('Player', self.playerTurn, 'has won!')



game = risk(2)
game.dealCard()
game.dealCard()
game.dealCard()
game.playGame()