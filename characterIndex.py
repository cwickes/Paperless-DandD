def characterIndex(name):
    name = name.lower()
    for i in range(len(gameData['pcs'])):
        if ((gameData['pcs'][i].name).lower() == name):
            return 'pcs', i
    for i in range(len(gameData['ecs'])):
        if ((gameData['ecs'][i].name).lower() == name):
            return 'ecs', i
    return '', -1

##gameData = {
##	'pcs' : [],
##	'ecs' : []
##	}

#to acess things you would do
#gameData[charType][index].member_variable
#e.g. to get John's lvl you do
#charType, charIndex = characterIndex('John')
#e.g. gameData[charType][charIndex].lvl
