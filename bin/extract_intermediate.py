import common
DECADES = common.DECADES
HIGHLIGHTS = common.HIGHLIGHTS

import csv

with open('data/bibliography.csv') as full_csv:
    full = list(csv.DictReader(full_csv))

with open('data/raw/us_cities.csv') as us_cities:
    cities = list(csv.DictReader(us_cities))

keys = ["Name", "City", "State", "Lat", "Lon", "Publisher"] + [str(d) for d in DECADES] + HIGHLIGHTS + ["HasLink"]

with open('data/queries/intermediate.csv', 'w') as compiled:
  print(",".join(keys), file=compiled)

  for line in full:
    decades = [0]*len(DECADES)
    for i in range(len(DECADES)):
      if int(line["First"]) % DECADES[i] < 10:
        decades[i] = 1
      if line["Last"] and decades[i-1] == 1 and int(line["Last"]) >= DECADES[i]:
        decades[i] = 1

    lat = None
    lon = None

    for city in cities:
      if line["City"] == city["CITY"] and line["State"] == city["STATE_NAME"]:
        lat = city["LATITUDE"]
        lon = city["LONGITUDE"]

    highlights = [0]*len(HIGHLIGHTS)

    for i in range(len(HIGHLIGHTS)):
      if HIGHLIGHTS[i] in line["Subject"]:
        highlights[i] = 1

    link = 1 if line["Link"] else 0
    to_write = ["\"%s\""%line["Name"], "\"%s\""%line["City"], "\"%s\""%line["State"], lat, lon, "\"%s\""%line["Publisher"]]+[str(d) for d in decades]+[str(h) for h in highlights] + [str(link)]
    
    try:
      print(",".join(to_write), file=compiled)
    except:
      print(to_write)
