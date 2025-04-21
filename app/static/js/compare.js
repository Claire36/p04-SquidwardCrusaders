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


d3.csv("../static/congestion_filtered_transposed.csv",

  function(data) {
    // Add X axis --> it is a date format
    var x = d3.scaleLinear()
      .domain([2000, 2011])
      .range([ 0, width ]);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0.75, 1.25])
      .range([ height, 0 ]);
    svg.append("g")
      .call(d3.axisLeft(y));

var city = document.getElementById("city").textContent;
    // Add the line
    svg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) {
		return x(d.year)
	})
        .y(function(d) { return y(d[city]) })
        )

})








//2nd graph
var svg2 = d3.select("#my_dataviz2")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

var pollutant = document.getElementById("pollutant").textContent;
var pollURL = "../static/pollution_" + pollutant + ".csv"
d3.csv(pollURL,

  function(data) {
    // Add X axis --> it is a date format
    var x = d3.scaleLinear()
      .domain([2000, 2011])
      .range([ 0, width ]);
    svg2.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    if (pollutant == "O3") {
        var bound = 0.15;
    } else if (pollutant == "CO") {
        var bound = 2;
    } else if (pollutant == "SO2") {
        var bound = 40;
    } else {
        var bound = 55;
    }
    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, +bound])
      .range([ height, 0 ]);
    svg2.append("g")
      .call(d3.axisLeft(y));

var county = document.getElementById("county").textContent;
    // Add the line
    svg2.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) {
		return x(d.year)
	})
        .y(function(d) { return y(d[county]) })
        )

})
