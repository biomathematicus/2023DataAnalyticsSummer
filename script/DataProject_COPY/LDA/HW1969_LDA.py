# import numpy as np
# #counters
# data =[]
# i=0
# var1 = []
# counter=0
# count_r_tx=0 
# count_nr_ntx=0
# count_r_ntx=0
# counter2=0
# counter_main = 0 
# educounter0=0
# educounter1=0
# educounter2=0
# educounter3=0
# educounter4=0
# educounter5=0
# educounter6=0

# #pulling data from .dat
# f = open(r"D:\Downloads\US1969.dat", "r", encoding="cp1252")
# for x in f:
#     i=i+1
#     if x[1]==0: #and x[2] == "1": 
#         var1 = np.append(var1,x[1])
        
# print('Total entries in dataset\n', i)

# #sorting data meeting parameters from dictionary
# f = open(r"D:\Downloads\US1969.dat", "r", encoding="cp1252")
# for x in f:
#     if x[11] == "1":
#         counter_main = counter_main+1
#     else:
#         counter2= counter2 +1 
#     if x[12]=="4" and x[13]=="3":
#         count_r_tx = count_r_tx +1
#         if x[101] == "1":
#             educounter1= educounter1+1
#         elif x[101] == "2":
#             educounter2= educounter2+1
#         elif x[101] == "3":
#             educounter3 =  educounter3+1
#         elif x[101] =="4":
#             educounter4 = educounter4+1
#         elif x[101] == "5":
#             educounter5 = educounter5+1
#         elif x[101] == "6":
#             educounter6 = educounter6+1 
#         else: 
#          x[101] == "0"
#          educounter0= educounter0 +1  
#     else:
#         count_r_ntx= count_r_ntx +1     
                 

        

# print('Residents\n', counter_main)
# print('Resident but not Texan\n', count_r_ntx)
# print('Resident & Texas\n', count_r_tx)
# print('Non Residents\n', counter2)
# print('0-8 Years\n',educounter1)
# print('9-11 Years\n',educounter2)
# print('12 Years\n',educounter3)
# print('13-15 Years\n',educounter4)
# print('16 Years+\n',educounter5)
# print('Not Stated\n',educounter6) 







# Counters and other variables
data = []
var1 = []
counters = {
    "counter_main": 0,
    "count_r_tx": 0,
    "count_r_ntx": 0,
    "counter2": 0,
    "educounter0": 0,
    "educounter1": 0,
    "educounter2": 0,
    "educounter3": 0,
    "educounter4": 0,
    "educounter5": 0,
    "educounter6": 0,
}

# Pulling data from US1969.dat, change path as needed to confirm working script
file_path = r"D:\Downloads\US1969.dat"
data1969 = file_path
with open(file_path, "r", encoding="cp1252") as f:
    for x in f:
        data.append(x.strip())

# Sorting data meeting parameters from dictionary
for x in data:
    if x[11] == "1":
        counters["counter_main"] += 1
    else:
        counters["counter2"] += 1
#taking n^3 loop to n^2         
for x in data: 
    if x[12] == "4" and x[13] == "3":
        counters["count_r_tx"] += 1
        education_level = x[101]    
        if education_level in ("1", "2", "3", "4", "5", "6"):
            counters[f"educounter{education_level}"] += 1
        else: 
            counters["educounter0"] += 1
    else:
        counters["count_r_ntx"] += 1

# Print the results
print("Total entries in dataset:", len(data))
print("Residents:", counters["counter_main"])
print("Resident but not Texan:", counters["count_r_ntx"])
print("Resident & Texas:", counters["count_r_tx"])
print("Non Residents:", counters["counter2"])
print("0-8 Years:", counters["educounter1"])
print("9-11 Years:", counters["educounter2"])
print("12 Years:", counters["educounter3"])
print("13-15 Years:", counters["educounter4"])
print("16 Years+:", counters["educounter5"])
print("Not Stated:", counters["educounter6"])

