$(document).ready( function() {
    $('#mau_limit_reminder a.remove_btn').live('click', function() {
      $.ajax({
        url: KT_ENV_JS['root_url'] + '/hide_mau_limit_prompt/',
        method: 'POST',
        success : function() {
          $('#mau_limit_reminder').hide();
        }
      });
    });
});
