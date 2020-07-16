/**
 * Formats points for graphing.
 * @param {Array} points TimeSeries points. Ordered from most recent to oldest.
 * @return {Array} An array where the first element representing the time
 * series values and the corresponding dates.
 */
function formatPoints(points) {
  const n = points.length;
  const values = Array(n);
  const dates = Array(n);

  for (i = 0; i < n; i++) {
    values[i] = points[i]["value"]["doubleValue"];
    dates[i] = new Date(points[i]["interval"]["startTime"]);
  }

  return [values, dates];
}

/**
 * Displays an error message with the status argument.
 * @param {string} status The error status.
 */
function showError(status) {
  d3.selectAll(".timeSeries")
      .attr("opacity", 0);
  d3.select("svg#chart").append("text")
      .attr("x", 20)
      .attr("y", 20)
      .text("Error: " + status + ".");
}

/**
 * Requests the data and draws the chart.
 */
const drawChart = async () => {
  const url = 'http://127.0.0.1:5000/';
  const chartId = "001";
  try {
    const response = await fetch(url + "data/" + chartId);

    if (response.status >= 200 && response.status <= 299) {
      const data = await response.json();
      const formattedData = data.timeSeries.map((timeSeries) => {
        return formatPoints(timeSeries.points);
      });

      const margin = {left: 40, right: 20, top: 30, bottom: 40};
      const svg = d3.select("svg#chart");
      const h = svg.attr("height") - margin.bottom - margin.top;
      const w = svg.attr("width") - margin.left - margin.right;

      const maxY = formattedData.reduce((acc, cur) => {
        return d3.max([acc, d3.max(cur[0])]);
      }, 0);
      const yScale = d3.scaleLinear().domain([0, maxY]).range([h, 0]);
      svg.append("g").call(d3.axisLeft(yScale))
          .attr("color", "#404040")
          .attr("transform",
              "translate(" + margin.left + ", " + margin.top + ")");

      const maxDate = formattedData[0][1][0];
      const minDate = formattedData[0][1][formattedData[0][1].length - 1];
      const dateScale = d3.scaleTime().domain([minDate, maxDate]).range([0, w]);
      svg.append("g").call(d3.axisBottom(dateScale))
          .attr("color", "#404040")
          .attr("transform", "translate(" +
                    margin.left + ", " + (h + margin.top) + ")");

      svg.append("g")
          .call(d3.axisLeft(yScale).tickSize(-w).tickFormat(""))
          .attr("color", "lightgrey")
          .attr("transform",
              "translate(" + margin.left + ", " + margin.top + ")");

      const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

      formattedData.forEach((elt, index) => {
        const zipped = elt[0].map((val, i) => [val, elt[1][i]]);

        svg.append("path")
            .datum(zipped)
            .attr("fill", "none")
            .attr("stroke", (d) => colorScale(d))
            .attr("stroke-width", 1)
            .attr("d", d3.line()
                .y((d) => yScale(d[0]))
                .x((d) => dateScale(d[1])),
            ).attr("transform",
                "translate(" + margin.left + ", " + margin.top + ")")
            .attr("id", "id"+index)
            .attr("class", "timeSeries cluster-All");
      });
      selectors(url, chartId, colorScale);
    } else {
      showError(response.status);
    }
  } catch (error) {
    showError(error);
  }
};

drawChart();
