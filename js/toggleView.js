import { filterRaces } from "/js/filterRaces.js";

// Get references to the buttons and header elements
const listViewButton = document.querySelector(".list-view-button");
const mapViewButton = document.querySelector(".map-view-button");
const listHeader = document.querySelector(".list-header");
const mapHeader = document.querySelector(".map-header");

// Add event listeners to the buttons
listViewButton.addEventListener("click", toggleActiveClass);
mapViewButton.addEventListener("click", toggleActiveClass);

// Define the toggleActiveClass function
function toggleActiveClass(event) {
  // Prevent the default button behavior (e.g. page refresh)
  event.preventDefault();

  // Toggle the "active-button" class on both buttons
  listViewButton.classList.toggle("active-button");
  mapViewButton.classList.toggle("active-button");

  // Toggle the display of the header elements
  if (listViewButton.classList.contains("active-button")) {
    listHeader.style.display = "block";
    mapHeader.style.display = "none";

    const filterSection = document.querySelector(".filter-section");

    // Collapse the map
    map.style.height = "0";
    setTimeout(function () {
      map.style.border = "solid 1px #555";
    }, 300);

    /* test */

    filterRaces();

    // add county filter
    const countySelector = document.getElementById("county-selector");
    countySelector.style.display = "block";
    const element = document.querySelector(".map-or-list-view");
    element.style.width = "40rem";
    element.style.paddingRight = "10rem";

    /*     // Add an event listener to the selector
    countySelector.addEventListener("change", () => {
      // Get the selected county
      const selectedCounty = countySelector.value;

      // Filter the races by county
      const filteredRaces = races.filter((race) => {
        return race.county === selectedCounty;
      });

      // Update the display with the filtered races
      displayRaces(filteredRaces);
    }); */

    /* end test */
  } else {
    listHeader.style.display = "none";
    mapHeader.style.display = "block";
    const countySelector = document.getElementById("county-selector");
    countySelector.style.display = "none";
    const element = document.querySelector(".map-or-list-view");
    element.style.width = "20rem";
    element.style.paddingRight = "0";
    // Open up the map again
    map.style.height = "70rem";
    map.style.border = "solid #333 2px";
    //drop racecontainer content
    const raceInfoBoxes = document.querySelectorAll(".race-info-box");
    raceInfoBoxes.forEach((raceInfoBox) => {
      raceInfoBox.style.display = "none";
    });
  }
}
