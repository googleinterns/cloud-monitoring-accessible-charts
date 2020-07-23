/**
 * Draws a graph for each shart, showing the results of the tuning algorithm.
 * @param {string} mode The algorithm for which a paramter is being tuned.
 */
const tuning = async (mode) => {
  const chartIds = ["001", "002", "004", "005"];

  for (let index = 0; index < chartIds.length; index++) {
    const response = await callFetch("tuning/" + mode + "/" +
            chartIds[index]);
    const distances = await response.json();

    const points = distances.map((elt, index) => index+1);

    d3.select("body")
        .append("div")
        .attr("style", "width:300px;height:300px")
        .attr("id", "tuningChart" + chartIds[index]);

    const chart = document.getElementById('tuningChart' + chartIds[index]);

    Plotly.newPlot(chart, [{x: points, y: distances}],
        {margin: {t: 20, l: 50, b: 50, r: 20}});
  }
};

tuning("DBSCAN");
