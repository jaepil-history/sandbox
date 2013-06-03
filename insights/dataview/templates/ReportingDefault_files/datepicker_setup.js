var canFocus = true;
var numCalendars = 0;

$(document).ready( function() {
  // Hide calendar if anything else is clicked
  $('body').click(function(e) {
    var $target = $(e.target);
    var isCalendar = $target.parents('.widget-calendar').length || $target.hasClass('widget-calendar');
    var isDateRangeInput = $target.hasClass('startend-time');
    var isBoxyAlert = $target.parent('.answers').length;

    if (!isCalendar && !isDateRangeInput && !isBoxyAlert) {
      hideCalendar();
    }

    var isPresetSelector = $target.hasClass('preset-ranges');
    if (!isPresetSelector) {
      $('.preset-ranges').removeClass('active');
      $('.preset-range-list').hide();
    }
  });

  // Reposition the calendar if the window is resized
  $(window).resize(function() {
    $('.startend-time:visible').each(function() {
      setPosition($(this).data().id);
    });
  });
});

/**************************
 *
 * Initialize the calendar
 *
 **************************/

function initCalendar(options, $startend, $calendarParent, start, end) {
  // Clear any calendars already associated with this $startend
  $('#widget-calendar-' + $startend.data().id).remove();
  $startend.off('click');

  // Set the new calendar ID
  var calendarID = numCalendars;
  $startend.data('id', numCalendars);
  numCalendars++;

  // If available, store the initial start/end dates
  $startend.data('start', start ? start : '');
  $startend.data('end', end ? end : '');

  // Append calendar widget to the appropriate area
  $calendarParent.append('<div id="widget-calendar-' + calendarID + '" class="calendar-hidden widget-calendar"></div>');

  // datepicker-wrapper on left, datepicker-info on right
  var $widgetCalendar = $('#widget-calendar-' + calendarID);
  $widgetCalendar.append('<div id="datepicker-wrapper-' + calendarID + '" class="datepicker-wrapper"></div>');
  $widgetCalendar.append('<div id="datepicker-info-' + calendarID + '" class="datepicker-info kt-right"></div>');
  var $datepickerWrapper = $('#datepicker-wrapper-' + calendarID);

  // Store the id of the startend input field and calendarID
  $widgetCalendar.data('startend', $startend.attr('id'));
  $widgetCalendar.data('id', calendarID);

  // Set up the calendar
  var defaultOptions = {
    date: new Date(),
    flat: true,
    starts: 0,
    prev: '',
    next: '',
    mode: 'range',
    locale: {
      days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      daysMin: ["S", "M", "T", "W", "T", "F", "S", "S"],
      months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      weekMin: 'wk'
    }    
  };
  $datepickerWrapper.DatePicker($.extend(defaultOptions, options))
  $datepickerWrapper.DatePickerClear();

  // Enable the first and last month selectors
  $($('#widget-calendar-' + calendarID + ' .datepickerGoPrev a').get(0)).css('display', 'block');
  $($('#widget-calendar-' + calendarID + ' .datepickerGoNext a').get(-1)).css('display', 'block');

  // Disable the built-in calendar view selector
  $('.datepickerMonth a').bind('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
  });

  // Show or hide the calendar panel
  $startend.on('click', function(e) {
    var $this = $(this);
    var $widgetCalendar = $('#widget-calendar-' + $this.data().id);
    var calendarHidden = $widgetCalendar.hasClass('calendar-hidden');

    if (calendarHidden) {
      $widgetCalendar.removeClass('calendar-hidden').show();
      setPosition($this.data().id);
    } else {
      hideCalendar();
    }
  });
}

/*********************************************
 *
 * Add the editable start and end input boxes
 *
 *********************************************/

function appendEditableDates(calendarID, startDate, endDate) {
  var $datepickerInfo = $('#datepicker-info-' + calendarID);

  // Editable start/end fields
  var editableHtml = '<input id="editable-start-' + calendarID + '" class="editable-date"/>';
  editableHtml += '<label>---</label>';
  editableHtml += '<input id="editable-end-' + calendarID + '" class="editable-date"/>';
  editableHtml += '<small>All metrics reported in UTC time.</small>';
  $datepickerInfo.append(editableHtml);

  var $editableDate = $('.editable-date');
  
  // Set the dates
  $('#editable-start-' + calendarID).val(stringToWordDateFormat(startDate));
  $('#editable-end-' + calendarID).val(stringToWordDateFormat(endDate));

  // Chrome window blur/focus triggers a blur/focus event on all elements.
  // canFocus tests if the blur/focus is caused by the window so $editableDate does not blur/focus multiple times.
  $editableDate.on('focus', function() {
    if (canFocus) {
      var $this = $(this);
      var calendarID = $this.parents('.widget-calendar').data().id;
      $this.data('date', $this.val());
      var numFormat = stringToNumberDateFormat($this.val());
      $this.val(numFormat);
      $('#preset-ranges-' + calendarID).val('Date Range Presets');
    }
  });

  $editableDate.on('blur', function() {
    if (!canFocus) {
      var $this = $(this);
      var calendarID = $this.parents('.widget-calendar').data().id;
      var $editableStart = $('#editable-start-' + calendarID);
      var $editableEnd = $('#editable-end-' + calendarID);
      var wordFormat = stringToWordDateFormat($this.val());
      if (wordFormat === "Invalid date") {
        Boxy.alert("Incorrect date format.<br>Please input the date in the form yyyy-mm-dd.");
        $this.val($this.data('date'));
      } else if (wordFormat === '') {
        $this.val($this.data('date'));
      } else {
        $this.val(wordFormat);

        var numStartDate = stringToNumberDateFormat($editableStart.val());
        var numEndDate = stringToNumberDateFormat($editableEnd.val());
        if (numEndDate) {
          setCalendarDates(calendarID, numStartDate, numEndDate);
          $('.startend-cohort-query:visible').val(''); // Cohort startend doesn't update until apply 
        }

        // Check if start is before end
        var start = $editableStart.val();
        var end = $editableEnd.val();
        if (start && end) {
          start = stringToNumberDateFormat(start);
          end = stringToNumberDateFormat(end);
          checkStartBeforeEnd(calendarID, start, end);
        }
      }
    }
  });

  $editableDate.on({
    "focus": function() {
      canFocus = false;
    },
    "blur": function() {
      canFocus = true;
    }
  });
}

/***********************************
 *
 * Add the apply and cancel buttons
 *
 ***********************************/

function appendApplyCancel(calendarID) {
  var $datepickerInfo = $('#datepicker-info-' + calendarID);

  // Apply button applies changes
  $datepickerInfo.append('<a href="#" id="time-filter-apply-' + calendarID + '" class="kt-button kt-primary time-filter-button">Apply</a>');
  $('#time-filter-apply-' + calendarID).on('click', function(e) {
    e.preventDefault();
    if ($('#datepicker-wrapper-' + calendarID).DatePickerGetDate().length) {
      applyTimeFilter(calendarID);
    }
  });

  // Cancel button reverts back to when apply was last pressed and closes the widget
  $datepickerInfo.append('<a href="#" id="time-filter-cancel-' + calendarID + '" class="time-filter-button">Cancel</a>');
  $('#time-filter-cancel-' + calendarID).on('click', function(e) {
    e.preventDefault();
    var $startend = $('#' + $(this).parents('.widget-calendar').data().startend);
    var calendarID = $startend.data().id;
    setCalendarDates(calendarID, $startend.data('start'), $startend.data('end'));
    cancelTimeFilter(calendarID);
    hideCalendar();
  });
}

/*********************
 *
 * Hides the calendar
 *
 *********************/

function hideCalendar() {
  $('.widget-calendar').addClass('calendar-hidden');
}

/***********************************
 *
 * Adjust the width and positioning
 *
 ***********************************/

function setPosition(calendarID) {
  var $startend = getStartEndFromID(calendarID);
  if (!$startend) { return false; }

  var $widgetCalendar = $('#widget-calendar-' + calendarID);
  var $datepickerWrapper = $('#datepicker-wrapper-' + calendarID);
  var $datepickerInfo = $('#datepicker-info-' + calendarID);

  // Set dividing border
  var datepickerHeight = $datepickerWrapper.outerHeight(true);
  var datepickerInfoHeight = $datepickerInfo.outerHeight(true);
  if (datepickerHeight > datepickerInfoHeight) {
    $datepickerWrapper.addClass('inner-calendar-border');
    $datepickerInfo.removeClass('inner-calendar-border');
  } else {
    $datepickerWrapper.removeClass('inner-calendar-border');
    $datepickerInfo.addClass('inner-calendar-border');
  }

  // Set calendar widget width
  var datepickerWidth = $datepickerWrapper.outerWidth(true);
  var datepickerInfoWidth = $datepickerInfo.children().length ? $datepickerInfo.outerWidth(true) : 0;
  $widgetCalendar.css('width', datepickerWidth + datepickerInfoWidth + 1 + 'px');

  // Set left positioning
  var position = $startend.position().left;
  if (!$startend.hasClass('calendar-left-align')) {
    position -= $widgetCalendar.outerWidth(true);
    position += $startend.outerWidth(true);
  }
  $widgetCalendar.css('left', position + 'px');

  // Set top position
  position = $startend.position().top;
  position += $startend.outerHeight();
  $widgetCalendar.css('top', position + 'px');
}

/*****************************************
 *
 * Check if start date is before end date
 *
 *****************************************/

function checkStartBeforeEnd(calendarID, start, end) {
  // Expects start/end to be in yyyy-mm-dd format
  var $warning = $('#datepicker-info-' + calendarID + ' .warning-js');
  if (stringToDateFormat(start) > stringToDateFormat(end)) {
    if (!$warning.length) {
      var message = '<div class="warning-js">End date cannot end before start date.</div>';
      $('#datepicker-info-' + calendarID).append(message);
    }
    return false;
  }
  $warning.remove();
  return true;
}

/*************************************
 *
 * Update dates in relevant locations
 *
 *************************************/

function setCalendarDates(calendarID, start, end) {
  var $startend = getStartEndFromID(calendarID);
  var $datepicker = $('#datepicker-wrapper-' + calendarID + ' .datepicker');
  var $datepickerWrapper = $('#datepicker-wrapper-' + calendarID);

  // Place the last selected month in the last calendar
  var numCalendars = $datepicker.data().datepicker.calendars;
  var displayEnd = stringToDateFormat(end);
  if (displayEnd) {
    displayEnd.setDate(1);
    if (numCalendars > 1) {
      displayEnd.setMonth(displayEnd.getMonth()-1);
    }
    $datepicker.data().datepicker.current = displayEnd;
  }

  // Set the dates on the calendar
  if (!start || !end) {
    $datepickerWrapper.DatePickerClear();
  } else {
    $datepickerWrapper.DatePickerSetDate([start, end]);
  }

  // Update the histogram
  if ($startend.data().histogram) {
    refreshHistogramOverlay(calendarID, 'datepicker', start, end);
  }

  // Update the visible start/end input date values
  start = stringToWordDateFormat(start);
  end = stringToWordDateFormat(end);
  if ($startend.is('#startend-retention')) {
    // Retention pages only show the start date
    $startend.val(start);
  } else {
    $startend.val(start === end ? start : start + ' - ' + end);
  }
  $('#editable-start-' + calendarID).val(start);
  $('#editable-end-' + calendarID).val(end);
}

/*********************************
 *
 * Find $startend from calendarID
 *
 *********************************/

function getStartEndFromID(calendarID) {
  var $widgetCalendar = $('#widget-calendar-' + calendarID);
  if ($widgetCalendar) {
    var $startend = $('#' + $widgetCalendar.data().startend);
    return $startend;
  }
  return false;
}

/***************************
 *
 * Date Parsing Functions
 *
 ***************************/

function appendLeadingZero(number) {
  if (number < 10) {
    return '0' + number;
  }
  return number;
}

function dateToWordDateFormat(dateobj) {
  if (!dateobj) { return false; }
  return dateobj.getMonthName()
   + ' '
   + appendLeadingZero(dateobj.getDate())
   + ', '
   + dateobj.getFullYear();
}

function dateToNumberDateFormat(dateobj, includeTime) {
  if (!dateobj) { return false; }
  var date = dateobj.getFullYear()
    + '-'
    + appendLeadingZero(dateobj.getMonth() + 1)
    + '-'
    + appendLeadingZero(dateobj.getDate());
  if (includeTime) {
    date += ' ' + (appendLeadingZero(dateobj.getHours()) + ':00');
  }
  return date;
}

function dateToNumberDateUTCFormat(dateobj, includeTime) {
  if (!dateobj) { return false; }
  var date = dateobj.getUTCFullYear()
    + '-'
    + appendLeadingZero(dateobj.getUTCMonth() + 1)
    + '-'
    + appendLeadingZero(dateobj.getUTCDate());
  if (includeTime) {
    date += ' ' + (appendLeadingZero(dateobj.getUTCHours()) + ':00');
  }
  return date;
}

function stringToWordDateFormat(strdate) {
  if (strdate === '') { return ''; }
  var date = stringToDateFormat(strdate.slice(0,10)); // Only want yyyy-mm-dd portion, not time
  return dateToWordDateFormat(date);
}

function stringToNumberDateFormat(strdate) {
  if (strdate === '') { return ''; }
  var date = stringToDateFormat(strdate);
  return dateToNumberDateFormat(date);
}

function stringToDateFormat(strdate) {
  var strRegEx = new RegExp('^[A-z]{3}\\s[0-9]{1,2},\\s[0-9]{4}(\\s[0-9]{2}:[0-9]{2})?$');
  var numRegEx = new RegExp('^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}(\\s[0-9]{2}:[0-9]{2})?$');

  if (strRegEx.test(strdate)) {
    // e.g. Jan 01, 2013
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var date = strdate.split(' ');
    var time = date.length > 3 ? date[3].split(':') : ['00', '00'];

    return new Date(
      date[2],                  // Year
      months.indexOf(date[0]),  // Month (Months in JS are zero-indexed)
      date[1].slice(0,2),       // Day
      time[0],                  // Hour
      time[1]                   // Minute
    );
  } else if (numRegEx.test(strdate)) {
    // e.g. 2013-01-01
    var parts = strdate.split(' ');
    var date = parts[0].split('-');
    var time = parts.length > 1 ? parts[1].split(':') : ['00', '00'];

    return new Date(
      date[0],    // Year
      date[1]-1,  // Month (Months in JS are zero-indexed)
      date[2],    // Day
      time[0],    // Hour
      time[1]     // Minute
    );
  } else {
    return false;
  }
}

function unixTimestampToNumberDateFormat(timestamp) {
  var date = new Date(timestamp*1000); // javascript uses milliseconds
  return dateToNumberDateUTCFormat(date);
}

