//manipulates the svg variable in the home.html file
var svg = d3.select("svg"),
  width = +svg.attr("width"),
  height = +svg.attr("height");

var pollution = d3.map();

//given geojson file, it'll help define the path that will be drawn
var path = d3.geoPath();
var projection = d3.geoMercator()
  .scale(600)
  .center([-120,50])
  .translate([width/2, height/2]);

var x = d3.scaleLinear().domain([1,10]).rangeRound([600,860]);

//var color = d3.scaleThreshold()
  //.domain(d3.range(2, 10))
  //.range(d3.schemeBlues[7]);

d3.queue()
  .defer(d3.json, "https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson")
  .await(ready);

function ready(error, topo){
  svg.append("g")
    .selectAll("path")
    .data(topo.features)
    .enter()
    .append("path")
      .attr("d", d3.geoPath()
        .projection(projection)
      )
      .attr("fill", "lightblue")
      .attr("stroke-width", 0.5);
}
