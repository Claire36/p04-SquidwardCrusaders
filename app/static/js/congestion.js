var margin = {top: 60, right: 30, bottom: 30, left: 60},
    width = 1000 - margin.left - margin.right,
    height = 550 - margin.top - margin.bottom;

var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
var svgPar = svg.select(function() {
    return this.parentNode;
});


// Map and projection
var path = d3.geoPath();
var projection = d3.geoMercator()
  .scale(875)
  .center([-97,38])
  .translate([width / 2, height / 2]);

var bound = 1.3;
//var bound = 0.5;

// Data and color scale
var data = d3.map();
var colorScale = d3.scaleLinear()
  .domain([0.8, +bound])
  .range(["white", "#950606"]);

var grad_1 = svgPar.append("linearGradient")
    .attr("id", "grad_1")
    .attr("x1", "0%")
    .attr("y1", "100%")
    .attr("x2", "100%")
    .attr("y2", "100%");

grad_1.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", "white");

grad_1.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", "#950606");

svgPar.append("rect")
    .attr("width", 300)
    .attr("height", 50)
    .attr("fill", "url(#grad_1)")
    .attr("x", "0%")
    .attr("y", height + 5);

var tickScale = d3.scaleLinear()
    .domain([0.8, +bound])
    .range([0, 300]);

var tickFormat = d3.format(".2f");
var tickCount = 5;

var ticks = svgPar.append("g")
    .selectAll("text")
    .data(tickScale.ticks(tickCount))
    .enter().append("text")
        .attr("x", tickScale)
        .attr("y", height - 2)
        .attr("text-anchor", "middle")
        .text(tickFormat);

var tickLines = svgPar.append("g")
    .selectAll("line")
    .data(tickScale.ticks(tickCount))
    .enter().append("line")
        .attr("x1", tickScale)
        .attr("x2", tickScale)
        .attr("y1", height)
        .attr("y2", height + 5)
        .attr("stroke", "black");

// Load external data and boot
d3.queue()
  .defer(d3.json, "../static/cities.geojson")
  .defer(d3.csv, "../static/congestion_filtered.csv", function(d) { 
      data.set(d.Urban_area, +d["1982"]); 
                                                               })
  .await(ready);

//var ind = 1982;

function ready(error, topo) {
  // Draw the map
  svg.append("g")
    .selectAll("path")
    .data(topo.features)
    .enter()
    .append("path")
      // draw each country
      .attr("d", d3.geoPath()
        .projection(projection)
      )
      // set the color of each country
      .attr("fill", function (d) {
        d.total = data.get(d.properties.NAME) || 0;
        return colorScale(d.total);
      })
      .attr("stroke-width", 0.4)
      .attr("stroke", "black");
    //year(ind);
    //if (ind == 1982) {
    //    ind = 1985;
    //} else if (ind == 1985) {
    //    ind = 1990;
    //} else {
    //    ind = ind+1;
    //}
}

function year(text) {
    if (text<2024) {
        var div=document.getElementById("year");
        div.textContent = "Year: " + text;
    }
}

function animate1() {
    for (let i = 2001; i<2024; i++) {
        d3.queue()
          .defer(d3.json, "https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson")
          .defer(d3.csv, "../static/congestion_filtered.csv", function(d) { 
              if(d.Date=="" + i + "-01-01") {
                  data.set(d.County, +d["O3_Mean"]); 
              }
                                                               })
          .await(ready);
    }
}

function animate2() {
    for (let i = 2000; i<2024; i++) {
        d3.queue()
      .defer(d3.csv, "../static/congestion_filtered.csv", function(d) {
            if(d.Date=="" + i + "-01-01") {
                data.set(d.County, +d["O3_Mean"]);
            }
        })
    d3.selectAll("path")
        .attr("fill", function (d) {
            d.total = data.get(d.properties.NAME) || 0;
            return colorScale(d.total);
        })
    }
}

function animate3() {
	for (let i = 2001; i<2024; i++) {
		d3.csv("../static/congestion_filtered.csv", function(d) {
			if(d.Date=="" + i + "-01-01") {
				data.set(d.County, +d["O3_Mean"]);
			}
		})
		svg.selectAll("path")
			.attr("fill", function(d) {
				d.total = data.get(d.properties.NAME) || 0;
				return colorScale(d.total);
			})
		year(i)
	}
}

var yr = 1985;
var progBar = document.getElementById('progress-bar');
var progress = 0.0;
function animate4(yr) {
	year(yr)
        d3.queue()
          .defer(d3.json, "../static/cities.geojson")
          .defer(d3.csv, "../static/congestion_filtered.csv", function(d) { 
                  data.set(d.Urban_area, +d[yr.toString()]); 
		  //data.get(d["Urban_area"])
                                                               })
          .await(ready);
	progress = (yr-1982)/28.0*100;
	if (progress < 101) {
		progBar.style.width = "" + progress + "%";
	}
	if (yr==1982) {
		yr = yr+3;
	} else if (yr<2000) {
		yr = yr+5;
	} else {
		yr++;
	}
	if (yr < 2011) {
		setTimeout(animate4, 1000, yr);
	}
}

