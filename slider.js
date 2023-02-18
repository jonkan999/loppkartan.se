import { filterMarkersOnDays } from "/filterMarkersOnDays.js";

$.event.special.swipe = {
  setup: function () {
    var thisObject = this;
    var $this = $(thisObject);

    $this
      .bind("touchstart", function (event) {
        var data = event.originalEvent.touches
          ? event.originalEvent.touches[0]
          : event;
        start = {
          time: new Date().getTime(),
          coords: [data.pageX, data.pageY],
          origin: $(event.target),
        };
      })
      .bind("touchmove", function (event) {
        var data = event.originalEvent.touches
          ? event.originalEvent.touches[0]
          : event;
        if (!start) {
          return;
        }
        var end = {
          time: new Date().getTime(),
          coords: [data.pageX, data.pageY],
        };
        var deltaX = end.coords[0] - start.coords[0];
        var deltaY = end.coords[1] - start.coords[1];
        if (Math.abs(deltaX) > 30) {
          $this
            .trigger("swipe")
            .trigger(
              start.coords[0] > end.coords[0] ? "swipeleft" : "swiperight"
            );
          start = null;
        } else if (Math.abs(deltaY) > 30) {
          $this
            .trigger("swipe")
            .trigger(start.coords[1] > end.coords[1] ? "swipeup" : "swipedown");
          start = null;
        }
      })
      .bind("touchend", function (event) {
        if (start) {
          $this.trigger("tap");
        }
        start = null;
      });
  },
};

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
