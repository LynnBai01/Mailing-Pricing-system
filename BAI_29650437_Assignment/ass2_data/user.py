# -*-coding:utf-8-*-

from datetime import datetime
import data_manager as dm

# Global Variables:
# listCart：
# format of the item: type, method, country, weight, price, quantity, cost
listCart = []
totalCost = 0

# Define the Customer main menu
def main():
    select = ''
    while True:
        select = getMenuInput()
        if(select == '1'):
            addItem()
        elif(select == '2'):
            amendItem()
        elif(select == '3'):
            removeItem()
        elif(select == '4'):
            printCart()
        elif(select == '5'):
            checkout()
        elif(select == '6'):
            # empty the Cart and checkout
            listCart = []
            updateTotalCost()
            break
        else:
            print('Input error, try input again:')

# Show the main menu
def getMenuInput():
    return input('''
    Please select the following：
    1. Add Item
    2. Amend Item
    3. Remove Item
    4. View shopping cart
    5. Checkout and Print receipt
    6. Quit 
    ''')

# Add Item:
def addItem():
    type = getInputType()
    method = getInputMethod(type)
    country = getInputCountry()
    weight = getInputWeight()
    # Find and provide the price guide according to the input above. If no price can find, then indicate an error.
    prices = dm.dictPrice.get(dm.listStampMethod[type][method])
    zone = dm.dictCountry.get(country)
    zoneIndex = dm.listZone.index(zone)
    weightValid = False
    price = 0
    for p in prices:
        # If the weight is in the price range(because in some method, some weight range to some zones are not available)
        if(p[0] >= weight):
            weightValid = True
            price = p[zoneIndex+1]
            break
    if(not weightValid):
        print('Your item is overweight and cannot be sent')
        return
    elif(price <= 0):
        print('Invalid destination, method and weight, your item cannot be sent')
        return
    quantity = getInputQuantity()
    cost = price * quantity
    item = getItem(type, method, country, weight)
    global listCart
    # Cannot find identical item.
    if(not item):
        item = []
        item.append(type)
        item.append(method)
        item.append(country)
        item.append(weight)
        item.append(price)
        item.append(quantity)
        item.append(cost)
        listCart.append(item)
    else:
        item[5] += quantity
        item[6] += cost
    printCart()
    updateTotalCost()

# I want to amend the Item
def amendItem():
    printCart()
    global listCart
    if (not listCart):
        return
    print('Please input the no. of the item you want to amend:')
    amendIndex = getInputItemNo()
    item = listCart[amendIndex]
    select = getInputAmendOption()
    if(select == 1):
        type = item[0]
        method = getInputMethod(type)
        country = item[2]
        weight = item[3]
        # Find the price according to the type, method, country and weight
        prices = dm.dictPrice.get(dm.listStampMethod[type][method])
        zone = dm.dictCountry.get(country)
        zoneIndex = dm.listZone.index(zone)
        weightValid = False
        price = 0
        for p in prices:
            # The weight is in the price range.
            if (p[0] > weight):
                weightValid = True
                price = p[zoneIndex+1]
                break
        if (not weightValid):
            print('Your item is overweight and cannot be sent. Amend fail')
            return
        elif (price <= 0):
            print('Your method or destination is not available. The item cannot be sent. Amend fail.')
            return
        item[1] = method
        item[4] = price
        item[6] = item[4] * item[5]
    else:
        quantity = getInputQuantity()
        item[5] = quantity
        item[6] = item[4] * item[5]
    updateTotalCost()
    print('Amend successful')
    printCart()

# Remove Item
def removeItem():
    printCart()
    global listCart
    if (not listCart):
        return
    print('Please input the no. of the item you want to remove:')
    removeIndex = getInputItemNo()
    confirm = input('Do you want to remove the no.%d item?' % (removeIndex + 1))
    if(confirm == 'yes'):
        item = listCart[removeIndex]
        del(listCart[removeIndex])
        updateTotalCost()
        print('Remove successful')
        printCart()
    else:
        print('Remove cancelled')

# View shopping cart
def printCart():
    global listCart, totalCost
    if(not listCart):
        print('Your shopping cart is empty!')
        return
    i = 1
    for item in listCart:
        print('Here is your shopping cart:')
        print('Item No: %d\tType: %s\tMethod: %s\tDestination: %s\tWeight: %.1fKG\tPrice: $%.2f\tQuantity: %d\tCost: $%.2f' % (
            i,
            dm.listStampType[item[0]],
            dm.listStampMethod[item[0]][item[1]],
            item[2],
            item[3],
            item[4],
            item[5],
            item[6]
        ))
        i += 1
    print('Total Cost: $%.2f' % totalCost)

# Checkout, print invoice and receipt
def checkout():
    printCart()
    global listCart
    if (not listCart):
        return
    # write in the sales_history.csv
    dm.writeSalesRecord(listCart)
    print('Processing...')
    # Create a .txt file with the name of datetime.
    fileName = datetime.now().strftime('%Y-%m-%d %H_%M_%S') + '.txt'
    fileHandle = open(fileName, 'w')
    # print the invoice
    fileHandle.write(getInvoiceContent())
    # print the receipt
    fileHandle.write(getReceiptContent())
    fileHandle.close()
    print('Printing completed.')
    ##After checkout, empty the Cart and empty the total cost.
    listCart = []
    updateTotalCost()
########################
#    Below is the definition of some of the BASIC functions required in this programme.    #
########################

# Get the input 'type'
def getInputType():
    print('Please select the type:')
    i = 1
    for t in dm.listStampType:
        print('%d. %s' % (i, t))
        i += 1
    type = ''
    while True:
        inputValid = False  ##Assume the user input is false
        type = input()       ##Let him input
        try:
            type = int(type)
            if(type > 0 and type <= len(dm.listStampType)):
                inputValid = True
        except:
            # input error
            pass
        if(inputValid):
            break
        else:
            print('Input error, try input again.')
    # return the index so minus 1
    return type - 1

# Get the input method
def getInputMethod(type):
    print('Please select the input method:')
    i = 1
    for m in dm.listStampMethod[type]:
        print('%d. %s' % (i, m))
        i += 1
    method = ''
    while True:
        inputValid = False
        method = input()
        try:
            method = int(method)
            if(method > 0 and method <= len(dm.listStampType[type])):
                inputValid = True
        except:
            # input error
            pass
        if(inputValid):
            break
        else:
            print('input error, please try again.')
    return method - 1

# Get the destination
def getInputCountry():
    print('Please input the destination:')
    country = ''
    while True:
        inputValid = False
        country = input()
        zone = dm.dictCountry.get(country)
        # Cannot fine the destination
        if(zone):
            inputValid = True
        if(inputValid):
            break
        else:
            print('Invalid destination, please input again.')
    return country

# Get the weight
def getInputWeight():
    print('Please input the weight of the item(kg)：')
    weight = ''
    while True:
        inputValid = False
        weight = input()
        try:
            weight = float(weight)
            inputValid = True
        except:
            # Input error
            pass
        if(inputValid):
            break
        else:
            print('Input error, try input again:')
    return weight

# Get the quantity:
def getInputQuantity():
    print('please input the quantity:')
    quantity = ''
    while True:
        inputValid = False
        quantity = input()
        try:
            quantity = int(quantity)
            inputValid = True
        except:
            # input error
            pass
        if(inputValid):
            break
        else:
            print('input error, try input again:')
    return quantity

# Get the input of the item number in the shopping cart.
def getInputItemNo():
    global listCart
    if (not listCart):
        return -1
    itemIndex = ''
    while True:
        inputValid = False
        itemIndex = input()
        try:
            itemIndex = int(itemIndex)
            if(itemIndex > 0 and itemIndex <= len(listCart)):
                inputValid = True
        except:
            # input error
            pass
        if (inputValid):
            return itemIndex - 1  ##return index
        else:
            print('input error please input again.')

# Get the input of the amend item
def getInputAmendOption():
    print('What do you want to amend:\n1. Method\n2. Quantity')
    select = ''
    while True:
        inputValid = False
        select = input()
        try:
            select = int(select)
            if(select == 1 or select == 2):
                inputValid = True
        except:
            # input error
            pass
        if (inputValid):
            break
        else:
            print('Input error try input again.')
    return select

# Find Item in the cart according to type, method, country and weight
def getItem(type, method, country, weight):
    global listCart
    if(not listCart):
        return None
    for item in listCart:
        if(item[0] == type and item[1] == method and item[2] == country and item[3] == weight):
            return item
    return None

# get the invoice content
def getInvoiceContent():
    global listCart, totalCost
    content = ''
    content += '----------------Invoice---------------\n'
    i = 1
    for item in listCart:
        content += 'Item No: %d\tType: %s\tMethod: %s\tDestination: %s\tWeight: %.1fKG\tPrice: $%.2f\tQuantity: %d\tCost: $%.2f\n' % (
            i,
            dm.listStampType[item[0]],
            dm.listStampMethod[item[0]][item[1]],
            item[2],
            item[3],
            item[4],
            item[5],
            item[6]
        )
        i += 1
    content += '\nTotal Cost: $%.2f\n' % totalCost
    content += '--------------End Invoice--------------\n\n'
    return content

# Get Stamp Receipt Content
def getReceiptContent():
    global listCart, totalCost
    content = ''
    content += '\n------------Purchased Stamps------------\n'
    for item in listCart:
        for quantity in range(item[5]):
            content += '\n----------------------------------------\n'
            content += dm.listStampMethod[item[0]][item[1]] + '\n'
            content += 'Destination: %s\t\tWeight: %.2f' % (item[2], item[3])
            content += '\n----------------------------------------\n'
    return content

# Update Total Cost
def updateTotalCost():
    global listCart, totalCost
    totalCost = 0
    if(not listCart):
        return
    for item in listCart:
        totalCost += item[6]
