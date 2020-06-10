import common

decade_choices = "\n".join(["    <option value=\"%d\">%ds</option>"%(dec, dec) for dec in common.DECADES])

highlight_choices = "\n".join(["    <option value=\"%s\">%s</option>"%(hi, hi) for hi in common.HIGHLIGHTS])


index_html = """
<!DOCTYPE html>
<meta charset="UTF-8">
<html>

<head>
  <title>African-American Periodicals: a Visual Bibliography</title>
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
  <h1>African-American Periodicals: a Visual Bibliography</h1>
  <div class="hbar"> </div>
  <p>
    Select a decade and topic from the drop-down menus to see where relevant periodicals were published.
    City circles are <mark>red</mark> when we have a link to at least one periodical archive from that location.
    Click cities to learn more; click states to zoom in and out.
  </p>
  <p>
    All initial data comes from <a href="https://archive.org/details/africanamericanne00dank">African-American newspapers and periodicals: a national bibliography</a>. 
    So far, links come from the <a href="https://www.oaklandlibrary.org/locations/african-american-museum-library-oakland">African American Museum & Library at Oakland</a>, 
    the <a href="http://www.oac.cdlib.org/">Online Archive of California</a>, and
    the <a href="http://libguides.marist.edu/c.php?g=87271&p=563206">James A. Cannavino Library</a>.
    I have three (unattainable) goals for this project: to fix all data-mining mistakes; to add the 21st century; 
    and to link to an archive of every periodical in the dataset.
    If you would like to contribute to any of these goals, please do!
    The project is on github and the dataset is <a href="https://github.com/FedericoAureliano/periodicals/blob/master/data/bibliography.csv">here</a>.
    If you are not comfortable with git/github, but would still like to report an issue, you can contact <a href="https://federicoaureliano.github.io/">me</a> through e-mail.
  </p>
  <br>
  <div class="hbar"> </div>
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