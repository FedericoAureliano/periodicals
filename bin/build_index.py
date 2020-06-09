import common

decade_choices = "\n".join(["    <option value=\"%d\">%ds</option>"%(dec, dec) for dec in common.DECADES])

highlight_choices = "\n".join(["    <option value=\"%s\">%s</option>"%(hi, hi) for hi in common.HIGHLIGHTS])


index_html = """
<!DOCTYPE html>
<meta charset="UTF-8">
<html>

<head>
  <title>African-American Newspapers and Periodicals: a Visual Bibliography</title>
  <link href="https://fonts.googleapis.com/css?family=Muli" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="css/main.css">
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
  <h2>African-American Newspapers and Periodicals: a Visual Bibliography</h2>
  <div class="hbar"> </div>
  <p>
    Select a decade and topic from the drop-down menus (both default to all) to see where newspapers and periodicals related to that topic were being published during that decade.
    For any given decade and topic, cities are red if we have a link to see at least one newspaper or periodical in that city from that decade related to that topic.
    Click a city to see all relevant newspapers and periodicals, and links.
  </p>
  <p>
    All initial data comes from <a href="https://archive.org/details/africanamericanne00dank">African-American newspapers and periodicals: a national bibliography</a>.
    I have three (unattainable) goals for this project: to fix all data-mining mistakes; to add decades; 
    and to link to a scan of at least one issue of every newspaper or periodical in the data-set.
    If you would like to contribute to any of these goals, please do!
    The project is on github and the data-set is <a href="https://github.com/FedericoAureliano/periodicals/blob/master/data/bibliography.csv">here</a>.
    If you are not comfortable with git/github, but would still like to report an issue, you can contact <a href="https://federicoaureliano.github.io/">me</a> through e-mail.
  </p>
  <br>
  <select id="Decade">
    <option value="All">All Decades</option>
%s
  </select>
  <select id="Highlight">
    <option value="All">All Topics</option>
%s
  </select>
  <svg></svg>
  <script src="javascript/map.js"></script>
</body>

</html>
"""%(decade_choices, highlight_choices)

with open('index.html', 'w') as index:
    index.write(index_html)