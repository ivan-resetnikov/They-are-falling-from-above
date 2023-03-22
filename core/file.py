import json


def loadFromJSON (path) :
	with open(path, 'r') as file :
		return json.load(file)


def writeToJSON (path, content) :
	with open(path, 'w') as file :
		return json.dump(content, file)