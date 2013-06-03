/*
 *   Depends:
 *	ui.core.js
 */

(function($) {

    function AbstractRaphaelRtHandler(element, options) {
        this.element = element;
        this.options = options;
        this.create = true;
        this._chartId = $(this.element).prop('id');
        this.numOfShownData = 0;
        this.cachedUnixStartTime = null;
        this.cachedUnixEndTime = null;
    };

    AbstractRaphaelRtHandler.prototype = {

        unix2time: function(unix_time) {
            var date = new Date(unix_time * 1000);
            var hours = date.getHours();
            var minutes = date.getMinutes();
            var seconds = date.getSeconds();
            if (hours <= 9) hours = '0' + hours;
            if (minutes <= 9) minutes = '0' + minutes;
            if (seconds <= 9) seconds = '0' + seconds;

            var time = hours + ':' + minutes + ':' + seconds;
            return time;
        },

        // make sure that we get only a fixed number of data points.
        parse_chart: function(data, numOfShownData) {
            var data = _(data).chain().values().first().value();
            var _thisObj = this;
            var reducedData;
            if (data.length < numOfShownData) reducedData = data;
            else reducedData = _(data).rest(data.length - numOfShownData);

            var rawEndTime = _.last(reducedData)[0];
            if (!this.cachedUnixStartTime) {
                this.cachedUnixStartTime = _.first(reducedData)[0];
            } else {
                var timeDelta = rawEndTime - _thisObj.cachedUnixEndTime;
                _thisObj.cachedUnixStartTime += timeDelta;
            }
            this.cachedUnixEndTime = _.last(reducedData)[0];

            var chartData = _.reduce(reducedData, function(memo, item) {
                memo.push([_thisObj.unix2time(item[0]), item[1]]);
                return memo;
            }, []);
            return chartData;
        },

        bindEvents: function() {
            var _thisObj = this;
            var realTimeDataIndex = _thisObj.options['realtime_data_index'];
            var resetChart = function() {
                  // how the fuck do I clear the charts?
                  _thisObj.clearChart();
                  _thisObj.create = true;
                  _thisObj.cachedUnixStartTime = null;
                  _thisObj.cachedUnixEndTime = null;
           };
            $(document).bind('update_interval_updated', resetChart);

            $(document).bind('app_handle_updated', function() {
                // how the fuck do I clear the charts?
                _thisObj.clearChart();
                _thisObj.create = true;
                _thisObj.cachedUnixStartTime = 0;
                _thisObj.cachedUnixEndTime = 0;
            });

            $(document).bind(_thisObj.eventName, function(event, data) {
                var parsedData = _thisObj.parse_chart(data, _thisObj.numOfShownData);
                for (key in data) { // theres should only be one key for now.
                    var rawEndTime = _.last(data[key])[0];
                }
                var myData = _(parsedData).map(function(x) {
                    return x[1][realTimeDataIndex] ? x[1][realTimeDataIndex] : 0;
                });

                if (_thisObj.create) {
					_thisObj.bootstrap(_thisObj, myData);
                    _thisObj.create = false;
                } else {
                    // myData is assumed to be one new data point and any number of old data points before it
                    // previously plotted data points may change as data gets processed by the backend, so we want to update all of those old points
                    _thisObj.pushData(myData); // Update graph
                }
                
                var $chart_element = $('#' + _thisObj._chartId);
                $chart_element.parent().children('.rt_start').html( _thisObj.unix2time(_thisObj.cachedUnixStartTime));
                $chart_element.parent().children('.rt_end').hide().html(_thisObj.unix2time(_thisObj.cachedUnixEndTime)).fadeIn(400);
                $chart_element.parent().children('.rt_curr_value').html(_.last(myData));
            });
        },

        pushData: function(arg) {
            alert("not implemented"); //xxx
        },

        bootstrap: function() {
            alert("not implemented"); //xxx
        },

        clearChart: function() {
            alert("not implemented");
        },

        prevBindEventsInit: function() {
            var dataType = this.options['data_type'];
            if (dataType === 'summary') {
                this.eventName = 'setSummaryRealtimeRaphael';
            } else if (dataType === 'details') {
                this.eventName = 'setDetailRealtimeRaphael';
            }
        },

        init: function() {
            this.width = this.options['width_int'] - 2;
            this.height = this.options['height_int'];
            this.prevBindEventsInit();
            this.bindEvents();
        }

    }; // AbstractRaphaelRtHandler.prototype

    /////////////////// RaphaelRtAnimatedLineHandler ///////////////////


    function RaphaelRtAnimatedLineHandler(element, options) {
        this.inheritedFrom = AbstractRaphaelRtHandler;
        this.inheritedFrom(element, options);
        this.numOfShownData = 40;
        this.eventName = null, this.paths = null;
        this.dots = null;
        this.inc = 0;
    };
    RaphaelRtAnimatedLineHandler.prototype = new AbstractRaphaelRtHandler();

    RaphaelRtAnimatedLineHandler.prototype.init = function() {
        AbstractRaphaelRtHandler.prototype.init.call(this); //call parents init_impl
    };

    RaphaelRtAnimatedLineHandler.prototype.clearChart = function() {
        for (var i = 0; i < this.paths.length; i++) {
            this.paths[i].remove();
        }
        this.dots = null;
        this.paths = null;
        this.inc = 0;
    };

    RaphaelRtAnimatedLineHandler.prototype.pushData = function(y) {
    	y = y ? y[y.length-1] : undefined; // pushData previously took in a single value.  changed it to take in an array for the BarHandler.  this line is added to keep the previous functionality.
        var _thisObj = this;

        // always push the dots[1]
        if (y) {
            if (this.dots[0].length === this.dots[1].length) {
                //reset path that's moved off screen
                //++counter;
                this.dots[0] = this.dots[1];
                this.dots[1] = [];

                this.paths[0].remove();
                this.paths[0] = this.paths[1];
                this.paths[1] = this.lineChart.path("M0,0").attr({
                    "stroke-width": 2,
                    "stroke": this.options['color']
                });
                this.dots[1].push({
                    x: this.width,
                    y: _.last(this.dots[0]).y
                });
            }
            this.dots[1].push({
                x: this.width + this.inc,
                y: y
            });
        }

        function slideDots(i) {
            return _(_thisObj.dots[i]).map(function(dot) {
                return {
                    x: dot.x - _thisObj.inc,
                    y: dot.y
                };
            });
        }

        function normalize(dots, max) {
            return _(dots).map(function(dot) {
                return {
                    x: dot.x,
                    y: max === 0 ? 0 : dot.y * _thisObj.height / max
                };
            });
        }
        var max = Math.ceil(_(this.dots).chain().map(function(i) {
            return _(i).pluck('y');
        }).flatten().max().value() / 50) * 50;
        max = max / 3 + max; // get the line 1/3 of the way down.
        this.paths[1].attr({
            path: this.dots2path(normalize(this.dots[1], max))
        });

        if (y) {
            this.dots[0] = slideDots(0);
            this.dots[1] = slideDots(1);
        }

        this.paths[1].animate({
            path: this.dots2path(normalize(this.dots[1], max))
        }, 380);
        this.paths[0].animate({
            path: this.dots2path(normalize(this.dots[0], max))
        }, 380);
        return max;
    };


    RaphaelRtAnimatedLineHandler.prototype.bootstrap = function(_thisObj, data) {
        _thisObj.lineChart = Raphael(_thisObj._chartId, _thisObj.width, _thisObj.height);
        _thisObj.paths = _thisObj.lineChart.set();
        _thisObj.paths.push(_thisObj.lineChart.path("M0,0").attr({
            "stroke-width": 2,
            "stroke": _thisObj.options['color']
        }));
        _thisObj.paths.push(_thisObj.lineChart.path("M0,0").attr({
            "stroke-width": 2,
            "stroke": _thisObj.options['color']
        }));
        _thisObj.dots = [];
        var dots = [];
        var x_val = 0;
        _thisObj.inc = _thisObj.width / (data.length - 1);
        $.each(data, function(i, d) {
            dots.push({
                x: x_val,
                y: d
            });
            x_val += _thisObj.inc;
        });

        _thisObj.dots.push(dots);
        _thisObj.dots.push([{
            x: _thisObj.width,
            y: _thisObj.dots[0][_thisObj.dots[0].length - 1].y
        }]);

        _thisObj.paths[0].attr({
            path: _thisObj.dots2path(_thisObj.dots[0])
        });
        _thisObj.pushData();
    };

    RaphaelRtAnimatedLineHandler.prototype.dots2path = function(dots) {
        var i, num, path;
        path = "";
        num = dots.length - 1;
        for (i = 0;
        (0 <= num ? i <= num : i >= num);
        (0 <= num ? i += 1 : i -= 1)) {
            if (i) {
                path += "L" + [dots[i].x, this.height - dots[i].y];
            } else {
                path = "M" + [dots[0].x, this.height - dots[0].y];
            }
        }
        return path;
    };

    function RaphaelRtAnimatedLineChart() {
        this.handler = null;
        this._init = function() {
            this.handler = new RaphaelRtAnimatedLineHandler(this.element, this.options);
            this.handler.init();
        };
    };

    /////////////////// RaphaelRtAnimatedBarHandler ///////////////////


    function RaphaelRtAnimatedBarHandler(element, options) {
        this.inheritedFrom = AbstractRaphaelRtHandler;
        this.inheritedFrom(element, options);
        this.numOfShownData = options['num_of_bars'];
        this.eventName = null, this.flag = null;
        this.r = null;
        this.currBar = null;
        this.data = null;
    };

    RaphaelRtAnimatedBarHandler.prototype = new AbstractRaphaelRtHandler();

    RaphaelRtAnimatedBarHandler.prototype.prevBindEventsInit = function() {
        AbstractRaphaelRtHandler.prototype.prevBindEventsInit.call(this); //call my parents' prevBindEventsInit first
        this.barwidth = this.width / this.numOfShownData;
    };

    RaphaelRtAnimatedBarHandler.prototype.bootstrap = function(_thisObj, data) {
        _thisObj.r = Raphael(_thisObj._chartId, _thisObj.width, _thisObj.height);
        _thisObj.r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";

        _thisObj.data = data;
        _thisObj.drawChart();
    };

	// update assumes that the array of recentPoints contains ONE new value and any number of updated, previously plotted values.
	// For a situation such as:
	//   this.data = [1, 2, 3, 4, 5, 6]
	//   recentPoints = [5, 6, 7]
	// where 5 and 6 are the previously plotted value and 7 is the new value, we want to:
	//   - remove the oldest data point (1) to make room for the new one
	//   - remove the two most recently plotted values to replace with (possibly) updated values
	// thus, the slice should contain the values [2, 3, 4] and then we concatenate [5, 6, 7]
    RaphaelRtAnimatedBarHandler.prototype.update = function(recentPoints) {
        this.data = this.data.slice(1,-1*(recentPoints.length-1)).concat(recentPoints);
        return this.data;
    };

    RaphaelRtAnimatedBarHandler.prototype.replaceBars = function() {
        if (this.flag) {
            this.flag.remove();
        }
        this.clearChart();
        this.drawChart();
    };

	RaphaelRtAnimatedBarHandler.prototype.drawChart = function() {
		this.setHover(this);
		
		var _thisObj = this;
        
        _(this.restBars()).map(function(i) {
            return i.attr({
                opacity: 1,
                fill: _thisObj.options['color']
            });
        });
        
        this.fadeLast();
	}

    RaphaelRtAnimatedBarHandler.prototype.setHover = function(ele) {
         function fin() {
            return ele.flag = ele.r.g.popup(this.bar.x, this.bar.y, this.bar.value || "0").insertBefore(this);
        }

        function fout() {
            if (ele.flag) {
                return ele.flag.animate({
                    opacity: 0
                }, 0, function() {
                    return this.remove();
                });
            }
            return undefined;
        }

        ele.currBar = ele.r.g.barchart(3, 20, ele.width, ele.height, [ele.data]).hover(fin, fout).attr({
            opacity: 0
        });

    };

    RaphaelRtAnimatedBarHandler.prototype.restBars = function() {
        return _.first(_.last(this.currBar.bars.items).items, this.data.length - 1);
    };

    RaphaelRtAnimatedBarHandler.prototype.fadeLast = function() {
        var lastBar = _.last(_.last(this.currBar.bars.items).items);
        lastBar.animate({
            opacity: 0,
            fill: this.options['color']
        }, 0, function() {
            lastBar.animate({
                opacity: 1
            }, 700);
        });
    };

    RaphaelRtAnimatedBarHandler.prototype.clearChart = function() {
        this.currBar.remove();
    };

    RaphaelRtAnimatedBarHandler.prototype.pushData = function(recentPoints) {
        var r = this.update(recentPoints);
        this.replaceBars();
        return r;
    };

    function RaphaelRtAnimatedBarChart() {
        this.handler = null;
        this._init = function() {
            this.handler = new RaphaelRtAnimatedBarHandler(this.element, this.options);
            this.handler.init();
            $(this.element).css('height', (this.handler.height + 14) + 'px');
        };
    };

    /////////////////////// Widget Construction ///////////////////////
    var raphaelRtAnimatedBarChart = new RaphaelRtAnimatedBarChart();
    var raphaelRtAnimatedLineChart = new RaphaelRtAnimatedLineChart();

    $.widget("kt.RaphaelRtAnimatedBarChart", raphaelRtAnimatedBarChart);
    $.widget("kt.RaphaelRtAnimatedLineChart", raphaelRtAnimatedLineChart);

})(jQuery);
