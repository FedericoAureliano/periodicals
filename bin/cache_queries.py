import common
import csv

points = dict()

with open('data/queries/intermediate.csv') as full_csv:
    full = list(csv.DictReader(full_csv))


coordinates = dict()
links = dict()

for line in full:
    all_h_d = (line["City"], line["State"], "All", "All")
    if all_h_d in points:
        points[all_h_d] += 1
    else:
        points[all_h_d] = 1

    if all_h_d in links:
        links[all_h_d] += 1 if line["HasLink"] == "1" else 0
    else:
        links[all_h_d] = 1 if line["HasLink"] == "1" else 0

    # Add to cities
    if (line["City"], line["State"]) not in coordinates:
        coordinates[(line["City"], line["State"])] = (line["Lat"], line["Lon"])

    for d in common.DECADES:
        if line[str(d)] == "1":
            # Add to all
            all_h = (line["City"], line["State"], "All", d)
            if all_h in points:
                points[all_h] += 1
            else:
                points[all_h] = 1
            
            if all_h in links:
                links[all_h] += 1 if line["HasLink"] == "1" else 0
            else:
                links[all_h] = 1 if line["HasLink"] == "1" else 0

            for h in common.HIGHLIGHTS:
                cshd = (line["City"], line["State"], h, d)
                # Add to highlight
                if line[h] == "1":
                    if cshd in points:
                        points[cshd] += 1
                    else:
                        points[cshd] = 1

                    if cshd in links:
                        links[cshd] += 1 if line["HasLink"] == "1" else 0
                    else:
                        links[cshd] = 1 if line["HasLink"] == "1" else 0

    for h in common.HIGHLIGHTS:
        if line[str(h)] == "1":
            # Add to all
            all_d = (line["City"], line["State"], h, "All")
            if all_d in points:
                points[all_d] += 1
            else:
                points[all_d] = 1
            
            if all_d in links:
                links[all_d] += 1 if line["HasLink"] == "1" else 0
            else:
                links[all_d] = 1 if line["HasLink"] == "1" else 0

with open('data/queries/city_decade_highlight.csv', 'w') as compiled:
    print("Lat,Lon,City,State,Highlight,Decade,Count,Links", file=compiled)
    for p in points:
        c = coordinates[(p[0], p[1])]
        print("%s,%s,\"%s\",\"%s\",\"%s\",\"%s\",%d,%d" %(c[0], c[1], p[0], p[1], p[2], p[3], points[p], links[p]), file=compiled)