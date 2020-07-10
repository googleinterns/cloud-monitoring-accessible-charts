/**
 * Creates the selectors for the chart and updates the chart based on the 
 * selected values.
 */
const selectors = async (url, chartId, colorScale) => {
    let modes = ["Default", "K-means", "DBSCAN"];
    let modeSelector = d3.select("select#modeSelector");
    modeSelector.selectAll("option")
        .data(modes)
        .enter()
        .append("option")
        .attr("value", (d) => d)
        .text((d) => d);

    modeSelector.on("change", updateChart);

    let similarity = ["Correlation", "Proximity"];
    let similaritySelector = d3.select("select#similaritySelector");
    similaritySelector.selectAll("option")
        .data(similarity)
        .enter()
        .append("option")
        .attr("value", (d) => d)
        .text((d) => d);

    similaritySelector.on("change", updateChart);

    async function updateChart() {
        let currentMode = modeSelector.property("value");
        let currentSimilarity =  similaritySelector.property("value");

        if (currentMode == "Default"){
            d3.selectAll(".timeSeries")
                .attr("stroke", (d) => colorScale(d));
        } else {
            let response = await fetch(url + currentMode + "/" + currentSimilarity + "/" + chartId);
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
}