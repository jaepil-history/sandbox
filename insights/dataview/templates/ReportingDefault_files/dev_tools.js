$(document).ready(function () {
    $("#dev_tools_clear").click(dev_tools_clear);
    $("#dev_tools_close").click(dev_tools_hide);
    $("body").ajaxComplete(dev_tools_ajaxcomplete);

    $("#dev_tools_box").draggable();

    if (/dev_tools__DEBUG__=1/.exec(document.cookie)) {
        dev_tools_show();
    }
});


// POST to the provided URL with the specified parameters.
// adapted from http://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit/
function post(path, qs) {
    // enctype=text/plain because qs is already urlencoded
    var $form = $('<form method="post" target="_blank" enctype="text/plain"/>')
        .prop("action", path)
    // POST content hacking
    // Must name the field but this adds an artifact: dummy=
    // prepend qs with "dummy&". This neutralize the added dummy
    // name and by turning it into an unused field
    //      dummy=dummy&{original qs}
    // this works because no extra encoding is done for enctype=text/plain
    if (qs) {
        $form.append(
            $('<textarea name="dummy"/>')
                .text("dummy&" + qs)
        );
    }

    // The form needs to be apart of the document in
    // order for us to be able to submit it.
    $(document.body).append($form);
    $form.submit();

    // I hope it is ok to remove it. Note the form is opened in a new blank new
    // page. So we must clean the current page.
    $form.remove();
}


function dev_tools_ajaxcomplete(e, xhr, opt) {

    if (!$('#dev_tools_box').is(':visible')) return;

    // could they have not pass us a xhr?
    xhr = xhr || {};
    var responseText = xhr.responseText || '';
    var clen = responseText.length;
    var error = '';
    var match;

    if (xhr.status >= 300) {
        // Try these as error message
        // 1. HTTP message
        // 2. message from error_ajax_response
        // 3. Simple error message from APIException
        // 4. Django error message

        // 1. HTTP message
        error = xhr.statusText;

        // 2. message from error_ajax_response
        // heuristic to test json response
        if (xhr.responseText.slice(0,1) === '{') {
            if (xhr.responseText.indexOf('"errorMessage"') >= 0) {
                try {
                    // attempt to parse output of error_ajax_response
                    var data = $.parseJSON(xhr.responseText);
                    error = data.errorMessage;
                }
                catch(err) {
                }
            }
        }

        // 3. Simple error message from APIException
        match = /Error: (.*)/.exec(responseText)
        if (match) {
            error = match[0];
        }

        // 4. Django error message
        match = /<pre class=.exception_value.>(.*?)<\/pre>/.exec(responseText)
        if (match) {
            error = match[1];
        }
    }

    dev_tools_log(xhr.status, clen, opt.type.toUpperCase(), opt.url, opt.data, error)
}



function dev_tools_log(status, size, method, url, data, error) {
    var t = (new Date()).toLocaleTimeString();

    // create $test node.
    // It is hard to make a POST request from JavaScript!? Convert it to GET and hope it works..
    var $test = $('<td/>');
    var durl = url + (url.indexOf('?') > 0 ? "&" : "?") + "__debug__";
    if (method === "POST") {
        $test.append($('<a target="_blank">[POST] </a>').attr('href','javascript:void(0)'))
             .click(function() { post(durl, data); })
             .append($('<span />').text(durl));
    } else {
        $test.append($('<a target="_blank">[GET] </a>').attr('href',durl))
             .append($('<span />').text(durl));
    }
    if (error) {
        $test.append($('<div/>').addClass("dev_tools_error").text(error));
    }

    $("#dev_tools_heading").after(
        $('<tr/>')
            .append( $('<td/>').text(t))
            .append( $('<td/>').text(status || ''))
            .append( $('<td/>').text(size || ''))
            .append($test)
    );

    // keep 100 rows
    $("#dev_tools_table").find("tr:gt(100)").remove();
}

function dev_tools_clear() {
    $("#dev_tools_table").find("tr:gt(0)").remove();
}

function dev_tools_show() {
    document.cookie = "dev_tools__DEBUG__=1; path=/"
    $("#dev_tools_box").show();
}

function dev_tools_hide() {
    document.cookie = "dev_tools__DEBUG__=0; expires=Tue Jan 01 00:00:00 1980 UTC; path=/"
    $("#dev_tools_box").hide();
}

// command to manually show dev_tools from debug console
var dev_tools = dev_tools_show;
