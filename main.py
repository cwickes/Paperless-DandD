import math, pickle, random
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

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
           "set location", "fight", "clear ecs", "clear pcs",
           "new character", "remove character", "commands",
           "save", "load all", "load pcs", "load ecs",
           "search", "random ec", "load character",
           "character info", "characters", "help", "quit"]


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
        self.hpMax = int(hp)

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

        ecstr = [self.name, str(self.style).capitalize(), manastr, hpstr, str(self.init)]

        return ecstr



import sqlite3

class DND_DB:
	def __init__(self, name = "dnd35.db"):
		db = sqlite3.connect(name)
		self.cursor = db.cursor()
		
	def monsters(self, monName):
		monName = monName.title()
		print()
		if (monName == "Aberration" or monName == "Animal" or monName == "Celestial" or
		monName == "Construct" or monName == "Dragon" or monName == "Elemental" or
		monName == "Fey" or monName == "Fiend" or monName == "Giant" or monName == "Humanoid" or
		monName == "Magical Beast" or monName == "Monstrous Humanoid" or monName == "Ooze" or
		monName == "Outsider" or monName == "Plant" or monName == "Undead" or monName == "Vermin"):
			print(monName + " is a monster type, do you want monsters of that type listed? (y/n)")
			yes = input()
			if (yes.lower() == "y" or yes.lower() == "yes"):
					self.monsterByType(monName)
		else:
			attributes = ["id", "family", "name", "altname", "size", "type", "descriptor", "hit_dice", 
			"initiative", "speed", "armor_class", "base_attack", "grapple", "attack", "full_attack",
			"space", "reach", "special_attacks", "special_qualities", "saves", "abilities", "skills",
			"bonus_feats", "feats", "epic_feats", "environment", "organization", "challenge_rating",
			"treasure", "alignment", "advancement", "level_adjustment", "special_abilities",
			"stat_block", "full_text", "reference"]
			format = "SELECT * FROM monster WHERE (name='" + monName + "' OR altname='" + monName + "')"
			self.cursor.execute(format)
			if (len(self.cursor.fetchall()) == 0):
				print("You did not enter a valid monster name.")
			else:
				self.cursor.execute(format)
				temp = self.cursor.fetchall()[0]
				for x in range (1, len(temp) - 2):
					print(attributes[x] + ": " + temp[x])
				
	def monsterByType(self, monName):
		monName = monName.capitalize()
		print()
		format = "SELECT name FROM monster WHERE type='" + monName + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid monster name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()
			for x in range (0, len(temp)):
				print(temp[x])
				
	def spells(self, spellName):
		print()
		attributes = ["id", "name", "altname", "school", "subschool", "descriptor", "spellcraft_dc",
		"level", "components", "casting_time", "range", "target", "area", "effect", "duration",
		"saving_throw", "spell_resistance", "short_description", "to_develop", "arcane_material_components",
		"focus", "description", "xp_cost", "arcane_focus", "wizard_focus", "verbal_components",
		"sorcerer_focus", "bard_focus", "cleric_focus", "druid_focus", "full_attack", "reference"]
		format = "SELECT * FROM spell WHERE (name='" + spellName + "' OR altname='" + spellName + "')"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid spell name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()[0]
			for x in range (1, len(temp) - 2):
				print(attributes[x] + ": " + temp[x])
	
	
	def spells1wizard(self):
		level = input()
		format = "SELECT name FROM spell WHERE level=1"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid spell name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()[0]
			for x in range (1, len(temp) - 2):
				print(temp[x])
			
	def items(self, itemName):
		itemName = itemName.capitalize()
		print()
		attributes = ["id", "name", "category", "subcategory", "special_ability", "aura", "caster_level",
		"price", "manifester_level", "prereq", "cost", "weight", "full_text", "reference"]
		format = "SELECT * FROM item WHERE name='" + itemName + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid item name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()[0]
			for x in range (1, len(temp) - 2):
				print(attributes[x] + ": " + temp[x])
				
	def equipment(self, eName):
		eName = eName.capitalize()
		print()
		attributes = ["id", "name", "family", "category", "subcategory", "cost", "dmg_s",
		"armor_shield_bonus", "maximum_dex_bonus", "dmg_m",
		"weight", "critical", "armor_check_penalty", "arcane_spell_failure_chance", "range_increment",
		"speed_30", "type", "speed_20", "full_text", "reference"]
		format = "SELECT * FROM equipment WHERE name='" + eName + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid item name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()[0]
			for x in range (1, len(temp) - 2):
				print(attributes[x] + ": " + temp[x])
				
	def monsterAlignment(self, monAlign):
		print()
		format = "SELECT name FROM monster WHERE alignment='" + monAlign + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) != 0):
			self.cursor.execute(format)
			temp = self.cursor.fetchall()
			for x in range (0, len(temp)):
				print(temp[x][0] + monAlign)			
		format = "SELECT name FROM monster WHERE alignment='Usually " + monAlign + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) != 0):
			self.cursor.execute(format)
			temp = self.cursor.fetchall()
			for x in range (0, len(temp)):
				print(temp[x][0] + " is Usually " + monAlign)				
		format = "SELECT name FROM monster WHERE alignment='Always " + monAlign + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) != 0):
			self.cursor.execute(format)
			temp = self.cursor.fetchall()
			for x in range (0, len(temp)):
				print(temp[x][0] + " is Always " + monAlign)		
		format = "SELECT name FROM monster WHERE alignment='Often " + monAlign + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid alignment")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()
			for x in range (0, len(temp)):
				print(temp[x][0] + " is Often" + monAlign)
			
	def magicSchool(self, school):
		school = school.capitalize()
		print()
		format = "SELECT name, level FROM spell WHERE school='" + school + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid school of magic")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()
			for x in range (0, len(temp)):
				print(temp[x][0] + ", available to: " + temp[x][1])
				
	
	def feats(self, feat):
		print()
		attributes = ["id", "name", "type", "multiple", "stack", "choice", "prerequisite",
		"benefit", "normal", "special", "full_text", "reference"]
		format = "SELECT * FROM feat WHERE name='" + feat + "'"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid feat name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()[0]
			for x in range (1, len(temp) - 2):
				print(attributes[x] + ": " + temp[x])


'''********************FUNCTIONS********************'''
def ecCreate(autoGen = True):
    # DB connect
    dbFile = 'dnd35.db'
    con = sqlite3.connect(dbFile)
    cur = con.cursor()

    # Retrieve number of monsters in table
    cur.execute("SELECT COUNT(*) FROM monster;")
    monsterCount = cur.fetchone()[0]

    # Random monster selection from local SQLite DB
    monster = str(random.randint(1, monsterCount))
    cur.execute("SELECT name, challenge_rating, type, hit_dice FROM monster WHERE id = " + monster + ";")
    monsterData = cur.fetchone()

    # initialize monster data
    name = monsterData[0]
    lvl = monsterData[1]
    style = monsterData[2]

    if autoGen == True:
        hp = monsterData[3].split()
        hp = hp[1][1:]
        temp = ''
        for d in hp:
            if (d.isdigit()):
                temp+=d
        hp = temp
        hp = int(hp)
    else:
            hp = int(input('Set health for ' + name + ' with CR of ' + lvl + ': '))

    # prompt DM to determine mana for monster
    mana = int(input('Set mana for ' + name + ' with CR of ' + lvl + ': '))

    return ec(name, lvl, style, hp, mana)



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
        biglen = len(gameData['pcs'])
        smalllen = len(gameData['ecs'])
    else:
        moreEC = True
        biglen = len(gameData['ecs'])
        smalllen = len(gameData['pcs'])     
    for i in range(smalllen):
        pcinfo = gameData['pcs'][i].getInfo()
        ecinfo = gameData['ecs'][i].getInfo()
        condString = "{:^15}"
        if (len(gameData['pcs'][i].condNote) != 0):
            condString = '{:^' + str(15-len(gameData['pcs'][i].condNote) + 5) + '}'
        if (name == pcinfo[0] and namePC):
            print("---->" + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^7}".format(str(pcinfo[1])) + 
            "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^2}".format(gameData['pcs'][i].condNote) + condString.format("") + "     " + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
            "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]) + "{:^2}".format(gameData['ecs'][i].condNote))
        elif(name == ecinfo[0] and not namePC):
                print("     " + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^7}".format(str(pcinfo[1])) + 
            "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^2}".format(gameData['pcs'][i].condNote) + condString.format("") + "---->" + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
            "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]) + "{:^2}".format(gameData['ecs'][i].condNote))
        else:
            print("     " + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^7}".format(str(pcinfo[1])) + 
            "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^2}".format(gameData['pcs'][i].condNote) + condString.format("") + "     " + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
            "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]) + "{:^2}".format(gameData['ecs'][i].condNote))
    for i in range(smalllen, biglen):
        condString = "{:^15}"
        if (moreEC):
            ecinfo = gameData['ecs'][i].getInfo()
            if(name == ecinfo[0] and not namePC):
                print("{:^64}".format("") + condString.format("") + "---->" + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
                "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]) + "{:^2}".format(gameData['ecs'][i].condNote))
            else:
                print("{:^64}".format("") + condString.format("") + "     " + "{:^5}".format(str(i+1)) + "{:^15}".format(ecinfo[0]) + "{:^15}".format(str(ecinfo[1])) + 
                "{:^15}".format(ecinfo[2]) + "{:^15}".format(ecinfo[3]) + "{:^2}".format(gameData['ecs'][i].condNote))
        else:
            pcinfo = gameData['pcs'][i].getInfo()
            if (name == pcinfo[0] and namePC):
                print("---->" + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^5}".format(str(pcinfo[1])) + 
                "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^2}".format(gameData['pcs'][i].condNote))
            else:
                print("     " + "{:^5}".format(str(i+1)) + "{:^15}".format(pcinfo[0]) + "{:^5}".format(str(pcinfo[1])) + 
                "{:^15}".format(pcinfo[2]) + "{:^15}".format(pcinfo[3]) + "{:^2}".format(gameData['pcs'][i].condNote))
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
            print("\nEnemies:")
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
    plt.subplot(211)
    plt.bar(y_pos, stats, align='center', alpha=0.5)
    plt.xticks(y_pos, names)
    plt.ylabel(stat_type)
    plt.title(stat_type+" In Combat")

    plt.subplot(212)
    plt.pie(stats, labels=names)

    plt.tight_layout()
    plt.show()

# prompts for character name and checks all lists to see if it exists
def getPCName():
    global gameData
    charName = input("Which character? ").lower()
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
    try:
        saveFile = open(filename, "wb")
        pickle.dump(gameData['pcs'], saveFile)
        pickle.dump(gameData['ecs'], saveFile)

        saveFile.close()

        print("Session data saved")
    except:
        print("Unable to save at", filename)

def load_all(load_type = ""):
    global gameData
    name = ""
    if (load_type != "pc" and load_type != "ec"):
        name = load_type.lower()
        load_type = ""
    
    filename = input("Enter the name of the save file\n")
    try:
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
    except:
        print("Unable to load", filename)


'''****************MAIN****************'''


print("Initializing game...")
db = DND_DB()
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

# CURRENTLY LEFT TO BE IMPLEMENTED: 

# MAIN GAME WHILE LOOP FOR COMMANDS
while True:
    command = input('\n> ')
    command = command.lower()

    if command not in cmdList:
        print('Invalid command. Enter "help" to view valid commands.')
        continue
    elif (command == 'commands' or command == "help"):
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
        gameData[charType][charIndex].setMana(getFuncCount("mana"))
        continue
    elif command == 'cast':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].cast(getFuncCount("mana"))
        continue
    elif command == 'restore':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].restore(getFuncCount("mana"))
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
        gameData[charType][charIndex].setHpMax(getFuncCount("hp"))
        continue
    elif command == 'damage':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].dmg(getFuncCount("damage"))
        continue
    elif command == 'heal':
        name = getPCName()
        charType, charIndex = characterIndex(name)
        gameData[charType][charIndex].heal(getFuncCount("health"))
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
    elif (command == "character info"):
        name = getPCName()
        charType, charIndex = characterIndex(name)
        char = gameData[charType][charIndex]
        charinfo = char.getInfo()
        print("Name:", char.name)
        print("Level:", char.lvl)
        print("Class:", char.style)
        print("Health:", charinfo[3])
        print("Mana:", charinfo[2])
        print("Attributes:")
        if (charType == 'pcs'):
            for i in range(6):
                print(attributes[i], ": ", char.attr[i], sep ='')
            print("Items in bag:")
            for item in char.inventory:
                print(item.capitalize(), sep=', ')
        else:
            print("Location Encountered:", char.LocationEncountered)
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
    elif command == 'search':
        while(True):
            search = input("What are you trying to search? (monsters, items, feats, spells, equipment) : ")
            if(search in 'monsters'):
                search = input("Which monster would you like to lookup? ")
                db.monsters(search)
                break
            elif(search in 'spells'):
                search = input("Which spell would you like to lookup? ")
                db.spells(search)
                break
            elif(search in 'items'):
                search = input("Which item would you like to lookup? ")
                db.items(search)
                break
            elif(search in 'feats'):
                search = input("Which feat would you like to lookup? ")
                db.feats(search)
                break
            elif(search in 'equipment'):
                search = input("Which equipment would you like to lookup? ")
                db.equipment(search)
                break
            else:
                print(search, "not recognized")
    elif command == 'random ec':
        gameData['ecs'].append(ecCreate())
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
        print("Starting Combat")
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
            
        print("     "+ "{:^5}".format("#") + "{:^15}".format("Name") + "{:^7}".format("Level") + 
        "{:^15}".format("Mana") + "{:^15}".format("Health")  + "{:^17}".format("") + "     "+ "{:^5}".format("#") + "{:^15}".format("Name") + "{:^15}".format("Race/Type") + 
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
                print ( "Combat Command List:\n",
                        "quit\n",
                        'next turn or "+"\n',
                        'prev turn or "-"\n',
                        "roll [n-sided dice] [n-times]\n",
                        "reset hp [to-player]\n",
                        "reset mana [to-player]\n",
                        "hurt [to-player] [by-player] [damage-amount]\n",
                        "heal [to-player] [by-player] [heal-amount]\n",
                        "cast [to-player] [by-player] [mana-lost]\n",
                        "restore [to-player] [by-player] [mana-gained]\n",)
            elif (command[0] == 'cast'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].cast(getFuncCount("mana"))
                continue
            elif (command[0] == 'restore'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].restore(getFuncCount("mana"))
                continue
            elif (command[0] == 'damage' or command[0] == 'hurt'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].dmg(getFuncCount("damage"))
                continue
            elif (command[0] == 'heal'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].heal(getFuncCount("health"))
                continue
            elif (command[0] == 'sleep'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].sleep()
                continue
            elif (command[0] == 'wake'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].wake()
                continue
            elif (command[0] == 'search'):
                while(True):
                    search = input("What are you trying to search? (monsters, items, feats, spells, equipment) : ")
                    if(search in 'monsters'):
                        search = input("Which monster would you like to lookup? ")
                        db.monsters(search)
                        break
                    elif(search in 'spells'):
                        search = input("Which spell would you like to lookup? ")
                        db.spells(search)
                        break
                    elif(search in 'items'):
                        search = input("Which item would you like to lookup? ")
                        db.items(search)
                        break
                    elif(search in 'feats'):
                        search = input("Which feat would you like to lookup? ")
                        db.feats(search)
                        break
                    elif(search in 'equipment'):
                        search = input("Which equipment would you like to lookup? ")
                        db.equipment(search)
                        break
                    else:
                        print(search, "not recognized")
            
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
            else:
                print("Unrecognized command")
                            
        ################## END DOT SEPERATED ENTRY ##################

        elif (commandLen == 2):
            if (command[1] == 'hp'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].resetHp()
            elif (command[1] == 'mana'):
                name = getPCName()
                charType, charIndex = characterIndex(name)
                gameData[charType][charIndex].resetMana()
                continue
            
            elif (command[0] == "roll"):
                print("1 d", command[1], " : ", rollDice(int(command[1])), sep ='')
            elif (command[0] == "reset-hp"):
                gameData[charType][charIndex].resetHp()
            else:
                print("Unrecognized command")
                

        ################## HURT/HEAL/CAST/RESTORE IMPLEMENTATION ###################

        elif (commandLen >= 3):
                command[-1] = int(command[-1])

                if (command[0] == "roll"):
                    print(command[2], " d", command[1], " : ", rollDice(int(command[1]), int(command[2])), sep ='')
                          
                elif (command[0] == "hurt" or command[0] == "damage"):
                        charType1, charIndex1 = characterIndex(command[1])

                        if isinstance(command[2], int):
                                hurtstats[charIndex1] += int(command[2])
                                gameData[charType1][charIndex1].dmg(command[2])

                        elif isinstance(command[2], str):
                                charType2, charIndex2 = characterIndex(command[2])
                                dmgstats[charIndex2] += int(command[3])
                                if(charType1 == 'pcs'):
                                    hurtstats[charIndex1] += int(command[3])
                                gameData[charType1][charIndex1].dmg(command[3])

                elif (command[0] == "heal"):

                        charType1, charIndex1 = characterIndex(command[1])

                        if isinstance(command[2], int):
                                healstats[charIndex1] += int(command[2])
                                gameData[charType1][charIndex1].heal(command[2])

                        elif isinstance(command[2], str):
                                charType2, charIndex2 = characterIndex(command[2])
                                healstats[charIndex1] += int(command[3])
                                gameData[charType1][charIndex1].heal(command[3])

                elif (command[0] == "cast"):

                        charType1, charIndex1 = characterIndex(command[1])

                        if isinstance(command[2], int):
                                gameData[charType1][charIndex1].cast(command[2])
                                manastats[charIndex1] += int(command[2])

                        elif isinstance(command[2],str):
                                charType2, charIndex2 = characterIndex(command[2])
                                manastats[charIndex2] += int(command[3])
                                gameData[charType2][charIndex2].cast(command[3])

                elif (command[0] == "restore"):

                        charType1, charIndex1 = characterIndex(command[1])

                        if isinstance(command[2], int):
                                gameData[charType1][charIndex1].restore(command[2])

                        elif isinstance(command[2],str):
                                charType2, charIndex2 = characterIndex(command[2])
                                healstats[charIndex2] += int(command[3])
                                gameData[charType1][charIndex1].restore(command[3])
                                gameData[charType2][charIndex2].heal(command[3])
                elif (command[1] == "mana"):
                    charType, charIndex = characterIndex(command[1])
                    gameData[charType][charIndex].resetMana()
                elif (command[1] == "hp"):
                    charType, charIndex = characterIndex(command[1])
                    gameData[charType][charIndex].resetHp()
                else:
                    print("Unrecognized command")
                    

    
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
           
                                                      
