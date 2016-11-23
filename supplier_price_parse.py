import os
import sys
import xlrd

GRAM_CONVERSION_FACTOR = 453.59237

def scrape_third_party_price_list(filename):
    """
        Checks file existance and starts parsing process
    """
    if not os.path.isfile(filename):
        print ("File does not exist.")
        return

    try:
        workbook = xlrd.open_workbook(filename)
    except Exception as e:
        print (e)
        return

    worksheet = workbook.sheet_by_name('Sheet1')    #Sheet name of xlsx
    return get_from_file(worksheet)


def get_from_file(worksheet):
    """
        Gets data from file starting at row 4 (below titles)
    """
    num_rows = worksheet.nrows
    num_cols = worksheet.ncols

    titles = []
    prices = []

    for col in range (0,num_cols):
        for row in range (4,num_rows):
            if (col % 2 == 0):  #even columns (product name columns)
                titles.append(worksheet.cell(row,col))
            else:
                prices.append(worksheet.cell(row,col))

    return make_info_dict(titles, prices)


def make_info_dict(titles, prices):
    """
        Takes all information from provided xlsx file, and transfers it over to
        nested dictionaries for json communication
    """
    title = None
    mini_dict = {}
    supplier_info = {}

    for i in range(0,len(titles)-1):
        
        if (titles[i].value != "" and prices[i].value == ""):   #If a title
            if (mini_dict != {}): #If there is info in the mini dictionary
                supplier_info[title] = mini_dict

            title = titles[i].value #set new title
            mini_dict = {}  #empty dict

        elif (titles[i].value != "" and type(prices[i].value) == float): #product
            if "lb" in titles[i].value: #It can be converted

                price = prices[i].value
                products = titles[i].value.split()

                for item in products:   #removing "cs" from all product names
                    if item == "cs":
                        products.remove(item)

                for item in products:
                    if "lb" in item:    #if lb component
                        products.remove(item)
                        val = price_per_100grams(item, price)   #calculate price
                        if val != None: #If calculated properly, add to list
                            price = round(val,2)
                            product = " ".join(products)
                            mini_dict[product] = price

    return supplier_info


def price_per_100grams(item, price):
    """
        Calculates price of item per 100 grams
    """
    val = lb_to_grams(item)
    if val != None:
        per_gram = price/val
        return per_gram*100
    else:
        return None


def lb_to_grams(item):
    """
        Translates lbs to grams 
    """
    numbers = item.split("lb")
    try:
        val = float(numbers[0])
        val = (val*GRAM_CONVERSION_FACTOR)
        return val
    except Exception as e:
        return None


def main():

    try:
        supplier_info = scrape_third_party_price_list(sys.argv[1])
        print (supplier_info)
    except IndexError as e:
        print("File name is required as first arguemnt.")


if __name__ == "__main__":
    main()
