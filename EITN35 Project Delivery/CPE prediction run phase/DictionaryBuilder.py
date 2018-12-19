import json
productDict = {}
companyDict = {}
def build():
	global productDict
	global companyDict
	#Read dictionary from json containing affected companies and their affected products
	with open("prodict.json") as json_file:
		productDict = json.load(json_file)
	#Read dictionary from json containing affeted companies, what type it is and who made it
	with open("comdict.json") as json_file:
		companyDict = json.load(json_file)
def getProductDict():
	return productDict
def getCompanyDict():
	return companyDict