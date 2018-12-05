    turn = 0
    actions = -1

    for i in range(numPC):
        dmgstats.append(0)
        manastats.append(0)
        healstats.append(0)
        hurtstats.append(0)
        
    ################################# COMBAT START #################################
        
    while (combat_start == True):
        
        actions +=1
        print("\n" * 20)
		if(actions < 5):
			print('Enter a command or type "help" for a list of commands')
			
        if(gameData['pcs'][0].init != 0):
            num = (turn) % (numPC + numEC)
            roundNum = int((turn) / (numPC + numEC) + 1)
            print('{:^15}'.format("ROUND: " + str(roundNum)) + '{:^15}'.format("TURNS: " + str(turn)) + '{:^15}'.format("ACTIONS: " + str(actions)))
            gameData['pcs'] = sorted(gameData['pcs'], key=lambda pc: pc.init, reverse=True)
            gameData['ecs'] = sorted(gameData['ecs'], key=lambda ec: ec.init, reverse=True)
            
        else:
            gameData['pcs'] = sorted(gameData['pcs'], key=lambda pc: pc.name)
        print("     "+ "{:^5}".format("#") + "{:^20}".format("Name") + "{:^20}".format("Level") + 
        "{:^20}".format("Mana") + "{:^20}".format("Health")  + "{:^22}".format("") + "     "+ "{:^5}".format("#") + "{:^20}".format("Name") + "{:^20}".format("Race/Type") + 
        "{:^20}".format("Mana") + "{:^20}".format("Health"))
        printRosterInfo(gameData['pcs'], gameData['ecs'], num)

        ########### SPLIT COMMAND INTO STMT ###########
        
        command = input()
		command = comand.lower()
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
                
            elif (command[0] == "-" or command[0] == '_'):
                turn-=1
                actions -=1
                
            elif (command[0] == "--" or command[0] == '__'):
                actions -=1
                
	    elif (command[0] == "help"):
		print ("Command List:\n",
			"roll [n-sided dice]\n",
			"reset-hp [to-player]\n",
			"reset-mana [to-player]\n",
			"hurt [to-player] [by-player] [damage-amount]\n",
			"heal [to-player] [by-player] [heal-amount]\n",
			"cast [to-player] [by-player] [mana-lost]\n",
			"restore [to-player] [by-player] [mana-gained]\n",)
			
			################## DOT SEPERATED ENTRY ##################
				
			elif(len(command.split('.')) > 1)
				dotStmt = command.split(".")
				dotStmtLen = len(dotStmt)
		
				elif (dotStmtLen == 2):
					if (dotStmt[0] == "4""):
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
					print(dotStmt)

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
					print(dotStmt)
					if (dotStmt[2][0] == "0"):
						byPC = False
						dotStmt[2] = str(int(dotStmt[2])-1)
					else:
						dotStmt[2] = str(int(dotStmt[1])-1)
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

                                            

            	################## HURT/HEAL/CAST/RESTORE IMPLEMENTATION ###################

		elif (commandLen >= 3):

			if (command[0] == "hurt"):

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
                                        # not accounting effects of spell casted on player

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



								
