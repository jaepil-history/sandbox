$(document).ready( function() {
    $("#app_drop_down").change(function() {
      if($(this).val() != "no_app") {
        if (KT_ENV_JS['is_in_app']) {
          // ALL other pages

          $.ajax({
            type        : 'POST',
            data : {
              'app_api_key' : $(this).val()
            },
            url         : KT_ENV_JS['root_url'] + "/ajax_app_switch/",
            traditional : true,
            dataType    : 'json',
            success     : app_change
          });
        } else {
          // The Applications Page
          // Account Pages
          document.app_direct_form.submit();
        }
      }
    });

});

function app_change(data, textStatus){
  if(data.responseCode === 1){
    if (KT_ENV_JS['is_custom_page']){
       window.location="/dashboard/custom_dashboard/?api_key=" + data.api_key;
    } else{
      document.app_direct_form.submit();
    }
  }
}
