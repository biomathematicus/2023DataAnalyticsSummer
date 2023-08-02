import numpy as np
import matplotlib.pyplot as plt

data = []
var1 = []
counters = {
    "counter_main": 0,
    "count_r_tx": 0,
    "count_r_ntx": 0,
    "counter2": 0,
    "educounter14": 0,
    "educounter04": 0,
    "educounter05": 0,
    "educounter06": 0,
    "educounter07": 0,
    "educounter08": 0,
    "educounter09": 0,
    "educounter10": 0,
    "educounter11": 0,
    "educounter12": 0,
    "educounter13": 0,
    "birthorder1": 0,
    "birthorder2": 0,   
    "birthorder3": 0,
    "birthorder4": 0,
    "birthorder5": 0,
    "birthorder6": 0,
    "birthorder7": 0,
    "birthorder8": 0,
    "birthorder9": 0,
    "alive": 0
}


file_path = r"E:\DataAnalysisSum23\DataProject\US1969.dat"
data1969 = file_path
with open(file_path, "r", encoding="cp1252") as f:
    for x in f:
        data.append(x.strip())
        

educounter_years = ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]
birthorder_terms = [str(i) for i in range(1, 10)]

educounter_counter = {category: 0 for category in educounter_years}
birthorder_counters = {year: {str(i): 0 for i in range(1, 10)} for year in educounter_years}

for x in data:
    if x[11] == "1" and x[25:27] == "74" :       
        continue
    if x[51:53] == "55" or x[53:55] == "55":
        counters["alive"] +=1
    education_level = x[99:101]
    birth_order = x[62]   
    if education_level in educounter_years:
        educounter_counter[education_level] += 1
        if x[51:53] == "55":
          counters["alive"] +=1
        if birth_order in birthorder_terms:
            birthorder_counters[education_level][birth_order] += 1

print("Born Alive", counters["alive"])


#begin graphical set up
education_level_labels = {
    "04": "8 years",
    "05": "9 years",
    "06": "10 years",
    "07": "11 years",
    "08": "12 years",
    "09": "13 years",
    "10": "14 years",
    "11": "15 years",
    "12": "16 years",
    "13": "17+ years",
}
x_axis_labels = [education_level_labels[year] for year in educounter_years]

#BARCHART W YEAR 12
# Create grouped bar chart
plt.figure(figsize=(12, 6))

# Data preparation and plotting for each birth order within each education year
num_educounter_years = len(educounter_years)
bar_width = 0.15
bar_positions = np.arange(num_educounter_years)

for i, birth_order in enumerate(birthorder_terms):
    counts = [birthorder_counters[year][birth_order] for year in educounter_years]
    plt.bar(bar_positions + i * bar_width, counts, width=bar_width, label=f"Birth Order {birth_order}")

plt.xlabel("Years of Education")
plt.ylabel("Number of Children")
plt.title("Number of Children based on Years of Education and Birth Order")
plt.tight_layout()
plt.xticks(bar_positions + (bar_width * (len(birthorder_terms) - 1)) / 2, x_axis_labels)
plt.legend(title="Birth Order")
plt.show()
#BarchartWith12 End

#BARCHART W/OUT 12 YEARS
#because the two charts were so similar, it was necesarry to repeat this initilization step
educounter_years = ["04", "05", "06", "07", "09", "10", "11", "12", "13"]
birthorder_terms = [str(i) for i in range(1, 10)]

educounter_counter = {category: 0 for category in educounter_years}
birthorder_counters = {year: {str(i): 0 for i in range(1, 10)} for year in educounter_years}

for x in data:
    if x[11] == "1" or x[25:27] == "74":
        continue
    education_level = x[99:101]
    birth_order = x[62]   
    if education_level in educounter_years:
        educounter_counter[education_level] += 1
        if birth_order in birthorder_terms:
            birthorder_counters[education_level][birth_order] += 1

education_level_labels = {
    "04": "8 years",
    "05": "9 years",
    "06": "10 years",
    "07": "11 years",
    "08": "12 years",
    "09": "13 years",
    "10": "14 years",
    "11": "15 years",
    "12": "16 years",
    "13": "17+ years",
}
x_axis_labels = [education_level_labels[year] for year in educounter_years]
# Create grouped bar chart
plt.figure(figsize=(12, 6))

# Data preparation and plotting for each birth order within each education year
num_educounter_years = len(educounter_years)
bar_width = 0.15
bar_positions = np.arange(num_educounter_years)

for i, birth_order in enumerate(birthorder_terms):
    counts = [birthorder_counters[year][birth_order] for year in educounter_years]
    plt.bar(bar_positions + i * bar_width, counts, width=bar_width, label=f"Birth Order {birth_order}")

plt.xlabel("Years of Education")
plt.ylabel("Number of Children")
plt.title("Education v Birth Order with 12 years")
plt.tight_layout()
plt.xticks(bar_positions + (bar_width * (len(birthorder_terms) - 1)) / 2, x_axis_labels)
plt.legend(title="Birth Order")
plt.show()
#BarChartWithout12 End

#VIOLIN DATA PREP Start
#Needed to reinclude the initial data loop in order for this to work, not quite sure what the issue was
educounter_years = ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]
birthorder_terms = [str(i) for i in range(1, 10)]

educounter_counter = {category: 0 for category in educounter_years}
birthorder_counters = {year: {str(i): 0 for i in range(1, 10)} for year in educounter_years}

for x in data:
    if x[11] == "1" or x[25:27] == "74":
        continue
    education_level = x[99:101]
    birth_order = x[62]   
    if education_level in educounter_years:
        educounter_counter[education_level] += 1
        if birth_order in birthorder_terms:
            birthorder_counters[education_level][birth_order] += 1
            
# Prepare the data for the violin plot
data_for_violin = []
for year in educounter_years:
    for birth_order in birthorder_terms:
        for _ in range(birthorder_counters[year][birth_order]):
            data_for_violin.append((year, int(birth_order)))

# Convert the data to separate arrays for each education level
education_levels = educounter_years
birth_orders = [int(order) for order in birthorder_terms]
data_arrays = {year: np.array([order for (y, order) in data_for_violin if y == year]) for year in education_levels}

#ALL OF THE VIOLINS
# Create the violin plot
plt.figure(figsize=(12, 6))

violin_parts = plt.violinplot(
    [data_arrays[year] for year in education_levels],
    positions=np.arange(len(education_levels)),
    widths=0.5,
    showmedians=True,
    showextrema=False,
)

plt.xlabel("Years of Education")
plt.ylabel("Birth Order")
plt.title("Distribution of Birth Order by Years of Education")
#ViolinplotALL END

# Set x-axis labels
education_level_labels = {
    "04": "8 years of education",
    "05": "9 years of education",
    "06": "10 years of education",
    "07": "11 years of education",
    "08": "12 years of education",
    "09": "13 years of education",
    "10": "14 years of education",
    "11": "15 years of education",
    "12": "16 years of education",
    "13": "17+ years of education",
}
plt.xticks(np.arange(len(education_levels)), [education_level_labels[year] for year in education_levels], rotation=45)


## INDIVIDUAL VIOLINS START
# Customize the violins
for pc in violin_parts['bodies']:
    pc.set_facecolor('lightblue')
    pc.set_edgecolor('black')
    pc.set_alpha(0.7)

for partname in ('cmedians',):
    part = violin_parts[partname]
    part.set_edgecolor('black')

plt.tight_layout()
plt.show()

for i, year in enumerate(education_levels):
    fig, ax = plt.subplots(figsize=(6, 6))
    violin_parts = ax.violinplot(
        data_arrays[year],
        positions=[i],
        widths=0.5,
        showmedians=True,
        showextrema=False,
    )

    ax.set_ylabel("Birth Order")
    # ax.set_title(f"Distribution of Birth Order by dictionary code: {year}")

    # Customize the violins
    for pc in violin_parts['bodies']:
        pc.set_facecolor('lightblue')
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)

    for partname in ('cmedians',):
        part = violin_parts[partname]
        part.set_edgecolor('black')

    # Set x-axis label
    ax.set_xticks([i])
    ax.set_xticklabels([education_level_labels[year]], rotation=45)

    plt.xlabel("Years of Education")
    plt.tight_layout()
    plt.show()








