import math

'''********************GLOBAL VARIABLES********************'''
# holds all types of character data
gameData = {'pcs': [], 'ecs': []}


'''WHEN ADDING NEW COMMANDS FOR YOUR PARTS, INCLUDE THE SPECIFIC COMMAND
    THE USER SHOULD TYPE IN THE LIST BELOW. THIS LIST CHECKS FOR VALID COMMANDS
    SO IT'S IMPORTANT TO INCLUDE IT HERE SO THAT IT CAN BE CALLED. THEN
    PROCEED TO CREATE AN IF-CONDITION BLOCK IN MAIN FOR YOUR CODE'''

# list of available commands
cmdList = ["set level", "reset mana", "set mana max",
           "set mana", "cast", "restore", "set hp", "reset hp",
           "set hp max", "damage", "heal", "set init",
           "set cond note", "sleep", "wake", "set style", "fight",
           "new character", "set location", "commands", "quit"]


'''********************CLASSES********************'''

######################### NPC #########################

class pc:
    def manatotal(self, lvl, style):
        mt = 0
        mc = [5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560]
        lvl = int(lvl)

        if (lvl >= 4):
            if (lvl % 2 == 0):
                mt += mc[math.floor(lvl / 2) - 1] * 5
                mt += mc[math.floor(lvl / 2)] * 3

                for i in range(math.floor(lvl / 2) - 1):
                    mt += mc[i] * 6

            if (lvl % 2 == 1):
                mt += mc[math.floor(lvl / 2)] * 5

                for i in range(math.floor(lvl / 2)):
                    mt += mc[i] * 6
        else:
            mt = lvl * 10

        if (style == "Druid"):
            mt = int(mt * .75)
        elif (style == "Ranger" or style == "Paladin"):
            mt = (15 * lvl) - 50

            if (mt < 0):
                mt = 0
        else:
            mt = 0

        return mt

    def __init__(self, name, lvl, style, mana, hp, attr, init=0, inventory=[]):
        self.name = name
        self.lvl = int(lvl)
        self.style = style
        self.manaMax = self.manatotal(int(lvl), style)
        self.mana = int(mana)
        self.hpMax = int(hp)
        self.hp = int(hp)
        self.init = int(init)
        self.active = True
        self.attr = attr.split(' ')
        self.condNote = ""
        self.inventory = []

    def setLvl(self, lvl):
        self.lvl = lvl

    def setStyle(self, style):
        self.style = style

    def resetMana(self):
        self.mana = self.manaMax

    def setManaMax(self, mana):
        self.manaMax = int(mana)

    def setMana(self, mana):
        self.mana = int(mana)

    def cast(self, mana):
        self.mana -= int(mana)

    def restore(self, mana):
        self.mana += int(mana)

    def resetHp(self):
        self.hp = self.hpMax

    def setHp(self, hp):
        self.hp = hp

    def setHpMax(self, hp):
        self.hpMax = hp

    def dmg(self, dmg):
        self.hp -= int(dmg)

        if (self.hp <= 0):
            self.active = False

    def heal(self, heal):
        self.hp += int(heal)

    def setInit(self, init):
        self.init = int(init)

    def setCondNote(self, note):

        self.condNote = str(note)

    def sleep(self):
        self.active = False

    def wake(self):
        self.active = True

    def addItem(self, item):
        self.inventory.append(item)

    def getInfo(self):
        manastr = (str(self.mana) + "/" + str(self.manamax))
        hpstr = (str(self.hp) + "/" + str(self.hpmax))
        pcstr = [self.name, str(self.lvl), manastr, hpstr, str(self.init)]
        return pcstr


######################### Enemy NPC #########################


class ec:
    def __init__(self, name, lvl, style, mana, hp, init=0, location="", loot=[]):
        self.name = name
        self.lvl = int(lvl)
        self.style = style
        self.manamax = int(mana)
        self.mana = int(mana)
        self.hpmax = int(hp)
        self.hp = int(hp)
        self.init = int(init)
        self.condNote = ""
        self.active = True
        self.locationEncountered = location
        self.loot = loot

    def setLvl(self, lvl):
        self.lvl = lvl

    def setStyle(self, style):
        self.style = style

    def resetMana(self):
        self.mana = self.manaMax

    def setManaMax(self, mana):
        self.manaMax = int(mana)

    def setMana(self, mana):
        self.mana = int(mana)

    def cast(self, mana):
        self.mana -= int(mana)

    def restore(self, mana):
        self.mana += int(mana)

    def resetHp(self):
        self.hp = self.hpMax

    def setHp(self, hp):
        self.hp = hp

    def setHpMax(self, hp):
        self.hpMax = hp

    def dmg(self, dmg):
        self.hp -= int(dmg)

        if (self.hp <= 0):
            self.active = False

    def heal(self, heal):
        self.hp += int(heal)

    def setInit(self, init):
        self.init = int(init)

    def setCondNote(self, note):
        self.condNote = str(note)

    def sleep(self):
        self.active = False

    def wake(self):
        self.active = True

    def setLocationEncountered(self, location):
        self.locationEncountered = location

    def addLoot(self, loot):
        self.loot.append(loot)

    def getInfo(self):
        manastr = (str(self.mana) + "/" + str(self.manamax))
        hpstr = (str(self.hp) + "/" + str(self.hpmax))

        if (self.active == False):
            hpstr += " (unconscious)"

        ecstr = [self.name, str(self.style), manastr, hpstr, str(self.init)]

        return ecstr



    '''********************FUNCTIONS********************'''

# print list of commands
def printCommands():
    print("List of Valid Commands:")
    num = 0
    for cmd in cmdList:
        num += 1
        if num == len(cmdList):
            print(cmd)
        else:
            print(cmd, end=', ')
            if num % 5 == 0:
                print()
    return


# prompts for character name and checks all lists to see if it exists
def getPCName():
    charName = input("Which character? ")
    while True:
        check = 0
        for i in range(len(gameData['pcs'])):
            if gameData['pcs'][i].name.lower() == charName:
                check = 1
                break
        if check == 1:
            return charName

        for i in range(len(gameData['ecs'])):
            if gameData['ecs'][i].name.lower() == charName:
                check = 1
                break
        if check == 1:
            return charName
        else:
            print("Character name does not exist.")
            charName = input("Which character? ")
            continue


# prompts specifically for ec name and checks if exists
def getECName():
    charName = input("Which character? ")
    while True:
        check = 0
        for i in range(len(gameData['ecs'])):
            if gameData['ecs'][i].name.lower() == charName:
                check = 1
                break
        if check == 1:
            return charName
        else:
            print("Enemy character name does not exist.")
            charName = input("Which character? ")
            continue


# prompts for specific type of data specified by string
    # look at command implementations below for use
def getFuncCount(string):
    return int(input("How much " + string + "? "))


# prompts for character name and returns type of character
    # as well as the index in the list
def characterIndex(name):
    tempname = name.lower()
    for i in range(len(gameData['pcs'])):
        if gameData['pcs'][i].name.lower() == tempname:
            return 'pcs', i
    for i in range(len(gameData['ecs'])):
        if gameData['ecs'][i].name.lower() == tempname:
            return 'ecs', i
    return '', -1


# returns true if name already exists for either list, false if not
def isName():
    charName = input("Character name: ")
    while True:
        check = 0
        for i in range(len(gameData['pcs'])):
            if gameData['pcs'][i].name.lower() == charName:
                check = 1
                break
        if check == 0:
            for i in range(len(gameData['ecs'])):
                if gameData['ecs'][i].name.lower() == charName:
                    check = 1
                    break
        if check == 1:
            print("Character name already exists.")
            charName = input("Character name: ")
            continue
        else:
            return charName


# prompts user for the creation of a new character of either type
def newCharacter():
    print("Creating New Character")
    charType = str(input("pc or ec: "))
    if charType != "pc" and charType != "ec":
        while (charType != "pc" and charType != "ec"):
            print("Invalid. Enter 'pc' or 'ec'.")
            charType = str(input("pc or ec: "))

    # grab initialization parameters
    newname = isName()
    lvl = int(input("Character lvl: "))
    style = input("Character style: ")
    mana = int(input("Character mana: "))
    hp = int(input("Character hp: "))

    if charType == "pc":
        attr = str(input("Character attributes: "))
        new = pc(newname, lvl, style, mana, hp, attr)
        gameData['pcs'].append(new)
    elif charType == "ec":
        new = ec(newname, lvl, style, mana, hp)
        gameData['ecs'].append(new)
    return



'''****************MAIN****************'''


print("Initializing game...")

'''INITIALIZE CHARACTERS'''
# prompts for load of previous characters
while True:
    load = input("Would you like to load previous characters? (Y or N): ")

    if load == 'N' or load == 'n':
        numChar = int(input("Then, how many characters would you like to create? "))
        for i in range(numChar):
            newCharacter()
        break
    elif load == 'Y' or load == 'y':
        # LOAD PREVIOUS PLAYERS HERE BEFORE WHILE LOOP RIGHT BELOW THIS

        while True:   # prompts for additional created characters
            create = input("Would you like to create characters as well? (Y or N): ")

            if create == 'N' or create == 'n':
                break
            elif create == 'Y' or create == 'y':
                numChar = int(input("How many characters would you like to create? "))
                for i in range(numChar):
                    newCharacter()
                break
            else:
                print("Invalid answer. Enter Y for Yes or N for No.")

        break
    else:
        print("Invalid answer. Enter Y for Yes or N for No.")


print("\nCharacter Initialization Complete")
print("\n\nStarting Game\n\n")
printCommands()


# CURRENTLY LEFT TO BE IMPLEMENTED: fight, getInfo (i think michael),
                                    # plus whatever new commands yall add (check comment
                                    # at top for adding commands to list in beginning)

# MAIN GAME WHILE LOOP FOR COMMANDS
while True:
    command = input('\n> ')
    command = command.lower()

    if command not in cmdList:
        print("Invalid command. Enter 'commands' to view valid commands.")
        continue
    elif command == 'commands':
        printCommands()
        continue
    elif command == 'set level':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setLvl(int(input("What level? ")))
        continue
    elif command == 'reset mana':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].resetMana()
        continue
    elif command == 'set mana max':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setManaMax(getFuncCount("mana"))
        continue
    elif command == 'set mana':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setManaMax(getFuncCount("mana"))
        continue
    elif command == 'cast':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setManaMax(getFuncCount("mana"))
        continue
    elif command == 'restore':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setManaMax(getFuncCount("mana"))
        continue
    elif command == "set hp":
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setHp(getFuncCount("hp"))
        continue
    elif command == 'reset hp':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].resetHp()
        continue
    elif command == 'set hp max':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setManaMax(getFuncCount("hp"))
        continue
    elif command == 'damage':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setHp(getFuncCount("damage"))
        continue
    elif command == 'heal':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setHp(getFuncCount("health"))
        continue
    elif command == 'set init':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setInit(int(input("Set init to what? ")))
        continue
    elif command == 'set cond note':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setCondNote(str(input("What is the cond note? ")))
        continue
    elif command == 'sleep':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].sleep()
        continue
    elif command == 'wake':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].wake()
        continue
    elif command == 'set style':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].setStyle(str(input("What style? ")))
        continue
    elif command == "set location":
        name = getECName()
        charType, charIndex = characterIndex(name)
        gameData['ecs'][charIndex].setLocationEncountered(str(input("What location? ")))


    elif command == 'fight':
        continue
    elif command == 'get info':
        continue


    elif command == 'new character':
        newCharacter()
        continue
    elif command == 'quit':
        # save info
        print("End of Session")
        break
