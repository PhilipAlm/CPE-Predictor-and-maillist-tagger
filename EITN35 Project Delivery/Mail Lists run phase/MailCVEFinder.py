

#Find CVE in a specific mail and returns it as a list of CVEs
def CVE(mail):
    index = 0
    list=[]
    while(index != -1):
        index = mail.find("CVE", index+1)
        temp = CVEChecker(index,mail)
        if (temp!=0):
            if temp not in list:
                list.append(temp)
    return list

#Check that the CVE that is found is on the correct format and is a CVE ID
def CVEChecker(index, mail):
    temp = "CVE"
    index2=index+9
    if(mail[index+3] == "-"):
        temp+="-"
        if(mail[index+4:index+8].isdigit()):
            temp+=mail[index+4:index+8]
            if(mail[index+8] == "-"):
                temp+="-"
                while (mail[index2].isdigit()):
                    temp+= mail[index2]
                    index2+=1
                return temp
    return 0


mail1= "Title: Persistent Cross-Site Scripting (XSS) in SpagoBI Date published: 2014-03-01 Date of last update: 2014-03-01 Vendors contacted: Engineering Group Discovered by: Christian Catalano Severity: High 02. ###  Vulnerability Information ### CVE reference: CVE-2013-6232 CVSS v2 Base Score: 4CVSS v2 Vector: (AV:N/AC:L/Au:S/C:N/I:P/A:N)Component/s: SpagoBIClass: CVE Input Manipulation CVE-1995-08257624, cve-2099-0080. Hejsan feropemrioasd CvE-4356-65347, CVE-456-67890, CVE-34567-34567"
print CVE(mail1)