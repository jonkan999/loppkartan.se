export function filterMarkersOnDistance(minDistance, maxDistance) {
  // Fetch all_races.json and parse it into a JavaScript object
  fetch("all_races.json")
    .then((response) => response.json())
    .then((allRaces) => {
      // Get all marker icons
      let markerIcons = document.getElementsByClassName("leaflet-marker-icon");
      console.log("works");
      // Loop through all marker icons and get all the distance_m arrays from allRaces
      for (let i = 0; i < markerIcons.length; i++) {
        // Get distance date from marker
        const distanceM = markerIcons[i]
          .querySelector("div")
          .getAttribute("data-marker-distance_m");
        const distanceArr = distanceM.split(", ").map((x) => parseInt(x));
        let isInRange = false;
        for (let j = 0; j < distanceM.length; j++) {
          if (
            distanceArr[j] >= minDistance * 1000 &&
            distanceArr[j] <= maxDistance * 1000
          ) {
            isInRange = true;
            break;
          }
        }
        // If none of the values in distance_m is between minDistance and maxDistance, add "hideMarkerOnDays" to markerIcons[i].classList
        if (!isInRange) {
          markerIcons[i].classList.add("hideMarkerOnDays");
        } else {
          // Otherwise, remove "hideMarkerOnDays" from markerIcons[i].classList
          markerIcons[i].classList.remove("hideMarkerOnDays");
        }
      }
    })
    .catch((error) => console.error(error));
}
