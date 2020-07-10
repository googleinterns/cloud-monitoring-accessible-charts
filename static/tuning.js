/**
 * Draws a graph for each shart, showing the results of the tuning algorithm.
 * @param {string} mode The algorithm for which a paramter is being tuned.
 */
const tuning = async (mode) => {
    const url = 'http://127.0.0.1:5000/';
    const chartIds = ["001","002","004","005"];
    
    for (let index = 0; index < chartIds.length; index++){
        let response = await fetch(url + "tuning/" + mode + "/" 
            + chartIds[index]);
        let distances = await response.json();

        let points = [];
        distances.forEach((elt,index) => points.push(index+1));

        d3.select("body")
            .append("div")
            .attr("style", "width:300px;height:300px")
            .attr("id", "tuningChart" + chartIds[index]);
        
        let chart = document.getElementById('tuningChart' + chartIds[index]);

        Plotly.newPlot(chart, [{x: points, y: distances}], 
            {margin: {t: 20, l:50, b:50, r:20} });
    }
    
}

tuning("DBSCAN");