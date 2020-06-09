import common
import csv

with open('data/bibliography.csv') as full_csv:
    full = list(csv.DictReader(full_csv))

cities = set()

for line in full:
  cities.add((line["City"], line["State"]))

for city in cities:
  tables = []
  for highlight in common.HIGHLIGHTS + ["All"]:
    rows = []
    for line in full:
      if line["City"] == city[0] and line["State"] == city[1] and (highlight in line["Subject"] or highlight == "All"):
        if line["Link"]:
          name = "<a href=\"%s\">%s</a>"%(line["Link"], line["Name"])
        else:
          name = line["Name"]
        rows.append([name,line["Publisher"],line["First"],line["Last"]])
    
    if len(rows) == 0:
      continue

    rows = sorted(rows, key=lambda x: x[2])

    rows_html = ""
    for r in rows:
      rows_html += "<tr>\n"
      for e in r:
        rows_html += "<td>%s</td>\n"%(e)
      rows_html += "</tr>"

    table_html = """
<table>
  <tr>
    <th>Name</th>
    <th>Publisher</th>
    <th>First</th>
    <th>Last</th>
  </tr>
  %s
</table>
    """%(rows_html)

    page_html = """
<!DOCTYPE html>
<meta charset="UTF-8">
<html>

<head>
  <title>African-American Newspapers and Periodicals: a Visual Bibliography</title>
  <link href="https://fonts.googleapis.com/css?family=Muli" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="../css/main.css">
  <script src="https://d3js.org/d3.v3.min.js"></script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=UA-65924431-1"></script>
  <script>
      window.dataLayer = window.dataLayer || [];

      function gtag() {
          dataLayer.push(arguments);
      }
      gtag('js', new Date());
      gtag('config', 'UA-65924431-1');
  </script>
</head>

<body>
  <h1>%s, %s: %s</h1>
  <div class="dataset">
  %s
  </div>
</body>

</html>
"""%(city[0], city[1], highlight, table_html)
  
    with open('cities/%s_%s_%s.html'%(city[0].replace(" ", "_"), city[1].replace(" ", "_"), highlight.replace(" ", "_")), 'w') as page:
      page.write(page_html)


