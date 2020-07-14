/**
 * Creates the selectors for the chart and updates the chart based on the 
 * selected values.
 */
const selectors = async (url, chartId, colorScale) => {
    let modes = ["Default", "K-means", "DBSCAN"];
    let similarity = ["Correlation", "Proximity"];
    createSelector("mode", modes);
    createSelector("similarity", similarity);

    async function updateChart() {
        let currentMode = modeSelector.property("value");
        let currentSimilarity =  similaritySelector.property("value");

        if (currentMode == "Default"){
            d3.selectAll(".timeSeries")
                .attr("stroke", (d) => colorScale(d))
                .attr("opacity", 1);
        } else {
            let currentMode = d3.select("select#modeSelector");
            let currentSimilarity = d3.select("select#similaritySelector");
            let query = currentMode + "/" + currentSimilarity + "/" + chartId;
            let response = await fetch(url + "clustering/" + query);
            if (response.status >= 200 && response.status <= 299){
                const data = await response.json();
                data.forEach((elt,index) => {
                    d3.selectAll("#id" +index)
                        .attr("stroke", colorScale(elt));
                })
            } else {
                showError(response.status);
            }
        }
    }

    function createSelector(name, options){
        let selector = d3.select("select#"+ name + "Selector");
        selector.selectAll("option")
                .data(options)
                .enter()
                .append("option")
                .attr("value", (d) => d)
                .text((d) => d);

        selector.on("change", updateChart);
    }
}