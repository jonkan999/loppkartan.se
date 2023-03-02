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
  console.log(event.target);
  // Prevent the default button behavior (e.g. page refresh)
  event.preventDefault();
  if (event.target.classList.contains("active-button")) {
    /* if clicked already ActiveXObject, no nothin */
    return;
  }
  // Toggle the "active-button" class on both buttons
  listViewButton.classList.toggle("active-button");
  mapViewButton.classList.toggle("active-button");

  // Toggle the display of the header elements
  if (listViewButton.classList.contains("active-button")) {
    listHeader.style.display = "block";
    mapHeader.style.display = "none";

    const checkboxes = document.querySelector(".checkboxes");

    const filterSection = document.querySelector(".filter-section");
    // Check if the window size is narrower than 704px
    const mediaQuery = window.matchMedia("(max-width: 704px)");

    // If the window size is narrower than 704px, apply the media query style
    if (mediaQuery.matches) {
      // Your media query style here
      filterSection.style.marginTop = "6rem";
      checkboxes.style.marginTop = "-4rem";
    } else {
      filterSection.style.marginTop = "3rem";
    }

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
    setTimeout(function () {
      countySelector.style.opacity = "1";
    }, 10);

    const element = document.querySelector(".map-or-list-view");
    element.style.width = "32rem";
    element.style.paddingRight = "8rem";

    countySelector.addEventListener("change", function () {
      filterRaces();
    });
  } else {
    listHeader.style.display = "none";
    mapHeader.style.display = "block";
    const countySelector = document.getElementById("county-selector");
    countySelector.style.opacity = "0";
    const checkboxes = document.querySelector(".checkboxes");
    setTimeout(function () {
      countySelector.style.display = "none";
      const element = document.querySelector(".map-or-list-view");
      element.style.width = "16rem";
      element.style.paddingRight = "0";
      checkboxes.style.marginTop = "0rem";
    }, 200);

    // Open up the map again
    map.style.height = "50rem";
    map.style.border = "solid #333 2px";
    //drop racecontainer content
    const raceInfoBoxes = document.querySelectorAll(".race-info-box");
    raceInfoBoxes.forEach((raceInfoBox) => {
      raceInfoBox.style.display = "none";
    });
    const filterSection = document.querySelector(".filter-section");
    setTimeout(function () {
      filterSection.style.marginTop = "0";
    }, 200);

    //Turn off all months each time, maybe a more efficient way of doing this?
    const monthNames = document.querySelectorAll(".month-name");
    monthNames.forEach((monthName) => {
      monthName.style.display = "none";
    });
  }
}
