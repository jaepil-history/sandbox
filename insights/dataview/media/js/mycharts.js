/**
 * Created with PyCharm.
 * User: byouloh
 * Date: 13. 2. 25
 * Time: 오전 9:50
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function () {
    $.getJSON('/index', function (data) {

    });

    var charts = function () {
        var data = [];
        var range = [5, 10, 15, 20, 25, 30, 35, 40, 45,
            50, 55, 60, 65, 70, 75, 80, 85]; //90, 95, 100, 105, 110, 115, 120, 125, 130];
        var series1 = [];
        var series2 = [];
        var series3 = [];

//        $('#container4').empty();
//        $('#container4')
//        <label for="target-distance">타겟과의 거리(단위: meter)</label>
//        <input type="text" id="target-distance" value="5" style="width:70px; text-align:right">
//            <input id="reload" type="submit" value="연사 재계산">

        // 연사 결과는 result jqGrid를 지우고 다시 그린다.
        //  div(resultArea) 안에 테이블을 새로 그려야 이전 grid에 가리지 않는다.
        $('#resultArea').empty();
        for (var dist = 0; dist < 5; dist++) {
            $("#resultArea").append($("<table>").attr("id", "result" + String(dist)));
            $("#result" + String(dist)).jqGrid({
                data: resultData[String(targetDistance * (dist + 1))+'m'],
                datatype: 'local', //'local',
                //pager: jQuery('#result-pager'),
                height: 140,
                autowidth: true,
                shrinkToFit: false,
                sortable: true,
                editable: true,
                rowNum: 75,
                caption: "연사 결과값: " + String(targetDistance * (dist + 1)) + 'm',
                colNames: ['WeaponName', 'eDPS', 'HitRate',
                    'HitBullets', 'NumOfBullets', 'FireTime','fBaseDamage'
                ],
                colModel: [
                    {name: "WeaponName", index: 'WeaponName', width:150, align:'left'},
                    {name: "eDPS", index: 'eDPS', width:70, align:'center'},
                    {name: "HitRate", index: 'HitRate', width:70, align:'center'},
                    {name: "HitBullets", index: 'HitBullets', width:70, align:'center'},
                    {name: "NumOfBullets", index: 'NumOfBullets', width:70, align:'center'},
                    {name: "FireTime", index: 'FireTime', width:70, align:'center'},
                    {name: "fBaseDamage", index: 'fBaseDamage', width:80, align:'center'}
                ],
                sortname: 'Name',
                viewrecords: true,
                rownumbers: true,
                sortorder: "desc",
                editurl: 'Service.ashx?type=editdata',
                cellEdit: true,
                cellsubmit:'clientArray',
                resize: true,
                reloadAfterSubmit: true,
                gridComplete: function() {
                    var width = $('#container4').width();
                    if (width > 18) width = width - 18;
                    $("#result" + String(dist)).jqGrid('setGridWidth', width);
                }
            });
        }

        var chart1 = new Highcharts.Chart({
            chart: {
                renderTo: 'container1',
                type: 'line',
                marginRight: 130,
                marginBottom: 60
            },
            title: {
                text: '줌아웃 조준 사격시 명중률과 거리에 따른 데미지 기대값',
                x: -20 //center
            },
            subtitle: {
                text: '타겟 헤드를 기준으로 했을 때',
                x: -20
            },
            xAxis: {
                categories: range,
                title: {
                    text: '거리(meter)',
                    y: 20
                }
            },
            yAxis: {
                title: {
                    text: 'Damage(HP)'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y +'HP';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 30,
                borderWidth: 0
            },
            series: series1
        });

        var chart2 = new Highcharts.Chart({
            chart: {
                renderTo: 'container2',
                type: 'line',
                marginRight: 130,
                marginBottom: 60
            },
            title: {
                text: '줌인 조준 사격시 명중률과 거리에 따른 데미지 기대값',
                x: -20 //center
            },
            subtitle: {
                text: '타겟 몸통을 기준으로 했을 때',
                x: -20
            },
            xAxis: {
                categories: range,
                title: {
                    text: '거리(meter)',
                    y: 20
                }
            },
            yAxis: {
                title: {
                    text: 'Damage(HP)'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y +'HP';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 30,
                borderWidth: 0
            },
            series: series2
        });

        var chart3 = new Highcharts.Chart({

            chart: {
                renderTo: 'container3',
                type: 'scatter',
                polar: true
            },

            title: {
                text: '연사에 의한 탄착군'
            },

            pane: {
                startAngle: 0,
                endAngle: 360
            },

            xAxis: {
                tickInterval: 45,
                min: 0,
                max: 360,
                labels: {
                    formatter: function () {
                        return this.value + '°';
                    }
                },
                title: {
                    enabled: true,
                    text: '°'
                }
            },

            yAxis: {
                title: {
                    text: 'Recoil & Wag (m)'
                },
                min: 0
            },

            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +' °, '+ this.y +' m';
                }
            },

            plotOptions: {
                scatter: {
                    marker: {
                        radius: 5,
                        states: {
                            hover: {
                                enabled: true,
                                lineColor: 'rgb(100,100,100)'
                            }
                        }
                    },
                    states: {
                        hover: {
                            marker: {
                                enabled: false
                            }
                        }
                    }
                },
                series: {
                    pointStart: 0,
                    pointInterval: 45
                },
                column: {
                    pointPadding: 0,
                    groupPadding: 0
                }
            },

            series: series3
        });
    }

    $('#reload').click(charts); //.submit(charts);
});