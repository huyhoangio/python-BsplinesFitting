import csv
import numpy as np
'''
def main():
    B4 = generate4thorderbases()
    measuredData = {}
    with open('dataset.csv', mode='r') as file:
        reader = csv.reader(file)
        for rows in reader:
            measuredData[int(float(rows[0])*100)+100] = float(rows[1])
    #print(measuredData)

    
    upBound = [1.0 for i in range(len(B4))]  # initial upper bound
    lowBound = [0 for i in range(len(B4))]   # initial lower bound

    step = 0.2;

    upBound, lowBound, step = findBoundaries(measuredData, B4, upBound, lowBound, step)
    #upBound, lowBound, step = findBoundaries(measuredData, B4, upBound, lowBound, step)
    #upBound, lowBound, step = findBoundaries(measuredData, B4, upBound, lowBound, step)

    ampedB4 = [[B4[y][x] * upBound[y] for x in range(len(B4[0]))] for y in range(len(B4))]
    upperCurve = [sum(row[i] for row in ampedB4) for i in range(len(ampedB4[0]))]

    ampedB4 = [[B4[y][x] * lowBound[y] for x in range(len(B4[0]))] for y in range(len(B4))]
    lowerCurve = [sum(row[i] for row in ampedB4) for i in range(len(ampedB4[0]))]

    step = 0.01
    bestBases = B4
    fittedCurve = [0 for i in range(len(B4[0]))]

    ampedB4 = [[0 for x in range(len(B4[0]))] for y in range(len(B4))]
    for row in range(0, len(B4)):
    #for row in range(0,5):
        rowLength = len(B4[0])
        print "current bases: ", row
        #for amplitude in np.arange(lowBound[row], upBound[row], step):
        for amplitude in np.arange(0, upBound[row], step):
            #print("amplitude: ", amplitude)
            # Update amplitude of the current basis (row)

            for i in range(rowLength):
                ampedB4[row][i] = B4[row][i]*amplitude

            #ampedB4[row] = [i*amplitude for i in ampedB4[row]] # Update amplitude
            fittedCurve = [sum(row[i] for row in ampedB4) for i in range(rowLength)]
            newError = calculateError(measuredData, fittedCurve)

            if newError < minError:
                minError = newError
                #print("new min error: ", minError)

            elif newError > (minError*1.05):
            #elif newError > minError:
                prevAmplitude = amplitude - step
                for i in range(rowLength):  # Roll back amplitude one step
                    ampedB4[row][i] *= prevAmplitude

                bestBases = ampedB4 # Update best bases

                break # Then exit the loop, move on to the next basis

            if checkIfLarger(measuredData, fittedCurve):
                prevAmplitude = amplitude - step
                for i in range(rowLength):  # Roll back amplitude one step
                    ampedB4[row][i] *= prevAmplitude
                bestBases = ampedB4  # Update best bases
                break  # Then exit the loop, move on to the next basis

    bestFittedCurve = [sum(row[i] for row in ampedB4) for i in range(len(ampedB4[0]))]
    minError = calculateError(measuredData, bestFittedCurve)
    step = 0.1
    counter = 0
    for i1 in np.arange(lowBound[0], upBound[0], step):
        for i2 in np.arange(lowBound[1], upBound[1], step):
            print('check point i2')
            for i3 in np.arange(lowBound[2], upBound[2], step):
                for i4 in np.arange(lowBound[3], upBound[3], step):
                    for i5 in np.arange(lowBound[4], upBound[4], step):
                        for i6 in np.arange(lowBound[5], upBound[5], step):
                            for i7 in np.arange(lowBound[6], upBound[6], step):
                                for i8 in np.arange(lowBound[7], upBound[7], step):
                                    for i9 in np.arange(lowBound[8], upBound[8], step):
                                        for i10 in np.arange(lowBound[9], upBound[9], step):
                                            for i11 in np.arange(lowBound[10], upBound[10], step):
                                                for i12 in np.arange(lowBound[11], upBound[11], step):
                                                    for i13 in np.arange(lowBound[12], upBound[12], step):
                                                        amp = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13];
                                                        #ampedB4 = multAmplitude(amp, B4);
                                                        ampedB4 = [[B4[y][x]*amp[y] for x in range(len(B4[0]))] for y in range(len(B4))]

                                                        currentFittedCurve = [sum(row[i] for row in ampedB4) for i in range(len(ampedB4[0]))]
                                                        currentError = calculateError(measuredData, currentFittedCurve);
                                                        counter = counter + 1
                                                        if currentError < minError:
                                                            counter = 0;
                                                            #print('new error: ', minError)
                                                            minError = currentError #update minerror
                                                            fittedCurve = currentFittedCurve
                                                            bestBases = ampedB4
                                                            bestBases.append(fittedCurve)

                                                        elif counter > 1000:
                                                            exportToFile(measuredData, upperCurve, lowerCurve, bestBases)
                                                            print "limit iterations exceed"
                                                            return

    exportToFile(measuredData, upperCurve, lowerCurve, bestBases)

    return
'''
def main():
    B4 = generate4thorderbases()
    measuredData = {}
    with open('dataset.csv', mode='r') as file:
        reader = csv.reader(file)
        for rows in reader:
            measuredData[int(float(rows[0]) * 100) + 100] = float(rows[1])
    step = 0.1
    bestBases = B4
    fittedCurve = [0 for i in range(len(B4[0]))]  # initial fitted curve is just a straight line 0
    minError = calculateError(measuredData, bestFittedCurve)
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
        #error = error + abs(dataDict.get(key) - fittedValue[key])
        error = error + (dataDict.get(key) - fittedValue[key])
    return error

#def multAmplitude(amplitudeArr, basesArray):
#    ampedArray = basesArray
#    for i in range(0, len(basesArray)):
#        for j in range(0, len(basesArray[0])):
#           ampedArray[i][j] = basesArray[i][j] * amplitudeArr[i]
#    return ampedArray

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

def exportToFile(measuredData, upBound, lowBound, basis):
    file = open('out.csv', 'w')

    for i in range(len(upBound)):
        file.write(str(upBound[i]))
        if i != len(upBound) - 1:
            file.write(',')
        else:
            file.write('\n')
    for i in range(len(lowBound)):
        file.write(str(lowBound[i]))
        if i != len(lowBound) - 1:
            file.write(',')
        else:
            file.write('\n')

    writer = csv.writer(file)
    writer.writerows(basis)

    for i in range(len(upBound)):
        if i not in measuredData:
            file.write('')
        else:
            file.write(str(measuredData.get(i)))
        if i != len(upBound) - 1:
            file.write(',')
        else:
            file.write('\n')
    file.close()
    return

main()