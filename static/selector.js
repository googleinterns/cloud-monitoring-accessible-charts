/* eslint-disable quotes */
/**
 * Creates the selectors for the chart and updates the chart based on the
 * selected values.
 * @param {string} chartId The id of the chart being drawn.
 * @param {function} colorScale A d3 colorscale used for the line colors.
 */
const selectors = async (chartId, colorScale) => {
  const modes = ["Default", "K-means", "DBSCAN", "Zone"];
  const similarity = ["Correlation", "Proximity"];
  const encoding = ["None", "One-Hot"];
  let clusters = ["All"];
  updateSelector("mode", modes);
  updateSelector("similarity", similarity);
  updateSelector("encoding", encoding);
  updateSelector("cluster", clusters);
  d3.select("select#" + "mode" + "Selector").on("change", updateChart);
  d3.select("select#" + "similarity" + "Selector").on("change", updateChart);
  d3.select("select#" + "encoding" + "Selector").on("change", updateChart);
  d3.select("select#" + "cluster" + "Selector").on("change", updateCluster);

  /**
   * Updates the chart according to the values of the selectors.
   */
  async function updateChart() {
    const currentMode = d3.select("select#modeSelector").property("value");
    const currentSimilarity = d3.select("select#similaritySelector")
        .property("value");
    const currentEncoding = d3.select("select#encodingSelector")
        .property("value");
    updateSelector("cluster", ["All"]);
    updateCluster();
    if (currentMode == "Default") {
      d3.selectAll(".timeSeries")
          .attr("stroke", (d) => colorScale(d))
          .attr("opacity", 1);
    } else {
      try {
        let query = currentMode + "/" + currentSimilarity + "/" +
        currentEncoding + "/" + chartId;
        if (currentMode == "Zone") {
          query = query + "/" + "zone";
        }
        const response = await callFetch("clustering/" + query.toLowerCase());
        if (response.status >= 200 && response.status <= 299) {
          const clusterAssignment = await response.json();
          const labels = Object.values(clusterAssignment["cluster_labels"]);
          labels.forEach((elt, index) => {
            d3.selectAll("#id" + index)
                .attr("stroke", colorScale(elt))
                .attr("class", "timeSeries " + "cluster-All " +
                              "cluster-" + elt);
          });
          if (Number.isInteger(labels[0])) {
            clusters = ["All"].concat(Array.from(new Set(labels)))
                .sort((a, b) => a-b);
          } else {
            clusters = ["All"].concat(Array.from(new Set(labels))).sort();
          }
          updateSelector("cluster", clusters);
        } else {
          showError(response.status);
        }
      } catch (error) {
        showError(error);
      }
    }
  }
};

/**
 * Update the selector element called name with options.
 * @param {string} name The name of the selector element.
 * @param {Array} options The options of the selector element.
 */
function updateSelector(name, options) {
  const selector = d3.select("select#" + name + "Selector");
  selector.selectAll("option")
      .data(options)
      .join("option")
      .attr("value", (d) => d)
      .text((d) => d);
}

/**
 * Updates the chart to show the selected cluster.
 */
function updateCluster() {
  const currentCluster = d3.select("select#clusterSelector")
      .property("value");

  d3.selectAll(".timeSeries")
      .attr("opacity", 0);

  d3.selectAll(".cluster-" + currentCluster)
      .attr("opacity", 1);
}
