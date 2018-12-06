import math, pickle, random
import numpy as np
import matplotlib.pyplot as plt

'''********************GLOBAL VARIABLES********************'''
# holds all types of character data
gameData = {'pcs': [], 'ecs': []}
attributes = ["Strength", "Constitution", "Dexterity", "Intelligence", "Wisdom", "Charisma"] 

'''WHEN ADDING NEW COMMANDS FOR YOUR PARTS, INCLUDE THE SPECIFIC COMMAND
    THE USER SHOULD TYPE IN THE LIST BELOW. THIS LIST CHECKS FOR VALID COMMANDS
    SO IT'S IMPORTANT TO INCLUDE IT HERE SO THAT IT CAN BE CALLED. THEN
    PROCEED TO CREATE AN IF-CONDITION BLOCK IN MAIN FOR YOUR CODE'''

# list of available commands
cmdList = ["set level", "reset mana", "set mana max",
           "set mana", "cast", "restore", "set hp", "reset hp",
           "set hp max", "damage", "heal", "set init",
           "set cond note", "sleep", "wake", "set style",
           "set location", "fight", "clear ecs", "clear pcs", "new character",
           "remove character", "commands", "save", "load all",
           "load pcs", "load ecs", "load character", "quit"]


'''********************CLASSES********************'''

######################### PC #########################

class pc:
    def manatotal(self, lvl, style):
        mt = 0
        mc = [5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120]
        lvl = int(lvl)
        if (lvl > 20):
            lvl = 20

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

        if (style == "druid"):
            mt = int(mt * .75)
        elif (style == "ranger" or style == "paladin"):
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
        if(mana == "max"):
            self.mana = manaMax
        else:
            self.mana = int(mana)
            if (self.mana > self.manaMax):
                self.manaMax = self.mana
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
        manastr = (str(self.mana) + "/" + str(self.manaMax))
        hpstr = (str(self.hp) + "/" + str(self.hpMax))
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

def rollDice(sides, n = 1):
    total = 0
    for i in range(n):
        total += random.randint(1, sides)
    return total

def printRosterInfo(num):
    global gameData
    ros = gameData['pcs'] + gameData['ecs']
    ros = sorted(ros, key=lambda c: c.init, reverse=True)
    namePC = (type(ros[num]).__name__ == "pc")
    name = ros[num].name
    if (len(gameData['pcs']) > len(gameData['ecs'])):
        moreEC = False
    else:
        moreEC = True
    if (moreEC):       
        for i in range(len(gameData['pcs'])):
            pcinfo = gameData['pcs'][i].getInfo()
            ecinfo = gameData['ecs'][i].getInfo()
            if (name == pcinfo[0] and namePC):
                print("---->" + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^5}".format(str(pcinfo[1])) + 
                "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^10}".format(" ") + "     " + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
                "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]))
            elif(name == ecinfo[0] and not namePC):
                 print("     " + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^5}".format(str(pcinfo[1])) + 
                "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^10}".format(" ") + "---->" + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
                "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]))
            else:
                print("     " + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^5}".format(str(pcinfo[1])) + 
                "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^10}".format(" ") + "     " + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
                "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]))
    print("")

def rollInitiative(prompt = False):
    if (prompt):
        init = "str"
        print("Enter initiative for each player:\n")
        for character in gameData['pcs']:
            while(not init.isdigit()):
                init = input(character.name+ ': ')
            character.setInit(init)
        for character in gameData['ecs']:
            while(not init.isdigit()):
                init = input(character.name+ ': ')
            character.setInit(init)
    else:
        while(True):
            print("Players:")
            for character in gameData['pcs']:
                character.setInit(rollDice(20))
                print(character.name, ':', character.init)
            for character in gameData['ecs']:
                character.setInit(rollDice(20))
                print(character.name, ':', character.init)
            reroll = input("Would you like to reroll initiative? (Y or N): ").lower()
            if(reroll == 'n' or reroll == 'no'):
                break

def combatGraph(stat_type, stats):
    nameList = []
    for character in gameData['pcs']:
        nameList.append(character.name)
    names = tuple(nameList)
    y_pos = np.arange(len(names))
    plt.bar(y_pos, stats, align='center', alpha=0.5)
    plt.xticks(y_pos, names)
    plt.ylabel(stat_type)
    plt.title(stat_type+" In Combat")
     
    plt.show()

# prompts for character name and checks all lists to see if it exists
def getPCName():
    global gameData
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
    global gameData
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
    global gameData
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
    global gameData
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
    global gameData
    global attributes
    print("Creating New Character")
    charType = str(input("pc or ec: "))
    if charType != "pc" and charType != "ec":
        while (charType != "pc" and charType != "ec"):
            print("Invalid. Enter 'pc' or 'ec'.")
            charType = str(input("pc or ec: "))

    # grab initialization parameters
    newname = isName()
    lvl = input("Character lvl: ")
    while(not lvl.isdigit()):
        lvl = input("Please enter a valid number for level: ")
    lvl = int(lvl)
    style = input("Character style: ")
    mana = input("Character mana: ")
    while(not mana.isdigit()):
        mana = input("Please enter a valid number for mana: ")
    mana = int(mana)
    hp = input("Character hp: ")
    while(not hp.isdigit()):
        hp = input("Please enter a valid number for hp: ")
    hp = int(hp)

    if charType == "pc":
        attr = ""
        print("Character attributes")
        for stat in attributes:
            stat = str(input(stat+" : "))
            attr += " " + stat
        attr = attr[1:]
        new = pc(newname, lvl, style, mana, hp, attr)
        gameData['pcs'].append(new)
    elif charType == "ec":
        new = ec(newname, lvl, style, mana, hp)
        gameData['ecs'].append(new)
    return


def save():
    global gameData
    filename = input("Enter the name of the save file\n")
    saveFile = open(filename, "wb")
    pickle.dump(gameData['pcs'], saveFile)
    pickle.dump(gameData['ecs'], saveFile)

    saveFile.close()

    print("Session data saved")

def load_all(load_type = ""):
    global gameData
    name = ""
    if (load_type != "pc" and load_type != "ec"):
        name = load_type.lower()
        load_type = ""
    
    filename = input("Enter the name of the save file\n")
    loadFile = open(filename, "rb")
    if (load_type == "" or load_type == "pc"):
        pc_load = pickle.load(loadFile)
        if (name != ""):
            for character in pc_load:
                if (name == character.name.lower()):
                    pc_load = [character]
        gameData['pcs'] += pc_load
    if (load_type == "" or load_type == "ec"):
        ec_load = pickle.load(loadFile)
        if (name != ""):
            for character in ec_load:
                if (name == character.name.lower()):
                    ec_load = [character]
        gameData['ecs'] += ec_load

    loadFile.close()

    print("Data loaded")


'''****************MAIN****************'''


print("Initializing game...")

'''INITIALIZE CHARACTERS'''
# prompts for load of previous characters
while True:
    load = input("Would you like to load previous characters? (Y or N): ")

    if load == 'N' or load == 'n':
        numChar = int(input("How many characters would you like to create? "))
        for i in range(numChar):
            newCharacter()
        break
    elif load == 'Y' or load == 'y':
        load_all()

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
combat_start = False

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
        gameData['ecs'][charIndex].setLocationEncountered(str(input("What Location? ")))
    elif (command == "characters"):
        print("Players:")
        for character in gameData['pcs']:
            print(character.name)
        print("\nEnemies:")
        for character in gameData['ecs']:
            print(character.name)
    elif (command == "load all" or command == "load"):
        load_all()
        continue
    elif (command == "load pcs"):
        load_all("pc")
        continue
    elif (command == "load ecs"):
        load_all("ec")
    elif (command == "load character"):
        name = getPCName()
        load_all(name)
        continue
    elif (command == "clear pcs"):
        gameData['pcs'] = []
        continue
    elif (command == "clear ecs"):
        gameData['ecs'] = []
        continue
    elif (command == "remove character"):
        name = getPCName()
        charType, charIndex = characterIndex(name)
        del gameData[charType][charIndex]
    elif (command == "save"):
        name = getPCName()
        charType, charIndex = characterIndex(name)
        del gameData[charType][charIndex]
    elif command == 'fight':
        combat_start = True



    elif command == 'new character':
        newCharacter()
        continue
    elif command == 'quit':
        to_save = input("Would you like to save? (Y or N): ").lower()
        if(to_save == 'y' or to_save == 'yes'):
            save()
        print("End of Session")
        break
    	



    
    

        

   
        
    ################################# COMBAT START #################################
    if (combat_start):
        rollInit = input("Would you like to roll for initiative? (Y or N): ").lower()
        if (rollInit == 'y' or rollInit == 'yes'):
            rollInitiative()
        turn = 1
        actions = -1
        dmgstats = []
        manastats = []
        healstats = []
        hurtstats = []
        for i in range(len(gameData['pcs'])):
                dmgstats.append(0)
                manastats.append(0)
                healstats.append(0)
                hurtstats.append(0)

      
    while(combat_start):
        
        actions +=1
        print("\n" * 5)
        if(actions < 5):
                print('Enter a command or type "help" for a list of commands')
			
        if(gameData['pcs'][0].init != 0):
            num = (turn) % (len(gameData['pcs']) + len(gameData['ecs']))
            roundNum = int((turn) / (len(gameData['pcs']) + len(gameData['ecs'])) + 1)
            print('{:^15}'.format("ROUND: " + str(roundNum)) + '{:^15}'.format("TURNS: " + str(turn)) + '{:^15}'.format("ACTIONS: " + str(actions)))
            gameData['pcs'] = sorted(gameData['pcs'], key=lambda pc: pc.init, reverse=True)
            gameData['ecs'] = sorted(gameData['ecs'], key=lambda ec: ec.init, reverse=True)
            
        else:
            gameData['pcs'] = sorted(gameData['pcs'], key=lambda pc: pc.name)
            rollInit = input("Initiative is needed to continue, would you it to be rolled for you? (Y or N): ").lower()
            if (rollInit == 'y' or rollInit == 'yes'):
                rollInitiative()
            else:
                rollInitiative(True)
            
        print("     "+ "{:^5}".format("#") + "{:^15}".format("Name") + "{:^5}".format("Level") + 
        "{:^15}".format("Mana") + "{:^15}".format("Health")  + "{:^10}".format("") + "     "+ "{:^5}".format("#") + "{:^15}".format("Name") + "{:^15}".format("Race/Type") + 
        "{:^15}".format("Mana") + "{:^15}".format("Health"))
        num = (turn-1) % (len(gameData['pcs']) + len(gameData['ecs']))
        printRosterInfo(num)

        ########### SPLIT COMMAND INTO STMT ###########
        
        command = input('\n> ')
        command = command.lower()
        command = command.split(' ')
        commandLen = len(command)
		
        ########### MENU OPTIONS BASED ON NUMBER OF ARGUMENTS ###########

        if (commandLen == 1):
            if (command[0] == "q" or command[0] == "quit" or command[0] == "end"):
                combat_start = False
                
            elif (command[0] == "initiative"):
                 rollInit(gameData['pcs'])
                 
            elif (command[0] == "+"):
                turn+=1
                actions -=1
                print("\n" * 20)
                
            elif (command[0] == "-" or command[0] == '_'):
                turn-=1
                actions -=1
                print("\n" * 5)
                
            elif (command[0] == "--" or command[0] == '__'):
                actions -=1

            elif (command[0] == "help"):
                actions -= 1
                print ( "Command List:\n",
                        "quit\n",
                        'next turn or "+"\n',
                        'prev turn or "-"\n',
                        "roll [n-sided dice] [n-times]\n",
                        "reset-hp [to-player]\n",
                        "reset-mana [to-player]\n",
                        "hurt [to-player] [by-player] [damage-amount]\n",
                        "heal [to-player] [by-player] [heal-amount]\n",
                        "cast [to-player] [by-player] [mana-lost]\n",
                        "restore [to-player] [by-player] [mana-gained]\n",)
			
			################## DOT SEPERATED ENTRY ##################
				
            elif(len(command[0].split('.')) > 1):
                dotStmt = command[0].split(".")
                dotStmtLen = len(dotStmt)
    
                if (dotStmtLen == 2):
                    if (dotStmt[0] == "4"):
                            gameData['pcs'][int(dotStmt[1])].disable()
                    if (dotStmt[0] == "3"):
                            gameData['pcs'][int(dotStmt[1])].resetMana
                    if (dotStmt[0] == "2"):
                            gameData['pcs'][int(dotStmt[1])].resetHp

                                
                ########### ACTION.CHAR.MAGNITUDE ###########
                
                elif (dotStmtLen == 3):

                        if (dotStmt[1][0] == "0"):
                                toPC = False
                                dotStmt[1] = str(int(dotStmt[1])-1)
                        else:
                                dotStmt[1] = str(int(dotStmt[1])-1)
                                toPC = True
 

                        ### DAMAGE ##
                            
                        if (dotStmt[0] == "1"):
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].dmg(int(dotStmt[2]))
                                        hurtstats[int(dotStmt[1])] += int(dotStmt[2])
                                else:
                                        gameData['ecs'][int(dotStmt[1])].dmg(dotStmt[2])
                        ### HEAL ###
                            
                        if (dotStmt[0] == "2"):
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].heal(int(dotStmt[2]))
                                        healstats[int(dotStmt[1])] += int(dotStmt[2])
                                else:
                                        gameData['ecs'][int(dotStmt[1])].heal(dotStmt[2])
                        ### MANA ###
                            
                        if (dotStmt[0] == "3"):
                                if (dotStmt[2][0] == '('):
                                        dotStmt[2] = 5*math.pow(2, int(dotStmt[2][1]))
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].cast(int(dotStmt[2]))
                                        manastats[int(dotStmt[1])] += int(dotStmt[2])
                                else:
                                        gameData['ecs'][int(dotStmt[1])].cast(dotStmt[2])
                            
                        ### RESTORE MANA ##
                            
                        if (dotStmt[0] == "4"):
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].restore(int(dotStmt[2]))
                                else:
                                        gameData['ecs'][int(dotStmt[1])].restore(int(dotStmt[2]))
                            
                        ### INITIATIVE ###
                            
                        if (dotStmt[0] == "7"):
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].setInit(dotStmt[2])
                                else:
                                        gameData['ecs'][int(dotStmt[1])].setInit(dotStmt[2])
                            
                        ### CONDITION ###
                            
                        if (dotStmt[0] == "8"):
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].setCondNote(dotStmt[2])
                                else:
                                        gameData['ecs'][int(dotStmt[1])].setCondNote(dotStmt[2])

                ########### ACTION.TO_CHAR.BY_CHAR.MAGNITUDE ###########
                            
                elif (dotStmtLen == 4):
                        if (dotStmt[1][0] == "0"):
                                toPC = False
                                dotStmt[1] = str(int(dotStmt[1])-1)
                        else:
                                dotStmt[1] = str(int(dotStmt[1])-1)
                                toPC = True

                        if (dotStmt[2][0] == "0"):
                                byPC = False
                                dotStmt[2] = str(int(dotStmt[2])-1)
                        else:
                                dotStmt[2] = str(int(dotStmt[2])-1)
                                byPC = True


                        ### DAMAGE ##
                            
                        if (dotStmt[0] == "1"):
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].dmg(int(dotStmt[3]))
                                        hurtstats[int(dotStmt[1])] += int(dotStmt[3])
                                        if(byPC):
                                                dmgstats[int(dotStmt[2])] += int(dotStmt[3])
                                else:
                                        gameData['ecs'][int(dotStmt[1])].dmg(int(dotStmt[3]))
                                        if(byPC):
                                                dmgstats[int(dotStmt[2])] += int(dotStmt[3])
                                                print(int(dotStmt[2]), int(dotStmt[3]))

                        ### HEAL ###
                            
                        elif (dotStmt[0] == "2"):
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].heal(int(dotStmt[3]))
                                        healstats[int(dotStmt[2])] += int(dotStmt[3])
                                else:
                                        gameData['ecs'][int(dotStmt[1])].heal(dotStmt[3])
                                        healstats[int(dotStmt[2])] += int(dotStmt[3])

                        ### MANA ###
                            
                        elif (dotStmt[0] == "3"):
                                if (dotStmt[3][0] == '('):
                                        dotStmt[3] = 5*math.pow(2, int(dotStmt[3][1]))
                                if(toPC):
                                        gameData['pcs'][int(dotStmt[1])].cast(int(dotStmt[3]))
                                        manastats[int(dotStmt[1])] += int(dotStmt[3])
                                        if(byPC):
                                                gameData['pcs'][int(dotStmt[2])].cast(int(dotStmt[3]))
                                                manastats[int(dotStmt[2])] += int(dotStmt[3])
                                        else:
                                                gameData['ecs'][int(dotStmt[2])].cast(int(dotStmt[3]))
                                else:
                                        gameData['ecs'][int(dotStmt[1])].cast(int(dotStmt[3]))
                                        if(byPC):
                                                gameData['pcs'][int(dotStmt[2])].cast(int(dotStmt[3]))
                                                manastats[int(dotStmt[2])] += int(dotStmt[3])
                                        else:
                                                gameData['ecs'][int(dotStmt[2])].cast(int(dotStmt[3]))
                            
        ################## END DOT SEPERATED ENTRY ##################

            elif (commandLen == 2):
                if (command[0] == "reset-mana"):
                    charType, charIndex = characterIndex(command[1])
                    gameData[charType][charIndex].resetMana()
                elif (command[0] == "reset-hp"):
                    charType, charIndex = characterIndex(command[1])
                    gameData[charType][charIndex].resetHp()
                elif (command[0] == "roll"):
                    print("1 d", command[1], " : ", rollDice(int(command[1])), sep ='')
                elif (command[0] == "reset-hp"):
                    gameData[charType][charIndex].resetHp()
                    

            ################## HURT/HEAL/CAST/RESTORE IMPLEMENTATION ###################

            elif (commandLen >= 3):

                    if (command[0] == "roll"):
                        print(command[2], " d", command[1], " : ", rollDice(int(command[1]), int(command[2])), sep ='')
                              
                    elif (command[0] == "hurt"):
                            charType1, charIndex1 = characterIndex(command[1])

                            if isinstance(command[2], int):
                                    hurtstats[charIndex1] += command[2]
                                    gameData[charType1][charIndex1].dmg(command[2])

                            elif isinstance(command[2], str):
                                    charType2, charIndex2 = characterIndex(command[2])
                                    dmgstats[charIndex2] += command[3]
                                    hurtstats[charIndex1] += command[3]
                                    gameData[charType1][charIndex1].dmg(command[3])

                    elif (command[0] == "heal"):

                            charType1, charIndex1 = characterIndex(command[1])

                            if isinstance(command[2], int):
                                    healstats[charIndex1] += command[2]
                                    gameData[charType1][charIndex1].heal(command[2])

                            elif isinstance(command[2], str):
                                    charType2, charIndex2 = characterIndex(command[2])
                                    healstats[charIndex1] += command[3]
                                    gameData[charType1][charIndex1].heal(command[3])

                    elif (command[0] == "cast"):

                            charType1, charIndex1 = characterIndex(command[1])

                            if isinstance(command[2], int):
                                    continue

                            elif isinstance(command[2],str):
                                    charType2, charIndex2 = characterIndex(command[2])
                                    manastats[charIndex2] -= command[3]
                                    gameData[charType2][charIndex2].cast(command[3])

                    elif (command[0] == "restore"):

                            charType1, charIndex1 = characterIndex(command[1])

                            if isinstance(command[2], int):
                                    manastats[charIndex1] += command[2]
                                    gameDate[charType1][charIndex1].restore(command[2])

                            elif isinstance(command[2],str):
                                    charType2, charIndex2 = characterIndex(command[2])
                                    healstats[charIndex2] += command[3]
                                    manastats[charIndex1] += command[3]                                            
                                    gameDate[charType1][charIndex1].restore(command[3])
                                    gameDate[charType2][charIndex2].heal(command[3])

    
        if(not combat_start):
            print("Combat Ended")
            show_graph = input("Do you wish to view player preformance graphs? (Y or N): ").lower()
            if (show_graph == 'y' or show_graph == 'yes'):
                while(True):
                    print('Type the name of the graph you want or "quit" to exit')
                    show_graph = input("Available Graphs: damage dealt, healing, mana used, damage taken: ")
                    if(show_graph == "damage dealt"):
                        combatGraph("Damage Dealt", dmgstats)
                    elif(show_graph == "healing"):
                        combatGraph("Healing Done", healstats)
                    elif(show_graph == "mana used"):
                        combatGraph("Mana Used", manastats)
                    elif(show_graph == "damage taken"):
                        combatGraph("Damage Taken", hurtstats)
                    elif(show_graph == "quit"):
                        break
                    else:
                        print(show_graph, "is an unrecognized command")
           
                                                      
