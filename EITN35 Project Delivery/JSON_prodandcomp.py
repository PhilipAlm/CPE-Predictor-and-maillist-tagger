import json


#Creates a dictionary from the CPE dictionary and all the JSON feeds of CVE's on nist webb page.
#It has the product as key and the company and type is added as sets to the product.
def dictionary (datafile, word_dict):
    #dictionary = {}
    word = "cpe:2.3:"
    for line in datafile:
        if word in line:
            s = line[line.find(word) + 8:]
            type = s[:1]
            s = s[s.find(":") + 1:]
            s = s[:s.find(":")]
            company = s
            p = line[line.find(word) + 10:]
            p = p[p.find(":") + 1:]
            p = p[:p.find(":")]
            if p not in word_dict:
                word_dict[p] = set()
                word_dict[p].add(type)
                word_dict[p].add(company)
            else:
                word_dict[p].add(company)
    return word_dict

word_dict = dict()
datafile = open("cpe.txt",'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2018.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2017.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2016.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2015.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2014.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2013.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2012.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2011.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2010.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2009.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2008.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2007.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2006.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2005.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2004.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2003.json', 'r')
word_dict = dictionary(datafile, word_dict)
datafile = open('nvdcve-1.0-2002.json', 'r')
word_dict = dictionary(datafile, word_dict)
print (word_dict["terminal"])


#with open("prodict.json") as json_file:
 #   data = json.load(json_file)
#print (data)
for key in word_dict:
    #print(key)
    intelist = list(word_dict[key])
    word_dict[key] = intelist

with open('prodict.json', 'w') as fp:
    json.dump(word_dict, fp)

#    item = {
#            'company' : key,
#            'product': intelist
#            }
#with open('data.json', 'r') as fp:
#    temp = json.load(fp)
#print (temp["apple"])
#    data.append(item)
#with open('JSON1.json', 'w') as outfile:
#    json.dump(data, outfile)