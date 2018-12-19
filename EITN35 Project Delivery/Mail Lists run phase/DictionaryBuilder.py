import json
productDict = {}
companyDict = {}
def build():
	global productDict
	global companyDict
	with open("prodict.json") as json_file:
		productDict = json.load(json_file)
	with open("comdict.json") as json_file:
		companyDict = json.load(json_file)
	#print(productDict)
def getProductDict():
	return productDict
def getCompanyDict():
	return companyDict