/**
 *  Formats points for graphing.
 */
function formatPoints(points) {
    const n = points.length
    const values = Array(n);
    const dates = Array(n);

    for (i = 0; i < n; i++) {
        values[i] = points[i]["value"]["doubleValue"];
        dates[i] = new Date(points[i]["interval"]["startTime"]);
    }

    return [values, dates];
}

/**
 * Draws the chart.
 */
const drawChart = async () => {
    const url = 'http://127.0.0.1:5000/';
    const chartId = "001";
    const response = await fetch(url + "data/" + chartId);

    if (response.status >= 200 && response.status <= 299){
        const data = await response.json();
        const formatedData = Array(data["timeSeries"].length);
        data["timeSeries"].forEach((elt, index) => {
            formatedData[index] = formatPoints(elt["points"]);
        })

        let margin = { left: 40, right: 20, top: 20, bottom: 40 };
        let svg = d3.select("svg#chart")
        let h = svg.attr("height") - margin.bottom - margin.top;
        let w = svg.attr("width") - margin.left - margin.right;

        let maxY = formatedData.reduce((acc, cur) => { 
            return d3.max([acc, d3.max(cur[0])])}, 0);
        let yScale = d3.scaleLinear().domain([0, maxY]).range([h, 0]);
        svg.append("g").call(d3.axisLeft(yScale))
            .attr("color", "#404040")
            .attr("transform",
                "translate(" + margin.left + ", " + margin.top + ")");

        let maxX = formatedData[0][1][0];
        let minX = formatedData[0][1][formatedData[0][1].length - 1];
        let xScale = d3.scaleTime().domain([minX, maxX]).range([0, w]);
        svg.append("g").call(d3.axisBottom(xScale))
            .attr("color", "#404040")
            .attr("transform",
                "translate(" + margin.left + ", " + (h + margin.top) + ")");
        
        svg.append("g")
            .call(d3.axisLeft(yScale).tickSize(-w).tickFormat(""))
            .attr("color", "lightgrey")
            .attr("transform",
                "translate(" + margin.left + ", " + margin.top + ")");

        let colorScale = d3.scaleOrdinal(d3.schemeCategory10);

        let lines = formatedData.forEach((elt, index) => {
            let zipped = elt[0].map((val, i) => [val, elt[1][i]]);

            svg.append("path")
                .datum(zipped)
                .attr("fill", "none")
                .attr("stroke", (d) => colorScale(d))
                .attr("stroke-width", 1)
                .attr("d", d3.line()
                    .y((d) => yScale(d[0]))
                    .x((d) => xScale(d[1]))
                ).attr("transform",
                    "translate(" + margin.left + ", " + margin.top + ")");
        });

        let modes = ["Default", "K-means", "DBSCAN"];
        let modeSelector = d3.select("select#modeSelector");

        modeSelector.selectAll("option")
            .data(modes)
            .enter()
            .append("option")
            .attr("value", (d) => d)
            .text((d) => d);

        modeSelector.on("change", updateChart);

        function updateChart() {
            let currentMode = modeSelector.property("value");
        }
        
    } else{
        d3.select("svg#chart").append("text")
            .attr("x", 20)
            .attr("y", 20)
            .text("Error: " + response.status + ".");
    }
}

drawChart();