# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
import numpy as np
import data_manager as dm

# Global variable
listSalesRecord = []

# admin main menu
def main():
    global listSalesRecord
    # loading the sales history
    colNames, listSalesRecord = dm.loadSalesHistory()
    if(not listSalesRecord):
        print('no sales history available')
        return
    select = ''
    while True:
        select = getMenuInput()
        if(select == '1'):
            showSalesAmountYear()
        elif(select == '2'):
            showSalesItemCountHour()
        elif(select == '3'):
            showSalesNumMethod()
        elif(select == '4'):
            showSalesNumDestination()
        elif(select == '5'):
            break
        else:
            print('Invalid input, please input again.')

# print the main menu
def getMenuInput():
    return input('''
    Please select the following：
    1. Show the gross sales amount of different years.
    2. Show the customer flow during a day.
    3. Show the popularity of postate method for letter and parcel.
    4. Show the top 5 most popular destination countries including any postage.
    5. Quit
    ''')

# Show the gross sales amount of different year.
def showSalesAmountYear():
    global listSalesRecord
    # list of years
    listYear = []
    # dictionary of gross sales amount:
    dictAmount = {}
    for salesRecord in listSalesRecord:
        timeStr = salesRecord[1]
        year = (int)(timeStr.split('-')[0])
        if(year not in listYear):
            listYear.append(year)
            dictAmount[year] = 0
        dictAmount[year] += float(salesRecord[7])
    listYear.sort()
    listAmount = []
    for year in listYear:
        listAmount.append(dictAmount[year])
    plt.xticks(np.arange(listYear[0], listYear[-1] + 1, 1))
    plt.bar(listYear, listAmount)
    # show the gross sales amount on the relative year's bar in the bar charts
    for a, b in zip(listYear, listAmount):
        plt.text(a, b + 0.05, '%.2f' % b, ha='center', va='bottom', fontsize=11)
    plt.show()

# Show the customer flow during a day(in different hours).
def showSalesItemCountHour():
    global listSalesRecord
    # saleId list
    listSaleId = []
    # hour list
    listHour = range(0, 24)
    # sales item amount per hout:
    listItemCount = [0] * len(listHour)
    for salesRecord in listSalesRecord:
        saleId = salesRecord[0]
        if(saleId in listSaleId):
            continue
        else:
            listSaleId.append(saleId)
        timeStr = salesRecord[1]
        hour = (int)(timeStr.split(' ')[1].split(':')[0])
        listItemCount[hour] += 1
    plt.xticks(np.arange(listHour[0], listHour[-1] + 1, 1))
    plt.bar(listHour, listItemCount)
    # show the gross sales item number on each hour's bar in the bar chart.
    for a, b in zip(listHour, listItemCount):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
    plt.show()

# Show the popularity of postage method for letter and parcel.
def showSalesNumMethod():
    global listSalesRecord
    # list of method
    listMethod = []
    # dictionary of gross sales quantity with different method
    dictNum = {}
    for salesRecord in listSalesRecord:
        method = salesRecord[5]
        if (method not in listMethod):
            listMethod.append(method)
            dictNum[method] = 0
        dictNum[method] += float(salesRecord[6])
    listNum = []
    for method in listMethod:
        listNum.append(dictNum[method])
    plt.xticks(np.arange(0, len(listMethod) + 1, 1), listMethod)
    plt.bar(listMethod, listNum)
    # show the figure in the bar chart
    for a, b in zip(listMethod, listNum):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
    plt.show()

# Show the top 5 most popular destination countries including any postage.
def showSalesNumDestination():
    global listSalesRecord
    # the dictionary of gross sales quantity of different destination.
    dictNum = {}
    for salesRecord in listSalesRecord:
        destination = salesRecord[4]
        if(not dictNum.get(destination)):
            dictNum[destination] = salesRecord[6]
        else:
            dictNum[destination] += salesRecord[6]
    # sorted the dictionary, the dictNum.items() is turning the dict into tuples. key=lambda item:item[1]
    # means that the sorting is based on the second value of each tuples. reverse=True means it is descending order)
    # After sorting, we get a list of tuples.
    listItems = sorted(dictNum.items(), key=lambda item:item[1], reverse=True)
    # list of Destinations.
    listDestination = []
    # list of gross sales quantity.
    listNum = []
    count = 1
    for amount in listItems:
        if(count > 5): ###If we already have the top 5 popular destination countries.
            break
        listDestination.append(amount[0])
        listNum.append(amount[1])
        count += 1
    plt.xticks(np.arange(0, len(listDestination) + 1, 1), listDestination)
    plt.bar(listDestination, listNum)
    # show the figure in the bar chart.
    for a, b in zip(listDestination, listNum):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
    plt.show()

