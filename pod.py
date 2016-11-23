import xlrd
import json

def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def printAll(s):
    printOrder(s)
    printInvoice(s)
    
def printOrder(s):
    try:
        book = xlrd.open_workbook(s)
        sh = book.sheet_by_index(0)
        print sh.name, sh.nrows, sh.ncols

        jout = "{\"order sheet items\":[" #json format string builder
        total = 0 #total price
        org = 0 #organization
        week = 0 #week number
        date = 0 #delivery date
        for rx in range(sh.nrows):
            index = sh.cell_value(rowx=rx, colx=0)
            if isFloat(index):
                name = sh.cell_value(rowx=rx, colx=1)
                unit = sh.cell_value(rowx=rx, colx=2)
                supplier = sh.cell_value(rowx=rx, colx=3)
                pod = sh.cell_value(rowx=rx, colx=4)
                quantity = sh.cell_value(rowx=rx, colx=6)
                subtotal = sh.cell_value(rowx=rx, colx=7)
                js = {"number":index,"name":name,"unit":unit,"supplier":supplier,"pod":pod,"quantity":quantity,"subtotal":subtotal}
                js = json.dumps(js) #convert to string
                jout+=js #append to output string
                jout+="," #insert seperator
            else:
                if sh.cell_value(rowx=rx, colx=6).lower() == "total":
                    total = sh.cell_value(rowx=rx, colx=7)
                if sh.cell_value(rowx=rx, colx=1).lower() == "organization:":
                    org = sh.cell_value(rowx=rx, colx=2)
                if sh.cell_value(rowx=rx, colx=6).lower() == "week":
                    week = sh.cell_value(rowx=rx, colx=7)
                if sh.cell_value(rowx=rx, colx=1).lower() == "delivery date:":
                    date = sh.cell_value(rowx=rx, colx=2)
        jout = jout[:-1] #remove last comma
        jout+="],\"total\":"
        jout+=str(total)
        jout+=",\"organization\":\""
        jout+=str(org)
        jout+="\",\"week\":\""
        jout+=str(week)
        jout+="\",\"delivery date\":\""
        jout+=str(date)
        jout+="\"}"
        jout = json.loads(jout) #to json
        print jout
        return jout
    except:
        print "failed to read from POD order sheet"
        return None
    
def printInvoice(s):
    try:
        book = xlrd.open_workbook(s)
        sh = book.sheet_by_index(1)
        print sh.name, sh.nrows, sh.ncols

        jout = "{\"order sheet items\":[" #json format string builder
        total = 0 #total price
        org = 0 #organization
        week = 0 #week number
        date = 0 #date
        invoice = 0 #invoice number
        for rx in range(sh.nrows):
            index = sh.cell_value(rowx=rx, colx=0)
            if isFloat(index):
                name = sh.cell_value(rowx=rx, colx=1)
                unit = sh.cell_value(rowx=rx, colx=2)
                supplier = sh.cell_value(rowx=rx, colx=3)
                pod = sh.cell_value(rowx=rx, colx=4)
                quantity = sh.cell_value(rowx=rx, colx=6)
                subtotal = sh.cell_value(rowx=rx, colx=7)
                js = {"number":index,"name":name,"unit":unit,"supplier":supplier,"pod":pod,"quantity":quantity,"subtotal":subtotal}
                js = json.dumps(js) #convert to string
                jout+=js #append to output string
                jout+="," #insert seperator
            else:
                if sh.cell_value(rowx=rx, colx=5).lower() == "total payable:":
                    total = sh.cell_value(rowx=rx, colx=7)
                if sh.cell_value(rowx=rx, colx=4).lower() == "organization:":
                    org = sh.cell_value(rowx=rx, colx=6)
                if sh.cell_value(rowx=rx, colx=4).lower() == "week":
                    week = sh.cell_value(rowx=rx, colx=6)
                if sh.cell_value(rowx=rx, colx=4).lower() == "date:":
                    date = sh.cell_value(rowx=rx, colx=6)
                if sh.cell_value(rowx=rx, colx=4).lower() == "invoice number:":
                    date = sh.cell_value(rowx=rx, colx=6)
                    date += sh.cell_value(rowx=rx, colx=7)
                    date += sh.cell_value(rowx=rx, colx=8)
        jout = jout[:-1] #remove last comma
        jout+="],\"total\":"
        jout+=str(total)
        jout+=",\"organization\":\""
        jout+=str(org)
        jout+="\",\"week\":\""
        jout+=str(week)
        jout+="\",\"date\":\""
        jout+=str(date)
        jout+="\",\"invoice number\":\""
        jout+=str(invoice)
        jout+="\"}"
        jout = json.loads(jout) #to json
        print jout
        return jout
    except:
        print "failed to read from POD invoice sheet"
        return None
    
printAll("pod.xlsx")