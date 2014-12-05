$.ajax({
    type: "GET",
    url: "/stock_chart",
    data: {
        sector: "Technology",
        chart_type: "1y"
    },
    success: function (response) {
        nv.addGraph(function () {
            var chart = nv.models.lineChart();
            var fitScreen = false;
            var width = 800;
            var height = 300;
            var zoom = 1;

            chart.useInteractiveGuideline(true);
            chart.xAxis
                .tickFormat(function(d){
                    return d3.time.format('%Y-%m-%d')(new Date(d));
                });
            console.log(response);

            chart.yAxis
                .axisLabel('Price')
                .tickFormat(d3.format(',.2f'));

            d3.select('#chart1 svg')
                .attr('perserveAspectRatio', 'xMinYMid')
                .attr('width', width)
                .attr('height', height)
                .datum(response);

            setChartViewBox();
            resizeChart();

            // These resizes both do the same thing, and require recalculating the chart
            //nv.utils.windowResize(chart.update);
            //nv.utils.windowResize(function() { d3.select('#chart1 svg').call(chart) });
            nv.utils.windowResize(resizeChart);


            function setChartViewBox() {
                var w = width * zoom,
                    h = height * zoom;

                chart
                    .width(w)
                    .height(h);

                d3.select('#chart1 svg')
                    .attr('viewBox', '0 0 ' + w + ' ' + h)
                    .transition().duration(500)
                    .call(chart);
            }

            // This resize simply sets the SVG's dimensions, without a need to recall the chart code
            // Resizing because of the viewbox and perserveAspectRatio settings
            // This scales the interior of the chart unlike the above
            function resizeChart() {
                var container = d3.select('#chart1');
                var svg = container.select('svg');

                if (fitScreen) {
                    // resize based on container's width AND HEIGHT
                    var windowSize = nv.utils.windowSize();
                    svg.attr("width", windowSize.width);
                    svg.attr("height", windowSize.height);
                } else {
                    // resize based on container's width
                    var aspect = chart.width() / chart.height();
                    var targetWidth = parseInt(container.style('width'));
                    svg.attr("width", targetWidth);
                    svg.attr("height", Math.round(targetWidth / aspect));
                }
            }

            return chart;
        });
    }
});