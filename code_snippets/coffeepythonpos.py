# This program is meant to be run from the command prompt or terminal:
#  
# python3 coffeepythonpos.py



products = {
    "brewedcoffee":{"name":"Brewed Coffee","price":120.00},
    "espresso":{"name":"Espresso","price":140.00},
    "americano":{"name":"Americano","price":150.00},
    "capuccino":{"name":"Capuccino","price":170.00},
}

def get_product(code):
    return products[code]

def add_to_tray(food_tray, ordered_item):
    food_tray.append(ordered_item)

def generate_receipt(food_tray):
    running_total = 0
    print("-----------------------------------------------------")
    for i in food_tray:
        name = products[i["code"]]["name"]
        print("{}{}{:10d}{:10,}".format(i["code"].ljust(13),name.ljust(20),i["qty"],i["subtotal"]))
        running_total += i["subtotal"]

    print(" ")
    print("Total:                                     {:10,}".format(running_total))
    print("-----------------------------------------------------")

def main():

    food_tray = []
    command = "N"
    while(True):
        command = input("Options: N-New customer, Q-Quit ")
        if(command.upper()=="Q"):
            break
        else:
            more = "Y"
            while(more=="Y"):
                code = input("Enter Product Code: ")
                qty = int(input("Enter Quantity: "))
                print(code + ": "+str(qty))
                ## add code here
                ordered_item = dict()
                ordered_item["code"] = code
                ordered_item["qty"] = qty
                ## compute subtotal and add to the ordered_item dictionary
                ordered_item["subtotal"] = int(qty) * get_product(code)["price"]

                ## add to food_tray
                add_to_tray(food_tray,ordered_item)

                more = input("Add more items? (Y/N): ").upper()

        # print(food_tray) # replace with an on-screen receipt
        generate_receipt(food_tray)
        food_tray = [] # clear out food tray


    print("Exiting CoffeePython POS Terminal. Have a great day.")


main()
