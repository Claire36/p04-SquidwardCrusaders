L.geoJSON(data, {
    style: function (feature) {
        let s = feature.properties.shade;
        let gray = Math.round((1 - s) * 255);
        return {
            fillColor: `rgb(${gray}, ${gray}, ${gray})`,
            fillOpacity: 1,
            color: '#333',
            weight: 0.5
        };
    },
    onEachFeature: function (feature, layer) {
        let name = feature.properties.NAME || "Unknown";
        let shade = feature.properties.shade;
        layer.bindPopup(`<strong>${name}</strong><br>Shade: ${shade.toFixed(2)}`);
    }
}).addTo(map);
