
var menu_str = "";
function show_menu(menuobj, menuid) {
    menu_str += "<div class='menu-start'>\n";
    for (var i=0; i<menuobj.length; i++) {
	var mid = menuid + "-" + (i+1);
	if (typeof(menuobj[i].sub) != "undefined") {
	    menu_str += "<div class='menu-item'>";
	    menu_str += "<div class='menu-point' onclick='menu_toggle(\"" + mid + "\");'></div>";
	    if (typeof(menuobj[i].link) != "undefined") {
		menu_str += "<div class='menu-title' id='menu-" + menuobj[i].link + "' onclick='menu_click(this, \"" + menuobj[i].link + "\");'>" + menuobj[i].title + "</div>";
	    } else {
		menu_str += "<div class='menu-title' id='menu-" + menuobj[i].link + "' onclick='menu_toggle(\"" + mid + "\");'>" + menuobj[i].title + "</div>";
	    }
	    menu_str += "<div class='menu-unread' rsshashid='" + menuobj[i].link + "'>&nbsp;</div>";
	    menu_str += "</div>\n";

	    if (menuobj[i].sub != "") {
		menu_str += "<div id='" + mid + "' class='menu-sub' rsshashid='" + menuobj[i].link+ "'>";
		show_menu(menuobj[i].sub, mid);
		menu_str += "</div>\n";
	    }
	} else {
	    menu_str += "<div class='menu-item'>";
	    if (typeof(menuobj[i].link) != "undefined") {
		menu_str += "<div id='menu_" + menuobj[i].link + "' class='menu-title' onclick='menu_click(this,\"" + menuobj[i].link + "\");' title='" + menuobj[i].title + "'>" + menuobj[i].title + "</div>";
	    } else {
		menu_str += "<div id='menu_" + menuobj[i].link + "' class='menu-title' title='" + menuobj[i].title + "'>" + menuobj[i].title + "</div>";
	    }
	    if (menuobj[i].unread != 0) {
		menu_str += "<div class='menu-unread' rsshashid='" + menuobj[i].link + "'>" + menuobj[i].unread + "</div>";
	    } else {
		menu_str += "<div class='menu-unread' rsshashid='" + menuobj[i].link + "'>&nbsp;</div>";
	    }
	    menu_str += "</div>";
	}
    }
    menu_str += "</div>\n";
}

function menu_toggle(menuid) {
    jQuery("#"+menuid).toggle();
}

function menu_click(it, link) {
    jQuery("#menu").find("div[class^=menu]").css({'color':'#000000', 'font-weight':'normal'});
    $(it).css({'color':'blue', 'font-weight':'bold'});
    var menu_title = $(it).text();
    jQuery("#main").html(menu_title);
    if ((typeof(link) != "undefined") && (link != "")) {
	if (link == "star") {	// 星號 list
	    rssd_list(1, "");
	} else if (link == "search") { // 搜尋
	    rssd_search();
	} else if (link.substring(0,3) == "tag") { // TAG
	    tagid = parseInt(link.substring(4,link.length), 10);
	    rssd_list(3, "");
	} else {		// 一般
	    rssd_list(0, link);
	}
    }
}

function menu_start() {
    $.ajaxSetup({ cache: false });
    var menu_conf_url = "apps/menu/menu.py"
    $.ajaxSettings.async = false;
    $.getJSON(menu_conf_url,
	      function(jsonobj) {
		  menu_str = "";
		  show_menu(jsonobj, "menu", "");
		  jQuery("#menu").html(menu_str);
	      });
    $.ajaxSettings.async = true;

    jQuery("div[id^=menu-tag]").parent().parent().parent().show();
    recalc_tagunread();
}
