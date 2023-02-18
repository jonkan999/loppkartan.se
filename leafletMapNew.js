/* Initializing leaflet map map */

let map = L.map("map").setView([62.346972, 15.748689], 5.4);
window.globalMap = map;
L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
  {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }
).addTo(map);

/* Adding markers to the map */
let markers = [];

fetch("all_races.json")
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
            iconSize: [25, 25],
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

                div.appendChild(dateP);
                div.appendChild(divText);
                divText.appendChild(nameP);
                divText.appendChild(typeDiv);
                typeDiv.appendChild(typeIcon);
                typeDiv.appendChild(typeP);

                divText.appendChild(distanceP);
                div.appendChild(websiteA);

                container.appendChild(div);
              }
            }
          });
        });
      }
    });
  });
