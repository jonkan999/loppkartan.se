import { filterMarkersOnDays } from "/filterMarkersOnDays.js";

$(function () {
  $("#sliderDays").slider({
    range: true,
    min: 0,
    max: 230,
    values: [0, 100],
    slide: function (event, ui) {
      let now = new Date();
      let dayInMilliseconds = 24 * 60 * 60 * 1000;
      let startDay = $("#sliderDays").slider("values", 0);
      let endDay = $("#sliderDays").slider("values", 1);
      let startDate = new Date(now.getTime() + startDay * dayInMilliseconds);
      let endDate = new Date(now.getTime() + endDay * dayInMilliseconds);

      let options = { day: "numeric", month: "short" };
      let startDateString = startDate.toLocaleDateString("sv-SE", options);
      let endDateString = endDate.toLocaleDateString("sv-SE", options);

      $("#daysFilterText").val(startDateString + " - " + endDateString);

      // Use the startDay and endDay values for the downstream function
      filterMarkersOnDays(startDay, endDay);
    },
  });
  let now = new Date();
  let dayInMilliseconds = 24 * 60 * 60 * 1000;
  let startDate = new Date(
    now.getTime() + $("#sliderDays").slider("values", 0) * dayInMilliseconds
  );
  let endDate = new Date(
    now.getTime() + $("#sliderDays").slider("values", 1) * dayInMilliseconds
  );

  let startDay = $("#sliderDays").slider("values", 0);
  let endDay = $("#sliderDays").slider("values", 1);

  let options = { day: "numeric", month: "short" };
  let startDateString = startDate.toLocaleDateString("sv-SE", options);
  let endDateString = endDate.toLocaleDateString("sv-SE", options);
  filterMarkersOnDays(startDay, endDay);
  $("#daysFilterText").val(startDateString + " - " + endDateString);
});
