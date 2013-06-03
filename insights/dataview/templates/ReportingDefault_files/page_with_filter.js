
/* start of np_chart.js */

function np_get_chart_url (data, category, tab, page, id) {
  var root_url = data.attr('root_url');
  var url_str = root_url+"/np_ajax/" + category + "/" + tab + "/" + page + "/" + id + "/?t=x";
  return url_str;
}


function np_get_chart_multi_url(data, category, tab, page, id, saved_filters)
{
  var root_url = data.attr('root_url');
  var f_ids = saved_filters.join(",");
  var url_str = root_url+"/np_ajax_multi/" + category + "/" + tab + "/" + page + "/" + id + "/?t=x&f_ids=" +f_ids;
  return url_str;
}

function AM_np_get_chart_url(chart_obj, category, tab, page, id){
  var root_url = chart_obj.get_root_url();
  var url_str = root_url+"/np_ajax/" + category + "/" + tab + "/" + page + "/" + id + "/?t=x";
  return url_str;
}

function AM_np_get_chart_multi_url(chart_obj, category, tab, page, id, saved_filters){
  var root_url = chart_obj.get_root_url();
  var f_ids = saved_filters.join(",");
  var url_str = root_url+"/np_ajax_multi/" + category + "/" + tab + "/" + page + "/" + id + "/?t=x&f_ids=" +f_ids;
  return url_str;
}

function AM_np_get_dropdown_url(chart_obj, category, tab, page, id, dropdown_v)
{
  var root_url = chart_obj.get_root_url();
  var url_str = root_url + "/np_ajax/" + category + "/" + tab + "/" + page + "/" + id + "/?t=x&dropdown_v="+dropdown_v;
  return url_str;
}

function AM_np_get_dropdown_multi_url(chart_obj, category, tab, page, id, dropdown_v, saved_filters)
{
  var root_url = chart_obj.get_root_url();
  var f_ids = saved_filters.join(",");
  var url_str = root_url + "/np_ajax_multi/" + category + "/" + tab + "/" + page + "/" + id + "/?t=x&dropdown_v="+dropdown_v +"&f_ids=" + f_ids;
  return url_str;
}


/* end of np_chart.js */

/* start of np_custom_chart.js */

function np_get_chart_url (data, category, section, page, id) {
  var root_url = data.attr('root_url');
  var url_str = root_url+"/custom_dashboard_ajax/" + KT_ENV_JS['custom_dashboard_page_id'] + "/?t=x&id="+id;
  return url_str;
}

function AM_np_get_chart_url(chart_obj, category, section, page, id){
  var root_url = chart_obj.get_root_url();
  var url_str = root_url+"/custom_dashboard_ajax/" + KT_ENV_JS['custom_dashboard_page_id'] + "/?t=x&id="+id;
  return url_str;
}

/* end of np_custom_chart.js */

/* start of np_table_urls.js */

if (KT_ENV_JS['is_custom_page']) {
  window.np_get_table_url = function(table_obj, category, tab, page, id) {
    var root_url = table_obj.root_url;
    var url_str = root_url+"/custom_dashboard_ajax/" + KT_ENV_JS['custom_dashboard_page_id'] + "/?t=j&id="+id;
    return append_api_key_to_url(url_str);
  };

  window.np_get_table_export_url = function(table_obj, category, tab, page, id) {
    var root_url = table_obj.root_url;
    var url_str = root_url+"/custom_dashboard_export/" + KT_ENV_JS['custom_dashboard_page_id'] + "/?t=j&all_levels=1&id="+id;
    return append_api_key_to_url(url_str);
  };

  window.np_run_post_table_load = function(table_obj,id){
  };
} else {
  window.np_get_table_url = function(table_obj, category, tab, page, id) {
    var root_url = table_obj.root_url;
    var url_str = root_url+"/np_ajax/"+category+"/"+tab+"/"+page+"/"+id+"/?t=j";
    return append_api_key_to_url(url_str);
  };

  window.np_get_table_export_url = function(table_obj, category, tab, page, id) {
    var root_url = table_obj.root_url;
    var url_str = root_url+"/np_data_export/"+category+"/"+tab+"/"+page+"/"+id+"/?t=j&all_levels=1";
    return append_api_key_to_url(url_str);
  };

  window.np_run_post_table_load = function(table_obj,id){};
}

/* end of np_table_urls.js */

$(document).ready( function() {
    reset_selected_charts();

    $("[name=chart_selection]").change( function() {
        show_selected_chart($(this).parents(".chart_selector"));
    });

    $("#view_all_charts").click( view_all )
    $("#view_selector_groups").click( view_by_groups );
    
});

function view_by_groups() {
    $(".chart_selector_dropdown").show();
    $(".chart_selector .kt-chart").hide();
    reset_selected_charts();
}

function view_all() {
    $(".chart_selector_dropdown").hide();
    $(".chart_selector .kt-chart").show();
}

function reset_selected_charts() {
    $(".chart_selector").each( function() {
        show_selected_chart(this);
    });
}

function show_selected_chart( container ) {
    var selected_id = "c" + $(container).find("[name=chart_selection]").val();
    $(container).find(".kt-chart").each( function() {
        if($(this).prop('id') == selected_id) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });   
}

ADS_STATUS_LABEL = {
    1 : 'ACTIVE',
    2 : 'PAUSED',
    3 : 'DELETED',
    4 : 'PENDING_REVIEW',
    5 : 'DISAPPROVED',
    8 : 'CAMPAIGN_PAUSED',
    9 : 'ADGROUP_PAUSED'
}

$.fn.ktAdsControl = function() {
  var _columnNumbers = {};
  var getColumnNumber = function(field) {
    if(_columnNumbers[field]) {
      return _columnNumbers[field];
    }

    var result = -1;
    $(".k-table .head-tr td").each(function(i) {
      if($(this).attr("coln_id") == field) {
       result = i;
      }
    });
    _columnNumbers[field] = result;
    return result;
  }

  var PAUSE_BUTTON = '<a href="#pause" class="playback pause">PAUSE</a>';
  var RESUME_BUTTON = '<a href="#resume" class="playback resume">RESUME</a>';
  var makeEditable = function(row, field) {
    var colNum = getColumnNumber(field);
    var col = $(row.find("td:nth-child(" + (colNum + 1) +")"));
    var value = col.text();

    if(value) {
      switch(field) {
      case "status":
        if(row.attr('subtype2') && !row.attr('subtype3')) {
          break;
        }
        var html;

        switch(value) {
        case "ACTIVE":
          html = PAUSE_BUTTON;
          break;
        case "PAUSED":
        case "CAMPAIGN_PAUSED":
        case "ADGROUP_PAUSED":
          html = RESUME_BUTTON;
          break;
        }

        if(!html) {
          break;
        }

        col.append(html);
        col.click(function() {return false});
        $("a",col).click(function() {
          $this = $(this);
          var destStatus;

          switch($this.parent().find("p").text()) {
          case "ACTIVE":
            destStatus = row.attr('subtype2') ? 9 : 2;
            break;
          case "PAUSED":
          case "CAMPAIGN_PAUSED":
          case "ADGROUP_PAUSED":
            destStatus = 1;
            break;
          }

          if(!destStatus) {
            $this.html('');
            return false;
          }

          _saveControlValue(row, field, destStatus, function(data) {
            if(data.status) {
              $this.parent().find("p").html(ADS_STATUS_LABEL[data.status]);
              $this.html(data.status == 1 ? PAUSE_BUTTON : RESUME_BUTTON);
            }
          });
          return false;
        });
        break;
      case "bid":
        if(isNaN(value)) {
          break;
        }
        col.html('<input type="text" value="' + value.replace(/,/g,"") + '">');
        col.click(function() {return false});
        $("input",col).change(function() {
          _saveControlValue(row, field, this.value);
        });
        break;
      }
    }
  }

  this.each(function() {
    if(!this.kt_ads_control) {
      this.kt_ads_contol = true;
      var row = $(this);
      makeEditable(row, "status")
      makeEditable(row, "bid");
    }
  });
  return this;
}

var _saveControlValue = function(row, field, value,success) {
  var _loadedCampaigns = {};

  var getCampaignByLabel = function(label) {
    if(_loadedCampaigns[label]) {
      return _loadedCampaigns[label];
    }
    var result;
    $.ajax({
      type: "GET",
      url: "/dashboard/ad_buying/api/campaign/" + encodeURI(label),
      async: false,
      dataType: "json",
      success: function(data) {
        result = data;
      }
    });
    _loadedCampaigns[label] = result;
    return result;
  }

  var url = KT_ENV_JS['root_url'] + '/ad_buying/api/campaign/';
  var param = {};
  param[field] = value;

  if(row.attr('subtype3')) {
    url += "testing/st1/" + row.attr('subtype1') + "/st2/" + row.attr('subtype2') + "/st3/" + row.attr('subtype3');
  } else if (row.attr('subtype2')) {
    var campaign = getCampaignByLabel(row.attr('subtype1'));
    url += campaign.id + "/creative/" + row.attr('subtype2');
  } else {
    url += 'status/st1/' + row.attr('subtype1');
  }

  $.ajax({
    type: "PUT",
    url: url,
    data: JSON.stringify(param),
    async: false,
    dataType: "json",
    contentType:  'application/json',
    processData: false,
    success: function(data) {
      if(success) {
        success(data);
      }
      if(console) {
        console.info(field + ' value has successfully changed as ' + param[field])
      }
    }
  });
}
$(document).bind("load_all_table_data", function(event) {

  var post_load_events = window.np_run_post_table_load;

  window.np_run_post_table_load = function(table_obj,id){
    $(".k-table .st1_row").ktAdsControl();

    if(post_load_events) {
      post_load_events(table_obj, id);
    }
  }
});

$(document).bind("load_st2_table_data", function(event) {
  $(".k-table .st2_row").ktAdsControl();
});

$(document).bind("load_st3_table_data", function(event) {
  $(".k-table .st3_row").ktAdsControl();
});

var filterHelper = FilterHelper();
var Pinning = (function() {

  var applyInProgress = false;

  var sendPinRequest = function(resource_id, additional_data) {
    var chart_name = $('input[name="chart_name"]').val();
    var custom_page_name = $('input[name="custom_page_name"]').val();
    var custom_page_selection = $('select[name="custom_page_list"]').val();
    var share_level = $('input[name="share"]:checked').val();
    var multiple_filters = $('.pin_popup').data('multiple-filters');
    var existing_page = true;


    if(multiple_filters) {
      return "Please remove multiple saved filters to pin this chart";
    }

    if(!chart_name) {
      return "Must have a chart name";
    }

    if(!custom_page_name) {
      if(!custom_page_selection) {
        return "Must select a custom page";
      }
    } else {
      existing_page = false;
    }

    var url = KT_ENV_JS['root_url'] + '/pin_widget/' + resource_id + '/';

    var data = $.extend({
      'chart_title': chart_name
    }, additional_data);

    if(existing_page) {
      url += custom_page_selection + '/';
    } else {
      data['custom_page_name'] = custom_page_name;
      data['share_level'] = 'private';
    }


    ktAjaxWrapper({
      type: 'GET',
      url: url,
      data: data,
      displayPageMessageError: true,
      maxRetries: 0,
      success:function(data,textStatus)
      {
        var pinned_url = KT_ENV_JS['root_url'] + "/custom_dashboard/" + data.page_id + "/";
        var pinned_anchor = "<a href='" + pinned_url + "' target='_blank'>" + data.page_title + "</a>";

        PageMessage.addMessageToPage({
          type: PageMessage.SUCCESS,
          content: "Chart has been successfully pinned to " + pinned_anchor,
          hidable: true
        });
      }
    });
  };

  var validateAndSend = function(resource_id, additional_data) {
    var errors = sendPinRequest(resource_id, additional_data);

    if(errors) {
      $('.pin_popup .warning').show();
      $('.pin_popup .warning').text(errors);
      return false;
    } else {
      return true;
    }
  };

  var afterLoad = function(args) {
    var $popup = args['popup'];
    var boxy = args['boxy'];
    var resource_id = args['resource_id'];
    var additional_data = args['additional_data'];

    $popup.find("[name=chart_name]").focus();

    if(filterHelper.areDemoFiltersApplied()) {
      $popup.find('.popup-note').show();
    }

    $popup.find("[name=custom_page_list]").change(function() {
      var $createPageSection = $popup.find('.add_custom_page_section');

      if($(this).find(":selected").attr('name') === "create_new_custom_page") {
        $createPageSection.show();
      } else {
        $createPageSection.hide();
      }
    });

    $popup.find('.widget-popup-apply-button').click(function() {
      if(!applyInProgress) {
        applyInProgress = true;

        if(validateAndSend(resource_id, additional_data)) {
          boxy.hide(function() {
            applyInProgress = false;
          });
        } else {
          applyInProgress = false;
        }
      }
    });

  };

  return {
    validateAndSend: validateAndSend,
    afterLoad: afterLoad
  };

})();

$(document).ready(function() {
  $('.page-message-hide').click(PageMessage.hideHandler);

  if($.browser.msie) {
    PageMessage.addMessageToPage({
      type: PageMessage.WARNING,
      content: "Your browser is not supported at this time. Please use a compatible browser, such as Google Chrome, Mozilla Firefox, or Safari.",
      hidable: true,
      id: "IE-dep"
    });
  }
});

var PageMessage = (function() {
  var ERROR = 'error';
  var WARNING = 'warning';
  var INFO = 'info';
  var SUCCESS = 'success';
  var RAW = 'raw';

  var MESSAGE_TEMPLATE = new EJS({url: '/static/ui/js/templates/_page_message.ejs'});

  var hiddenIds = {};
  var messagingOn = true;

  function hideHandler() {
    var $hideButton = $(this);

    $hideButton.parent().hide(); //Hide the message box
    var id = $hideButton.data('page-message-id');

    if(id) {
      $.ajax({
        url: '/dashboard/ajax_hide_page_message/' + id + '/'
      });

      addHiddenId(id);
    }
  }

  function createMessage(type, hidable, content, id) {
    var context = {
      type: type,
      hidable: hidable,
      content: content,
      id: id
    };

    var $message = $(MESSAGE_TEMPLATE.render(context));
    $message.find('.page-message-hide').click(hideHandler);

    return $message;
  }

  function addMessageToPage(args) {
    var type = args['type'];
    var hidable = args['hidable'];
    var content = args['content'];
    var id = args['id'];
    var where = args['where'] || ".info";
    if(messagingOn && !(id in hiddenIds)) {
      var existingMessage = $(where).children('#'+id);
      if (existingMessage.length) {
        existingMessage.children('.page-message-content').html(content);
      } else {
        $(where).first().prepend(createMessage(type, hidable, content, id));
      }
    }
  }

  function addHiddenId(id) {
    hiddenIds[id] = true;
  }

  function turnOffMessaging() {
    messagingOn = false;
  }

  return {
    addMessageToPage: addMessageToPage,
    hideHandler: hideHandler,
    addHiddenId: addHiddenId,
    turnOffMessaging: turnOffMessaging,
    ERROR: ERROR,
    WARNING: WARNING,
    INFO: INFO,
    SUCCESS: SUCCESS
  };
})();

// There should only be one OverlayPageMessage showing at a time.  However, there may be multiple tabs.
// has some common funcs as the above PageMessage but is distinct enough not to inherit

var OverlayPageMessage = (function() {
  var TRAINING = 'training';
  
  var TAB_TITLES = {};
  TAB_TITLES[TRAINING] = 'Training';

  var MESSAGE_TEMPLATE = new EJS({url: '/static/ui/js/templates/_overlay_page_message.ejs'});

  function createMessage(type, hidable, title, content, id) {
    var context = {
      type: type,
      hidable: hidable,
      content: content,
      id: id,
      title: title,
      tab_title: TAB_TITLES[type]
    };

    var $message = $(MESSAGE_TEMPLATE.render(context));
    var $overlayBox = $message.filter('.overlay-dialog-wrapper');
    var $overlayBackground = $message.filter('.overlay-background');
    
    // $overlayBox.draggable({ handle: '.overlay-header', containment: 'document' }); // breaks in Chrome for our version of jquery UI (1.8.4) - gets fixed in 1.8.6
    
    $message.find('.close-btn').click({ overlayBox: $overlayBox, overlayBackground: $overlayBackground }, function(e) {
      var $overlayBox = e.data.overlayBox;
      var $overlayBackground = e.data.overlayBackground;
      $overlayBox.hide();
      $overlayBackground.hide();
    });
    
    $message.filter('.overlay-tab').click({ overlayBox: $overlayBox, overlayBackground: $overlayBackground }, function(e) {
      e.preventDefault();
      var $message = $(this).parent();
      var $overlayBox = e.data.overlayBox;
      var $overlayBackground = e.data.overlayBackground;
      if ($overlayBox.is(':hidden')) {
        $overlayBox.show();
        $overlayBackground.show();
      } else {
        $overlayBox.hide();
        $overlayBackground.hide();
      }
    });

    return $message;
  }

  function addMessageToPage(args) {
    var type = args['type'];
    var hidable = args['hidable'];
    var title = args['title'];
    var content = args['content'];
    var id = args['id'];
    var where = args['where'] || "body";
    var $existingMessage = $(where).children('#'+id);
    if ($existingMessage.length) {
      $existingMessage.children('.page-message-content').html(content);
    } else {
      $(where).first().prepend(createMessage(type, hidable, title, content, id));
    }
  }

  return {
    addMessageToPage: addMessageToPage,
    TRAINING: TRAINING
  };
})();

$(document).ready(function() {

	// Page level warnings should only appear if the customer is in an app
	if (!KT_ENV_JS['is_in_app']){
		return;
	}

	// If we are in an app, we can target the "current" app
	var ajaxGetData = {'target_current':true};
	var consultSystemStatusPage = "Please consult the <a href='" + KT_ENV_JS['root_url'] +"/tools/system_status/'>system status</a> page for further details.";

	ktAjaxWrapper({
        type: "GET",
        url: KT_ENV_JS['root_url'] + '/ajax_get_system_status/',
        traditional: true,
        data: ajaxGetData,
        dataType: 'json',
        success: function(response) {
       		if (response['resp']['current'].app_state === "delayed") {
                // KT-5117
				// PageMessage.addMessageToPage({
				// 	 type: PageMessage.WARNING,
				// 	 hidable: true,
				// 	 id: response["resp"]["app_handle_name"] + "-status-notification",
				// 	 content: "The current application is experiencing a temporary processing delay. " + consultSystemStatusPage
				// });
			}
    	}
    });
});
