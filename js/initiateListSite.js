import { filterRaces } from "/js/filterRaces.js";
filterRaces();

//Fix som padding and margins
// If the window size is narrower than 704px, apply the media query style
const checkboxes = document.querySelector(".checkboxes");

const filterSection = document.querySelector(".filter-section");
// Check if the window size is narrower than 704px
const mediaQuery = window.matchMedia("(max-width: 704px)");
if (mediaQuery.matches) {
  // Your media query style here
  filterSection.style.marginTop = "6rem";
  checkboxes.style.marginTop = "-4rem";
} else {
  filterSection.style.marginTop = "3rem";
}
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
