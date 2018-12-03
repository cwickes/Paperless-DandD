class pc:
    def manatotal(self, lvl, style):
        mt = 0
        mc = [5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560]

        lvl = int(lvl)
        if(lvl >= 4):
			if (lvl % 2 == 0):
				mt += mc[math.floor(lvl/2)-1] * 5
				mt += mc[math.floor(lvl/2)] * 3
				for i in range (math.floor(lvl/2)-1):
					mt += mc[i] * 6
			if (lvl % 2 == 1):
				mt += mc[math.floor(lvl/2)] * 5
				for i in range (math.floor(lvl/2)):
					mt += mc[i] * 6
		else:
			mt = lvl * 10
        if (style == "Druid"):
			mt = int(mt * .75)
		elif (style == "Ranger" or style == "Paladin"):
			mt = (15 * lvl)-50
			if (mt < 0):
				mt = 0
		else:
			mt = 0
             
        return mt
    def __init__(self, name, lvl, style, mana, hp, hpmax, attr, init = 0, inventory):
        self.name = name
        self.lvl = int(lvl)
        self.style = style
        self.manaMax = self.manatotal(int(lvl), style)
        self.mana = int(mana)
        self.hpMax = int(hpmax)
        self.hp = int(hp)
        self.init = init
        self.active = True
        self.attr = attr.split(' ')
        self.condNote = ""
	self.inventory = []

    def setName(self, name):
        self.name = name

    def setLvl(self, lvl):
        self.lvl = lvl

    def resetMana(self):
        self.mana =  self.manaMax

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
    def __init__(self, name, lvl, style, mana, hp, init = 0, location = "", loot = []):
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
    

    def resetMana(self):
        self.mana =  self.manaMax

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
	
    def setLocationEncountered(self, location):
	self.locationEncountered = location

    def addLoot(self, item):
	self.loot.append(item)

    def sleep(self):
        self.active = False

    def wake(self):
        self.active = True

    def getInfo(self):
        manastr = (str(self.mana) + "/" + str(self.manamax))
        hpstr = (str(self.hp) + "/" + str(self.hpmax))
        if (self.active == False):
            hpstr += " (unconscious)"
        ecstr = [self.name, str(self.style), manastr, hpstr, str(self.init)]
        return ecstr
