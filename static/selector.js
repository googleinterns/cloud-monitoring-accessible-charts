/**
 * Creates the selectors for the chart and updates the chart based on the
 * selected values.
 * @param {string} url The url for the application.
 * @param {string} chartId The id of the chart being drawn.
 * @param {*} colorScale A d3 colorscale used for the line colors.
 */
const selectors = async (url, chartId, colorScale) => {
  const modes = ["Default", "K-means", "DBSCAN"];
  const similarity = ["Correlation", "Proximity"];
  let clusters = ["All"];
  createSelector("mode", modes);
  createSelector("similarity", similarity);
  createSelector("cluster", clusters);

  /**
   * Updates the chart according to the values of the selectors.
   */
  async function updateChart() {
    const currentMode = d3.select("select#modeSelector").property("value");
    const currentSimilarity = d3.select("select#similaritySelector")
        .property("value");
    d3.select("select#clusterSelector").property("value", "All");
    updateCluster();

    if (currentMode == "Default") {
      d3.selectAll(".timeSeries")
          .attr("stroke", (d) => colorScale(d))
          .attr("opacity", 1);
    } else {
      const query = currentMode + "/" + currentSimilarity + "/" + chartId;
      const response = await fetch(url + "clustering/" + query);
      if (response.status >= 200 && response.status <= 299) {
        const data = await response.json();
        data.forEach((elt, index) => {
          d3.selectAll("#id" +index)
              .attr("stroke", colorScale(elt))
              .attr("class", "timeSeries " + "cluster-All " +
                            "cluster-" + elt);
        });
        clusters = ["All"].concat(Array.from(new Set(data)))
            .sort((a, b) => a-b);
        const selector = d3.select("select#"+ "cluster" + "Selector");
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

  /**
   * Update the selector element called name with options.
   * @param {string} name The name of the selector element.
   * @param {Array} options The options of the selector element.
   */
  function createSelector(name, options) {
    const selector = d3.select("select#"+ name + "Selector");
    selector.selectAll("option")
        .data(options)
        .enter()
        .append("option")
        .attr("value", (d) => d)
        .text((d) => d);

    selector.on("change", updateChart);
  }

  /**
   * Updates the chart to show the selected cluster.
   */
  function updateCluster() {
    const currentCluster = d3.select("select#clusterSelector")
        .property("value");

    d3.selectAll(".timeSeries")
        .attr("stroke", (d) => colorScale(d))
        .attr("opacity", 0);

    d3.selectAll(".cluster-" + currentCluster)
        .attr("stroke", (d) => colorScale(d))
        .attr("opacity", 1);
  }
};
