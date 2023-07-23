import numpy as np

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
## change file path for .dat to satisfy personal environment
### everything else should work
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

