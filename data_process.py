import csv
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

plt.close('all')

def clean_inspection():
    inspection = pd.read_csv("data/inspection_results.csv")
    week = pd.read_csv("data/restaurant_week_2018_final.csv")
    inspection["lname"] = inspection["DBA"].str.lower()
    week["lname"] = week["name"].str.lower()

    merging = pd.merge(week, inspection, on=['lname'], how='inner')
    counts = merging.groupby("lname").size()
    same = merging["lname"].unique()

    counts = dict(zip(counts.index, counts.values))

    all_counts = []
    for i in week["lname"]:
        if i in counts:
            all_counts.append(counts[i])
        else:
            all_counts.append(0)
    week["violations"] = all_counts
    # week.to_csv("data/cleaned_restaurant_week_2018_final.csv")

    ind = []
    for i in inspection["lname"]:
        if i in same:
            ind.append(True)
        else:
            ind.append(False)
        
    final_insp = inspection[ind]
    final_insp["sorted_date"] = pd.to_datetime(final_insp["INSPECTION DATE"])
    sorted_final = final_insp.sort_values(by=["lname","sorted_date"])
    print(sorted_final)
    sorted_final.to_csv("data/cleaned_inspection_results.csv")

def clean_geojson():
    districts = ["Washington Heights","Harlem", "Morningside Heights", "East Harlem", "Central Park", 
    "Upper West Side", "Upper East Side", "Hell's Kitchen", "Midtown", "Murray Hill",
    "Kips Bay", "Chelsea", "Gramercy", "Stuyvesant Town", "East Village", "Lower East Side",
    "Greenwich Village", "West Village" ,"SoHo", "Nolita", "Little Italy", "Chinatown",
    "Tribeca", "Civic Center", "Two Bridges", "Battery Park City", "Financial District",
    "Theater District", "Flatiron District", ""]
    nyc = gpd.read_file("data/nyc.geojson")
    ind = []
    for i in nyc["neighborhood"]:
        if i in districts:
            ind.append(True)
        else:
            ind.append(False)
    nyc[ind].to_file("data/cleaned_nyc.geojson", driver = "GeoJSON")

def histograms():
    week = pd.read_csv("data/cleaned_restaurant_week_2018_final.csv")
    print(week["violations"].idxmax())

    print(week.loc[85,:])
    plt.figure()
    week["violations"].plot.hist(bins=10)
    plt.show()

# histograms()
clean_inspection()
# clean_geojson()