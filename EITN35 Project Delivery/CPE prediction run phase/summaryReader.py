import nltk
from nltk.corpus import wordnet
import json

cveNr = 0
summary = ""
productNames =  {}
companyNames = {}
versionNumber = {}
CPEList = []
vendorList = []
versionList = []
affectedProductList = []

#Read files containing english words and filter words
with open("words.txt") as wordfile:
	dictionary = set(word.strip().lower() for word in wordfile)
with open("vulnerbilities.txt") as vuln:
	vulnerbilities = set(word.strip().lower() for word in vuln)
with open("filter.txt") as filterfile:
	filter = set(word.strip().lower() for word in filterfile)
#Read CVE's from nvdcve's json containing all CVE from that year
with open('nvdcve-1.0-2018.json') as json_data:
    data = json.load(json_data)
#Reads and saves values from a CVE. Reads in both affected companies, products and version to use as correct answer
#Reads summary to tag using nltk to get possible names and versions
def readNext():
	global cveNr
	print (cveNr)
	productNames.clear()
	companyNames.clear()
	versionNumber.clear()
	affectedProductList.clear()
	vendorList.clear()
	versionList.clear()
	print("Reading next CVE JSON")
	cve = data["CVE_Items"][cveNr]
	summary = "A " + cve["cve"]["description"]["description_data"][0]["value"]
	affectedVendors = cve["cve"]["affects"]["vendor"]["vendor_data"]
	for vendor in affectedVendors:
		vendorList.append(vendor["vendor_name"])
		affectedProducts = vendor["product"]["product_data"]
		for prod in affectedProducts:
			affectedProductList.append(prod["product_name"])
			for ver in prod["version"]["version_data"]:
				versionList.append(ver["version_value"])

	tokens = nltk.word_tokenize(summary)
	tagged = nltk.pos_tag(tokens)
	entities = nltk.chunk.ne_chunk(tagged)
	i=0
	for tag in tagged:
	#if tagged word is a NNP/a name
		if(tag[1] == 'NNP' or tag[1] == 'NN'):
			companyNames[tag[0].strip().lower().strip().lower()] = 0.5
			productNames[tag[0].strip().lower().strip().lower()] = 0.5
			if(len(tag[0].strip().lower()) == 1):
				companyNames[tag[0].strip().lower()] = 0
				productNames[tag[0].strip().lower()] = 0
			#Check if the NNP/name is a word in a dictionary.
			if (tag[0].strip().lower().strip().lower() in dictionary):
				#lower chance of NNP/name to be a company/product if it's an English word
				companyNames[tag[0].strip().lower()] *= 0.5
				productNames[tag[0].strip().lower()] *= 0.5
			if (tag[0].strip().lower().strip().lower() in vulnerbilities):
				companyNames[tag[0].strip().lower()] = 0
				productNames[tag[0].strip().lower()] = 0
			if (tag[0].strip().lower().strip().lower() in filter):
				companyNames[tag[0].strip().lower()] *= 0.25
				productNames[tag[0].strip().lower()] *= 0.25
			if ("." in tag[0].strip().lower()):
				companyNames[tag[0].strip().lower()] *= 0.5
				productNames[tag[0].strip().lower()] *= 0.5
			#Check if previous word is tagged as NN or NNP or IN
			if(i > 0):
				if(tagged[i-1][1] == "NNP" or tagged[i-1][1] == "NN"):
					companyNames[tagged[i-1][0].strip().lower() + "_" + tag[0].strip().lower().strip().lower()] = 0.5
					productNames[tagged[i-1][0].strip().lower()+ "_" +  tag[0].strip().lower().strip().lower() ] = 0.5
					companyNames[tagged[i-1][0].strip().lower()] *= 1.2
					productNames[tag[0].strip().lower()] *= 1.2
				if(tagged[i-1][1] == "IN"):
					companyNames[tag[0].strip().lower()] *= 1.2
					productNames[tag[0].strip().lower()] *= 1.5
			else:
				#Chance of being a company name increased if first NNP
				companyNames[tag[0].strip().lower()] *= 1.1
		#if tagged word is CD/number			
		if(tag[1]== "CD"): 
			versionNumber[tag[0].strip().lower()] = 0.5
			if(tagged[i-1][1] == "NNP" or tagged[i-1][1] == "NN" ):
				versionNumber[tag[0].strip().lower()] *= 1.5
			if("." in tag[0].strip().lower()):
				versionNumber[tag[0].strip().lower()] *= 1.8
			# Need to be the last check since it replaces version number with the "IN" tagged word + the version number
			#if(tagged[i-1][1] == "IN"):
			#	versionNumber[tag[0].strip().lower()] *= 1.8
			#	versionMod = tagged[i-1][0].strip().lower() + " " + tag[0].strip().lower()
			#	versionNumber[versionMod]= versionNumber[tag[0].strip().lower()]
			#	del versionNumber[tag[0].strip().lower()]
				
		i+=1
	cveNr +=1
def getProducts():
	return productNames
def getCompanies():
	return companyNames
def getVersions():
	return versionNumber
def getCPEList():
	return CPEList
def getAffectedVendors():
	return vendorList
def getAffectedProducts():
	return affectedProductList
def getAffectedVersions():
	return versionList
