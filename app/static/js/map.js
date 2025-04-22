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

var pollutant = document.getElementById("pollutant").textContent;
if (pollutant=="O3") {
	var bound = 0.04;
} else if (pollutant=="CO") {
	var bound = 0.8;
} else if (pollutant=="SO2") {
	var bound = 4;
} else if (pollutant=="NO2") {
	var bound = 20;
}
var pollutantKey = document.getElementById("pollutant").textContent + "_Mean";

// Data and color scale
var data = d3.map();
var colorScale = d3.scaleLinear()
  .domain([0, +bound])
  .range(["white", "#000060"]);

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
    .attr("stop-color", "#000060");

svgPar.append("rect")
    .attr("width", 300)
    .attr("height", 50)
    .attr("fill", "url(#grad_1)")
    .attr("x", "0%")
    .attr("y", height + 5);

var tickScale = d3.scaleLinear()
    .domain([0, +bound])
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
  .defer(d3.json, "https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson")
  .defer(d3.csv, "../static/pollution_2000_2023_filtered.csv", function(d) { 
      if(d.Date=="2000-01-01") {
          data.set(d.County, +d[pollutantKey]); 
      }
                                                               })
  .await(ready);

var ind = 2000;
var progBar = document.getElementById('progress-bar');
var progress = 0.0;
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
      .attr("stroke", "black");
    year(ind);
    ind = ind+1;
    progress = (ind-2001)/23.0*100;
    if (progress < 101) {
        progBar.style.width = "" + progress + "%";
    }
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
          .defer(d3.csv, "../static/pollution_2000_2023_filtered.csv", function(d) { 
              if(d.Date=="" + i + "-01-01") {
                  data.set(d.County, +d[pollutantKey]); 
              }
                                                               })
          .await(ready);
    }
}

function animate2() {
    for (let i = 2000; i<2024; i++) {
        d3.queue()
      .defer(d3.csv, "../static/pollution_2000_2023.csv", function(d) {
            if(d.Date=="" + i + "-01-01") {
                data.set(d.County, +d[pollutantKey]);
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
		d3.csv("../static/pollution_2000_2023.csv", function(d) {
			if(d.Date=="" + i + "-01-01") {
				data.set(d.County, +d[pollutantKey]);
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

var yr = 2001;
function animate4(yr) {
        d3.queue()
          .defer(d3.json, "https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson")
          .defer(d3.csv, "../static/pollution_2000_2023_filtered.csv", function(d) { 
              if(d.Date=="" + yr + "-01-01") {
                  data.set(d.County, +d[pollutantKey]); 
              }
                                                               })
          .await(ready);
	
	yr++;
	if (yr < 2024) {
		setTimeout(animate4, 1000, yr);
	}
}

