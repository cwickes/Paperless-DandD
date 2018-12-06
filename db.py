import sqlite3

class DND_DB:
	def __init__(self, name = "dnd35.db"):
		db = sqlite3.connect(name)
		self.cursor = db.cursor()
		
	def monsters(self):
		monName = input()
		monName = monName.capitalize()
		print()
		attributes = ["id", "family", "name", "altname", "size", "type", "descriptor", "hit_dice", 
		"initiative", "speed", "armor_class", "base_attack", "grapple", "attack", "full_attack",
		"space", "reach", "special_attacks", "special_qualities", "saves", "abilities", "skills",
		"bonus_feats", "feats", "epic_feats", "environment", "organization", "challenge_rating",
		"treasure", "alignment", "advancement", "level_adjustment", "special_abilities",
		"stat_block", "full_text", "reference"]
		format = "SELECT * FROM monster WHERE (name='" + monName + "' OR altname='"+ monName + "')"
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid monster name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()[0]
			for x in range (1, len(temp) - 2):
				print(attributes[x] + ": " + temp[x])

	def spells(self):
		spellName = input()
		#spellName = spellName.capitalize()
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
	
#this currently doesn't work	
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
			
	def items(self):
		itemName = input()
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
				
	def equipment(self):
		eName = input()
		eName = eName.capitalize()
		print()
		attributes = ["id", "name", "family", "category", "subcategory", "cost", "dmg_s",
		"armor_shield_bonus", "maximum_dex_bonus", "dmg_m",
		"weight", "critical", "armor_check_penalty", "arcane_spell_failure_chance", "range_increment",
		"speed_30", "type", "speed_20", "full_text", "reference"]
		format = "SELECT * FROM equipment WHERE name='" + eName + "'"
		#self.cursor.execute("SELECT * FROM eq
		self.cursor.execute(format)
		if (len(self.cursor.fetchall()) == 0):
			print("You did not enter a valid item name.")
		else:
			self.cursor.execute(format)
			temp = self.cursor.fetchall()[0]
			for x in range (1, len(temp) - 2):
				print(attributes[x] + ": " + temp[x])
				
	def monsterAlignment(self):
		monAlign = input()
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
			
	def magicSchool(self):
		school = input()
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
				
	
	def feats(self):
		feat = input()
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
