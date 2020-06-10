//Width and height of map
var width = 850;
var height = 500;
var centered;

// Define color scale
var color = d3.scale.linear()
    .domain([0, 110])
    .clamp(true)
    .range(['#fff', '#457b9d']);

// Get province name
function nameFn(d) {
    return d && d.properties ? d.properties.name : null;
}

// Get province name length
function nameLength(d) {
    var n = nameFn(d);
    return n ? n.length : 0;
}

// Get province color
function stateFill(d) {
    return color(nameLength(d));
}

// This is essentially the zoom factor...global variable...lol
var k = 1;

function radiusFunc(d) {
    if (d.Highlight == document.getElementById('Highlight').value) {
        if (d.Decade == document.getElementById('Decade').value) {
            return (Math.sqrt(d.Count) + 1) / k;
        } else {
            return 0;
        }
    } else {
        return 0;
    }
}

function fillFunc(d) {
    if (d.Links > 0) {
        return "#ff0013"
    } else {
        return "#1d3557";
    }
}

// D3 Projection
var projection = d3.geo.albersUsa()
.translate([width / 2, height / 2]) // translate to center of screen
.scale([970]);                     // scale things down so see entire US

// Define path generator
var path = d3.geo.path()    // path generator that will convert GeoJSON to SVG paths
.projection(projection);  // tell path generator to use albersUsa projection

//Create SVG element and append map to the SVG
var svg = d3.select("svg")
.attr('width', width)
.attr('height', height);

// Append Div for tooltip to SVG
var div = d3.select("body")
		    .append("div")   
    		.attr("class", "tooltip")               
    		.style("opacity", 0);

var g = svg.append('g');

d3.json("https://federicoaureliano.github.io/periodicals/data/us-states.json", function (json) {
    // Bind the data to the SVG and create one path per GeoJSON feature
    g.selectAll("path")
    .data(json.features)
    .enter()
    .append("path")
    .attr("d", path)      
    .attr("id", "states")
    .on("click", clicked)
    .style("stroke", "rgb(190,190,190)")
    .style("stroke-width", "1")
    .style("fill", stateFill);

    function clicked(d) {
        var x, y;
      
        if (d && centered !== d) {
          var centroid = path.centroid(d);
          x = centroid[0];
          y = centroid[1];
          k = 2.5;
          centered = d;
        } else {
          x = width / 2;
          y = height / 2;
          k = 1;
          centered = null;
        }
      
        g.transition()
            .duration(0)
            .selectAll("path")
            .style("opacity", function (d) {
                if (!centered || d === centered) {
                    return 1;
                } else {
                    return 0.2;
                }
            });

        g.transition()
            .duration(500)
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
            .style("stroke-width", 1 / k + "px")
            .selectAll("circle")
            .attr("r", function(d) { return radiusFunc(d, k); })            
            .style("opacity", function (d) {
                if (!centered || d.State === centered.properties.name) {
                    return 1;
                } else {
                    return 0.2;
                }
            });;
      }

    // Map the publications
    d3.csv("https://federicoaureliano.github.io/periodicals/data/queries/city_decade_highlight.csv", function (data) {

    g.selectAll("circle")
        .data(data)
        .enter()        
        .append("a")
        .attr("xlink:href", function (d) {
          return "./cities/" + d.City.replace(/ /g,"_").replace(/\./g,"") + "_" + d.State.replace(/ /g,"_") + "_" + document.getElementById('Highlight').value.replace(/ /g,"_") + ".html"
        })
        .append("circle")
        .attr("cx", function (d) {
            return projection([parseFloat(d.Lon), parseFloat(d.Lat)])[0];
        })
        .attr("cy", function (d) {
            return projection([parseFloat(d.Lon), parseFloat(d.Lat)])[1];
        })
        .attr("r", radiusFunc)
        .style("fill", "#a8dadc")
        .style("fill-opacity", 0.7)
        .style("stroke", fillFunc)

        .on("mouseover", function (d) {
        div.transition()
            .duration(200)
            .style("opacity", .9);
        div.text(d.City)
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px");
        })

        // fade out tooltip on mouse out               
        .on("mouseout", function (d) {
        div.transition()
            .duration(500)
            .style("opacity", 0);
        });

        d3.select("#Decade").on("change", update)
        d3.select("#Highlight").on("change", update)

        function update() {
            g.selectAll("circle")
            .data(data)
            .transition()
            .duration(500)
            .attr("r", radiusFunc)
            .style("stroke", fillFunc)

            g.selectAll("a")
            .attr("xlink:href", function (d) {
              return "./cities/" + d.City.replace(/ /g,"_").replace(/\./g,"") + "_" + d.State.replace(/ /g,"_") + "_" + document.getElementById('Highlight').value.replace(/ /g,"_") + ".html"
            })
        }
    });
});