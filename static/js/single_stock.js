//$(".modal-body").find("div").each(function () {
//    var chartData = [];
//    var symbol = this.id;
//    $.ajax({
//        type: "GET",
//        url: "/stock_api",
//        data: {
//            symbol: symbol
//        },
//        success: function (response) {
//            for (var i = 0; i < response.length; i++) {
//                var newDate = new Date(response[i]['date']);
//                var open = response[i]['open'];
//                var close = response[i]['close'];
//                var volume = response[i]['volume'];
//                var high = response[i]['high'];
//                var low = response[i]['low'];
//                var value = response[i]['value'];
//                chartData[i] = ({
//                    date: newDate,
//                    open: open,
//                    close: close,
//                    high: high,
//                    low: low,
//                    volume: volume,
//                    value: value
//                });
//
//            }
//
//            var chart;
//
//            makeChart("black", "#222222");
//
//            function makeChart(theme, bgColor) {
//
//                if (chart) {
//                    chart.clear();
//                }
//
//                // background
//                if (document.body) {
//                    document.body.style.backgroundColor = bgColor;
//                }
//
//                AmCharts.makeChart(symbol, {
//                    type: "stock",
//                    theme: theme,
//                    pathToImages: "/static/images/",
//
//                    dataSets: [{
//                        fieldMappings: [{
//                            fromField: "open",
//                            toField: "open"
//                        }, {
//                            fromField: "high",
//                            toField: "high"
//                        }, {
//                            fromField: "low",
//                            toField: "low"
//                        }, {
//                            fromField: "close",
//                            toField: "close"
//                        }, {
//                            fromField: "volume",
//                            toField: "volume"
//                        }, {
//                            fromField: "value",
//                            toField: "value"
//                        }],
//                        dataProvider: chartData,
//                        categoryField: "date",
//                        compared: true
//                    }
//                    ],
//
//                    panels: [{
//
//                        showCategoryAxis: false,
//                        title: "Price",
//                        percentHeight: 70,
//                        categoryAxis: {
//                            dashLength: 5
//                        },
//
//                        stockGraphs: [{
//                            type: "candlestick",
//                            id: "g1",
//                            openField: "open",
//                            closeField: "close",
//                            highField: "high",
//                            lowField: "low",
//                            valueField: "close",
//                            lineColor: "#000",
//                            fillColors: "#7f8da9",
//                            negativeLineColor: "#000",
//                            negativeFillColors: "#db4c3c",
//                            lineAlpha: 1,
//                            fillAlphas: 1,
//                            useDataSetColors: false,
//                            comparable: true,
//                            compareField: "value",
//                            balloonText: "open:<b>[[open]]</b><br>close:<b>[[close]]</b><br>low:<b>[[low]]</b><br>high:<b>[[high]]</b>"
//                        }],
//
//                        stockLegend: {
//                            periodValueTextRegular: " ",
//                            markerType: "none"
//                        }
//                    },
//
//                        {
//                            title: "Volume",
//                            percentHeight: 30,
//
//                            stockGraphs: [{
//                                valueField: "volume",
//                                type: "column",
//                                fillAlphas: 1
//                            }],
//
//
//                            stockLegend: {
//                                periodValueTextRegular: " ",
//                                makerType: "none"
//                            }
//                        }
//                    ],
//
//                    chartScrollbarSettings: {
//                        graph: "g1",
//                        graphType: "line",
//                        usePeriod: "WW"
//                    },
//
//                    chartCursorSettings: {
//                        valueBalloonsEnabled: true,
//                        graphBulletSize: 1
//                    },
//
//                    periodSelector: {
//                        periods: [{
//                            period: "DD",
//                            count: 10,
//                            label: "10 days"
//                        }, {
//                            period: "MM",
//                            selected: true,
//                            count: 1,
//                            label: "1 month"
//                        }, {
//                            period: "YYYY",
//                            count: 1,
//                            label: "1 year"
//                        }]
//                    },
//
//
//                    panelsSettings: {
//                        usePrefixes: true
//                    }
//                });
//            }
//        }
//
//    })
//});

$(".ui .modal .content").find("div").each(function () {
    var symbol = this.id;
    function get_chart_data() {
        var chartData = [];
        var response = $.ajax({
            type: "GET",
            url: "/stock_api",
            data: {
                symbol: symbol
            },
            success: function (response) {

            },
            async: false
        });

        var raw_data = response.responseJSON;

        for (var i = 0; i < raw_data.length; i++) {
            var newDate = new Date(raw_data[i]['date']);
            var open = raw_data[i]['open'];
            var close = raw_data[i]['close'];
            var volume = raw_data[i]['volume'];
            var high = raw_data[i]['high'];
            var low = raw_data[i]['low'];
            var value = raw_data[i]['value'];

            chartData[i] = ({
                date: newDate,
                open: open,
                close: close,
                high: high,
                low: low,
                volume: volume,
                value: value
            });

        }
        return chartData;

    }

    var chartData = get_chart_data();


    var chart;

    makeChart("black");

    function makeChart(theme) {

        chart = AmCharts.makeChart(symbol, {
            type: "stock",
            theme: theme,
            pathToImages: "/static/images/",

            dataSets: [{
                fieldMappings: [{
                    fromField: "open",
                    toField: "open"
                }, {
                    fromField: "high",
                    toField: "high"
                }, {
                    fromField: "low",
                    toField: "low"
                }, {
                    fromField: "close",
                    toField: "close"
                }, {
                    fromField: "volume",
                    toField: "volume"
                }, {
                    fromField: "value",
                    toField: "value"
                }],
                dataProvider: chartData,
                categoryField: "date",
                compared: true
            }
            ],

            panels: [{

                showCategoryAxis: false,
                title: "Price",
                percentHeight: 70,
                categoryAxis: {
                    dashLength: 5
                },

                stockGraphs: [{
                    type: "candlestick",
                    id: "g1",
                    openField: "open",
                    closeField: "close",
                    highField: "high",
                    lowField: "low",
                    valueField: "close",
                    lineColor: "#000",
                    fillColors: "#7f8da9",
                    negativeLineColor: "#000",
                    negativeFillColors: "#db4c3c",
                    lineAlpha: 1,
                    fillAlphas: 1,
                    useDataSetColors: false,
                    comparable: true,
                    compareField: "value",
                    balloonText: "open:<b>[[open]]</b><br>close:<b>[[close]]</b><br>low:<b>[[low]]</b><br>high:<b>[[high]]</b>"
                }],

                stockLegend: {
                    periodValueTextRegular: " ",
                    markerType: "none"
                }
            },

                {
                    title: "Volume",
                    percentHeight: 30,

                    stockGraphs: [{
                        valueField: "volume",
                        type: "column",
                        fillAlphas: 1
                    }],


                    stockLegend: {
                        periodValueTextRegular: " ",
                        makerType: "none"
                    }
                }
            ],

            chartScrollbarSettings: {
                graph: "g1",
                graphType: "line",
                usePeriod: "WW"
            },

            chartCursorSettings: {
                valueBalloonsEnabled: true,
                graphBulletSize: 1
            },

            periodSelector: {
                periods: [{
                    period: "DD",
                    count: 10,
                    label: "10 days"
                }, {
                    period: "MM",
                    selected: true,
                    count: 1,
                    label: "1 month"
                }, {
                    period: "YYYY",
                    count: 1,
                    label: "1 year"
                }]
            },


            panelsSettings: {
                usePrefixes: true
            }
        });
    }

//    $('.modal').on('shown.bs.modal', function () {
//        chart.validateNow();
//    });
    $('#button_' + symbol).click(function(e){
        e.preventDefault();
        chart.validateNow();
        console.log('test');
    })
});

var symbol = "EPD";
    function get_chart_data() {
        var chartData = [];
        var response = $.ajax({
            type: "GET",
            url: "/stock_api",
            data: {
                symbol: symbol
            },
            success: function (response) {

            },
            async: false
        });

        var raw_data = response.responseJSON;

        for (var i = 0; i < raw_data.length; i++) {
            var newDate = new Date(raw_data[i]['date']);
            var open = raw_data[i]['open'];
            var close = raw_data[i]['close'];
            var volume = raw_data[i]['volume'];
            var high = raw_data[i]['high'];
            var low = raw_data[i]['low'];
            var value = raw_data[i]['value'];

            chartData[i] = ({
                date: newDate,
                open: open,
                close: close,
                high: high,
                low: low,
                volume: volume,
                value: value
            });

        }
        return chartData;

    }

    var chartData = get_chart_data();


    var chart;

    makeChart("black");

    function makeChart(theme) {

        chart = AmCharts.makeChart("EPD", {
            type: "stock",
            theme: theme,
            pathToImages: "/static/images/",

            dataSets: [{
                fieldMappings: [{
                    fromField: "open",
                    toField: "open"
                }, {
                    fromField: "high",
                    toField: "high"
                }, {
                    fromField: "low",
                    toField: "low"
                }, {
                    fromField: "close",
                    toField: "close"
                }, {
                    fromField: "volume",
                    toField: "volume"
                }, {
                    fromField: "value",
                    toField: "value"
                }],
                dataProvider: chartData,
                categoryField: "date",
                compared: true
            }
            ],

            panels: [{

                showCategoryAxis: false,
                title: "Price",
                percentHeight: 70,
                categoryAxis: {
                    dashLength: 5
                },

                stockGraphs: [{
                    type: "candlestick",
                    id: "g1",
                    openField: "open",
                    closeField: "close",
                    highField: "high",
                    lowField: "low",
                    valueField: "close",
                    lineColor: "#000",
                    fillColors: "#7f8da9",
                    negativeLineColor: "#000",
                    negativeFillColors: "#db4c3c",
                    lineAlpha: 1,
                    fillAlphas: 1,
                    useDataSetColors: false,
                    comparable: true,
                    compareField: "value",
                    balloonText: "open:<b>[[open]]</b><br>close:<b>[[close]]</b><br>low:<b>[[low]]</b><br>high:<b>[[high]]</b>"
                }],

                stockLegend: {
                    periodValueTextRegular: " ",
                    markerType: "none"
                }
            },

                {
                    title: "Volume",
                    percentHeight: 30,

                    stockGraphs: [{
                        valueField: "volume",
                        type: "column",
                        fillAlphas: 1
                    }],


                    stockLegend: {
                        periodValueTextRegular: " ",
                        makerType: "none"
                    }
                }
            ],

            chartScrollbarSettings: {
                graph: "g1",
                graphType: "line",
                usePeriod: "WW"
            },

            chartCursorSettings: {
                valueBalloonsEnabled: true,
                graphBulletSize: 1
            },

            periodSelector: {
                periods: [{
                    period: "DD",
                    count: 10,
                    label: "10 days"
                }, {
                    period: "MM",
                    selected: true,
                    count: 1,
                    label: "1 month"
                }, {
                    period: "YYYY",
                    count: 1,
                    label: "1 year"
                }]
            },


            panelsSettings: {
                usePrefixes: true
            }
        });
        $('#button_EPD').click(function(){
        chart.validateNow();
        console.log('test');
    })
    }
