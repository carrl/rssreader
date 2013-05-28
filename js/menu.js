
var menu_str = "";
function show_menu(menuobj, menuid) {
    menu_str += "<table width='100%' border='0'>\n";
    for (var i=0; i<menuobj.length; i++) {
	var mid = menuid + (i+1);
	if (typeof(menuobj[i].sub) != "undefined") {
	    menu_str += "<tr onMouseOver=\"bgColor='#E5ECF5'; this.style.cursor='pointer'\" onMouseOut=\"bgColor='FFFFFF'\">";
	    menu_str += "<td width='6px' align='center' valign='middle' onMouseOver='this.style.cursor=\"pointer\"' onclick='menu_toggle(\"" + mid + "\");'>";
	    menu_str += "<img src='images/arrow_right.png' />";
	    menu_str += "</td>";
	    if (typeof(menuobj[i].link) != "undefined") {
		menu_str += "<td onClick='menu_click(this, \"" + menuobj[i].link + "\");'>" + menuobj[i].title + "</td>";
	    } else {
		menu_str += "<td onClick='menu_toggle(\"" + mid + "\");'>" + menuobj[i].title + "</td>";
	    }
	    menu_str += "</tr>\n";

	    menu_str += "<tr><td></td><td><div id='" + mid +"'>";
	    show_menu(menuobj[i].sub, mid);
	    menu_str += "</div></td></tr>\n";
	} else {
	    if (typeof(menuobj[i].link) != "undefined") {
		menu_str += "<td onMouseOver=\"bgColor='#E5ECF5'; this.style.cursor='pointer'\" onMouseOut=\"bgColor='FFFFFF'\" onClick='menu_click(this,\"" + menuobj[i].link + "\");'>";
	    } else {
		menu_str += "<td onMouseOver=\"bgColor='#E5ECF5'; this.style.cursor='pointer'\" onMouseOut=\"bgColor='FFFFFF'\">";
	    }
	    menu_str += "<div id='menu_" + menuobj[i].link + "' style='overflow:hidden; white-space:nowrap; width:160px;' title='" + menuobj[i].title + "'>" + menuobj[i].title + "</div>";
	    menu_str += "</td><td>";
	    if (menuobj[i].unread != 0) {
		menu_str += "<div style='overflow:hidden; white-space:nowrap; text-align:right;' id='unread-" + menuobj[i].link + "'>" + menuobj[i].unread + "</div>";
	    } else {
		menu_str += "<div style='overflow:hidden; white-space:nowrap; text-align:right;' id='unread-" + menuobj[i].link + "'>&nbsp;</div>";
	    }
	    menu_str += "</td></tr>\n";
	}
    }
    menu_str += "</table>\n";
}

function menu_toggle(menuid) {
    jQuery("#"+menuid).toggle();
}

function menu_click(it, link) {
    jQuery("#menu td").css({'color': '#000000', 'font-weight': 'normal'});
    $(it).css({'color': 'blue', 'font-weight': 'bold'});
    var menu_title = $(it).text();
    jQuery("#main").html(menu_title);
    if ((typeof(link) != "undefined") && (link != "")) {
	if (link == "star") {	// 星號 list
	    rssd_list(1, "");
	} else if (link == "search") { // 搜尋
	    rssd_search();
	} else {		// 一般
	    rssd_list(0, link);
	}
    }
}

function menu_start() {
    $.ajaxSetup({ cache: false });
    var menu_conf_url = "apps/menu/menu.py"
    $.getJSON(menu_conf_url,
	      function(jsonobj) {
		  menu_str = "";
		  show_menu(jsonobj, "menu", "");
		  jQuery("#menu").html(menu_str);
	      });
}
