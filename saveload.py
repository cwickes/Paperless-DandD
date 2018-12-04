import pickle

def save(filename, data):
	saveFile = open(filename, "wb")
	
	pcList = data['pcs']
	ecList = data['ecs']

	pickle.dump(pcList, saveFile)
	pickle.dump(ecList, saveFile)

	saveFile.close()

	print("Session data saved")

def load(filename):
	loadFile = open(filename, "rb")

	data = {'pcs': [], 'ecs': []}

	data['pcs'] = pickle.load(loadFile)
	data['ecs'] = pickle.load(loadFile)

	loadFile.close()

	return data