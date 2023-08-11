import psycopg2 as psy
import numpy as np
from matplotlib import pyplot as plt

oConn = psy.connect("dbname = USA user=postgres password=dataclass23")
oCur = oConn.cursor()

queryX = '''
    SELECT *
    FROM (
        SELECT "am_gestation", "am_birthweight", "id_sex"
        FROM "USA"."natalityConf"
        WHERE "id_sex" = '1' AND "am_gestation" NOT IN ('00', '99') AND "am_birthweight" <> '9999'
    ) AS male_data

    UNION ALL

    SELECT *
    FROM (
        SELECT "am_gestation", "am_birthweight", "id_sex"
        FROM "USA"."natalityConf"
        WHERE "id_sex" = '2' AND "am_gestation" NOT IN ('00', '99') AND "am_birthweight" <> '9999'
    ) AS female_data;
'''

x = oCur.execute(queryX)
results = np.array(oCur.fetchall())
male_results = []
female_results = []
for i in range(len(results)):
    if results[i,2] == '1':
        male_results.append(results[i])
    else:
        female_results.append(results[i])
male_results = np.array(male_results)
female_results = np.array(female_results)
male_results = np.vstack(male_results)
female_results = np.vstack(female_results)
male_results = male_results[:, 0:2].astype(int)
female_results = female_results[:, 0:2].astype(int)

oCur.close()
oConn.close()

# Count the total number of males and females born during each week of gestation
def count_births_by_gestation(data):
    gestation_counts = {}
    for gestation, _ in data:
        if gestation in gestation_counts:
            gestation_counts[gestation] += 1
        else:
            gestation_counts[gestation] = 1
    return gestation_counts

male_gestation_counts = count_births_by_gestation(male_results)
female_gestation_counts = count_births_by_gestation(female_results)

# Sort the gestations in ascending order
gestations = sorted(set(male_gestation_counts) | set(female_gestation_counts))

# Print the counts for each week of gestation
print("Male Births by Week of Gestation:")
for gestation in gestations:
    count = male_gestation_counts.get(gestation, 0)
    print(f"Week {gestation}: {count} males")

print("\nFemale Births by Week of Gestation:")
for gestation in gestations:
    count = female_gestation_counts.get(gestation, 0)
    print(f"Week {gestation}: {count} females")

# Calculate the ratio of males to females for each week of gestation
ratios = [male_gestation_counts.get(gestation, 0) / (female_gestation_counts.get(gestation, 1) or 1) for gestation in gestations]

# Plot the histogram
plt.bar(gestations, ratios, align='center', alpha=0.75)
plt.title('Histogram: Male-to-Female by Week of Gestation')
plt.xlabel('Week of Gestation')
plt.ylabel('Ratio (Males:Females)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='dashed')
plt.show()

# Create a function to plot a scatter plot
def plot_scatter(data, title, color):
    x_values = data[:, 0]
    y_values = data[:, 1]

    plt.scatter(x_values, y_values, alpha=0.2, color=color)
    plt.title(title)
    plt.xlabel('Weeks of Gestation')
    plt.ylabel('Birthweight (in grams)')
    plt.show()

# Plot male_results scatter plot
plot_scatter(male_results, 'Male Results Scatter Plot', color='blue')

# Plot female_results scatter plot
plot_scatter(female_results, 'Female Results Scatter Plot', color='red')