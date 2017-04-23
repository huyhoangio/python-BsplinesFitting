import csv
import numpy as np

def main():
    B4 = generate4thorderbases()
    measuredData = {}
    with open('dataset2.csv', mode='r') as file:
        reader = csv.reader(file)
        for rows in reader:
            measuredData[int(float(rows[0])*100)+200] = float(rows[1])
    #print(measuredData)

    # GROWING phase
    step = 0.001
    bestBases = B4
    fittedCurve = [0 for i in range(len(B4[0]))]  #Init fitted curve is a horizontal line of 0
    minError = calculateError(measuredData, fittedCurve)
    ampedB4 = [[0.0 for x in range(len(B4[0]))] for y in range(len(B4))]
    ampArray = [0.0 for i in range(len(B4))]
    rowLength = len(B4[0])
    for row in range(len(B4)):
        print "current basis: ", row + 1

        minError = sum(measuredData.values())
        for amplitude in np.arange(0.0, 1.2, step):
            for i in range(rowLength):
                ampedB4[row][i] = B4[row][i]*amplitude
            #fittedCurve = [sum(row[i] for row in ampedB4) for i in range(rowLength)]

            newError = calculateError(measuredData, ampedB4[row])
            if newError < minError:
                minError = newError
                ampArray[row] = amplitude
    # bestBases = [[B4[y][x] * ampArray[y] for x in range(len(B4[0]))] for y in range(len(B4))]
    # fittedCurve = [sum(row[i] for row in bestBases) for i in range(len(bestBases[0]))]
    # bestBases.append(fittedCurve)

    # SHRINKING phase
    newError = minError - step
    while newError < minError:
        minError = newError

        for i in range(2, len(ampArray)):
            ampArray[i] = ampArray[i] - step
        for i in range(len(ampArray)):
            if ampArray[i] < 0:
                ampArray[i] = 0
        bestBases = [[B4[y][x] * ampArray[y] for x in range(len(B4[0]))] for y in range(len(B4))]
        fittedCurve = [sum(row[i] for row in bestBases) for i in range(len(bestBases[0]))]
        newError = calculateError(measuredData, fittedCurve)
    print "minErr ", minError
    bestBases.append(fittedCurve)

    exportToFile(measuredData, bestBases)

    return

def findBoundaries(dataset, B4matrix, inputUpper, inputLower, inStep):
    # To return lower and upper boundary to speed up convergence
    outUpper = inputUpper
    outLower = inputLower

    for i in range(0, len(B4matrix)):
        currentBspline = B4matrix[i]

        for j in np.arange(inputLower[i], inputUpper[i], inStep):
            ampedCurrentBspline = [j*x for x in currentBspline]
            if checkIfLarger(dataset, ampedCurrentBspline):
                outUpper[i] = j
                outLower[i] = j - 2*inStep
                break
    outStep = inStep/5.0
    return outUpper, outLower, outStep

def checkIfLarger(dataset, ampedBspline):
    #larger = False
    startTimeForMeasuredData = min(dataset.iterkeys())
    endTimeForMeasuredData = max(dataset.iterkeys())
    for i in range(len(ampedBspline)):
        if ampedBspline[i] == 0 or (i > startTimeForMeasuredData and i < endTimeForMeasuredData and i not in dataset):
            continue
        else:
            if i <= startTimeForMeasuredData:
                pointToCompare = dataset.get(startTimeForMeasuredData)
            elif i >= endTimeForMeasuredData:
                pointToCompare = dataset.get(endTimeForMeasuredData)
            else:
                pointToCompare = dataset.get(i)

            if pointToCompare - ampedBspline[i] <= 0:
                return True
    return False

def calculateError(dataDict, fittedValue):
    error = 0
    for key in dataDict:
        error = error + abs(dataDict.get(key) - fittedValue[key])
    return error

def generate4thorderbases():
    maxRow, maxCol = 16, 1600

    # Time points
    T = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    # Populate B1 with impulse of amplitude 1
    B1 = [[0 for x in range(maxCol)] for y in range(maxRow)]
    for i in range(0, maxRow):
        for j in range(0, maxCol):
           if j/100 == i:
               B1[i][j] = 1

    # Create fake continous timescale
    time = [0 for i in range(0, maxCol)]
    start = 0.00
    for i in range(0, maxCol):
        time[i] = start
        start += 0.01

    B2 = generatenextorderbasis(B1, 2, time, T, 15, maxCol)
    B3 = generatenextorderbasis(B2, 3, time, T, 14, maxCol)
    B4 = generatenextorderbasis(B3, 4, time, T, 13, maxCol)

    return B4

def generatenextorderbasis(currentBasis, order, TC, T, numOfBases, maxCol):
    nextB = [[0 for x in range(maxCol)] for y in range(numOfBases)]
    for i in range(0, numOfBases):
        for j in range(0, maxCol):
            if T[i + order - 1] == T[i]:
                firstValue = 0
            else:
                firstValue = ((TC[j] - T[i]) / (T[i + order - 1] - T[i])) * currentBasis[i][j]
            if T[i + order] == T[i]:
                secondValue = 0
            else:
                secondValue = (1 - ((TC[j] - T[i + 1]) / (T[i + order] - T[i + 1]))) * currentBasis[i + 1][j];
            value = firstValue + secondValue
            nextB[i][j] = value;
    return nextB

def exportToFile(measuredData, basis):
    file = open('out.csv', 'w')

    writer = csv.writer(file)
    writer.writerows(basis)

    for i in range(len(basis[0])):
        if i not in measuredData:
            file.write('')
        else:
            file.write(str(measuredData.get(i)))
        if i != len(basis[0]) - 1:
            file.write(',')
        else:
            file.write('\n')
    file.close()
    return

main()