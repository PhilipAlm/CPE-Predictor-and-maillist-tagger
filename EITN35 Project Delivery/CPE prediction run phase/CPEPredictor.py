#import nltk
#from nltk.corpus import wordnet
#import operator
import DictionaryBuilder 
import summaryReader

DictionaryBuilder.build()
companyDict = DictionaryBuilder.getCompanyDict()
productDict = DictionaryBuilder.getProductDict()
amount = 15
correctProducts = 0
correctCompanies = 0
correctVersions = 0
correctAll = 0
amountProducts = amount
amountVendors = amount
amountVersions = amount
amountAll = amount

#takes three strings and formats it to a cpe 2.3. Version is left out if missing. a for application is default if missing
def buildCPE(comp,prod,ver):
	cpe = "cpe:2.3:"
	if prod in productDict:
		temp = productDict[prod]
		for word in temp:
			if (word == "a" or word == "h" or word == "o"):
				cpe += word
	else:
		cpe += "a"
	cpe += ":"
	cpe += comp
	cpe += ":"
	cpe += prod
	cpe += ":"
	if ver != "null":
		cpe += ver
	else:
		cpe += "*"
	cpe += ":*:*:*:*:*:*:*"
	return cpe

for i in range (0,amount):
	correct = True
	#Call summary reader to read next summary from json file
	summaryReader.readNext()
	#Get all lists from summary reader
	companies = summaryReader.getCompanies()
	products = summaryReader.getProducts()
	versions = summaryReader.getVersions()
	#Check possible products with the dictionary of previosly affected products
	for product in products:
		if (product.strip().lower() in productDict):
			#when a product match is found, also check if the companies that made that product is mentioned in the summary
			for comp in productDict[product.strip().lower()]:
				if(comp.strip().lower() in companies):
					#Score the found company and product to raise probabillity
					products[product] *= 2.5
					companies[comp] *= 2.5
			products[product] *= 2.5
	#Check possible companies with dictionary of previosly mentioned affected companies
	for company in companies:
		if (company.strip().lower() in companyDict):
			companies[company] *= 2.5
	# Check if the most likely company is in the dictionary for affected companies
	if(max(companies, key=lambda i: companies[i]) in companyDict):
		for prod in companyDict[max(companies, key=lambda i: companies[i])]:
			if prod[:-1] in products:
			#if a company´s product is mentioned add probabillity, applications are more 
			#likely than operative systems and hardware so the multiplier is higher
				if(prod[-1:] == "a"):
					products[prod[:-1]] *= 2.5
				if(prod[-1:] == "o"):
					products[prod[:-1]] *= 2
				if(prod[-1:] == "h"):
					products[prod[:-1]] *= 1.5
	#Check if the max probabillity company is part of the affected vendors in the .json
	if(max(companies, key=lambda i: companies[i]) in summaryReader.getAffectedVendors() ):
		correctCompanies += 1
	else:
		correct = False;
	#Check if the max probabillity product is part of the affected products in the .json
	if(max(products, key=lambda i: products[i]) in summaryReader.getAffectedProducts() ):
		correctProducts += 1
	else:
		correct = False;
	if(versions):
		#Check if the max probabillity version is part of the affected versions in the .json
		if (max(versions, key=lambda i: versions[i]) in summaryReader.getAffectedVersions() ):
			correctVersions += 1
		else:
			correct = False
	elif summaryReader.getAffectedVersions:
		correct = False
	if(correct):
		correctAll += 1
	#If the affected part is missing in the .json remove it from the total count
	if not summaryReader.getAffectedVendors():
		amountVendors -= 1
	if not summaryReader.getAffectedProducts():
		amountProducts -= 1
	if not summaryReader.getAffectedVersions():
		amountVersions -= 1
		
	#Print the most probable answer for each part of the cpe and what was part of the affected section in the .json
	print("Guessed company: " + max(companies, key=lambda i: companies[i]) + " was : " + str(summaryReader.getAffectedVendors()))
	print("Guessed product: " + max(products, key=lambda i: products[i]) + " was : " + str(summaryReader.getAffectedProducts()))
	#Call build CPE with the most probable answers
	if(versions):
		print("Guessed version: " + max(versions, key=lambda i: versions[i]) + " was : " + str(summaryReader.getAffectedVersions()))
		cpe = buildCPE(max(companies, key=lambda i: companies[i]),max(products, key=lambda i: products[i]),max(versions, key=lambda i: versions[i]))
		print(cpe)
	else :
		cpe = buildCPE(max(companies, key=lambda i: companies[i]),max(products, key=lambda i: products[i]),"null")
		print(cpe)
#Print the total result
print ( "--------- Done, Result: -------------")	
print ( "Guessed " + str (correctCompanies) + " out of " + str (amountVendors) + " Vendors" + " Rate: " + (str(correctCompanies/amountVendors)))
print ( "Guessed " + str (correctProducts) + " out of " + str (amountProducts) + " Products" + " Rate: " + (str(correctProducts/amountProducts)))
print ( "Guessed " + str (correctVersions) + " out of " + str (amountVersions) + " Versions" + " Rate: " + (str(correctVersions/amountVersions)))
print ( "Total fully correct: " + str(correctAll))


	
