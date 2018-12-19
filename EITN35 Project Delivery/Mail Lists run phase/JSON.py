import json

def JSON(mail, date, CVE, vendors, products):
    with open("JSON.json") as json_file:
        data = json.load(json_file)
    item = {
        'mail' : mail,
        'date' : date,
        'CVE' : CVE,
        'vendors' : vendors,
        'products' : products
    }
    data.append(item)
    with open('JSON.json', 'w') as outfile:
        json.dump(data, outfile)

#JSON("HEJ", "1/9/2003", ["CVE-1234-5678", "CVE-4567-6543"])
#JSON("HEJsan", "1/9/2003", ["CVE-1234-5678", "CVE-4567-6543"])
#JSON("HEJsan123", "1/9/2003", ["CVE-1234-5678", "CVE-4567-6543"])
