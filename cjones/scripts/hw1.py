import matplotlib.pyplot as plt
import numpy as np

#the following block of code in the driver function, main()
def main():

    data1969 = open("D:\\Documents\\School\\graduate_courses\DataAnalytics\\HW\HW_1\\US1969.dat", "r", encoding = "cp1252")
    data1969.seek(0)

    #counts total number of TX-mothers giving birth in TX
    count = 0
    data1969.seek(0)
    for x in data1969:
        if isTxMother(data1969, x) and bornAlive(data1969, x):
            count = count + 1
    print("The total number of live-births in Texas to mothers residing in Texas is: " + str(count) + ".")

    #counts the total number of births by order vs mother's education level
    data1969.seek(0)
    educVsNumChildren = educationVsBirthOrder(data1969)
    #breaks the data apart into easily-plottable formats
    #this hack-job is the best I could do sans libraries
    educVsNumChildren.pop(0)
    elemSchoolTotals = []
    highSchoolTotals = []
    collegeTotals = []
    for i in range(8):
        elemSchoolTotals.append(educVsNumChildren[i][0])
    for i in range(8):
        highSchoolTotals.append(educVsNumChildren[i][1])
    for i in range(8):
        collegeTotals.append(educVsNumChildren[i][2])
    birthOrder = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th+']
    educationLevel = ["At Most K-8th", "At Most 9th-12th", "At least Some College"]

    #graphs the data
    width = 0.25
    xAxis = np.arange(8) #please forgive this single use of numpy, I could not figure out
    #how to get it to work without it, even pyplots official documentation examples uses numpy for this
    plt.figure()
    plt.bar(xAxis - width, elemSchoolTotals, width, color="green")
    plt.bar(xAxis, highSchoolTotals, width, color="orange")
    plt.bar(xAxis + width, collegeTotals, width, color="purple")
    plt.xticks(xAxis, birthOrder)
    plt.xlabel("Birth Order of Child")
    plt.ylabel("Total Children Born")
    plt.legend(educationLevel)
    #plots the values over the bars for elementary-educated mothers
    for i in range(len(educVsNumChildren)-3):
        plt.text(i-width, elemSchoolTotals[i]-(elemSchoolTotals[i]*.25), elemSchoolTotals[i], ha = 'center')
    for i in range(5,8):
        plt.text(i-width, elemSchoolTotals[i]+2*(elemSchoolTotals[i]*.5), elemSchoolTotals[i], ha = 'center')
    for i in range(5,8):
        plt.vlines(i-width, elemSchoolTotals[i], elemSchoolTotals[i]+2*(elemSchoolTotals[i]*.5), color='green')
    #plots the values over the bars for high school-educated mothers
    for i in range(len(educVsNumChildren)-3):
        plt.text(i, highSchoolTotals[i], highSchoolTotals[i], ha = 'center')
    for i in range(5,8):
        plt.text(i, highSchoolTotals[i]+2*highSchoolTotals[i], highSchoolTotals[i], ha = 'center')
    for i in range(5,8):
        plt.vlines(i, highSchoolTotals[i], highSchoolTotals[i]+2*highSchoolTotals[i], color='orange')
    #plots the values over the bars for college-educated mothers
    for i in range(len(educVsNumChildren)-3):
        plt.text(i+width, collegeTotals[i], collegeTotals[i], ha = 'center')
    for i in range(5,8):
        plt.text(i+width, collegeTotals[i]+2*(collegeTotals[i]*.75), collegeTotals[i], ha = 'center')
    for i in range(5,8):
        plt.vlines(i+width, collegeTotals[i], collegeTotals[i]+2*(collegeTotals[i]*.75), color='purple')
    plt.show()

#the following blocks of code are the various functions
def isTxMother(file, posVal):
    for posVal in file:
        if posVal[25] == "7" and posVal[26] == "4" and (posVal[27] == "4" and posVal[27] == "4"):
            return True

def bornAlive(file, posVal):
    for posVal in file:
        if (int(posVal[59]) or int(posVal[62]) or int(posVal[63]) or int(posVal[64]) or int(posVal[65]) or int(posVal[66])) in range(1, 10):
            return True

def educationVsBirthOrder(file):
    arr = [[0 for x in range(3)] for y in range(9)]
    for x in file:
        if int(x[59]) in range(1,9):
            #elementary school educated birth totals
            if int(x[97] + x[98]) in range(9) or int(x[99] + x[100]) in range(4) or int(x[101]) == 1:
                arr[int(x[59])][0] += 1
            #high school educated birth totals
            if int(x[97] + x[98]) in range(9,13) or int(x[99] + x[100]) in range(5,9) or int(x[101]) in range(2,4):
                arr[int(x[59])][1] += 1
            #college educated birth totals
            if int(x[97] + x[98]) in range(13,18) or int(x[99] + x[100]) in range(9,14) or int(x[101]) in range(4,6):
                arr[int(x[59])][2] += 1
        elif int(x[62]) in range(1,9):
            #elementary school educated birth totals
            if int(x[97] + x[98]) in range(9) or int(x[99] + x[100]) in range(4) or int(x[101]) == 1:
                arr[int(x[62])][0] += 1
            #high school educated birth totals
            if int(x[97] + x[98]) in range(9,13) or int(x[99] + x[100]) in range(5,9) or int(x[101]) in range(2,4):
                arr[int(x[62])][1] += 1
            #college educated birth totals
            if int(x[97] + x[98]) in range(13,18) or int(x[99] + x[100]) in range(9,14) or int(x[101]) in range(4,6):
                arr[int(x[62])][2] += 1
    return arr

if __name__ == "__main__":
    main()