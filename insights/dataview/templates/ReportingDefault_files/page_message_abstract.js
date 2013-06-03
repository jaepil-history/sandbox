function ajaxCreatePageMessage(where){
  $.ajax({
    type: 'POST',
    dataType: 'json',
    url: '/dashboard/ajax_get_page_message/' + where,
    success: function(resp){
      var obj = $.parseJSON(resp.data);
      //Only deal with the request if response has data
      if(obj.content){
        //In the future, we may want to deal with showing messages differently
        //For now, the options are "pop_up", "sidebar", and "top"
        if(where === "pop_up"){
          Boxy.alert(obj.content)
        } else if (where === "overlay") {
          OverlayPageMessage.addMessageToPage({
            type: obj.type,
            hidable: obj.hidable,
            title: obj.rule,
            content: obj.content,
            where: obj.where
          });
        } else {
          PageMessage.addMessageToPage({
            type: obj.type,
            hidable: obj.hidable,
            content: obj.content,
            where: obj.where
          });
        }
        //We also want to handle storing which rules the current user has seen
        //ky_message_rules is a cookie which stores a list of rule objects
        //[{"firedrulerule":rulename,"count":num}, ..]
        var ktMessageCookie = getCookie("kt_message_rules");
        if(ktMessageCookie){
          //parse and update the cookie with the new rule that was fired
          var jsonCookie = $.parseJSON(ktMessageCookie);
        } else {
          var jsonCookie = {};
        }

        if (obj.id in jsonCookie) {
          var ruleDetails = jsonCookie[obj.id];
          ruleDetails['count']++;
        } else {
          //create a new rule in the cookie
          jsonCookie[obj.id] = { 'count':1 };
        }
        updateCookie("kt_message_rules", JSON.stringify(jsonCookie), 365);
      }
    }
  });
}
