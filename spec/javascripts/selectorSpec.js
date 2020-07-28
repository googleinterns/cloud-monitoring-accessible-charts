describe("Suite for selector", function() {
  afterEach(function() {
    d3.select("select").selectAll("*").remove();
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
});
