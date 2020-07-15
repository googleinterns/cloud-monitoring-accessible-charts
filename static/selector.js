/**
 * Creates the selectors for the chart and updates the chart based on the 
 * selected values.
 */
const selectors = async (url, chartId, colorScale) => {
    let modes = ["Default", "K-means", "DBSCAN"];
    let similarity = ["Correlation", "Proximity"];
    let clusters = ["All"];
    createSelector("mode", modes);
    createSelector("similarity", similarity);
    createSelector("cluster", clusters);

    async function updateChart() {
        let currentMode = d3.select("select#modeSelector").property("value");
        let currentSimilarity = d3.select("select#similaritySelector")
            .property("value");
        if (currentMode == "Default"){
            d3.selectAll(".timeSeries")
                .attr("stroke", (d) => colorScale(d))
                .attr("opacity", 1);
        } else {
            let query = currentMode + "/" + currentSimilarity + "/" + chartId;
            let response = await fetch(url + "clustering/" + query);
            if (response.status >= 200 && response.status <= 299){
                const data = await response.json();
                data.forEach((elt,index) => {
                    d3.selectAll("#id" +index)
                        .attr("stroke", colorScale(elt))
                        .attr("class", "timeSeries " + "cluster-All " + 
                            "cluster-" + elt);
                });
                clusters = ["All"].concat(Array.from(new Set(data)))
                    .sort((a,b) => a-b)
                let selector = d3.select("select#"+ "cluster" + "Selector");
                selector.selectAll("option")
                        .data(clusters)
                        .enter()
                        .append("option")
                        .attr("value", (d) => d)
                        .text((d) => d);

                selector.on("change", updateCluster);

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

    function updateCluster(){
        let currentCluster = d3.select("select#clusterSelector")
            .property("value");

        d3.selectAll(".timeSeries")
                .attr("stroke", (d) => colorScale(d))
                .attr("opacity", 0);

        d3.selectAll(".cluster-" + currentCluster)
                .attr("stroke", (d) => colorScale(d))
                .attr("opacity", 1);
    }
}