
def calculatePercentError(yData, yPredictions, verbose=0, checkTitle=""):
    j = 0
    sumOfPercentError = 0
    listOfDifferences = []
    listOfPercentErrors = []
    listOfBadPredictions = []

    if verbose == 1:
        print("====================================== " + checkTitle + " CHECK ======================================")
        print("\r\nACTUAL\t\t====>\t\tPREDICTION\t\t====>\t\tPERCENT ERROR")
        print("========================================================================================")

    for y in yData:
        yHat = yPredictions[j]

        # Preventing divide by zero errors
        if y < 0.0001:
            y = 0.0001
        
        if yHat < 0.0001:
            yHat = 0.0001
        difference = abs(yHat - y)
        percentError = abs(difference / y) * 100.0
        if verbose == 1:
            print("%.2f\t\t====>\t\t%.2f\t\t\t====>\t\t%.2f %%" % (y, yHat, percentError))

        sumOfPercentError += percentError
        listOfDifferences.append(difference)
        listOfPercentErrors.append(percentError)
        j += 1

        # if percentError > 5.5:
        #     listOfBadPredictions.append({
        #         'radioName': radioName
        #     })


    averagePercentError = sumOfPercentError / j
    maximumPercentError = max(listOfPercentErrors)
    minimumPercentError = min(listOfPercentErrors)
    maximumDifference = max(listOfDifferences)
    if verbose == 1:
        print("\r\nAVERAGE PERCENT ERROR:", averagePercentError)
        print("\r\nMAX PERCENT ERROR:", maximumPercentError)
        print("\r\nMIN PERCENT ERROR:", minimumPercentError)
        print("\r\nMAX DIFFERENCE:", maximumDifference)
        print("\r\n\r\n")

    return averagePercentError, maximumPercentError, minimumPercentError, maximumDifference
