var TimeMode = function(mode) {
  if (mode === undefined) {
    mode = 'daily';
  }

  var inputSuffix = {
    'daily': 'day',
    'hourly': 'hour',
    'weekly': 'week',
    'monthly': 'month'
  };
  var MAX_RANGES = {
    'daily': 2 * 365,
    'hourly': 168,
    'weekly': 52 * 3,
    'monthly': 7 * 12
  };
  var MAX_RANGES_MS = {
    'daily': MAX_RANGES['daily'] * 24 * 60 * 60 * 1000, // max two years of data
    'hourly': MAX_RANGES['hourly'] * 60 * 60 * 1000,
    'weekly': MAX_RANGES['weekly'] * 7 * 24 * 60 * 60 * 1000,
    'monthly': MAX_RANGES['monthly'] * 31 * 24 * 60 * 60 * 1000 
  };

  this.timeMode = mode;
  this.inputSuffix = inputSuffix[mode];
  this.MAX_RANGE_MS = MAX_RANGES_MS[mode];

  this.picklistOptions = function() {
    var picklistOptions;
    if (mode === 'daily') {
      picklistOptions = '<li><label class="one-week">One Week to Date</label></li>';
      picklistOptions += '<li><label class="two-weeks">Two Weeks to Date</label></li>';
      picklistOptions += '<li><label class="one-month">One Month to Date</label></li>';
      picklistOptions += '<li><label class="two-months">Two Months to Date</label></li>';
    } else if (mode === 'hourly') {
      picklistOptions = '<li><label class="24-hours">Last 24 Hours</label></li>';
    } else if (mode === 'weekly') {
      picklistOptions = '<li><label class="one-week">Week to Date</label></li>';
      picklistOptions += '<li><label class="two-weeks">Last Week</label></li>';
    } else if (mode === 'monthly') {
      picklistOptions = '<li><label class="one-month">This Month</label></li>';
      picklistOptions += '<li><label class="six-months">Six Months to Date</label></li>';
    }
    return picklistOptions;
  }
  this.addTimestamp = function(strDate) {
    if (mode !== 'daily' && strDate.length === 10) { return strDate + ' 00:00'; }
    return strDate;
  }
  this.dateToFormat = function(date) {
    return dateToNumberDateFormat(date, !(mode === 'daily'));
  }
  this.rangeExceededMssg = function() {
    if (mode === 'hourly') { return "End date for hourly mode cannot be more than a week after start date."; }
    return "The Date range selection exceeds the maximum number of " + this.inputSuffix + "s allowed : " + MAX_RANGES[mode] + " " + this.inputSuffix + "s ";
  }
}

$(document).ready( function() {
  var $activeTimeMode = $('.time_mode_button.active');
  if ($activeTimeMode.data('time-mode') !== 'daily') {
    $('.trends').addClass('disabled-trends');
    $('.trends').prop("title", "Trendlines are currently only supported in daily time series");
  }

  $('a.time_mode_button').click(function(e) {
    e.preventDefault();
    hideCalendar();

    var $this = $(this),
        mode = $this.data('time-mode'),
        $trends = $('a.trends');

    // Make the current time mode button display as active
    $('a.time_mode_button').removeClass('active');
    $this.addClass('active');
    if (mode == 'daily') {
      $trends.removeClass('disabled-trends');
      $trends.prop("title", "Trends");
    } else {
      $trends.addClass('disabled-trends');
      $trends.prop("title", "Trendlines are currently only supported in daily time series");
    }
    ktAjaxWrapper({
      type: "POST",
      url: KT_ENV_JS['root_url'] + "/ajax_set_time_segment/",
      caller: 'set_time_segment',
      data: {
        time_segment: mode[0]
      },
      success: function(data) {
        ktFilterHelper.reloadCharts();
        // show only the current time filter selection boxes
        $('.time_selection').hide();
        $('.time_selection.' + mode).show();
        setup_daterangepickers();
      }
    });

    return false;
  });

  // calendar selection setup
  setup_daterangepickers();
});

var setup_daterangepickers = function() {
  var timeMode = new TimeMode($('a.time_mode_button.active').data('time-mode'));
  var $start = $("#start_" + timeMode.inputSuffix);
  var $end = $("#end_" + timeMode.inputSuffix);
  var $startend = $("#startend-" + timeMode.inputSuffix);

  if ($start.length && $end.length) {
    var startDate = $('#start_' + timeMode.inputSuffix).val();
    var endDate = $('#end_' + timeMode.inputSuffix).val();

    var options = {
      calendars: 3,
      onChange: function(dates) {
        var calendarID = $startend.data().id;
        var wordDate = [];
        if (dates[0] === dates[1]) {
          wordDate[0] = stringToWordDateFormat(dates[0]);
          $startend.val(wordDate[0]);
          $('#editable-start-' + calendarID).val(wordDate[0]);
          $('#editable-end-' + calendarID).val(wordDate[0]);
        } else {
          wordDate[0] = stringToWordDateFormat(dates[0]);
          wordDate[1] = stringToWordDateFormat(dates[1]);
          $startend.val(wordDate.join(' - '));
          $('#editable-start-' + calendarID).val(wordDate[0]);
          $('#editable-end-' + calendarID).val(wordDate[1]);
        }
        $('#preset-ranges-' + calendarID).val('Date Range Presets');
      }
    };
    initCalendar(options, $startend, $('.submenu.submenu-dropdown'), $start.val(), $end.val());
    setCalendarDates($startend.data().id, startDate, endDate);
  }

  var calendarID = $startend.data().id;
  var $widgetCalendar = $('#widget-calendar-' + calendarID);
  var $datepickerInfo = $('#datepicker-info-' + calendarID);
  var $datepickerWrapper = $('#datepicker-wrapper-' + calendarID);

  // Preset time period picklist
  var picklist = '<div>';
  picklist += '<input id="preset-ranges-' + calendarID + '" class="preset-ranges" value="Date Range Presets" readonly>';
  picklist += '<ul id="preset-range-list-' + calendarID + '" class="preset-range-list">';
  picklist += timeMode.picklistOptions();
  picklist += '</ul>';
  picklist += '</div>';
  $datepickerInfo.append(picklist);
  $('#preset-ranges-' + calendarID).click(function() {
    var $this = $(this);
    $this.toggleClass('active');
    $('#preset-range-list-' + calendarID).toggle();
  });

  $('#preset-range-list-' + calendarID + ' label').click(function() {
    var $this = $(this);
    var startDate = new Date();
    var endDate = new Date();

    if ($this.hasClass('one-week')) {
      startDate.addDays(-7);
    } else if ($this.hasClass('two-weeks')) {
      startDate.addDays(-14);
      if (timeMode.timeMode === 'weekly') {
        endDate.addDays(-7);
      }
    } else if ($this.hasClass('one-month')) {
      startDate.addMonths(-1);
    } else if ($this.hasClass('two-months')) {
      startDate.addMonths(-2);
    } else if ($this.hasClass('six-months')) {
      startDate.addMonths(-6);
    } else if ($this.hasClass('24-hours')) {
      startDate.addDays(-1);
    }

    $('#preset-ranges-' + calendarID).val($this.html()).removeClass('active');
    $('#preset-range-list-' + calendarID).hide();

    startDate = timeMode.dateToFormat(startDate);
    endDate = timeMode.dateToFormat(endDate);
    setCalendarDates(calendarID, startDate, endDate);
  });

  appendEditableDates($startend.data().id, $start.val(), $end.val());
  appendApplyCancel(calendarID);
};

function applyTimeFilter(calendarID) {
  var timeMode = new TimeMode($('a.time_mode_button.active').data('time-mode'));
  var $datepickerWrapper = $('#datepicker-wrapper-' + calendarID);
  var startDate = $datepickerWrapper.DatePickerGetDate(true)[0];
  var endDate = $datepickerWrapper.DatePickerGetDate(true)[1];
  var validDates = checkStartBeforeEnd(calendarID, startDate, endDate);
  var $startend = $("#startend-" + timeMode.inputSuffix);

  if (validDates) {
    var $start = $("#start_" + timeMode.inputSuffix);
    var $end = $("#end_" + timeMode.inputSuffix);

    // Modifications to date fields are to send to the server, as it expects hh:mm formatting
    $start.val(timeMode.addTimestamp(startDate));
    $end.val(timeMode.addTimestamp(endDate));

    startDate = stringToDateFormat($start.val());
    endDate = stringToDateFormat($end.val());

    var maxEndDate = new Date(startDate.getTime() + timeMode.MAX_RANGE_MS);

    if (endDate > maxEndDate) {
      Boxy.alert(timeMode.rangeExceededMssg())
      $end.val(timeMode.dateToFormat(maxEndDate));
    }

    hideCalendar();

    var arg = $('form#time_filter_form').serializeArray();
    arg.push({'submit_type':'apply'});
    arg = $.param(arg);

    ktAjaxWrapper({
      type : "POST",
      url : KT_ENV_JS['root_url'] + "/ajax_set_time/",
      traditional: true,
      data : arg,
      dataType: 'json',
      success : function (data, textStatus) {
        ktFilterHelper.reloadCharts();
      }
    });

    // Update the calendar with the new date values
    startDate = $start.val();
    endDate = $end.val()
    $startend.data('start', startDate);
    $startend.data('end', endDate);
    setCalendarDates(calendarID, startDate, endDate);
  }
}

function cancelTimeFilter(calendarID) {
  $('#preset-ranges-' + calendarID).val('Date Range Presets');
  $('.warning-js').hide();
}

