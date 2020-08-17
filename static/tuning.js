/**
 * Draws a graph for each shart, showing the results of the tuning algorithm.
 * @param {string} mode The algorithm for which a paramter is being tuned.
 * @param {string} similarity The similarity measure used for clustering.
 * @param {string} encoding The encoding for the labels.
 */
const tuning = async (mode, similarity, encoding) => {
  const chartIds = ["002"];
  const xLabel = {"dbscan": "time series", "k-means": "k"};
  const yLabel = {"dbscan": "distance to nearest neighbor", "k-means":
    "sum of squared distances"};

  for (let index = 0; index < chartIds.length; index++) {
    try {
      const response = await callFetch("tuning/" + mode + "/" + similarity +
      "/" + encoding + "/" + chartIds[index]);
      const distances = await response.json();

      const points = distances.map((elt, index) => index+1);

      d3.select("body")
          .append("div")
          .attr("style", "width:300px;height:300px")
          .attr("id", "tuningChart" + chartIds[index] + similarity);

      const chart = document.getElementById('tuningChart' + chartIds[index] +
      similarity);

      Plotly.newPlot(chart, [{x: points, y: distances}],
          {margin: {t: 30, l: 50, b: 80, r: 20}, title: mode + "-" + similarity,
            xaxis: {title: xLabel[mode]}, yaxis: {title: yLabel[mode]}});
    } catch (error) {
      showError(error);
    }
  }
};

tuning("k-means", "correlation", "none");
