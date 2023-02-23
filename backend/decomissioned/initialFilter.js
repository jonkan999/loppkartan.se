/* Initial days filter */

import { filterMarkersOnDays } from "/filterMarkersOnDays.js";
import { filterMarkersOnDistance } from "/filterMarkersOnDistance.js";

export function initialFilter() {
  let startDay = $("#sliderDays").slider("values", 0);
  let endDay = $("#sliderDays").slider("values", 1);

  filterMarkersOnDays(startDay, endDay);

  /* Initial distance filter */

  const power = 3;

  let minDistance = Math.pow($("#sliderDistance").slider("values", 0), power);
  let maxDistance = Math.pow($("#sliderDistance").slider("values", 1), power);

  // Round the distance values to the nearest integer
  minDistance = Math.round(minDistance);
  maxDistance = Math.round(maxDistance);

  filterMarkersOnDistance(minDistance, maxDistance);
}
