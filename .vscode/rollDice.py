import random

attackerDiceNo = 3
defenderDiceNo = 2

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

print('a=',attackerLoss)
print('d=',defenderLoss)