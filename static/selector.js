/**
 * Creates the selectors for the chart and updates the chart based on the
 * selected values.
 * @param {string} chartId The id of the chart being drawn.
 * @param {function} colorScale A d3 colorscale used for the line colors.
 * @param {Set} zones A list of the unique zones for the chart.
 */
const selectors = async (chartId, colorScale, zones) => {
  const modes = ["Default", "K-means", "DBSCAN", "K-means-constrained", "Zone"];
  const similarity = ["Correlation", "Proximity"];
  const encoding = ["None", "One-Hot"];
  const outlier = ["Off", "On"];
  clusters = ["All"];
  allZones = ["All"].concat(zones);
  const filterBy = ["Cluster", "Zone"];
  updateSelector("mode", modes);
  updateSelector("similarity", similarity);
  updateSelector("encoding", encoding);
  updateSelector("outlier", outlier);
  updateSelector("cluster", clusters);
  updateSelector("filter", filterBy);
  d3.select("select#" + "mode" + "Selector").on("change", updateChart);
  d3.select("select#" + "similarity" + "Selector").on("change", updateChart);
  d3.select("select#" + "encoding" + "Selector").on("change", updateChart);
  d3.select("select#" + "outlier" + "Selector").on("change", updateChart);
  d3.select("select#" + "cluster" + "Selector").on("change", updateCluster);
  d3.select("select#" + "filter" + "Selector").on("change", updateFilter);

  /**
   * Updates the chart according to the values of the selectors.
   */
  async function updateChart() {
    const currentMode = d3.select("select#modeSelector").property("value");
    const currentSimilarity = d3.select("select#similaritySelector")
        .property("value");
    const currentEncoding = d3.select("select#encodingSelector")
        .property("value");
    const currentOutlier = d3.select("select#outlierSelector")
        .property("value");
    updateSelector("cluster", ["All"]);
    updateCluster();
    if (currentMode == "Default") {
      d3.selectAll(".timeSeries")
          .attr("stroke", (d) => colorScale(d))
          .attr("opacity", 1);
      clusters = ["All"];
      updateFilter();
    } else {
      try {
        let query = currentMode + "/" + currentSimilarity + "/" +
        currentEncoding + "/" + currentOutlier + "/" + chartId;
        if (currentMode == "Zone") {
          query = query + "/" + "zone";
        }
        const response = await callFetch("clustering/" + query.toLowerCase());
        if (response.status >= 200 && response.status <= 299) {
          const clusterAssignment = await response.json();
          const labels = Object.values(clusterAssignment["cluster_labels"]);
          labels.forEach((elt, index) => {
            const classes = d3.select("#id" + index).attr("class");
            const indexCluster = classes.lastIndexOf(" ");
            d3.selectAll("#id" + index)
                .attr("stroke", () => {
                  if (elt < 0) {
                    return "#737373";
                  } else {
                    return colorScale(elt);
                  }
                })
                .attr("class", classes.substring(0, indexCluster) +
                              " cluster-" + elt);
          });
          if (Number.isInteger(labels[0])) {
            const uniqueClusters = labels.map((elt) => Math.abs(elt));
            clusters = ["All"].concat(Array.from(new Set(uniqueClusters)))
                .sort((a, b) => a-b);
          } else {
            clusters = ["All"].concat(Array.from(new Set(labels))).sort();
          }
          updateFilter();
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
  const currentFilter = d3.select("select#filterSelector").property("value");
  const currentCluster = d3.select("select#clusterSelector").property("value");

  d3.selectAll(".timeSeries")
      .attr("opacity", 0);

  if (currentCluster == "All") {
    d3.selectAll(".timeSeries")
        .attr("opacity", 1);
  } else if (currentFilter == "Cluster") {
    d3.selectAll(".cluster-" + currentCluster)
        .attr("opacity", 1);
    d3.selectAll(".cluster--" + currentCluster)
        .attr("opacity", 1);
  } else {
    d3.selectAll("." + currentCluster)
        .attr("opacity", 1);
  }
}

/**
 * Based on the filter selector value, updates the cluster selector and the
 * clusters shown on the chart.
 */
function updateFilter() {
  const currentFilter = d3.select("select#filterSelector").property("value");
  d3.select("select#clusterSelector").property("value", "All");

  if (currentFilter == "Cluster") {
    updateSelector("cluster", clusters);
  } else {
    updateSelector("cluster", allZones);
  }
  updateCluster();
}
