attackConfirmation = None

while not (attackConfirmation == "n" or attackConfirmation == "y"):
    attackConfirmation = input("Would you like to attack a country?")
while not playerTurn == ownerList[attackerCountry] and troopList[attackerCountry]>1:
    attackerCountry = input("Which country would you like to attack from?")
defenderCountry = input("Which country would you like to attack?")