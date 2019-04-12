import csv
import sqlite3

from ski.models import State, Mountain, Comments, Geography


con = sqlite3.connect("ski/snowfall.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

# State.objects.all().delete()
# Mountain.objects.all().delete()
# Comments.objects.all().delete()

# python3 manage.py shell < ski/load.py
# def load_mountains():
cur.execute("SELECT * FROM Mountains")
for row in [dict(row) for row in cur.fetchall()]:
    if row["Snowpack"] != "None":
        row["Snowpack"] = "{}%".format(int(float(row["Snowpack"]) * 100))
    if row["OpenPercent"] != "None":
        row["OpenPercent"] = "{}%".format(int(float(row["OpenPercent"]) * 100))
    if row["Base"] != "None":
        row["Base"] = '{}"'.format(row["Base"])
    try:
        row["NewSnow"] = int(row["NewSnow"])
    except:
        row["NewSnow"] = 0

    try:
        S = State.objects.get(state_name=row["State"])
    except:
        S = State(state_name=row["State"])
        S.save()
        # print('fail here')

    try:
        M = Mountain.objects.get(name=row["MountainName"])
        M.status = row["status"]
        M.new_snow = row["NewSnow"]
        try:
            M.new_snow = int(row["NewSnow"])
        except:
            M.new_snow = 0
        # if row['NewSnow'] == "None":
        #     M.new_snow = 0
        M.current_weather = row["CurrentWeather"]
        M.snowpack = row["Snowpack"]
        M.open_percent = row["OpenPercent"]
        M.trails = row["Trails"]
        M.lifts = row["Lifts"]
        M.base = row["Base"]
        M.conditions = row["Conditions"]
        M.save()
    except:
        M = Mountain(
            name=row["MountainName"],
            state_name=S,
            url=row["URL"],
            status=row["status"],
            new_snow=row["NewSnow"],
            current_weather=row["CurrentWeather"],
            snowpack=row["Snowpack"],
            open_percent=row["OpenPercent"],
            trails=row["Trails"],
            lifts=row["Lifts"],
            base=row["Base"],
            conditions=row["Conditions"],
        )
        # print(M)
        # print('fail here')
        # M.save()

# def load_geography():
cur.execute("SELECT * FROM Geography")
for row in [dict(row) for row in cur.fetchall()]:
    S = State.objects.get(state_name=row["State"])
    try:
        M = Mountain.objects.get(name=row["Name"], state_name=S)
        # print(M)
    except:
        continue
    try:
        G = Geography.objects.get(mountain=M)
    except:
        if row["Latitude"] == "Error":
            row["Latitude"] = None
        if row["Longitude"] == "Error":
            row["Longitude"] = None
        G = Geography(mountain=M, latitude=row["Latitude"], longitude=row["Longitude"])
        G.save()
