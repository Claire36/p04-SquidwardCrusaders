// Set up the width and height of the map
const width = 800;
const height = 600;

// Create an SVG element to hold the map
const svg = d3.select("#map")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

// Set up a geographic projection
const projection = d3.geoMercator()  // You can use other projections like geoAlbers, geoOrthographic, etc.
  .scale(150)  // Adjust the scale to zoom in/out
  .translate([width / 2, height / 2]);  // Center the map

// Set up a path generator using the projection
const path = d3.geoPath().projection(projection);

// Load your GeoJSON data (use your file's path)
d3.json("../../../counties.geojson").then(function(geoData) {

  // Draw the GeoJSON data on the SVG map
  svg.selectAll(".country")
    .data(geoData.features)  // geoData.features will be an array of features in the GeoJSON
    .enter()
    .append("path")
    .attr("class", "country")
    .attr("d", path)
    .attr("fill", "#69b3a2")
    .attr("stroke", "#fff")
    .attr("stroke-width", 0.5)
    .on("mouseover", function(event, d) {
      // Handle mouseover (optional: add interactivity like tooltips)
      d3.select(this).attr("fill", "#ff7f0e");
    })
    .on("mouseout", function(event, d) {
      // Reset the color on mouseout
      d3.select(this).attr("fill", "#69b3a2");
    });
})
  .catch(function(error) {
    console.error("Error loading the GeoJSON data:", error);
  });
