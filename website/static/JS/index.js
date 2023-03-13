// alert("testing");

var owl = $(".owl-carousel");
owl.owlCarousel({
  dots: false,
  items: 1,
  loop: true,
  margin: 0,
  autoWidth: true,
  autoplay: true,
  autoplayTimeout: 1000,
  autoplayHoverPause: true,
  center: true,
});
$(".play").on("click", function () {
  owl.trigger("play.owl.autoplay", [1000]);
});
$(".stop").on("click", function () {
  owl.trigger("stop.owl.autoplay");
});
// Mimics Haskell's currying and partial application
Function.prototype.curry = function (...curriedArgs) {
  const target = this;
  return function (...restArgs) {
    return target.call(this, ...curriedArgs, ...restArgs);
  };
};

// init Isotope
var $grid = $(".grid").isotope({
  itemSelector: ".element-item",
  layoutMode: "fitRows",
});
// filter functions

function filter(min, max, findingClass) {
  var number = $(this).find(findingClass).text();
  console.log(number);
  return parseInt(number, 10) > min && parseInt(number, 10) <= max;
}

var filterFns = {
  // show if number is greater than 50
  capacity_0_49: function () {
    return filter.curry(0, 49, ".guest_capacity");
    // var number = $(this).find(".guest_capacity").text();
    // return parseInt(number, 10) > 0 && parseInt(number, 10) <= 49;
  },
  capacity_50_99: function () {
    var number = $(this).find(".guest_capacity").text();
    return parseInt(number, 10) >= 50 && parseInt(number, 10) <= 99;
  },
  capacity_100_249: function () {
    return filter.curry(100, 249, ".guest_capacity");
    // var number = $(this).find(".guest_capacity").text();
    // return parseInt(number, 10) >= 100 && parseInt(number, 10) <= 249;
  },
  capacity_250_499: function () {
    var number = $(this).find(".guest_capacity").text();
    return parseInt(number, 10) >= 250 && parseInt(number, 10) <= 499;
  },
  capacity_500_999: function () {
    var number = $(this).find(".guest_capacity").text();
    return parseInt(number, 10) >= 500 && parseInt(number, 10) <= 999;
  },
  capacity_over_1000: function () {
    var number = $(this).find(".guest_capacity").text();
    // console.log(number);
    return parseInt(number, 10) >= 1000;
  },
  worth_50_499: function () {
    var number = $(this).find(".worth").text();
    return parseInt(number, 10) > 50 && parseInt(number, 10) < 499;
  },
  worth_500_4999: function () {
    var number = $(this).find(".worth").text();
    return parseInt(number, 10) > 500 && parseInt(number, 10) < 4999;
  },
  worth_5000_24999: function () {
    var number = $(this).find(".worth").text();
    return parseInt(number, 10) > 5000 && parseInt(number, 10) < 24999;
  },
  worth_25000: function () {
    var number = $(this).find(".worth").text();
    return parseInt(number, 10) > 25000;
  },
};
// bind filter button click
$(".filters-button-group").on("click", "button", function () {
  var filterValue = $(this).attr("data-filter");
  // use filterFn if matches value
  filterValue = filterFns[filterValue] || filterValue;
  $grid.isotope({
    filter: filterValue,
  });
});
// change is-checked class on buttons
$(".button-group").each(function (i, buttonGroup) {
  var $buttonGroup = $(buttonGroup);
  $buttonGroup.on("click", "button", function () {
    $buttonGroup.find(".is-checked").removeClass("is-checked");
    $(this).addClass("is-checked");
  });
});

// $("#register_checkbox").change(function () {
//   if ($(this).is(":checked")) {
//     alert("checked");
//   }
// });

/* --- events --- */

// Mimics Haskell's currying and partial application
Function.prototype.curry = function(...curriedArgs) {
    const target = this;
    return function(...restArgs) {
        return target.call(this, ...curriedArgs, ...restArgs);
    };
};

// Functions to apply for each sort type
let eventSorts = {
    date: function(element) {
        let date = $(element).find(".card-date").text();
        let match = /^(?<date>[a-zA-Z]{3,4}\. \d{1,2}, \d{4,})(?:, (?<time>.+))?$/g.exec(date);
        console.log(match.groups["date"])
        return Date.parse(match.groups["date"].replaceAll(".", ""));
    },
    name: function(element) {
        return $(element).find(".card-title").text();
    },
    topic: function(element) {
        return $(element).find(".topic").text();
    },
    type: function(element) {
        console.log($(element).find(".type").text())
        return $(element).find(".type").text();
    },
};

// Initialise card grid isotope
let grid = $(".d-flex flex-wrap").isotope({
    itemSelector: ".grid-element",
    getSortData: {
        date: eventSorts["date"],
        name: eventSorts["name"],
        topic: eventSorts["topic"],
        type: eventSorts["type"],
    },
    sortBy: "date",
    layoutMode: "fitRows",
});

let sortDropdowns = $(".sort-dropdown");

// Apply sort when dropdown is selected
sortDropdowns.on("change", function(event) {
    let select = $(this);
    let sortValue = select.val();
    if (sortValue === "any")
    {
        select.val("title");
        sortValue = "original-order";
    }
    grid.isotope({
        sortBy: sortValue,
    });
})

// Functions to apply for each filter category
let eventFilters = {
    status: function(filterValue) {
        return filterValue === "any" ? true : $(this).find(".status").text().toLowerCase() === filterValue;
    },
    type: function(filterValue) {
        return filterValue === "any" ? true : $(this).find(".type").text().toLowerCase() === filterValue;
    },
    worth: function(filterValue) {
        return filterValue === "any" ? true : filterByAmount(parseInt($(this).find(".worth").text().replaceAll(",", "")), filterValue);
    },
    capacity: function(filterValue) {
        return filterValue === "any" ? true : filterByAmount(parseInt($(this).find(".capacity").text().replaceAll(",", "")), filterValue);
    },
};

let filterDropdowns = $(".filter-dropdown");
let search = $(".search");

// Apply filter when "enter" is pressed in searchbar
search.on("keypress", function(event) {
    if (event.key !== "Enter")
    {
        return;
    }
    filterDropdowns.val("title");
    grid.isotope({
        filter: filterByName.curry($(this)[0].value),
    })
});

// Apply filter when dropdown is selected
filterDropdowns.on("change", function(event)
{
    let select = $(this);
    let filterName = select.attr("name");
    let filterValue = select.val();
    search.val("")
    filterDropdowns.val("title");
    select.val(filterValue === "any" ? "title" : filterValue);
    grid.isotope({
        filter: eventFilters[filterName].curry(filterValue),
    });
});

// Filter by an amount range
function filterByAmount(actualValue, filterValue)
{
    let rangeRegex = /(\d+) - (\d+)/;
    let unboundedRegex = /(\d+) \+/;
    let range = filterValue.match(rangeRegex);
    if (range)
    {
        return parseInt(range[1], 10) <= actualValue && actualValue < parseInt(range[2], 10);
    }
    let unbounded = filterValue.match(unboundedRegex);
    if (unbounded)
    {
        return actualValue >= parseInt(unbounded[1], 10);
    }
    return false;
}

// Filter by name
function filterByName(filterName)
{
    if (filterName === "")
    {
        return true;
    }
    filterName = filterName.toLowerCase();
    let card = $(this);
    let title = card.find(".card-title").text().toLowerCase();
    let topic = card.find(".card-info.topic").text().toLowerCase();
    return title.includes(filterName) || topic.includes(filterName);
}