f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[0] == "9": #count all the rows
        counter = counter + 1
print(counter)

print("Problem 1")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[25] == "7" and x[26] == "4" and x[27] == "4" and x[28] == "3": # birth occurred in Texas from mothers residing in Texas
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[27] == "4" and x[28] == "3": # birth occurred in Texas
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[25] == "7" and x[26] == "4": # mothers residing in Texas
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[57] == x[60] and x[58] == x[61]: # total live birth equals to total children born to mother
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[57] == x[60] and x[58] == x[61] and x[25] == "7" and x[26] == "4" and x[27] == "4" and x[28] == "3": # live birth occurred in Texas from mothers residing in Texas
        counter = counter + 1
print(counter)

print("Problem 2a")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1": # numbers of first born 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1" and x[101] == "1": # 1st born of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1" and x[101] == "2": # 1st born of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1" and x[101] == "3": # 1st born of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1" and x[101] == "4": # 1st born of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1" and x[101] == "5": # 1st born of mothers with 16 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1" and x[101] == "0": # testing
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "1" and x[101] == "6": # testing
        counter = counter + 1
print(counter)

print("Problem 2b")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "2": # numbers of second born 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "2" and x[101] == "1": # 2nd born of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "2" and x[101] == "2": # 2nd born of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "2" and x[101] == "3": # 2nd born of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "2" and x[101] == "4": # 2nd born of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "2" and x[101] == "5": # 2nd born of mothers with 16 years of education
        counter = counter + 1
print(counter)

print("Problem 2c")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "3": # numbers of third born 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "3" and x[101] == "1": # 3rd born of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "3" and x[101] == "2": # 3rd born of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "3" and x[101] == "3": # 3rd born of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "3" and x[101] == "4": # 3rd born of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "3" and x[101] == "5": # 3rd born of mothers with 16 years of education
        counter = counter + 1
print(counter)

print("Problem 2d")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "4": # numbers of fourth born 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "4" and x[101] == "1": # 4th born of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "4" and x[101] == "2": # 4th born of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "4" and x[101] == "3": # 4th born of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "4" and x[101] == "4": # 4th born of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "4" and x[101] == "5": # 4th born of mothers with 16 years of education
        counter = counter + 1
print(counter)

print("Problem 2e")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "5": # numbers of fifth born 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "5" and x[101] == "1": # 5th born of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "5" and x[101] == "2": # 5th born of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "5" and x[101] == "3": # 5th born of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "5" and x[101] == "4": # 5th born of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "5" and x[101] == "5": # 5th born of mothers with 16 years of education
        counter = counter + 1
print(counter)

print("Problem 2f")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "6": # numbers of sixth born 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "6" and x[101] == "1": # 6th born of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "6" and x[101] == "2": # 6th born of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "6" and x[101] == "3": # 6th born of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "6" and x[101] == "4": # 6th born of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "6" and x[101] == "5": # 6th born of mothers with 16 years of education
        counter = counter + 1
print(counter)

print("Problem 2g")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "7": # numbers of seventh born 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "7" and x[101] == "1": # 7th born of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "7" and x[101] == "2": # 7th born of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "7" and x[101] == "3": # 7th born of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "7" and x[101] == "4": # 7th born of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "7" and x[101] == "5": # 7th born of mothers with 16 years of education
        counter = counter + 1
print(counter)

print("Problem 2h")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "8": # numbers of eighth born and over
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "8" and x[101] == "1": # 8th born and over of mothers with 0-8 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "8" and x[101] == "2": # 8th born and over of mothers with 9-11 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "8" and x[101] == "3": # 8th born and over of mothers with 12 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "8" and x[101] == "4": # 8th born and over of mothers with 13-15 years of education
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "8" and x[101] == "5": # 8th born and over of mothers with 16 years of education
        counter = counter + 1
print(counter)

print("testing")

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[101] == "1": # numbers of mothers with 0-8 years of education 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[101] == "2": # numbers of mothers with 9-11 years of education 
        counter = counter + 1
print(counter)

f = open("US1969.dat", "r", encoding="cp1252")
counter = 0;
for x in f:
    if x[62] == "9" and x[101] == "1": 
        counter = counter + 1
print(counter)