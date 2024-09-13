from datetime import datetime, timedelta
import re
from prettytable import PrettyTable

from lists.user_list import users
from lists.car_list import cars
from lists.rent_list import rents

usersColumnsHeader = [key for key in users[0].keys()]
carsColumnsHeader = [key for key in cars[0].keys()]
rentsColumnsHeader = [key for key in rents[0].keys()]

from lists.validator_set import countries
from lists.validator_set import car_brands

def readData():
    choiceReadDataFlag = True

    while(bool(choiceReadDataFlag)):
        choiceReadData = dataChooser('get')
        if (choiceReadData == '1'):
            getDataFromList(users, 'users', 'get')
            choiceReadDataFlag = False
        elif (choiceReadData == '2'):
            getDataFromList(cars, 'cars', 'get')
            choiceReadDataFlag = False
        elif (choiceReadData == '3'):
            getDataFromList(rents, 'rents', 'get', True)
            choiceReadDataFlag = False
        elif (choiceReadData == '4'):
            choiceReadDataFlag = False
        else:
            print("Invalid choice")
            retypeOption = input("Do you want to retype? (y or else as no): ")
            if (retypeOption.lower() in ['y', 'yes']):
                continue
            else:
                choiceReadDataFlag = False

def getDataFromList(listData, dataTable, method, isRent = False):
    table = tableHeaderMaker(dataTable, isRent)

    choiceReadDataOptionFlag = True

    while (bool(choiceReadDataOptionFlag)):
        print('\nChoose data:')
        print("1. Whole")
        print("2. Queried")
        print("3. Back")
        choiceReadDataOption = input(f'\nChoose selected {method} data menu (1-3): ')

        if (choiceReadDataOption == '1'):
            if (method == 'get'):
                processedData = listSorter(listData, dataTable)
                dataPrinter(table, dataTable, processedData, isRent)
            choiceReadDataOptionFlag = False
        elif (choiceReadDataOption == '2'):
            conditions = int(input(f'\nInput query conditions: '))
            setsList = []
            logicalConnectorsList = []
            
            for i in (range(conditions)):
                resultSet = filterer(i, listData, dataTable, method)
                setsList.append(set(resultSet))
                
            for i in (range(conditions)):
                if (i == 0):
                    logicalConnectorsList.append('or')
                else:
                    temp = logicalConnector(i)
                    if (temp != ''):
                        logicalConnectorsList.append(temp)
            
            if (len(logicalConnectorsList) < len(setsList)):
                print("Invalid querying")
                readData()

            setResult = set()
            for i in (range(len(logicalConnectorsList))):
                if (logicalConnectorsList[i] == 'and'):
                    temp = setResult.intersection(setsList[i])
                    setResult = temp
                elif (logicalConnectorsList[i] == 'or'):
                    temp = setResult.union(setsList[i])
                    setResult = temp
                    
            setResultToList = list(setResult)
            if (len(setResultToList) == 0):
                print("\nNo Data Found")
                choiceReadDataOptionFlag = False
            else:
                if (method == 'get'):
                    retrievedDataList = []
                    indexer = getValueFromCheckingTableName(dataTable, 'indexer')

                    for i in range(len(setResultToList)):
                        for j in range(len(listData)):
                            if (setResultToList[i] == listData[j][indexer]):
                                retrievedDataList.append(listData[j])
                    processedData = listSorter(retrievedDataList, dataTable)
                    dataPrinter(table, dataTable, processedData, isRent)
                choiceReadDataOptionFlag = False
        elif (choiceReadDataOption == '3'):
            choiceReadDataOptionFlag = False
            readData()
        else:
            print("Invalid choice")
            retypeOption = input("Do you want to retype? (y or else as no): ")
            if (retypeOption.lower() in ['y', 'yes']):
                continue
            else:
                choiceReadDataOptionFlag = False

def tableHeaderMaker(dataTable, isRent = False):
    columnHeader = getValueFromCheckingTableName(dataTable, 'column_header')

    columnNameList = ['no.']
    columnNameList.extend(columnHeader)
    if (bool(isRent)):
        columnNameList.extend(['user.user_id', 'user.name', 'user.legal_id_no', 'car.car_id', 'car.brand', 'car.type', 'car.no_plate'])
    table = PrettyTable(columnNameList)

    return table

def filterer(i, listData, dataTable, method):
    print(f'\nCondition No. {i + 1}')
    stringJoin = ' / '
    filterKeyFlag = True
    resultSet = []

    columnHeader = getValueFromCheckingTableName(dataTable, 'column_header')

    while (bool(filterKeyFlag)):
        filterKey = input(f'\nChoose selected {method} data option ({stringJoin.join(columnHeader)}): ')
        if filterKey in columnHeader:
            if (method == 'get'):
                filterValue = inputValue(filterKey, 'get')
            
            if (filterValue != ''):
                signList = ['is_equal', 'is_not_equal', 'is_greater_than', 'is_greater_than_or_equal', 'is_lower_than', 'is_lower_than_or_equal', 'like_first', 'like_last', 'like_middle']
                signFlag = True

                while(bool(signFlag)):
                    sign = input(f'\nChoose comparator sign {stringJoin.join(signList)}: ').lower()

                    if (sign not in signList):
                        print("Invalid choice")
                        retypeOption = input("Do you want to retype? (y or else as no): ")
                        if (retypeOption.lower() in ['y', 'yes']):
                            continue
                        else:
                            signFlag = False
                    else:
                        if (filterKey in ['user_id', 'car_id', 'rent_id', 'daily_fee', 'fee', 'date_of_birth', 'rent_date', 'return_date']):
                            if (sign in ['like_first', 'like_last', 'like_middle']):
                                print("Invalid choice")
                                retypeOption = input("Do you want to retype? (y or else as no): ")
                                if (retypeOption.lower() in ['y', 'yes']):
                                    continue
                                else:
                                    signFlag = False
                            else:
                                resultSet = dataChecker(listData, dataTable, filterKey, filterValue, sign)
                                signFlag = False
                        elif (filterKey in ['isWatchlisted', 'isBlacklisted', 'isAvailable', 'isDamaged', 'isReturned', 'isDamagedAfterUsage']):
                            if (sign not in ['is_equal', 'is_not_equal']):
                                print("Invalid choice")
                                retypeOption = input("Do you want to retype? (y or else as no): ")
                                if (retypeOption.lower() in ['y', 'yes']):
                                    continue
                                else:
                                    signFlag = False
                            else:
                                resultSet = dataChecker(listData, dataTable, filterKey, filterValue, sign)
                                signFlag = False
                        else:
                            if (sign in ['is_greater_than', 'is_greater_than_or_equal', 'is_lower_than', 'is_lower_than_or_equal']):
                                print("Invalid choice")
                                retypeOption = input("Do you want to retype? (y or else as no): ")
                                if (retypeOption.lower() in ['y', 'yes']):
                                    continue
                                else:
                                    signFlag = False
                            else:
                                resultSet = dataChecker(listData, dataTable, filterKey, filterValue, sign)
                                signFlag = False
                    filterKeyFlag = False
            else:
                filterKeyFlag = False
        
        else:
            print("Invalid choice")
            retypeOption = input("Do you want to retype? (y or else as no): ")
            if (retypeOption.lower() in ['y', 'yes']):
                continue
            else:
                filterKeyFlag = False
    
    return resultSet

def inputValue(inputKey, method):
    inputValue = ''
    if (inputKey in ['user_id', 'car_id', 'rent_id', 'daily_fee', 'fee', 'legal_id_no', 'data_amount', 'rental_days']):
        flag = True
        while (bool(flag)):
            inputValue = input(f'\nChoose selected {method} data value for {inputKey}: ')
            if (bool(inputValue.isdigit())):
                if (inputKey in ['user_id', 'car_id', 'rent_id', 'daily_fee', 'fee', 'data_amount', 'rental_days']):
                    inputValue = int(inputValue)
                flag = False
            else:
                print("Invalid input")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    inputValue = ''
                    flag = False
    elif (inputKey in ['date_of_birth', 'rent_date', 'return_date']):
        flag = True
        while (bool(flag)):
            strShown = f'\nChoose selected {method} data value for {inputKey} (YYYY-MM-DD)'
            if (inputKey == 'rent_date' and method == 'post'):
                strShown += ' [for rent date: empty input = now]: '
            else:
                strShown += ': '
            inputValue = input(strShown)
            if (bool(validDate(inputValue))):
                flag = False
            else:
                if (inputKey == 'rent_date' and method == 'post'):
                    dateNow = datetime.now()
                    inputValue = dateNow.strftime('%Y-%m-%d')
                    flag = False
                else:
                    print("Invalid input")
                    retypeOption = input("Do you want to retype? (y or else as no): ")
                    if (retypeOption.lower() in ['y', 'yes']):
                        continue
                    else:
                        inputValue = ''
                        flag = False
    elif (inputKey in ['isWatchlisted', 'isBlacklisted', 'isAvailable', 'isDamaged', 'isReturned', 'isDamagedAfterUsage']):
        inputValue = input(f'\nChoose selected {method} data value for {inputKey} (y or else as no): ')
        if (inputValue.lower() in ['y', 'yes']):
            inputValue = True
        else:
            inputValue = False
    elif (inputKey == 'gender'):
        flag = True
        while (bool(flag)):
            inputValue = input(f'\nChoose selected {method} data value for {inputKey} (M/F): ').upper()
            if (inputValue in ['M', 'F']):
                inputValue = inputValue.upper()
                flag = False
            else:
                print("Invalid input")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    inputValue = ''
                    flag = False
    elif (inputKey in ['domicile_country', 'nationality_country']):
        flag = True
        while (bool(flag)):
            tempList = input(f'\nChoose selected {method} data value for {inputKey}: ').split(' ')
            for i in range(len(tempList)):
                tempList[i] = tempList[i].capitalize()
            inputValue = ' '.join(tempList)
            if (inputValue in countries):
                flag = False
            else:
                print("Invalid input")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    inputValue = ''
                    flag = False
    elif (inputKey in ['phone_number']):
        flag = True
        while (bool(flag)):
            inputValue = input(f'\nChoose selected {method} data value for {inputKey} (with country code): ')
            if (inputValue[0] == '+' and bool(inputValue[1:len(inputValue)].isdigit())):
                flag = False
            else:
                print("Invalid input")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    inputValue = ''
                    flag = False
    elif (inputKey in ['email']):
        flag = True
        while (bool(flag)):
            inputValue = input(f'\nChoose selected {method} data value for {inputKey}: ')
            if (bool('@' in inputValue)):
                flag = False
            else:
                print("Invalid input")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    inputValue = ''
                    flag = False
    elif (inputKey in ['no_plate']):
        flag = True
        while (bool(flag)):
            inputValue = input(f'\nChoose selected {method} data value for {inputKey}: ')
            splitNoPlate = inputValue.split(' ')
            if (len(splitNoPlate) == 3):
                flag = False
            else:
                print("Invalid input")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    inputValue = ''
                    flag = False
    elif (inputKey in ['brand']):
        flag = True
        while (bool(flag)):
            tempList = input(f'\nChoose selected {method} data value for {inputKey}: ').split(' ')
            for i in range(len(tempList)):
                tempList[i] = tempList[i].capitalize()
            inputValue = ' '.join(tempList)
            if (inputValue in car_brands):
                flag = False
            else:
                print("Invalid input")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    inputValue = ''
                    flag = False
    else:
        tempList = input(f'\nChoose selected {method} data value for {inputKey}: ').split(' ')
        for i in range(len(tempList)):
            tempList[i] = tempList[i].capitalize()
        inputValue = ' '.join(tempList)
    return inputValue

def validDate(datestring):
    try:
        datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except (ValueError):
        return False

def dataChecker(listData, dataTable, filterKey, filterValue, sign):
    listData = listSorter(listData, dataTable)
    filteredDataSet = set()
    for i in range(len(listData)):
        birthdate = listData[i][filterKey]
        if (filterKey in ['date_of_birth', 'rent_date', 'return_date']):
            comparationResult = comparationFunction(sign, datetime.strptime(birthdate, '%Y-%m-%d'), datetime.strptime(filterValue, '%Y-%m-%d'))
        elif (filterKey not in ['date_of_birth', 'rent_date', 'return_date'] and (bool(isinstance(filterValue, str)) and filterValue != '')):
            comparationResult = comparationFunction(sign, listData[i][filterKey].lower(), filterValue.lower())
        elif (filterValue != ''):
            comparationResult = comparationFunction(sign, listData[i][filterKey], filterValue)
        if (bool(comparationResult)):
            if (dataTable == 'users'):
                filteredDataSet.add(listData[i]['user_id'])
            elif (dataTable == 'cars'):
                filteredDataSet.add(listData[i]['car_id'])
            elif (dataTable == 'rents'):
                filteredDataSet.add(listData[i]['rent_id'])
    return filteredDataSet

def getValueFromCheckingTableName(dataTable, valueNeeded):
    if (valueNeeded == 'indexer'):
        indexer = ''
        if (dataTable == 'users'):
            indexer = 'user_id'
        elif (dataTable == 'cars'):
            indexer = 'car_id'
        elif (dataTable == 'rents'):
            indexer = 'rent_id'
        return indexer
    elif (valueNeeded == 'column_header'):
        columnHeader = []
        if (dataTable == 'users'):
            columnHeader = usersColumnsHeader
        elif (dataTable == 'cars'):
            columnHeader = carsColumnsHeader
        elif (dataTable == 'rents'):
            columnHeader = rentsColumnsHeader
        return columnHeader


def comparationFunction(functionString, a, b):
    if (functionString == 'is_equal'):
        return isEqual(a, b)
    elif (functionString == 'is_not_equal'):
        return isNotEqual(a, b)
    elif (functionString == 'is_greater_than'):
        return isGreaterThan(a, b)
    elif (functionString == 'is_greater_than_or_equal'):
        return isGreaterThanOrEqual(a, b)
    elif (functionString == 'is_lower_than'):
        return isLowerThan(a, b)
    elif (functionString == 'is_lower_than_or_equal'):
        return isLowerThanOrEqual(a, b)
    elif (functionString == 'like_first'):
        return likeFirst(a, b)
    elif (functionString == 'like_last'):
        return likeLast(a, b)
    elif (functionString == 'like_middle'):
        return likeMiddle(a, b)

def isEqual(a, b):
    if (a == b):
        return True
    else:
        return False
    
def isNotEqual(a, b):
    if (a != b):
        return True
    else:
        return False
    
def isGreaterThan(a, b):
    if (a > b):
        return True
    else:
        return False
    
def isGreaterThanOrEqual(a, b):
    if (a >= b):
        return True
    else:
        return False
    
def isLowerThan(a, b):
    if (a < b):
        return True
    else:
        return False
    
def isLowerThanOrEqual(a, b):
    if (a <= b):
        return True
    else:
        return False

def likeFirst(a, b):
    listRegexSearch = re.search(f'^{b}', a)
    if (listRegexSearch):
        return True
    else:
        return False

def likeLast(a, b):
    listRegexSearch = re.search(f'{b}$', a)
    if (listRegexSearch):
        return True
    else:
        return False
    
def likeMiddle(a, b):
    listRegexSearch = re.search(f'{b}', a)
    if (listRegexSearch):
        return True
    else:
        return False

def logicalConnector(i):
    if (i == 0):
        return 'or'
    else:
        print(f"Logical Connector No. {i}")
        validator = True
        result = ''            
        while(bool(validator)):
            logicalConnector = input("\nInput logical connector? (and / or): ")
            if (logicalConnector in ['and', 'or']):
                result = logicalConnector
                validator = False
            else:
                print("Invalid choice")
                retypeOption = input("Do you want to retype? (y or else as no): ")
                if (retypeOption.lower() in ['y', 'yes']):
                    continue
                else:
                    validator = False
        return result
    
def listSorter(listData, dataTable):
    if (len(listData) == 0):
        return []
    else:
        sortedList = listData
        temp = listData[0]
        indexer = getValueFromCheckingTableName(dataTable, 'indexer')
        for i in range(len(sortedList)):
            for j in range(len(sortedList)):
                if sortedList[i][indexer] < sortedList[j][indexer]:
                    temp = sortedList[i]
                    sortedList[i] = sortedList[j]
                    sortedList[j] = temp
        return sortedList
    
def dataPrinter(table, dataTable, listData, isRent):
    tableRowNumber = 1
    listData = listSorter(listData, dataTable)
    for i in range(len(listData)):
        if (bool(isRent)):
            tableAppend(listData, table, i, tableRowNumber, True)
            tableRowNumber += 1
        else:
            tableAppend(listData, table, i, tableRowNumber)
            tableRowNumber += 1
    print('\nData List:')
    print(table)
    
def tableAppend(listData, table, i, tableRowNumber, isRent = False):
    rowValuesList = [tableRowNumber]
    rowValuesList.extend([value for value in listData[i].values()])
    if (bool(isRent)):
        userIndex = 0
        for j in range(len(users)):
            if (users[j]['user_id'] == listData[i]['user_id']):
                userIndex = j
        carIndex = 0
        for j in range(len(cars)):
            if (cars[j]['car_id'] == listData[i]['car_id']):
                carIndex = j
        rowValuesList.extend([users[userIndex]['user_id'], users[userIndex]['name'], users[userIndex]['legal_id_no'], cars[carIndex]['car_id'], cars[carIndex]['brand'], cars[carIndex]['type'], cars[carIndex]['no_plate']])
    table.add_row(rowValuesList)

def createData():
    choiceCreateDataFlag = True

    while(bool(choiceCreateDataFlag)):
        choiceCreateData = dataChooser('post')
        if (choiceCreateData == '1'):
            insertData(users, 'users')
            choiceCreateDataFlag = False
        elif (choiceCreateData == '2'):
            insertData(cars, 'cars')
            choiceCreateDataFlag = False
        elif (choiceCreateData == '3'):
            insertData(rents, 'rents', True)
            choiceCreateDataFlag = False
        elif (choiceCreateData == '4'):
            choiceCreateDataFlag = False
        else:
            print("Invalid choice")
            retypeOption = input("Do you want to retype? (y or else as no): ")
            if (retypeOption.lower() in ['y', 'yes']):
                continue
            else:
                choiceCreateDataFlag = False

def insertData(listData, dataTable, isRent = False):
    columnHeader = getValueFromCheckingTableName(dataTable, 'column_header')
    indexer = getValueFromCheckingTableName(dataTable, 'indexer')

    uniqueValuesList = []
    idsList = []
    userIdsList = []
    carIdsList = []
    if (dataTable == 'users'):
        for i in range(len(listData)):
            uniqueValuesList.append(listData[i]['legal_id_no'])
            idsList.append(listData[i][indexer])
    elif (dataTable == 'cars'):
        for i in range(len(listData)):
            uniqueValuesList.append(listData[i]['no_plate'])
            idsList.append(listData[i][indexer])
    elif (dataTable == 'rents'):
        for i in range(len(listData)):
            idsList.append(listData[i][indexer])
        for i in range(len(users)):
            userIdsList.append(users[i]['user_id'])
        for i in range(len(cars)):
            carIdsList.append(cars[i]['car_id'])

    
    missingIdsList = []
    for i in range(max(idsList)):
        availabiliyFlag = False
        for j in range(len(listData)):
            if ((i + 1) == listData[j][indexer]):
                availabiliyFlag = True
        if (availabiliyFlag == False):
            missingIdsList.append((i + 1))

    dataAmount = inputValue('data_amount', 'post')
    validatedInsertedDataCount = 0
    savedDataForShown = []
    for i in range(dataAmount):
        print(f'\nInsert new data no. {i + 1}')
        inputUniqueValue = ''
        inputUserId = ''
        inputCarId = ''
        if (dataTable in ['users', 'cars']):
            flagUniqueValueChecker = True
            while (bool(flagUniqueValueChecker)):
                if (dataTable in ['users']):
                    inputUniqueValue = inputValue('legal_id_no', 'post')
                elif (dataTable in ['cars']):
                    inputUniqueValue = inputValue('no_plate', 'post')
                
                if (inputUniqueValue not in uniqueValuesList):
                    flagUniqueValueChecker = False
                else:
                    print("Data already exists")
                    retypeOption = input("Do you want to retype? (y or else as no): ")
                    if (retypeOption.lower() in ['y', 'yes']):
                        continue
                    else:
                        inputUniqueValue = ''
                        flagUniqueValueChecker = False
        elif (dataTable in ['rents']):
            flagUserIdChecker = True
            while (bool(flagUserIdChecker)):
                inputUserId = inputValue('user_id', 'post')
                if (inputUserId in userIdsList):
                    if (bool(users[userIdsList.index(inputUserId)]['isBlacklisted']) == False and bool(users[userIdsList.index(inputUserId)]['isAvailable']) == True):
                        flagUserIdChecker = False
                    else:
                        print("Data can not be submitted: user is blacklisted")
                        retypeOption = input("Do you want to retype? (y or else as no): ")
                        if (retypeOption.lower() in ['y', 'yes']):
                            continue
                        else:
                            inputUserId = ''
                            flagUserIdChecker = False
                else:
                    print("No Data Found")
                    retypeOption = input("Do you want to retype? (y or else as no): ")
                    if (retypeOption.lower() in ['y', 'yes']):
                        continue
                    else:
                        inputUserId = ''
                        flagUserIdChecker = False
            flagCarIdChecker = True
            while (bool(flagCarIdChecker)):
                inputCarId = inputValue('car_id', 'post')
                if (inputCarId in carIdsList):
                    if (bool(cars[carIdsList.index(inputCarId)]['isAvailable'])):
                        flagCarIdChecker = False
                    else:
                        print("Data can not be submitted: user is not available")
                        retypeOption = input("Do you want to retype? (y or else as no): ")
                        if (retypeOption.lower() in ['y', 'yes']):
                            continue
                        else:
                            inputCarId = ''
                            flagCarIdChecker = False
                else:
                    print("No Data Found")
                    retypeOption = input("Do you want to retype? (y or else as no): ")
                    if (retypeOption.lower() in ['y', 'yes']):
                        continue
                    else:
                        inputCarId = ''
                        flagCarIdChecker = False
        
        if (inputUniqueValue != '' or (inputUserId != '' and inputCarId != '')):
            newData = {}
            rentalDays = ''
            for key in columnHeader:
                if (key in ['user_id', 'car_id', 'rent_id']):
                    if (dataTable == 'rents'):
                        if (key in ['rent_id']):
                            newData[key] = newDataIdPicker(validatedInsertedDataCount, missingIdsList, idsList)
                        elif (key in ['user_id']):
                            newData[key] = inputUserId
                        elif (key in ['car_id']):
                            newData[key] = inputCarId
                    else:
                        newData[key] = newDataIdPicker(validatedInsertedDataCount, missingIdsList, idsList)
                elif (key in ['legal_id_no', 'no_plate']):
                    newData[key] = inputUniqueValue
                elif (key in ['isWatchlisted', 'isBlacklisted', 'isDamaged', 'isReturned', 'isDamagedAfterUsage']):
                    newData[key] = False
                elif (key in ['isAvailable']):
                    newData[key] = True
                elif (key in ['fee']):
                    rentalDays = inputValue('rental_days', 'post')
                    if (rentalDays != ''):
                        if (bool(users[userIdsList.index(inputUserId)]['isWatchlisted'])):
                            newData[key] = 1.25 * rentalDays * cars[carIdsList.index(inputCarId)]['daily_fee']
                        else:
                            newData[key] = rentalDays * cars[carIdsList.index(inputCarId)]['daily_fee']
                    else:
                        newData[key] = ''
                elif (key in ['return_date']):
                    if (rentalDays != ''):
                        striptimeReturnDate = datetime.strptime(newData['rent_date'], '%Y-%m-%d') + timedelta(days = rentalDays)
                        newData[key] = striptimeReturnDate.strftime('%Y-%m-%d')
                    else:
                        newData[key] = ''
                else:
                    newData[key] = inputValue(key, 'post')
            if ('' not in newData.values()):
                saveDataOption = input("Do you want to save the data? (y or else as no): ")
                if (saveDataOption.lower() in ['y', 'yes']):
                    savedDataForShown.append(newData)
                    listData.append(newData)
                    validatedInsertedDataCount += 1
                else:
                    print('\nData is decided to be not submitted')
            else:
                print('\nData is not submitted')
        else:
            print('\nData is not submitted')

    if (len(savedDataForShown) == 0):
        print('\nNo Data Saved')
    else:
        table = tableHeaderMaker(dataTable, isRent)
        dataPrinter(table, dataTable, savedDataForShown, isRent)

def newDataIdPicker(validatedInsertedDataCount, missingIdsList, idsList):
    if (validatedInsertedDataCount < len(missingIdsList)):
        return missingIdsList[validatedInsertedDataCount]
    else:
        return max(idsList) + validatedInsertedDataCount + 1


def dataChooser(method):
    print('\nChoose data:')
    print("1. Users")
    print("2. Cars")
    print("3. Rents")
    print("4. Back")
    choice = input(f'\nChoose selected {method} data menu (1-4): ')
    return choice

def menuDisplay():
    print('\nMenu List')
    print("1. Get Data")
    print("2. Post Data")
    print("3. Put Data")
    print("4. Delete Data")
    print("5. Exit")

def main():
    while True:
        menuDisplay()
        choice = input('\nChoose selected menu (1-5): ')
        if (choice == '1'):
            readData()
        if (choice == '2'):
            createData()
        elif (choice == '5'):
            print('\nProgram has been stopped')
            break

if __name__ == '__main__':
    main()