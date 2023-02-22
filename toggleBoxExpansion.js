export function toggleBoxExpansion(event) {
  const raceInfoBox = event.currentTarget;
  const summaryDiv = raceInfoBox.querySelector(".race-info-summary");
  const currentPosition = window.pageYOffset;

  raceInfoBox.classList.toggle("race-info-box--expanded");
  summaryDiv.classList.toggle("show-div");

  /*   if (raceInfoBox.classList.contains("race-info-box--expanded")) {
    const boxBottom = raceInfoBox.getBoundingClientRect().bottom + 300;
    const windowHeight = window.innerHeight;
    console.log(windowHeight);
    console.log(boxBottom);
    if (boxBottom > windowHeight) {
      const scrollDistance = boxBottom - windowHeight + 10;
      window.scrollBy({
        top: scrollDistance,
        behavior: "smooth",
      });
      window.lastScroll = scrollDistance;
    }
  } else {
    console.log("here");
    const boxBottom = raceInfoBox.getBoundingClientRect().bottom - 300;
    const windowHeight = window.innerHeight;
    if (boxBottom < windowHeight) {
      const scrollDistance = boxBottom - windowHeight + 100;
      window.scrollBy({
        top: scrollDistance,
        behavior: "smooth",
      });
    }
  } */
}
