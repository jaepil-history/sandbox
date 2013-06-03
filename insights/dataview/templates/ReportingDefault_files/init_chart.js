/////////// BEGIN: CHART RELATED STUFF ///////////

// 1) make sure js is ready.
// 2) make sure flex is ready.
var jsReady = false;

$(document).ready(function(){
  jsReady = true;
  var ktFilterHelper = FilterHelper();
});


function isReady(){
  return jsReady && ktFilterHelper.savedFiltersReady;
}

function init_chart_info() {
  var filterType = KT_ENV_JS['filter_type'];
  var isCustomPage = KT_ENV_JS['is_custom_page'];

  if (filterType == 'apply_saved' && !isCustomPage) {
    return { 
      type               : 'multiple_filter',
      saved_filters      : ktFilterHelper.getCheckedFilterInfo(),
      saved_filter_names : ktFilterHelper.getCheckedFilterInfo('name')
    };
  } else {
    return { 
      type: 'singular_filter' 
    };
  }
}

/////////// END: CHART RELATED STUFF ///////////
