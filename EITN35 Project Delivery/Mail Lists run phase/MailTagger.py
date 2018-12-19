from lxml import html
import requests
import datetime
from MailDateFinder import date
from MailCVEFinder import CVE
from JSON import JSON
#from ProductVendorFinder import readText
import ProductVendorFinder

timendate = datetime.datetime.now()
baseUrlFull = "http://seclists.org/fulldisclosure"
baseUrlBug = "http://seclists.org/bugtraq"
baseUrlOSS = "http://seclists.org/oss-sec"
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
quaters = ["q1", "q2", "q3", "q4"]
lastYear = 0
lastMonth = 0
lastPage = 0
lastQuater = 0
lastFetch = "lastFetch.txt"
defaultYear = 2018

#Check inside the file lastFetch and return it
def checkLastFetch():
	fo = open(lastFetch, "r")
	ly = int(fo.readline())
	if (ly == 0):
		ly = defaultYear
	lm = int(fo.readline())
	lp = int(fo.readline())
	lq = int(fo.readline())
	fo.close()
	lastFetchList = [ly, lm, lp, lq]
	return lastFetchList

#saves the current year, month, page, quater into the lastFetch file
def saveLastFetch(y, m, p, q):
	file2write = open(lastFetch, "w")
	file2write.write(y + "\n")
	file2write.write(m + "\n")
	file2write.write(p + "\n")
	file2write.write(q)
	file2write.close()

#Gets the email content from the webpage, this is specially made for seclist site last visited 20180530
def getContent(webpage):
	page = requests.get(webpage, allow_redirects=False)
	tree = html.fromstring(page.content)
	contentlist = [td.text_content() for td in tree.xpath('//td')]
	text = ''.join(contentlist)
	return text

#The main function that works with fulldisclosure and OSS
def MailFinderByMonth(webBaseUrl):
	lastFetch = checkLastFetch()
	startYear = lastFetch[0]
	print(str(startYear) + "START YEAR")
	startMonth = lastFetch[1]
	startPage = lastFetch[2] + 1
	currentYear = timendate.year
	#Traverse years
	for x in range (startYear, currentYear + 1):
		#Traverse months
		for y in range(startMonth, 12):
			dowloading = True
			pageNum = startPage
			while dowloading:
				page = webBaseUrl+"/"+str(x)+"/"+months[y]+"/"+str(pageNum) #Fabricate URL of the page
				print(page)
				content = getContent(page)
				pageNum += 1
				#Check if end of month
				if(content==""):
					dowloading = False
					print("done with " + page)
				else:
					#Call to textfinders
					#print(pageNum)
					#print(content)
					print("PAGE NUMBER IS: " + str(pageNum-1))
					datedate = ""
					datedate = date(content) #Fetch date
					print (datedate)
					cvelist = []
					cvelist = CVE(content) #Fetch CVE
					print (cvelist)
					#print(content)
					listComp = []
					listProd = []
					listComp, listProd = MailgetCompanyProduct(content) #Fetch possible company names and product names
					JSON(page, datedate, cvelist, listComp, listProd)
					print("STORED")
					saveLastFetch(str(x), str(y), str(pageNum - 1), "0")

		startMonth = 0
		startPage = 0

#Main version that works with bugtraq
def MailFinderByQuarter(webBaseUrl):
	startYear = 2018
	startQuater = 0
	startPage = 0
	currentYear = timendate.year
	for x in range (startYear, currentYear + 1):
		for y in range(startQuater, 4):
			dowloading = True
			pageNum = startPage
			while dowloading:
				page = webBaseUrl+"/"+str(x)+"/"+quaters[y]+"/"+str(pageNum)
				content = getContent(page)
				print(page)
				content = getContent(page)
				pageNum += 1
				#Check if end of month
				if(content==""):
					dowloading = False
					print("done")
				else:
					#Call to textfinders
					#print(pageNum)
					#print(content)
					print("PAGE NUMBER IS: " + str(pageNum-1))
					datedate = ""
					datedate = date(content) #Fetch date
					print (datedate)
					cvelist = []
					cvelist = CVE(content) #Fetch CVE
					print (cvelist)
					#print(content)
					listComp = []
					listProd = []
					listComp, listProd = MailgetCompanyProduct(content) #Fetch possible company names and product names
					JSON(page, datedate, cvelist, listComp, listProd)
					print("STORED")
					saveLastFetch(str(x), str(y), str(pageNum - 1), "0")
		startMonth = 0
		startPage = 0

#Funtion that fetches company and product
def MailgetCompanyProduct(mailContent):
	ProductVendorFinder.readText(mailContent)
	companies = ProductVendorFinder.getCompanies()
	products = ProductVendorFinder.getProducts()
	#Create lists to return
	affectedCompanies = []
	affectedProducts = []
	for comp in companies:
		if(companies[comp] > 2):
			#print("POINTS COMP ARE: " + str(companies[comp]))
			affectedCompanies.append(comp)
	for prod in products:
			if(products[prod] > 2):
				#print("POINT PROD ARE: " + str(products[prod]))
				affectedProducts.append(prod)

	print("TOP Vendor: " + max(companies, key=lambda i: companies[i]))
	print("TOP Product: " + max(products, key=lambda i: products[i]))
	print("All Vendors")
	print(affectedCompanies)
	print("All products")
	print(affectedProducts)
	return affectedCompanies, affectedProducts

#MailFinderByQuarter(baseUrlOSS)
MailFinderByMonth(baseUrlFull) #Fetch mail from fulldisclosure
