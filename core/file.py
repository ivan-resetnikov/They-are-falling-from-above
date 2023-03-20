from json import load, dump

def loadFromJSON (path) :
	with open(path, 'r') as file :
		return load(file)


def writeToJSON (path, content) :
	with open(path, 'w') as file :
		return dump(content, file)