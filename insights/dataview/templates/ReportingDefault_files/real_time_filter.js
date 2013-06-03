function KtRealTimeDataSource(rootUrl) {
    this.rootUrl = rootUrl;
    this.msgType = null;
    this.realtimeRaphaelUpdateEvent = null;
    this.lastTimeStamp = null;
    this.cachedData = null;
}

KtRealTimeDataSource.prototype = {
    clearDataCache: function() {
        this.lastTimeStamp = null;
        this.cachedData = null;
    },

    renderRtChartData: function() {
        if (this.cachedData) {
            $(document).trigger(this.realtimeRaphaelUpdateEvent, this.cachedData);
        }
    },

    getRtChartData: function() {
        var queryUrl = this.rootUrl + '/ajax_get_app_messages/' + this.msgType + '/';
        //TODO: if summary_data_cache is there, grab the most recent timestamp and send it over ajax.
        // Likewise with detail_data_cache
        var args = {};
        var _thisObj = this;
        if (_thisObj.lastTimeStamp) {
            args['last_time_stamp'] = _thisObj.lastTimeStamp;
        }
        args['interval'] = KT_ENV_JS['ui_update_frequency'];
        $.ajax({
            type: 'GET',
            url: queryUrl,
            data: args,
            async: true,
            dataType: 'json',
            timeout: _thisObj.RT_DELAY * 1000,
            traditional: true,
            success: function(data, textStatus, jqXHR) {
                if (data) {
                    var first_time = false;
                    if (!_thisObj.cachedData) first_time = true;
                    _thisObj.cachedData = data;

                    for (key in data) {
                        // there should only be one key for the monitor_rt page.
                        var lastTimeStampIndex = data[key].length - 1;
                        if (lastTimeStampIndex >= 0) _thisObj.lastTimeStamp = data[key][lastTimeStampIndex][0];
                        if (first_time) {
                            _thisObj.renderRtChartData();
                        }
                    }
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                //What should we do here?
            }
        });
    }
};

function KtRealTimeSummaryDataSource(rootUrl) {
    this.inheritedFrom = KtRealTimeDataSource;
    this.inheritedFrom(rootUrl);
    this.msgType = "summary";
    this.realtimeRaphaelUpdateEvent = "setSummaryRealtimeRaphael";
}
KtRealTimeSummaryDataSource.prototype = new KtRealTimeDataSource();


function KtRealTimeDetailDataSource(rootUrl) {
    this.inheritedFrom = KtRealTimeDataSource;
    this.inheritedFrom(rootUrl);
    this.msgType = "detail";
    this.realtimeRaphaelUpdateEvent = "setDetailRealtimeRaphael";
}
KtRealTimeDetailDataSource.prototype = new KtRealTimeDataSource();


function KtRealTimeFilter(rootUrl, intervalSeconds) {
    this.rootUrl = rootUrl;
    this.countDownSeconds = null;
    this.countDownTimer = null;
    this.uiIntervalSeconds = intervalSeconds;
    this.RT_DELAY = 2;
    this.summaryDataSource = new KtRealTimeSummaryDataSource(rootUrl);
    this.detailDataScource = new KtRealTimeDetailDataSource(rootUrl);
}

KtRealTimeFilter.prototype = {
    init: function() {
        var _thisObj = this;
        this.activateTimer();
        $(document).bind('app_handle_updated', function() {
            _thisObj.activateTimer(); //start anew
        });
        $("input.view_message").click(function() {
            _thisObj.toggleRtChart(this);
        });
    },

    toggleRtChart: function(item) {
        if ($(item).is(':checked')) {
            var chartId = $(item).prop('id').replace('check_', 'c');
            $('#' + chartId).parent().parent().fadeIn();
        } else {
            var chartId = $(item).prop('id').replace('check_', 'c');
            $('#' + chartId).parent().parent().fadeOut();
        }
    },

    activateTimer: function() {
        var _thisObj = this;
        this.summaryDataSource.clearDataCache();
        this.detailDataScource.clearDataCache();

        this.summaryDataSource.getRtChartData();
        this.detailDataScource.getRtChartData();

        //this.summaryDataSource.renderRtChartData();
        //this.detailDataScource.renderRtChartData();
        if (this.countDownTimer) {
            clearInterval(this.countDownTimer);
        }
        this.countDownSeconds = this.uiIntervalSeconds;

        this.countDownTimer = setInterval(function() {
            _thisObj.showTimeRemaining();
        }, 1000);
    },
    setUpdateInterval : function(updateInterval) {
        this.uiIntervalSeconds = updateInterval;
        this.countDownSeconds = updateInterval;
    },
	reloadCharts : function() {
	    this.summaryDataSource.clearDataCache();
	    this.detailDataScource.clearDataCache();
	
	    this.summaryDataSource.getRtChartData();
	    this.detailDataScource.getRtChartData();
	
	    this.summaryDataSource.renderRtChartData();
	    this.detailDataScource.renderRtChartData();
	},

    showTimeRemaining: function() {
        var minutes = Math.floor(this.countDownSeconds / 60);
        var seconds = this.countDownSeconds - (minutes * 60);

        var padding = (seconds < 10) ? "0" : "";

        $("#next_realtime_update span").text(minutes + ":" + padding + seconds);

        if (this.countDownSeconds === 3) {
            // avoid the delay with count down. Fetch the data a couple seconds earlier.
            this.summaryDataSource.getRtChartData();
            this.detailDataScource.getRtChartData();
        }
        if (this.countDownSeconds === 0) {
            this.summaryDataSource.renderRtChartData();
            this.detailDataScource.renderRtChartData();
            this.countDownSeconds = this.uiIntervalSeconds;
        } else {
            this.countDownSeconds = this.countDownSeconds - 1;
        }
    }
};
