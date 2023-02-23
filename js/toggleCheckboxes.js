import { filterMarkersOnChecks } from "/js/filterMarkersOnChecks.js";

const relay = document.getElementById("relayCheckbox");
const terrain = document.getElementById("terrainCheckbox");
const trail = document.getElementById("trailCheckbox");
const road = document.getElementById("roadCheckbox");
const track = document.getElementById("trackCheckbox");

relay.addEventListener("click", function () {
  this.classList.toggle("active");
  /* If it was untoggled then it is toggled now */
  if (this.classList.contains("active")) {
    /* Was untoggled so after clicking we show */
    filterMarkersOnChecks("relay", "show");
  } else {
    filterMarkersOnChecks("relay", "hide");
  }
});
terrain.addEventListener("click", function () {
  this.classList.toggle("active");
  if (this.classList.contains("active")) {
    filterMarkersOnChecks("terrain", "show");
  } else {
    filterMarkersOnChecks("terrain", "hide");
  }
});

trail.addEventListener("click", function () {
  this.classList.toggle("active");
  /* If it was untoggled then it is toggled now */
  if (this.classList.contains("active")) {
    /* Was untoggled so after clicking we show */
    filterMarkersOnChecks("trail", "show");
  } else {
    filterMarkersOnChecks("trail", "hide");
  }
});
road.addEventListener("click", function () {
  this.classList.toggle("active");
  if (this.classList.contains("active")) {
    filterMarkersOnChecks("road", "show");
  } else {
    filterMarkersOnChecks("road", "hide");
  }
});
track.addEventListener("click", function () {
  this.classList.toggle("active");
  if (this.classList.contains("active")) {
    filterMarkersOnChecks("track", "show");
  } else {
    filterMarkersOnChecks("track", "hide");
  }
});
