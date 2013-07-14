
var rss_hashid = "";
var show_mode = 2;		// 顯示模式, 1:顯示全部, 2:僅顯示未閱讀
var rssdlast = 0;		// 是否已到最後
var rssdloading = 0;		// 是否在 loading 中
var tags = [];
var tag_selected = [];
var tagid = -1;

function addweb() {
    // 顯示 訂閱 視窗, 讓 user 輸入要訂閱的網站 URL
    jQuery("#addweb_input").toggle();
    jQuery("#addweb_url").focus();
}

function addweb_hidden() {
    // 隱藏 訂閱 視窗
    jQuery("#addweb_url").val("");
    jQuery("#addweb_input").hide();
}

function addweb_submit() {
    // 訂閱
    var my_hashid = "";
    var weburl = jQuery("#addweb_url").val();
    addweb_hidden();

    // show_message("讀取資料中, 請稍候");
    if (weburl != "") {
	$.blockUI({message: "讀取資料中, 請稍候...", css:{"font-size":"20px"}});
	$.ajaxSetup({ cache: false });
	var rss_addweb_url = "apps/rss/addweb.py?weburl=" + weburl;
	// $.ajaxSettings.async = false;
	$.getJSON(rss_addweb_url,
		  function(data) {
		      if (data["result"] == "ok") {
			  my_hashid = data["hashid"];

			  menu_start();

			  // 重新讀取 rss detail 資料
			  var rss_rss2db_url = "apps/rss/rss2db_web.py?id=" + my_hashid;
			  $.getJSON(rss_rss2db_url,
				    function(data) {
					// 跳到剛剛訂閱網站
					jQuery("#menu td").css({'color': '#000000', 'font-weight': 'normal'});
					jQuery("#menu_"+my_hashid).parent().css({'color': 'blue', 'font-weight': 'bold'});
					jQuery("#menu-td").scrollTop(0);
					var my_menu_pos = jQuery("#menu_"+my_hashid).parent().position();
					jQuery("#menu-td").scrollTop(my_menu_pos.top - jQuery("#my-banner").outerHeight() - jQuery("#addweb-div").outerWidth());
					rssd_list(0, my_hashid);

					$.unblockUI();
				    });
		      } else {
			  $.unblockUI();
			  alert(data["message"]);
		      }
		  });
	// $.ajaxSettings.async = true;
    } else {
	$.unblockUI();
	alert("無法取得 RSS 資料");
    }
}

function rssd_cancel(hashid) {
    // 取消訂閱
    if (confirm("確定要取消訂閱??\n注意, 取消後無法恢復, 必須重新訂閱!!") == true) {

	$.ajaxSetup({ cache: false });
	var rssd_cancel_url = "apps/rssdetail/rssd_cancel.py?id=" + hashid;
	$.ajaxSettings.async = false;
	$.getJSON(rssd_cancel_url,
		  function(data) {
		      if (data["result"] == "ok") {
			  show_message("取消訂閱成功");
			  jQuery("#rss-toolbar").html("");
			  jQuery("#rss-title").html("");
			  jQuery("#main").html("");
			  menu_start();
		      } else {
			  show_message("取消訂閱失敗");
		      }
		  });
	$.ajaxSettings.async = false;
    }
}

function rssd_list(atype ,hashid) {
    // 顯示某網頁的 rss 列表
    // atype==0 : 一般情形
    // atype==1 : 檢視 星號List
    // atype==2 : 搜尋
    // atype==3 : TAG

    jQuery("#main-td").unbind("scroll");

    rss_hashid = hashid;
    rssdlast = 0;
    rssdloading = 0;

    var keyword = "";
    if (atype == 2) {
	keyword = jQuery("#keyword").val();
    }

    $.ajaxSetup({ cache: false });
    // var rssd_list_url = "apps/rssdetail/rssd_list.py?type=" + atype + "&id=" + hashid + "&keyword=" + keyword + "&showmode=" + show_mode;
    var rssd_list_url = "apps/rssdetail/rssd_list.py?type=" + atype + "&id=" + hashid + "&keyword=" + keyword + "&showmode=" + show_mode + "&tagid=" + tagid;
    // alert(rssd_list_url);
    $.ajaxSettings.async = false;
    $.getJSON(rssd_list_url,
	  function(data) {
	      var rssd_list = data["detail"];
	      var rssd_list_str = "";

	      for (var i=0; i<rssd_list.length; i++) {
		  rssd_list_str += "<div id='rssd-list-" + rssd_list[i].id + "' class='rssd-list' my_selected='0'>";
		  rssd_list_str += "<div style='background-color:#F1F1F1;'>";
		  if (rssd_list[i].star == 1) {
		      rssd_list_str += "<div class='star1' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
		  } else {
		      rssd_list_str += "<div class='star' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
		  }
		  rssd_list_str += "<div id='rssd-title' onclick='rssd_detail(" + rssd_list[i].id + ")'>";
		  if (atype != 0) {
		      rssd_list_str += "<div class='rssd-main-title'>" + rssd_list[i].main_title + "</div>";
		  }
		  if (rssd_list[i].readed != 1) {
		      rssd_list_str += "<div class='rssd-title-title' style='font-weight:bold;'>" + rssd_list[i].title + "</div>";
		  } else {
		      rssd_list_str += "<div class='rssd-title-title' style='font-weight:100;'>" + rssd_list[i].title + "</div>";
		  }
		  var pubdate = new Date();
		  pubdate.setTime(rssd_list[i].pubdate * 1000);
		  var ayear = pubdate.getFullYear();
		  var amonth = pubdate.getMonth() + 1;
		  var aday = pubdate.getDate();

		  rssd_list_str += "<div class='rssd-title-date' rssd_date='" + rssd_list[i].pubdate + "'>" + ayear + "-" + amonth + "-" + aday + "</div>";

		  rssd_list_str += "</div>";
		  rssd_list_str += "</div>";
		  rssd_list_str += "<div id='rssd-detail'></div>";
		  rssd_list_str += "</div>";
	      }

	      var toolbar_str = "";
	      if (atype == 0) {	// 一般
		  toolbar_str += "<button class='reload_button' onclick='rssd_reload(\"" + hashid +"\")'>reload</button>&nbsp;";
		  toolbar_str += "<button class='markasread' onclick='rssd_markasread(\"" + hashid + "\")'>全部標示為已閱讀</button>&nbsp;";
		  toolbar_str += "<button id='showmode_button' onclick='showmode(this)'>show mode</button>";
		  toolbar_str += "<div id='showmode' style='display:none;'>";
		  toolbar_str += "<div class='showmode-item' onclick='showmode_choice(0,1)'><div id='showmode1'>&nbsp;</div>顯示全部</div>";
		  toolbar_str += "<div class='showmode-item' onclick='showmode_choice(0,2)'><div id='showmode2'>&nbsp;</div>僅顯示未閱讀</div>";
		  toolbar_str += "</div>&nbsp;";
		  toolbar_str += "<button id='tag_button' onclick='tag_select(this)'>TAG</button>&nbsp;";
		  toolbar_str += "<div id='tag_option' style='display:none;'>";
		  toolbar_str += "</div>";
		  toolbar_str += "<button class='rssd_cancel_button' onclick='rssd_cancel(\"" + hashid +"\")'>取消訂閱</button>&nbsp;";
	      } else if (atype == 1) { // 星號
		  toolbar_str += "<button onclick='rssd_list(1, \"\")'>reload</button>&nbsp;";
	      } else if (atype == 3) { // TAG
		  // toolbar_str += "<button onclick='rssd_list(3, \"\")'>reload</button>&nbsp;";
		  toolbar_str += "<button class='markasread' onclick='rssd_tag_markasread(\"" + tagid + "\")'>全部標示為已閱讀</button>&nbsp;";
		  toolbar_str += "<button id='showmode_button' onclick='showmode(this)'>show mode</button>";
		  toolbar_str += "<div id='showmode' style='display:none;'>";
		  toolbar_str += "<div class='showmode-item' onclick='showmode_choice(3,1)'><div id='showmode1'>&nbsp;</div>顯示全部</div>";
		  toolbar_str += "<div class='showmode-item' onclick='showmode_choice(3,2)'><div id='showmode2'>&nbsp;</div>僅顯示未閱讀</div>";
		  toolbar_str += "</div>&nbsp;";
		  toolbar_str += "<button id='tag_rename' onclick='tag_rename()'>RENAME</button>&nbsp;";
	      }

	      if (atype != 2) {
		  jQuery("#rss-toolbar").html(toolbar_str);
	      }
	      if (atype == 0) {
		  tag_choice(rss_hashid, -1, -1);
	      }
	      var title_title = data.title;
	      if (data.link) {
	      	  title_title = "<a href='" + data.link + "' target='_blank'>" + data.title + "</a>";
	      }
	      jQuery("#rss-title").html(title_title);
	      jQuery("#main").html(rssd_list_str);

	      var title_title_width = jQuery("#rssd-title").outerWidth() - jQuery(".rssd-main-title").outerWidth() - jQuery(".rssd-title-date").outerWidth() - 40;
	      // alert(title_title_width);
	      jQuery("#rssd-title .rssd-title-title").css({"width":title_title_width});

	      // 更新 unreadcnt
	      if (atype == 0) {
		  if (data["unreadcnt"] != 0) {
		      jQuery("div[class=menu-unread][rsshashid="+data["hashid"]+"]").text(data["unreadcnt"]);
		  } else {
		      jQuery("div[class=menu-unread][rsshashid="+data["hashid"]+"]").html("&nbsp;");
		  }
	      }
	  });
    $.ajaxSettings.async = true;

    jQuery("#main-td").scrollTop(0);

    if (atype == 0 || atype == 3) {
	showmode_button_title();
    }

    $("#main-td").scroll(function() {
	if (rssdloading != 1) {
	    if ($("#main-td").height() + $("#main-td").scrollTop() >= $("#main").height()-100) {
		loadmoredata(atype);
	    }
	}
    });
}

function rssd_detail(id) {
    // 顯示 rss 明細資料

    var rssd_list_obj = "#rssd-list-" + id;
    var rssd_title_obj = "#rssd-list-" + id + " #rssd-title";
    var rssd_detail_obj = "#rssd-list-" + id + " #rssd-detail";
    if (jQuery(rssd_detail_obj).html() != "" ) {
	if (jQuery(rssd_detail_obj).is(":hidden")) {
	    rssd_list_unselect();
	    jQuery("#main").find("#rssd-detail").hide();
	    jQuery("#main-td").scrollTop(0);
	    var descination = jQuery(rssd_list_obj).position().top;
	    jQuery(rssd_detail_obj).show();
	    jQuery("#main-td").scrollTop(descination - jQuery("#rss-toolbar").outerHeight() - jQuery("#my-banner").outerHeight());
	    jQuery(rssd_title_obj).css("background-color", "#c1ffc1");
	    jQuery(rssd_title_obj).siblings(":first").css("background-color", "#c1ffc1");
	    rssd_detail_readed(rssd_title_obj, id);
	} else {
	    jQuery(rssd_detail_obj).hide();
	}
    } else {
	rssd_list_unselect();
	jQuery("#main").find("#rssd-detail").hide();
	jQuery("#main-td").scrollTop(0);
	var descination = jQuery(rssd_list_obj).position().top;

	$.ajaxSetup({ cache: false });
	var rssd_detail_url = "apps/rssdetail/rssd_detail.py?id=" + id;
	$.ajaxSettings.async = false;
	$.getJSON(rssd_detail_url,
		  function(data) {
		      var rssd_detail_str = "";
		      rssd_detail_str += "<div class='rssd-detail-title'><a href='" + data["link"] + "' target='_blank'>" + data["title"] + "</a></div>";
		      rssd_detail_str += "<div class='rssd-detail-author'>" + data["author"] + "</div>";
		      rssd_detail_str += "<div class='rssd-detail-content'>" + data["content"] + "</div>";

		      jQuery(rssd_detail_obj).html(rssd_detail_str);
		      jQuery(rssd_detail_obj).show();
		  });
	$.ajaxSettings.async = true;
	jQuery("#main-td").scrollTop(descination - jQuery("#rss-toolbar").outerHeight() - jQuery("#my-banner").outerHeight());
	jQuery(rssd_title_obj).css("background-color", "#c1ffc1");
	jQuery(rssd_title_obj).siblings(":first").css("background-color", "#c1ffc1");
	rssd_detail_readed(rssd_title_obj, id);
	var title_title_width = jQuery("#rssd-title").outerWidth() - jQuery(".rssd-main-title").outerWidth() - jQuery(".rssd-title-date").outerWidth() - 40;
	jQuery("#rssd-title .rssd-title-title").css({"width":title_title_width});
    }
    recalc_tagunread();

    jQuery(".rssd-list").each( function() {
	jQuery(this).attr("my_selected", "0");
    });
    jQuery(rssd_list_obj).attr("my_selected", "1");
}

function rssd_list_unselect() {
    // 將所有的 rssd-title 都改回原底色
    jQuery("#main").find(".star").css("background-color", "#f1f1f1");
    jQuery("#main").find(".star1").css("background-color", "#f1f1f1");
    jQuery("#main").find("#rssd-title").css("background-color", "#f1f1f1");
}

function rssd_detail_readed(aobj, id) {
    // 已經閱讀
    jQuery(aobj).find(".rssd-title-title").css("font-weight", "100");

    $.ajaxSetup({ cache: false });
    var rssd_readed_url = "apps/rssdetail/rssd_readed.py?id=" + id;
    $.getJSON(rssd_readed_url,
	      function(data) {
		  // 更新 unreadcnt
		  if (data["unreadcnt"] != 0) {
		      jQuery("div[class=menu-unread][rsshashid="+data["hashid"]+"]").text(data["unreadcnt"]);
		  } else {
		      jQuery("div[class=menu-unread][rsshashid="+data["hashid"]+"]").html("&nbsp;");
		  }
		  recalc_tagunread();
	      });
}

function rssd_markasread(hashid) {
    // 將所有未讀 item 改為已閱讀
    var last_rssddate = jQuery("#main").children(":first").find(".rssd-title-date").attr("rssd_date");
    // alert(last_rssddate);

    if (typeof(last_rssddate) != "undefined") {
	// show_message("全部標示為已閱讀");
	$.blockUI({message: "處理中, 請稍候...", css:{"font-size":"20px"}});

	setTimeout(function() {
	    $.ajaxSetup({ cache: false });
	    var rssd_markasread_url = "apps/rssdetail/rssd_markasread.py?id=" + hashid + "&lastdate=" + last_rssddate;
	    $.ajaxSettings.async = false;
	    $.getJSON(rssd_markasread_url,
    		      function(data) {

    		      });
	    $.ajaxSettings.async = true;

	    rssd_list(0, hashid);
	    recalc_tagunread();
	    $.unblockUI();
	}, 500);
    }
}

function tag_markasread(id_name) {
    // 將目前 TAG 的所有 item 改為已閱讀
    var last_rssddate = jQuery("#main").children(":first").find(".rssd-title-date").attr("rssd_date");
    // alert(last_rssddate);

    if (typeof(last_rssddate) != "undefined") {
    	// show_message("全部標示為已閱讀");
    	$.blockUI({message: "處理中, 請稍候...", css:{"font-size":"20px"}, fadeIn:0});

    	setTimeout(function() {
    	    $.ajaxSetup({ cache: false });
    	    var rssd_tag_markasread_url = "apps/rssdetail/rssd_tag_markasread.py?tagid=" + tagid + "&lastdate=" + last_rssddate;
    	    $.ajaxSettings.async = false;
    	    $.getJSON(rssd_tag_markasread_url,
    		      function(data) {

    		      });
    	    $.ajaxSettings.async = true;

    	    rssd_list(3, "");
    	    // recalc_tagunread();
    	    start();
    	    $.unblockUI();
    	}, 500);
    }
}

function rssd_tag_markasread() {
    // 將目前 TAG 的所有 item 改為已閱讀, 如果未讀數量超過 99, 要 confirm
    // alert("rssd_tag_markasread");
    var tagid_str = "";
    for (var i=0; i<(3-(tagid+"").length); i++) {
	tagid_str += "0";
    }
    tagid_str += tagid;

    var id_name = "#menu-tag_" + tagid_str;

    var tag_unread_cnt = jQuery(id_name).parent().find(".menu-unread-tag").html();
    if (tag_unread_cnt > 99) {
	if (confirm("確定要全部標示為已閱讀?") == true) {
	    tag_markasread(id_name);
	}
    } else {
	tag_markasread(id_name);
    }
}

function rssd_reload(hashid) {
    // reload rss detail
    jQuery.blockUI({message: "讀取資料中, 請稍候...", css:{"font-size":"20px"}});

    $.ajaxSetup({ cache: false });
    var rss_rss2db_url = "apps/rss/rss2db_web.py?id=" + hashid;
    // $.ajaxSettings.async = false;
    $.getJSON(rss_rss2db_url,
	      function(data) {
		  rssd_list(0, hashid);
		  recalc_tagunread();
		  jQuery.unblockUI();
	      });
    // $.ajaxSettings.async = true;
}

function showmode(it) {
    // 顯示 顯示型態 讓 user 選擇
    var element = it;
    var apos = $(element).offset();

    var xx = apos.left;
    var yy = apos.top + $(element).outerHeight();

    jQuery("#showmode").css({"left":xx, "top":yy});

    if (show_mode == 1) {
	jQuery("#showmode1").html("<img src='images/checkmark.png'></img>");
	jQuery("#showmode2").html("&nbsp;");
    } else {
	jQuery("#showmode2").html("<img src='images/checkmark.png'></img>");
	jQuery("#showmode1").html("&nbsp;");
    }

    jQuery("#showmode").toggle();
}

function showmode_choice(atype, mode) {
    // 改變 showmode, 並重新顯示
    show_mode = mode;

    if (atype == 3) {
	rssd_list(3, "");
    } else {
	rssd_list(0, rss_hashid);
    }
}

function showmode_button_title() {
    // 顯示 showmode_button 名稱
    if (show_mode == 1) {
	jQuery("#showmode_button").text("顯示全部");
    } else {
	jQuery("#showmode_button").text("僅顯示未閱讀");
    }
}

function loadmoredata(atype) {
    // load 進更多資料
    rssdloading = 1;

    var keyword = "";
    if (atype == 2) {
	keyword = jQuery("#keyword").val();
    }

    if (rssdlast != 1) {
	var last_rssdlist = jQuery("#main").children(":last").attr("id");
	if (typeof(last_rssdlist) != "undefined") {
	    var lastid = last_rssdlist.split("-").reverse()[0];

	    $.ajaxSetup({ cache: false });
	    var rssd_loadmoredata_url = "apps/rssdetail/rssd_list.py?type=" + atype + "&id=" + rss_hashid + "&keyword=" + keyword + "&showmode=" + show_mode + "&lastid=" + lastid + "&tagid=" + tagid;
	    // alert(rssd_loadmoredata_url);
	    $.ajaxSettings.async = false;
	    $.getJSON(rssd_loadmoredata_url,
    		      function(data) {
			  var rssd_list = data["detail"];

			  if (rssd_list.length > 0) {
			      for (var i=0; i<rssd_list.length; i++) {
				  var rssd_list_str = "";
				  rssd_list_str += "<div id='rssd-list-" + rssd_list[i].id + "' class='rssd-list' my_selected='0'>";
				  if (rssd_list[i].star == 1) {
				      rssd_list_str += "<div class='star1' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
				  } else {
				      rssd_list_str += "<div class='star' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
				  }
				  rssd_list_str += "<div id='rssd-title' onclick='rssd_detail(" + rssd_list[i].id + ")'>";
				  if (atype != 0) {
				      rssd_list_str += "<div class='rssd-main-title'>" + rssd_list[i].main_title + "</div>";
				  }
				  if (rssd_list[i].readed != 1) {
				      rssd_list_str += "<div class='rssd-title-title' style='font-weight:bold;'>" + rssd_list[i].title + "</div>";
				  } else {
				      rssd_list_str += "<div class='rssd-title-title' style='font-weight:100;'>" + rssd_list[i].title + "</div>";
				  }
				  var pubdate = new Date();
				  pubdate.setTime(rssd_list[i].pubdate * 1000);
				  var ayear = pubdate.getFullYear();
				  var amonth = pubdate.getMonth() + 1;
				  var aday = pubdate.getDate();

				  rssd_list_str += "<div class='rssd-title-date'>" + ayear + "-" + amonth + "-" + aday + "</div>";
				  rssd_list_str += "</div>";
				  rssd_list_str += "<div id='rssd-detail'></div>";
				  rssd_list_str += "</div>";

				  jQuery("#main").append(rssd_list_str);
			      }
			  } else {
			      rssdlast = 1; // 已經到最後了
			  }

    		      });
	}
	$.ajaxSettings.async = true;
    }
    rssdloading = 0;

    var title_title_width = jQuery("#rssd-title").outerWidth() - jQuery(".rssd-main-title").outerWidth() - jQuery(".rssd-title-date").outerWidth() - 40;
    // alert(title_title_width);
    jQuery("#rssd-title .rssd-title-title").css({"width":title_title_width});
}

function starclick(it, id) {
    // alert(id);
    var element = it;
    if ($(element).attr('class') == 'star') { // 未加星號 變 已加星號
	$(element).attr('class', 'star1');

	$.ajaxSetup({ cache: false });
	var rssd_rssdstar_url = "apps/rssdetail/rssd_star.py?id=" + id + "&star=1"
	$.getJSON(rssd_rssdstar_url,
		  function(data) {

		  });
    } else {			// 已加星號 變 未加星號
	$(element).attr('class', 'star');

	$.ajaxSetup({ cache: false });
	var rssd_rssdstar_url = "apps/rssdetail/rssd_star.py?id=" + id + "&star=0"
	$.getJSON(rssd_rssdstar_url,
		  function(data) {

		  });
    }
}

function rssd_search() {
    // 搜尋
    var toolbar_str = "";
    toolbar_str += "Search:&nbsp;<input id='keyword' type='text'></input>&nbsp;";
    toolbar_str += "<button onclick='rssd_list(2, \"\")'>Search</button>&nbsp;";

    jQuery("#rss-toolbar").html(toolbar_str);
    jQuery("#rss-title").html("搜尋");
    jQuery("#main").html("");

    jQuery("#keyword").focus();
}

function get_tags() {
    // 取得 TAG List
    $.ajaxSetup({ cache: false });
    var rssd_taglist_url = "apps/rssdetail/rssd_taglist.py";
    $.ajaxSettings.async = false;
    $.getJSON(rssd_taglist_url,
	      function(data) {
		  tags = data.taglist;
	      });
    $.ajaxSettings.async = true;
    jQuery("#tag_option").hide();
}

function new_tag() {
    // 新增 新的TAG
    var tagname = prompt("TAG名稱??");
    // alert(tagname);

    if (tagname != null && tagname != "" ) {
	$.ajaxSetup({ cache: false });
	var rssd_newtag_url = "apps/rssdetail/rssd_newtag.py?tagname=" + tagname;
	$.ajaxSettings.async = false;
	$.getJSON(rssd_newtag_url,
		  function(data) {
		      tags = data.taglist;
		      tag_options();
		  });
	$.ajaxSettings.async = true;
	jQuery("#tag_option").hide();
    }
}

function tag_select(it) {
    // 顯示/隱藏 TAG 選擇視窗
    var element = it;
    var apos = $(element).offset();

    var xx = apos.left;
    var yy = apos.top + $(element).outerHeight();

    jQuery("#tag_option").css({"left":xx, "top":yy});

    jQuery("#tag_option").toggle();
}

function tag_options() {
    // 產生 TAG 選項
    var tag_option_str = "";
    for (var i=0; i<tags.length; i++) {
	if (jQuery.inArray(tags[i].id, tag_selected) != -1) {
	    tag_option_str += "<div class='tag_item' onclick='tag_choice(\"" + rss_hashid + "\"," + tags[i].id + ",0)'><div class='tag_checkmark' my_selected='1'>&nbsp;</div>" + tags[i].name + "</div>";
	} else {
	    tag_option_str += "<div class='tag_item' onclick='tag_choice(\"" + rss_hashid + "\"," + tags[i].id + ",1)'><div class='tag_checkmark' my_selected='0'>&nbsp;</div>" + tags[i].name + "</div>";
	}
    }
    tag_option_str += "<div class='tag_item' style='border-top:1px solid #cccccc;' onclick='new_tag()'><div class='tag_checkmark' my_selected='0'>&nbsp;</div>新增TAG</div>";

    jQuery("#tag_option").html(tag_option_str);

    // 將 attr my_selected=1 的加上 打勾圖示
    jQuery(".tag_checkmark[my_selected=1]").html("<img src='images/checkmark.png'></img>");
}

function tag_choice(hashid, tagid, sel) {
    // 加上 tag
    // alert(hashid);
    $.ajaxSetup({ cache: false });
    var rssd_tagchoice_url = "apps/rssdetail/rssd_tagchoice.py?hashid=" + hashid + "&tagid=" + tagid + "&sel=" + sel;
    $.ajaxSettings.async = false;
    $.getJSON(rssd_tagchoice_url,
    	      function(data) {
		  tag_selected = data["tagselected"];
		  // alert(tag_selected);
    	      });
    $.ajaxSettings.async = true;

    tag_options();
    jQuery("#tag_option").hide();
}

function recalc_tagunread() {
    // 重新計算 各個TAG 的未讀數量
    jQuery("div[id^=menu-tag]").parent().siblings("div[class='menu-sub']").each(function(data) {
	var taghashid = $(this).attr("rsshashid");
    	var tag_unread = 0;
    	$(this).find("div[class=menu-unread]").each(function(data) {
    	    var unread_num = parseInt($(this).text(), 10);
    	    if (isNaN(unread_num) == false) {
    		tag_unread = tag_unread + unread_num;
    	    }
    	});
    	// alert(tag_unread);
	if (tag_unread > 0) {
	    jQuery("div[class^=menu-unread][rsshashid=" + taghashid + "]").html(tag_unread).addClass("menu-unread-tag");
	} else {
	    jQuery("div[class^=menu-unread][rsshashid=" + taghashid + "]").html("&nbsp;").removeClass("menu-unread-tag");;
	}
    });
}

function tag_rename() {
    // TAG 改名稱
    var tagid_str = "";
    for (var i=0; i<(3-(tagid+"").length); i++) {
	tagid_str += "0";
    }
    tagid_str += tagid;

    var id_name = "#menu-tag_" + tagid_str;
    var old_name = jQuery(id_name).text();
    var new_name = prompt("原TAG名稱: " + old_name + "\n新TAG名稱?");

    if (new_name != null && new_name != "") {
	$.ajaxSetup({ cache: false });
	var rssd_tagrename_url = "apps/rssdetail/rssd_tagrename.py?tagid=" + tagid + "&newname=" + new_name;
	$.ajaxSettings.async = false;
	$.getJSON(rssd_tagrename_url,
    		  function(data) {
		      if (data["result"] == "ok") {
		      	  jQuery(id_name).text(new_name);
		      	  jQuery("#rss-title").text(new_name);
		      }
    		  });
	$.ajaxSettings.async = true;
    }
}

function next_rssd() {
    // 下一筆 rss
    if (jQuery("#main").find(".rssd-list").length > 0) {
	// alert("OK");
	if (jQuery(".rssd-list[my_selected='1']").length > 0) {
	    var next_rssd_id = jQuery(".rssd-list[my_selected='1']").next().attr("id")
	    // alert(next_rssd_id);
	    if (typeof(next_rssd_id) != "undefined") {
		rssd_detail(next_rssd_id.split("-")[2]);
	    }
	} else {
	    var first_rssd_id = jQuery(".rssd-list:first").attr("id");
	    // alert(first_rssd_id);
	    rssd_detail(first_rssd_id.split("-")[2]);
	}
    }
}

function prev_rssd() {
    // 上一筆 rss
    if (jQuery("#main").find(".rssd-list").length > 0) {
	// alert("OK");
	if (jQuery(".rssd-list[my_selected='1']").length > 0) {
	    var prev_rssd_id = jQuery(".rssd-list[my_selected='1']").prev().attr("id");
	    // alert(prev_rssd_id);
	    if (typeof(prev_rssd_id) != "undefined") {
		rssd_detail(prev_rssd_id.split("-")[2]);
	    }
	} else {
	    var first_rssd_id = jQuery(".rssd-list:first").attr("id");
	    // alert(first_rssd_id);
	    rssd_detail(first_rssd_id.split("-")[2]);
	}
    }
}

function rssd_detail_hide() {
    // 隱藏明細
    jQuery(".rssd-list[my_selected='1']").find("#rssd-detail").hide();
}

function rssd_detail_show() {
    // 顯示明細
    jQuery(".rssd-list[my_selected='1']").find("#rssd-detail").show();
}