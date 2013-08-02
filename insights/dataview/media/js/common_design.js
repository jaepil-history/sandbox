$(document).ready(function() {
			
			$(".login input").focus(function(){
				$(this).removeClass("bg"); 
			});
			
			$(".login input").focusout(function(){
				var login = $(this).attr("value");
				if (login == "") {
					$(this).addClass("bg");
				} else {
					return false;
				}
			});
		});






function setPng24(obj) {
	obj.width=obj.height=1;
	obj.className=obj.className.replace(/\bpng24\b/i,'');
	obj.style.filter =
	"progid:DXImageTransform.Microsoft.AlphaImageLoader(src='"+ obj.src +"',sizingMethod='image');" 
	obj.src=''; 
	return '';
}

