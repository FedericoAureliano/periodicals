//Width and height of map
var width = 700;
var height = 500;
var centered;

// Define color scale
var color = d3.scale.linear()
    .domain([0, 200])
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

// D3 Projection
var projection = d3.geo.albersUsa()
.translate([width / 2, height / 2]) // translate to center of screen
.scale([950]);                     // scale things down so see entire US

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

d3.json("https://federicoaureliano.github.io/periodicals/data/us-states.json", function (json) {
    // Bind the data to the SVG and create one path per GeoJSON feature
    svg.selectAll("path")
    .data(json.features)
    .enter()
    .append("path")
    .attr("d", path)      
    .on("click", clicked)
    .style("stroke", "rgb(200,200,200)")
    .style("stroke-width", "1")
    .style("fill", stateFill);

    function clicked(d) {
        var x = 0,
            y = 0;
            k = 1;
        
        // If the click was on the centered state or the background, re-center.
        // Otherwise, center the clicked-on state.
        if (!d || centered === d) {
            centered = null;
        } else {
            var centroid = path.centroid(d);
            x = width / 2 - centroid[0];
            y = height / 2 - centroid[1];
            centered = d;
            k = 2;
        }
        
        // Transition to the new transform.
        svg.transition()
            .duration(750)
            .attr("transform", "translate(" + x + "," + y + ")scale(" + k + ")");
    }

    // Map the publications
    d3.csv("https://federicoaureliano.github.io/periodicals/data/queries/city_decade_highlight.csv", function (data) {

    svg.selectAll("circle")
        .data(data)
        .enter()        
        .append("a")
        .attr("xlink:href", function (d) {
          return "./cities/" + d.City.replace(" ","_") + "_" + d.State.replace(" ","_") + "_" + document.getElementById('Highlight').value.replace(" ","_") + ".html"
        })
        .append("circle")
        .attr("cx", function (d) {
            return projection([parseFloat(d.Lon), parseFloat(d.Lat)])[0];
        })
        .attr("cy", function (d) {
            return projection([parseFloat(d.Lon), parseFloat(d.Lat)])[1];
        })
        .attr("r", radiusFunc)
        .style("fill", fillFunc)
        .style("opacity", 0.7)
        .style("stroke", "#1d3557")

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

        function radiusFunc(d) {
            if (d.Highlight == document.getElementById('Highlight').value) {
                if (d.Decade == document.getElementById('Decade').value) {
                    return Math.sqrt(d.Count);
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
                return "#a8dadc";
            }
        }

        d3.select("#Decade").on("change", update)
        d3.select("#Highlight").on("change", update)

        function update() {
            svg.selectAll("circle")
            .data(data)
            .transition()
            .duration(750)
            .attr("r", radiusFunc)
            .style("fill", fillFunc);

            svg.selectAll("a")
            .attr("xlink:href", function (d) {
              return "./cities/" + d.City.replace(" ","_") + "_" + d.State.replace(" ","_") + "_" + document.getElementById('Highlight').value.replace(" ","_") + ".html"
            })
        }
    });
});