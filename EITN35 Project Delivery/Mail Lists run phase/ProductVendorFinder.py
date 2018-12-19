import nltk
from nltk.corpus import wordnet
import json
import DictionaryBuilder

DictionaryBuilder.build()
companyDict = DictionaryBuilder.getCompanyDict()
productDict = DictionaryBuilder.getProductDict()

summary = ""
productNames =  {}
companyNames = {}

with open("words.txt") as wordfile:
	dictionary = set(word.strip().lower() for word in wordfile)
with open("vulnerbilities.txt") as vuln:
	vulnerbilities = set(word.strip().lower() for word in vuln)
with open("filter.txt") as filterfile:
	filter = set(word.strip().lower() for word in filterfile)

def readText(summaryText):
	summary = summaryText
	productNames.clear()
	companyNames.clear()
	#print("Reading Mail Text")
	tokens = nltk.word_tokenize(summary)
	tagged = nltk.pos_tag(tokens)
	entities = nltk.chunk.ne_chunk(tagged)
	i=0
	for tag in tagged:
		#print(tag)
	#if tagged word is a NNP/a name
		if(tag[1] == 'NNP' or tag[1] == 'NN'):
			companyNames[tag[0].strip().lower()] = 0.5
			productNames[tag[0].strip().lower()] = 0.5
			if(len(tag[0].strip().lower()) == 1):
				companyNames[tag[0].strip().lower()] = 0
				productNames[tag[0].strip().lower()] = 0
			#Check if the NNP/name is a word in a dictionary.
			if (tag[0].strip().lower() in dictionary):
				#lower chance of NNP/name to be a company/product if it's an English word
				companyNames[tag[0].strip().lower()] *= 0.5
				productNames[tag[0].strip().lower()] *= 0.5
			if (tag[0].strip().lower() in vulnerbilities):
				companyNames[tag[0].strip().lower()] = 0
				productNames[tag[0].strip().lower()] = 0
			if (tag[0].strip().lower() in filter):
				companyNames[tag[0].strip().lower()] *= 0.25
				productNames[tag[0].strip().lower()] *= 0.25
			if ("." in tag[0].strip().lower()):
				companyNames[tag[0].strip().lower()] *= 0.5
				productNames[tag[0].strip().lower()] *= 0.5
			#Check if previous word is tagged as NN or NNP or IN
			if(i > 0):
				if(tagged[i-1][1] == "NNP" or tagged[i-1][1] == "NN"):
					companyNames[tagged[i-1][0].strip().lower() + "_" + tag[0].strip().lower()] = 0.5
					productNames[tagged[i-1][0].strip().lower()+ "_" +  tag[0].strip().lower()] = 0.5
					companyNames[tagged[i-1][0].strip().lower()] *= 1.2
					productNames[tag[0].strip().lower()] *= 1.2
				if(tagged[i-1][1] == "IN"):
					companyNames[tag[0].strip().lower()] *= 1.2
					productNames[tag[0].strip().lower()] *= 1.5
			else:
				#Chance of being a company name increased if first NNP
				companyNames[tag[0].strip().lower()] *= 1.1
		i+=1
	#print(companyNames)
	#print(productNames)
	#print("\n")
	#print(max(companyNames, key=lambda i: companyNames[i]))
	#print(max(productNames, key=lambda i: productNames[i]))
	checkWithDict()

def checkWithDict():
	for product in productNames:
		if (product.strip().lower() in productDict):
			for comp in productDict[product.strip().lower()]:
				if(comp.strip().lower() in companyNames):
					productNames[product] *= 2.5
					companyNames[comp] *= 2.5
			productNames[product] *= 2.5
	for company in companyNames:
		if (company.strip().lower() in companyDict):
			companyNames[company] *= 2.5
	if(max(companyNames, key=lambda i: companyNames[i]) in companyDict):
		for prod in companyDict[max(companyNames, key=lambda i: companyNames[i])]:
			if prod[:-1] in productNames:
				if(prod[-1:] == "a"):
					productNames[prod[:-1]] *= 2.5
				if(prod[-1:] == "o"):
					productNames[prod[:-1]] *= 2
				if(prod[-1:] == "h"):
					productNames[prod[:-1]] *= 1.5
	#print(max(companyNames, key=lambda i: companyNames[i]))
	#print(max(productNames, key=lambda i: productNames[i]))

def getProducts():
	return productNames
def getCompanies():
	return companyNames
