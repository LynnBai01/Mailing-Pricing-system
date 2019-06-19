# -*-coding:utf-8-*-

from datetime import datetime
import pandas

# Define the Constant
# data file path
DATA_FILE_PATH = './ass2_data'
# type
listStampType = ['letter', 'parcel']
# method
listStampMethod = [['Economy Letter', 'Express Letter'],
                   ['Economy Parcel By Air', 'Economy Parcel By Sea', 'Standard Parcel', 'Express Parcel']]


# global varialble
# dictionary of countries and zone
dictCountry = {}
# list of the zones
listZone = []
# price dictionary
dictPrice = {}
# sales history
listSalesHistory = []


# Import data
def importData():
    importCountryZoneData(DATA_FILE_PATH + '/Countries and Zones.csv')
    importEconomyLetterPriceData(DATA_FILE_PATH + '/Economy Letters Price Guide ($).csv')
    importPriceData(listStampMethod[0][1], DATA_FILE_PATH + '/Express Letter Price Guide ($).csv')
    importPriceData(listStampMethod[1][0], DATA_FILE_PATH + '/Economy Parcel Price Guide_by Air ($).csv')
    importPriceData(listStampMethod[1][1], DATA_FILE_PATH + '/Economy Parcel Price Guide_by Sea ($).csv')
    importPriceData(listStampMethod[1][2], DATA_FILE_PATH + '/Standard Parcel Price Guide ($).csv')
    importPriceData(listStampMethod[1][3], DATA_FILE_PATH + '/Express Parcel Price Guide ($).csv')

# import the countries and zone data
def importCountryZoneData(fileName):
    global dictCountry, listZone
    dictCountry = {}
    colNames, datas = loadCsv(fileName)
    for data in datas:
        zone = data[1]
        dictCountry[data[0]] = zone ##write zone into dictionary.
        if(zone not in listZone):
            listZone.append(zone)
    listZone.sort()

# Import the economy letter price Data
def importEconomyLetterPriceData(fileName):
    global dictPrice
    dictPrice[listStampMethod[0][0]] = []
    colNames, datas = loadCsv(fileName)
    for data in datas:
        li = [0 for x in range(0, 10)]
        li[0] = (getWeightUpper(data[0]))
        # the first column is zone 1
        li[1] = float(data[1])
        # the second column is zone 2, 3, 5
        for i in [2, 3, 5]:
            li[i] = float(data[2])
        # the third column is zone 4,6,7,9
        for i in [4, 6, 7, 9]:
            li[i] = float(data[3])
        dictPrice[listStampMethod[0][0]].append(li)

# Import Price Data
def importPriceData(method, fileName): ##type: which method?
    global dictPrice
    dictPrice[method] = []  ##first layer
    colNames, datas = loadCsv(fileName)
    for data in datas:
        li = [0 for x in range(0, 10)]   ##0*10
        li[0] = (getWeightUpper(data[0]))
        for i in range(1, 10):
            try:
                li[i] = float(data[i])
            except:
                # Invalid data format, ignore the data.
                pass
        dictPrice[method].append(li)

# load CSV foundation function.
def loadCsv(fileName):
    data = pandas.read_csv(fileName)
    li = []
    for i in data.index:
        li.append(data.loc[i].values.tolist())
    liKey = data.columns.values.tolist()
    return liKey, li

# load Sales history
def loadSalesHistory():
    fileName = DATA_FILE_PATH + '/sales_history.csv'
    return loadCsv(fileName)

# Write in the sales history
def writeSalesRecord(items):
    global listStampType, listStampMethod
    if(not items):
        return
    colNames, salesRecords = loadSalesHistory()
    lastSalesId = 0
    if(salesRecords):
        lastSalesId = int(salesRecords[-1][0])
    # assemble the item with salesId and timeStr
    salesId = lastSalesId + 1
    timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csvFile = open(DATA_FILE_PATH + '/sales_history.csv', "a")
    for item in items:
        csvFile.write('\n%d,%s,%s,%.2f,%s,%s,%d,%.2f' % (
            salesId,
            timeStr,
            listStampType[item[0]],
            item[3],
            item[2],
            listStampMethod[item[0]][item[1]],
            item[5],
            item[6]
        ))

# Deal with the string 'weight'.（kg）extract the last element of the string'up to xxxkg'
def getWeightUpper(str):
    strs = str.split(' ')
    weightStr = strs[-1]
    if('kg' in weightStr):
        return float(weightStr.replace('kg', '')) ##remove kg and turn this into float
    elif('g' in weightStr):
        return float(weightStr.replace('g', ''))/1000
    else:
        return 0
