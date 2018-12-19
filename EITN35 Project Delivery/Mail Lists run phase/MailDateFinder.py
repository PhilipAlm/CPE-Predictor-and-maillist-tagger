

#Find the date on a specific mail and returns the date.
def date(mail):
    index = mail.find("Date:")
    index = index+11
    date = ""
    month = ""
    year = ""
    while(mail[index].isdigit()):
        date+=mail[index]
        index+=1
    date+="/"+str(switch_demo(mail[index+1:index+4]))
    date+= "/" + mail[index + 5:index + 10]
    return date

#Changes the form of the months to the corresponding number.
def switch_demo(argument):
    switcher = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    return switcher.get(argument, "Invalid month")

date("Date: Mon, 1 Sep 2003 07:54:03 +0200")