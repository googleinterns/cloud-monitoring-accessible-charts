/**
 * Fetches the frequency data for the selected chart and plots the data in a
 * heatmap.
 * @param {string} chartId The id of the data being fetched and drawn.
 * @param {string} algorithm The algorithm run on the data.
 * @param {string} similarity The similairty measure used for clustering.
 * @param {string} labelEncoding The encoding for the labels.
 */
const frequency = async (chartId, algorithm, similarity, labelEncoding) => {
  try {
    const res = await callFetch("frequency/" + algorithm + "/" + similarity +
      "/" + labelEncoding + "/" + chartId);
    const frequencies = await res.json();

    const tsLabels = frequencies.ts_labels.map((elt, index) => index);
    const clusterLabels = frequencies.cluster_labels.map((elt, index) => index);

    d3.select("body")
        .append("div")
        .attr("style", "width:1000px;height:400px")
        .attr("id", "freqChart" + chartId + algorithm + similarity +
          labelEncoding);
    d3.select("body")
        .append("div")
        .attr("style", "width:1600px;height:400px")
        .attr("id", "freqChart2" + chartId + algorithm + similarity +
          labelEncoding);

    const chart = document.getElementById("freqChart" + chartId + algorithm +
        similarity + labelEncoding);
    const chart2 = document.getElementById("freqChart2" + chartId + algorithm +
      similarity + labelEncoding);

    Plotly.newPlot(chart, [{y: tsLabels, x: frequencies.labels,
      z: frequencies.ts_labels, type: "heatmap"}], {margin: {t: 20, l: 100,
      b: 100, r: 20}, title: "time series labels"});
    Plotly.newPlot(chart2, [{y: clusterLabels, x: frequencies.labels,
      z: frequencies.cluster_labels, type: "heatmap"}], {margin: {t: 40,
      l: 100, b: 100, r: 20}, title: similarity + "-" + labelEncoding} );
  } catch (error) {
    showError(error);
  }
};

frequency("002", "k-means", "correlation", "none");
frequency("002", "k-means-constrained", "correlation", "none");
