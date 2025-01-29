document.addEventListener("DOMContentLoaded", function () {
    // Select necessary elements
    const heightUnit = document.getElementById("height_unit");
    const usHeight = document.getElementById("us-height");
    const metricHeight = document.getElementById("metric-height");


    // Function to handle height unit change
    function onHeightUnitChange() {
        if (heightUnit.value === "US") {
            usHeight.style.display = "flex";
            metricHeight.style.display = "none";
        } else if (heightUnit.value === "METRIC") {
            usHeight.style.display = "none";
            metricHeight.style.display = "flex";
        }
    }


    // Attach change event listener
    heightUnit.addEventListener("change", onHeightUnitChange);


    // Initialize visibility state on page load
    onHeightUnitChange();

});

