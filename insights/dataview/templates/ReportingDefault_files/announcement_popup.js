var entryID = KT_ENV_JS['announcement_ids'] || [];
var currentID = entryID[0];
var page_number = 1;

function announcementCloseDialog() {
    jQuery(".boxy-modal-blackout").remove();
    jQuery(".boxy-wrapper").remove();
    return false;
}
function announcementNext(){

    for (var i=0; i < entryID.length; i++){
        if (entryID[i] == currentID ){
            if (entryID[i+1] != undefined){
                var nextID = entryID[i+1];
                page_number++;
                jQuery('#popup_entry_' + currentID).hide();
                jQuery('#popup_entry_' + nextID).show();
                jQuery('#checkbox_' + currentID).hide();
                jQuery('#checkbox_' + nextID).show();
                jQuery('#popup_title_' + currentID).hide();
                jQuery('#popup_title_' + nextID).show();
                jQuery('#current_page').text(page_number);
                currentID = nextID;
                break;
            }
        }
    }

}

function announcementPrevious(){

    for (var i=0; i < entryID.length; i++){
        if (entryID[i] == currentID ){
            if (entryID[i-1] != undefined){
                var nextID = entryID[i-1];
                page_number--;                
                jQuery('#popup_entry_' + currentID).hide();
                jQuery('#popup_entry_' + nextID).show();
                jQuery('#checkbox_' + currentID).hide();
                jQuery('#checkbox_' + nextID).show();
                jQuery('#popup_title_' + currentID).hide();
                jQuery('#popup_title_' + nextID).show();
                jQuery('#current_page').text(page_number);
                currentID = nextID;
                break;
            }
        }
    }
    
}

function announcementSave() {
    var reminders = new Array();
    jQuery('[name=announcement_checkbox_entry]').each( 
        function() {
            if(jQuery(this).is(':checked')) {
                reminders.push(jQuery(this).val());
            }
    });
    if (reminders.length != 0){
        jQuery.ajax({
            type: "POST",
            url : KT_ENV_JS['root_url'] + "/ajax_announcement_save/",
            traditional: true,
            data: {'reminders': reminders},
            success: function(response) {
                if (!response.display && response.display != undefined) {
                    jQuery('#announcement_popup_link').hide();
                }
            },
            dataType: "json"
        });
    }
    announcementCloseDialog();
}

function show_announcement_popup(){
    Boxy.load(KT_ENV_JS['root_url'] + "/announcement_popup/", 
       {
         modal:true
       });
}

function announcementOpenImage(image){
    Boxy.alert("<div style=\"overflow:auto;max-height:400px;max-width:600px\"> \
                <img src=\" + image + \"></img> \
                </div>");
}
