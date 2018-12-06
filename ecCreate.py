import sqlite3
import os
import random

# method returns initialized ec object
# autoGen is boolean variable used to determine whether to automatically generate hp value
def ecCreate(autoGen = True):
	# DB connect
	dbFile = os.path.dirname(__file__) + '/dnd35.db'
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
		hp = int(hp[1][1:])
	else:
		hp = int(input('Set health for ' + name + ' with CR of ' + lvl + ': '))

	# prompt DM to determine mana for monster
	mana = int(input('Set mana for ' + name + ' with CR of ' + lvl + ': '))

	return ec(name, lvl, style, hp, mana)
