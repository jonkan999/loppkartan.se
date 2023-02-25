/* Initializing leaflet map map */
import { smoothScrollDown } from "/js/smoothScrollDown.js";
import { toggleBoxExpansion } from "/js/toggleBoxExpansion.js";
import { enlargeMarkersOnZoom } from "/js/enlargeMarkersOnZoom.js";

let map = L.map("map", { attributionControl: false }).setView(
  [60.346972, 15.748689],
  5
);
window.globalMap = map;

// Fetching mapbox API
fetch(
  "/.netlify/functions/get-api-key"
  /* "/backend/config.json" */
)
  .then((response) => response.json())
  .then((data) => {
    const MAPBOX_API_KEY = data.MAPBOX_BASIC_STYLE_API_KEY;
    // Add a tile layer to the map
    L.tileLayer(
      "https://api.mapbox.com/styles/v1/jonkanx3/cleil8zxx001201o9krzob8a5/tiles/{z}/{x}/{y}?access_token=" +
        MAPBOX_API_KEY,
      {
        minZoom: 5,
        maxZoom: 19,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }
    ).addTo(map);
  })
  .catch((error) => {
    console.error("Error loading config file", error);
  });

/* Adding markers to the map */
let markers = [];

fetch("/all_races_w_formatted_summary.json")
  .then((response) => response.json())
  .then((races) => {
    races.forEach((markerRace) => {
      /* ONLY ROAD AND TRAIL FOR NOW */
      if (
        markerRace.type.includes("trail") ||
        markerRace.type.includes("track") ||
        markerRace.type.includes("relay") ||
        markerRace.type.includes("terrain") ||
        markerRace.type.includes("road")
      ) {
        let marker = new L.marker([markerRace.latitude, markerRace.longitude], {
          icon: new L.DivIcon({
            className: `marker-${
              markerRace.type
            } marker-${markerRace.name.replace(/\s/g, "")}-${
              markerRace.date
            } raceMarker`,
            iconSize: [12, 12],
            html: `
              <div 
                data-marker-id="${markerRace.id}"
                data-marker-lat-long="${markerRace.latitude}, ${markerRace.longitude}"
                data-marker-distance_m="${markerRace.distance_m}"
              ></div>`,
          }),
        }).addTo(map);
        marker.addTo(map);
        markers.push(marker);
        // Add a popup to the marker
        marker.on("click", () => {
          let container = document.querySelector(".race-container");
          container.innerHTML = "";

          let markerIcons = document.getElementsByClassName("raceMarker");

          let markerLatLng = marker.getLatLng();
          Array.from(markerIcons).forEach((markerIcon) => {
            // Check if markerIcon has either "hideMarkerOnCheck" or "hideMarkerOnDays" class
            if (
              !markerIcon.classList.contains("hideMarkerOnCheck") &&
              !markerIcon.classList.contains("hideMarkerOnDays")
            ) {
              const markerDiv = markerIcon.querySelector("div");
              const markerId = markerDiv.getAttribute("data-marker-id");

              let race = races.find((race) => race.id === markerId);
              let raceLatLng = [race.latitude, race.longitude];
              const tolerance = 0.001;
              // Check if the lat/long of the marker and the race match
              if (
                Math.abs(markerLatLng.lat - raceLatLng[0]) <= tolerance &&
                Math.abs(markerLatLng.lng - raceLatLng[1]) <= tolerance
              ) {
                // Add the information about the race to the race-text-box

                let div = document.createElement("div");
                div.classList.add("race-info-box");
                div.classList.add("margin-bottom--small");
                div.classList.add("border-style");

                let upperDiv = document.createElement("div");
                upperDiv.classList.add("race-info-box-upper-content");

                if (race.name === "KfS Kungsholmen Runt") {
                  div.classList.add("highlighted-box");
                  let highlightText = document.createElement("div");
                  highlightText.classList.add(
                    `highlight-text-box-${race.type}`
                  );
                  highlightText.textContent = `featured ${race.type} race`;
                  div.appendChild(highlightText);
                }

                let dateP = document.createElement("p");
                dateP.classList.add("race-date");

                // Convert YYYYMMDD string to Date object
                const year = race.date.substring(0, 4);
                const month = race.date.substring(4, 6);
                const day = race.date.substring(6, 8);

                //Convert to date
                const raceDate = new Date(`${year}-${month}-${day}`);
                let options = { day: "numeric", month: "short" };
                const raceDateString = raceDate.toLocaleDateString(
                  "sv-SE",
                  options
                );
                dateP.textContent = `${raceDateString}`;

                let divText = document.createElement("div");
                divText.classList.add("race-text-box");
                divText.classList.add("margin-bottom--tiny");

                let nameP = document.createElement("p");
                nameP.classList.add("race-name");

                nameP.textContent = `${race.name}`;

                let typeDiv = document.createElement("div");
                typeDiv.classList.add("race-type-box");
                typeDiv.classList.add("margin-bottom--tiny");

                let typeIcon = document.createElement("div");
                typeIcon.classList.add(`text-icon-${race.type}`);

                let typeP = document.createElement("p");
                typeP.classList.add("race-type");
                typeP.textContent = `${race.type}`;

                let distanceP = document.createElement("p");
                distanceP.classList.add("race-distance");
                if (!isNaN(race.distance_m)) {
                  distanceP.textContent = `Distanser: ${
                    race.distance_m / 1000
                  } k`;
                }

                let websiteA = document.createElement("a");
                websiteA.classList.add("race-website");
                websiteA.href = race.website;
                websiteA.target = "_blank";

                websiteA.textContent = "Mer info";

                let summary = document.createElement("div");
                summary.classList.add("race-info-summary");
                let summaryP = document.createElement("p");
                summaryP.classList.add("race-info-summary-content");
                summaryP.innerHTML = `${race.summary}`;
                console.log("race.summary");
                console.log(race.summary);

                upperDiv.appendChild(dateP);
                upperDiv.appendChild(divText);
                divText.appendChild(nameP);
                divText.appendChild(typeDiv);
                typeDiv.appendChild(typeIcon);
                typeDiv.appendChild(typeP);

                divText.appendChild(distanceP);
                upperDiv.appendChild(websiteA);

                div.appendChild(upperDiv);

                summary.appendChild(summaryP);
                div.appendChild(summary);

                container.appendChild(div);
              }
            }
          });
          /*scroll down so we see markers*/
          smoothScrollDown();
          /*Adding event listeners to the boxes*/
          const raceInfoBoxes = document.querySelectorAll(".race-info-box");
          raceInfoBoxes.forEach((raceInfoBox) => {
            raceInfoBox.addEventListener("click", toggleBoxExpansion);
          });
        });
      }
    });
  });

/* Adding functionality for enlarging markers on zoom */
enlargeMarkersOnZoom(map);
