/**
 * Formats points for graphing.
 * @param {Array} points TimeSeries points. Ordered from most recent to oldest.
 * @return {Array} An array where the first element represents the time
 * series value and the second element represents the corresponding date.
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
      .attr("id", "err")
      .text("Error: " + status + ".");
}

/**
 * Requests the data and draws the chart.
 */
const drawChart = async () => {
  const chartId = "002";
  try {
    const response = await callFetch("data/" + chartId);
    const allZones = new Set();
    if (response.status >= 200 && response.status <= 299) {
      const data = await response.json();
      const formattedData = data.timeSeries.map((timeSeries) => {
        const zone = timeSeries["resource"]["labels"]["zone"];
        allZones.add(zone);
        const points = formatPoints(timeSeries.points);
        points.push(zone);
        return points;
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

      const colors = ["#ee99bb", "#cc5588", "#9144BB", "#7e21ff",
        "#2266ff", "#4593db", "#44dcb4", "#3DAF21", "#eaca58", "#e99958",
        "#8A8883", "#994F14", "#123898"];
      const colorScale = d3.scaleOrdinal().range(colors);
      drawLines(svg, formattedData, colorScale, yScale, dateScale, margin);
      selectors(svg, formattedData, colorScale, yScale, dateScale, margin,
          chartId, Array.from(allZones).sort());
    } else {
      const error = await response.json();
      showError(response.status + ". " + error.error.message );
    }
  } catch (error) {
    showError(error);
  }
};

/**
 * Draws the time series as lines.
 * @param {svg} svg The svg used for plotting that chart.
 * @param {Array} formattedData An array where the ith element represents the
 * time series value and corresponding date, for the ith timeSeries.
 * @param {function} colorScale A d3 colorscale used for the line colors.
 * @param {function} yScale The scale used to convert the time series values.
 * @param {function} dateScale The scale used to convert the time series dates.
 * @param {object} margin An object with the values for the chart margins.
 */
function drawLines(svg, formattedData, colorScale, yScale, dateScale, margin) {
  const currentRep = d3.select("select#repSelector").property("value");
  formattedData.forEach(([values, dates, zone], index) => {
    const zipped = values.map((val, i) => [val, dates[i]]);

    svg.append("path")
        .datum(zipped)
        .attr("fill", "none")
        .attr("stroke", (d) => currentRep == "Bands" ? "#ff0000": colorScale(d))
        .attr("stroke-width", 1)
        .attr("d", d3.line()
            .y((d) => yScale(d[0]))
            .x((d) => dateScale(d[1])),
        ).attr("transform",
            "translate(" + margin.left + ", " + margin.top + ")")
        .on("mouseover", function() {
          const currentFilter = d3.select("select#filterSelector")
              .property("value");
          const cluster = d3.select("select#clusterSelector")
              .property("value");
          const classes = d3.select(this).attr("class").split(" ");
          let currentCluster = classes[classes.length-1];
          const dashIndex = currentCluster.lastIndexOf("-") + 1;
          currentCluster = currentCluster.slice(dashIndex);
          if (currentRep == "Bands") {
            d3.select(this)
                .attr("stroke-width", 3);
          } else if (cluster == "All") {
            d3.select(this)
                .attr("stroke-width", 3);
            d3.selectAll(".timeSeries")
                .attr("opacity", 0.2);
            d3.selectAll(".cluster-" + currentCluster)
                .attr("opacity", 1);
            d3.selectAll(".cluster--" + currentCluster)
                .attr("opacity", 1);
          } else if (currentCluster == cluster || -currentCluster ==
                      cluster || currentFilter == "Zone") {
            d3.select(this)
                .attr("stroke-width", 3);
          }
        })
        .on("mouseout", function() {
          const currentFilter = d3.select("select#filterSelector")
              .property("value");
          const cluster = d3.select("select#clusterSelector")
              .property("value");
          const classes = d3.select(this).attr("class").split(" ");
          let currentCluster = classes[classes.length-1];
          const dashIndex = currentCluster.lastIndexOf("-") + 1;
          currentCluster = currentCluster.slice(dashIndex);
          if (currentRep == "Bands") {
            d3.select(this)
                .attr("stroke-width", 1);
          } else if (cluster == "All") {
            d3.select(this)
                .attr("stroke-width", 1);
            d3.selectAll(".timeSeries")
                .attr("opacity", 1);
          } else if (currentCluster == cluster || -currentCluster ==
                  cluster || currentFilter == "Zone") {
            d3.select(this)
                .attr("stroke-width", 1);
          }
        })
        .attr("id", "id"+index)
        .attr("class", "timeSeries " + zone + " cluster-All");
  });
}

/**
 * Draws the time series as bands.
 * @param {Array} minMax An array where the ith element has the [min,max] values
 * for the ith cluster.
 * @param {Array} dates An array of dates that correspond to the minMax values.
 * @param {svg} svg The svg used to draw the chart.
 * @param {function} colorScale A d3 colorscale used for the line colors.
 * @param {function} yScale The scale used to convert the time series values.
 * @param {function} dateScale The scale used to convert the time series dates.
 * @param {object} margin An object with the values for the chart margins.
 * @param {Array} outlierLines An array where the ith element represents the
 * time series value and corresponding date, for the ith timeSeries.
 */
function drawBands(minMax, dates, svg, colorScale, yScale, dateScale, margin,
    outlierLines) {
    drawLines(svg, outlierLines, colorScale, yScale, dateScale, margin);

  minMax.forEach(([minTS, maxTS], index) => {
    const minLine = minTS.map((val, i) => [val, maxTS[i], new Date(dates[i])]);
    const area = d3.area()
        .x((d) => dateScale(d[2]))
        .y0((d) => yScale(d[0]))
        .y1((d) => yScale(d[1]));

    svg.append("path")
        .datum(minLine)
        .attr("fill", colorScale(index+1))
        .attr("opacity", 0.5)
        .attr("d", area)
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")")
        .attr("class", "timeSeries cluster-All cluster-"+(index+1));
  });
}

chartMode = "lines";
drawChart();
