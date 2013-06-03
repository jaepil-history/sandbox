var joinEventDict = {};
var ktFilterHelper = FilterHelper();

$(document).ready( function() {
  var $countryInput = $('#country-input');
  var $deviceInput = $('#device-input');
  var ENTER_KEY = 13;
  var $filterPanel = $('#filter-panel');

  // calls the init method to initialize properties and load all saved filters
  ktFilterHelper.init();

  /* Filter panel handlers */
  $filterPanel.hide();
  $('#filter-panel-toggle').click(function(e) {
    e.preventDefault();
    var $this = $(this);

    $filterPanel.slideToggle('fast', function() {
      var $that = $(this);

      if($that.is(':hidden')) {
        $this.removeClass('filter-active');
      } else {
        $this.addClass('filter-active');
      }
    });
  });

  ktFilterHelper.recordCurrentFilters();

  /* Filter search handlers */
  var hasSelected = false;

  $("#device-input, #country-input").keydown(function() {
    $(this).removeClass('help-textbox');
  });

  $("#device-input, #country-input").keyup(function() {
    var $this = $(this);
    if ($this.val() === "") {
      $this.addClass('help-textbox');
    }
  });

  $("#device-input, #country-input").blur(function() {
    var $this = $(this);
    if ($this.val() === "") {
      $this.addClass('help-textbox');
    }
  });

  $("#add-device-btn").click(function() {
    var deviceStr = $deviceInput.val();
    if (deviceStr !== "") {
      ktFilterHelper.ajaxAddDeviceToSelectables(deviceStr);
    }
  });

  $deviceInput.keypress(function(e) {
    var deviceStr = $(this).val();
    if (e.which === ENTER_KEY && deviceStr !== '') {
      ktFilterHelper.ajaxAddDeviceToSelectables(deviceStr);
    }
  });

  $deviceInput.autocomplete({
    source: KT_ENV_JS['root_url'] + '/devices/ajax_device_autocomplete/',
    minLength: 2,
    select: function(event, ui) {
      ktFilterHelper.ajaxAddDeviceToSelectables(ui.item.value);
      hasSelected = true;
    },
    close: function(event, ui) {
      if (hasSelected) {
        $(this).val('');
      }
      hasSelected = false;
    }
  });

  $("#add-location-btn").click(function() {
    var countryStr = $countryInput.val();
    if (countryStr !== "") {
      ktFilterHelper.saveCountryGetIso(countryStr);
    }
  });

  $countryInput.keypress(function(e) {
    var countryStr = $(this).val();
    if (e.which === ENTER_KEY && countryStr !== '') {
      ktFilterHelper.saveCountryGetIso(countryStr);
    }
  });

  $countryInput.autocomplete({
    source: KT_ENV_JS['root_url'] + '/countries/ajax_country_autocomplete/',
    minLength: 2,
    select: function(event, ui) {
      ktFilterHelper.saveCountryGetIso(ui.item.value);
      hasSelected = true;
    },
    close: function(event, ui) {
      if (hasSelected) {
        $(this).val('');
      }
      hasSelected = false;
    }
  });

  $('#saved-filter').on('click', '.saved-filter-name', function(e) {
    e.preventDefault();

    var $this = $(this);
    var filterId = $this.data('filter-id');

    ktFilterHelper.editFilter(filterId);
  });

  $("#event-property-input").autocomplete({
    source: '/event_filter/ajax_event_property_autocomplete/',
    minLength: 2
  });

  $("#device-list").on("click", ".remove-list", function(e) {
    e.preventDefault();
    var $this = $(this);
    var $parentEl = $this.closest("li");
    var deviceToDelete = $parentEl.find("input").val();
    var deviceName = $.trim($parentEl.find("label").text());

    Boxy.confirm("Are you sure you want to delete " + deviceName + "?", function() {
      var deviceArray = [];
      deviceArray.push(deviceToDelete);

      ktAjaxWrapper({
        type: 'POST',
        traditional: true,
        data: {
          'sel_devices': deviceArray
        },
        url: KT_ENV_JS['root_url'] + "/devices/ajax_remove_saved_devices/",
        success: function(data, textStatus) {
          ktFilterHelper.removeDeviceFromDeviceList($parentEl);
        }
      });
    });
  });

  $("#country-list").on("click", ".remove-list", function(e) {
    e.preventDefault();
    var $this = $(this);
    var $parentEl = $this.closest("li");
    var isoToDelete = $parentEl.find("input").val();
    var countryName = $.trim($parentEl.find("label").text());

    Boxy.confirm("Are you sure you want to delete " + countryName + "?", function() {
      var isoArray = [];
      isoArray.push(isoToDelete);

      ktAjaxWrapper({
        type: 'POST',
        traditional: true,
        data: {
          'sel_iso': isoArray
        },
        url: KT_ENV_JS['root_url'] + "/countries/ajax_remove_saved_countries/",
        success: function(data, textStatus) {
          ktFilterHelper.removeCountryFromLocationList($parentEl);
        }
      });
    });
  });

  $("#filter-list").on("click", ".remove-list", function(e) {
    e.preventDefault();
    var $this = $(this);
    var $parentEl = $this.closest("li");
    var filterToDelete = $parentEl.find("input").val();
    var filterName = $.trim($parentEl.find("label").text());

    Boxy.confirm("Are you sure you want to delete " + filterName + "?", function() {
      ktFilterHelper.removeFilter(filterToDelete, $parentEl);
    });
  });

  $('.deletable-list').on('mouseenter', 'li', function() {
    var $this = $(this);
    $this.find('.remove-list').stop(true, true).fadeIn(200);
  });

  $('.deletable-list').on('mouseleave', 'li', function() {
    var $this = $(this);
    $this.find('.remove-list').hide();
  });

  $("#filter-apply-submit").click(function(e) {
    e.preventDefault();
    ktFilterHelper.handleFilter('apply');
  });

  $("#save-submit").click(function(e) {
    e.preventDefault();
    ktFilterHelper.saveFilterModal();
  });

  if (!ktFilterHelper.savedFiltersButtonActivated) {
    ktFilterHelper.savedFiltersButtonActivated = true;

    $("#apply-saved-filters").click(function(e) {
      e.preventDefault();
      ktFilterHelper.applySavedFilters();
    });
  }

  if (KT_ENV_JS['show_event_subtype_filter']) {
    joinEventDict['event_subtype_filter_done'] = false;
  }

  joinEventDict['saved_filter_done'] = false;

  $(document).bind('event_subtype_filter_done', function(event) {
    joinEventDict['event_subtype_filter_done'] = true;
    ktFilterHelper.triggerInitializeAmchartEventIfReady();
  });

  $(document).bind('saved_filter_done', function(event) {
    joinEventDict['saved_filter_done'] = true;
    ktFilterHelper.triggerInitializeAmchartEventIfReady();
  });

  $(".select-all").click(function(e) {
    e.preventDefault();

    var $this = $(this);
    var $listItems = $this.closest('div').find('input');
    $listItems.prop('checked', true);
  });

  $("#filter-clear-all").click(function(e) {
    e.preventDefault();
    var $listItems = $('#filter-panel input');
    var $defaultGender = $('#gender-filter input[value="A"]');

    $listItems.prop('checked', false);
    $defaultGender.prop('checked', true);
  });

});
