// Get references to the buttons
const listViewButton = document.querySelector(".list-view-button");
const mapViewButton = document.querySelector(".map-view-button");

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
}
