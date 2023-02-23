import { toggleBoxExpansion } from "/js/toggleBoxExpansion.js";
// Create a map centered on a specific location
let map = L.map("map", { attributionControl: false }).setView(
  [60.346972, 15.748689],
  5
);
window.globalMap = map;
// Add a tile layer to the map
L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
  {
    minZoom: 5,
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }
).addTo(map);

let marker;

// Add an event listener to the map that creates a marker on a click
map.on("click", function (event) {
  if (marker) {
    marker.remove();
  }
  const markerClass = document.getElementById("type").value || "default";
  const latlng = event.latlng;
  marker = L.marker(latlng, {
    icon: new L.DivIcon({
      className: `marker-${markerClass}`,
      iconSize: [18, 18],
    }),
  }).addTo(map);

  // Set the value of the latitude and longitude inputs, and update text in display box
  document.getElementById("latitude").value = latlng.lat;
  document.getElementById("longitude").value = latlng.lng;
  document.getElementById(
    "latlongBox"
  ).innerHTML = `Loppets latitud: ${latlng.lat.toFixed(
    2
  )} och longitud: ${latlng.lng.toFixed(2)}`;
});

// Update marker class when type select value changes
const typeSelect = document.getElementById("type");
typeSelect.addEventListener("change", function () {
  if (marker) {
    const markerClass = typeSelect.value || "default";
    marker.getElement().className = `marker marker-${markerClass}`;
  }
});

const raceInfoBoxes = document.querySelectorAll(".race-info-box");
raceInfoBoxes.forEach((raceInfoBox) => {
  raceInfoBox.addEventListener("click", toggleBoxExpansion);
});
