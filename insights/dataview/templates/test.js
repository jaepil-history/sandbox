/**
 * Created by byouloh on 13. 10. 2.
 */

var dump_data = [{'date': '2013-09-30', 'counts': 5876}, {'date': '2013-10-01', 'counts': 5913}];
var x_range = [];
var y_values = [];
var DAU_series = [];

for(var i = 0; i < dump_data.length; i++) {
    x_range.push(dump_data[i]['date']);
    print(x_range);
    y_values.push(dump_data[i]['counts']);
    print(y_values);
}

DAU_series.push({name: "DAU", data: y_values});

//    var DAU_chart = new Highcharts.Chart({
//        chart: {
//            renderTo: 'DAU_container',
//            type: 'line',
//            marginRight: 130,
//            marginBottom: 60
//        },
//        title: {
//            text: 'DAU',
//            x: -20 //center
//        },
//        subtitle: {
//            text: '',
//            x: -20
//        },
//        xAxis: {
//            categories: x_range,
//            title: {
//                text: 'date',
//                y: 20
//            }
//        },
//        yAxis: {
//            title: {
//                text: 'number'
//            },
//            plotLines: [{
//                value: 0,
//                width: 1,
//                color: '#808080'
//            }]
//        },
//        tooltip: {
//            formatter: function() {
//                return '<b>'+ this.series.name +'</b><br/>'+
//                    this.x +': '+ this.y +'HP';
//            }
//        },
//        legend: {
//            layout: 'vertical',
//            align: 'right',
//            verticalAlign: 'top',
//            x: -10,
//            y: 30,
//            borderWidth: 0
//        },
//        series: DAU_series
//    });