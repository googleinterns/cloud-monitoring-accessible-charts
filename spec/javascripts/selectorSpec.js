describe("Suite for selector", function() {
  afterEach(function() {
    d3.selectAll("select").remove();
  });

  it("should make an option and set it as the value", function() {
    d3.select("body")
        .append("select")
        .attr("id", "clusterSelector");

    expect(d3.select("#clusterSelector")).not.toBeNull();
    expect(d3.select("#clusterSelector").property("value")).toEqual("");

    updateSelector("cluster", ["All"]);
    expect(d3.select("#clusterSelector").property("value")).toEqual("All");
  });

  it("should append options", function() {
    d3.select("body")
        .append("select")
        .attr("id", "encodingSelector");

    const clusters = ["All", "0", "1"];
    updateSelector("encoding", clusters);

    d3.selectAll("option").each( (elt, i) => {
      expect(elt).toEqual(clusters[i]);
    });
  });

  it("should remove all options", function() {
    d3.select("body")
        .append("select")
        .attr("id", "aSelector");

    updateSelector("a", ["All", 0]);
    updateSelector("a", []);
    expect(d3.select("#aSelector").property("value")).toEqual("");
  });

  it("should update clusterSelector when filterSelector==Cluster", function() {
    d3.select("body")
        .append("select")
        .attr("id", "clusterSelector");
    d3.select("body")
        .append("select")
        .attr("id", "filterSelector");

    updateSelector("cluster", ["All", "cat", "dog"]);
    updateSelector("filter", ["Cluster", "Zone"]);
    d3.select("select#clusterSelector").property("value", "cat");

    clusters = ["All", 0, 1];
    updateFilter();

    // The value should be All because All is one of the options for
    // clusterSelector and updateFilter() sets its to All.
    expect(d3.select("#clusterSelector").property("value")).toEqual("All");
    d3.selectAll("#clusterSelector").selectAll("option").each((elt, i) => {
      expect(elt).toEqual(clusters[i]);
    });
  });

  it("should update clusterSelector when filterSelector==Zone", function() {
    d3.select("body")
        .append("select")
        .attr("id", "clusterSelector");
    d3.select("body")
        .append("select")
        .attr("id", "filterSelector");

    updateSelector("cluster", ["All", "cat", "dog"]);
    updateSelector("filter", ["Cluster", "Zone"]);

    d3.select("select#filterSelector").property("value", "Zone");

    allZones = ["All", "zone-1", "zone-2", "zone-3"];
    updateFilter();
    expect(d3.select("#clusterSelector").property("value")).toEqual("All");
    d3.selectAll("#clusterSelector").selectAll("option").each( (elt, i) => {
      expect(elt).toEqual(allZones[i]);
    });
  });
});
