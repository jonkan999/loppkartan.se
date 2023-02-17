import { filterMarkersOnDistance } from "/filterMarkersOnDistance.js";

const power = 3;

$(function () {
  $("#sliderDistance").slider({
    range: true,
    min: 0,
    max: 6,
    step: 0.1,
    values: [0.8, 2],
    slide: function (event, ui) {
      let minDistance = Math.pow(ui.values[0], power);
      let maxDistance = Math.pow(ui.values[1], power);

      // Round the distance values to the nearest integer
      minDistance = Math.round(minDistance);
      maxDistance = Math.round(maxDistance);

      $("#distanceFilterText").val(minDistance + " - " + maxDistance + "km");

      filterMarkersOnDistance(minDistance, maxDistance);
    },
  });

  let minDistance = Math.pow($("#sliderDistance").slider("values", 0), power);
  let maxDistance = Math.pow($("#sliderDistance").slider("values", 1), power);

  // Round the distance values to the nearest integer
  minDistance = Math.round(minDistance);
  maxDistance = Math.round(maxDistance);

  filterMarkersOnDistance(minDistance, maxDistance);
  $("#distanceFilterText").val(minDistance + " - " + maxDistance + "km");
});
