document.addEventListener("DOMContentLoaded", function () {
    const weightUnit = document.getElementById("weight_unit");
    const usWeight = document.getElementById("weight_us");
    const metricWeight = document.getElementById("weight_metric");


    function onWeightUnitChange() {
        if (weightUnit.value === "US") {
            usWeight.style.display = "flex";
            metricWeight.style.display = "none";
        } else if (weightUnit.value === "METRIC") {
            usWeight.style.display = "none";
            metricWeight.style.display = "flex";
        }
    }

    weightUnit.addEventListener("change", onWeightUnitChange);
    onWeightUnitChange();

});