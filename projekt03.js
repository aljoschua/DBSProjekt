// Assuminig 1080x1920
$(function() {
    sigma.parsers.json('js/sigma-data.json', {
        container: 'sigma',
        settings: {
            defaultNodeColor: '#0ff'
        }
    }, function(s) {
        s.bind('clickNode', onClick);
    });
    barchartForAll();
    window.scrollTo(0,0);
});
function barchartForAll() {
    $.getJSON("js/blockchart-data.json", function(data) {
        var plotDataArray = [];
        counter = 0;
        for (day in data) {
            plotDataArray[counter++] = [day, data[day].length];
        }
        plot(plotDataArray);
    });
}
function plot(plotDataArray) {
    plotDataArray = plotDataArray.sort();
    var middle = plotDataArray.length/2;
    var slices = [];
    slices[0] = plotDataArray.slice(0,middle);
    slices[1] = plotDataArray.slice(middle, middle*3);
    for ( i = 0; i < 2; ++i){
        $.plot("#barchart"+i, [{
            data: slices[i],
            color: "#ec5148",
            bars: {
                show: true,
                barWidth: 0.3,
                fill: false
            }
        }], {
            xaxis: {
                mode: "categories",
                rotateTicks: 90
            },
            yaxis: {
                min: 0  
            }
        })
    }
    window.scrollTo(0,1300);
}
function onClick(event) {
    var givenHashtag = event.data.node.label;
    var plotDataDict = {};
    $.getJSON("js/blockchart-data.json", function(data) {
        for (day in data) {
            var list = data[day];
            plotDataDict[day] = 0
            for (index in list) {
                var hashtag = list[index];
                if (hashtag == givenHashtag)
                    plotDataDict[day]++;
            }
        }
        var plotDataArray = [];
        var counter = 0;
        for (day in plotDataDict) {
            plotDataArray[counter++] = [day, plotDataDict[day]];
        }
        plot(plotDataArray);
    });
}
