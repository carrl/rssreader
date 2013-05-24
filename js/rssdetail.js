
var rss_hashid = "";
var show_mode = 2;
var rssdlast = 0;		// 是否已到最後
var rssdloading = 0;		// 是否在 loading 中

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

    jQuery("#main-td").unbind("scroll");

    rss_hashid = hashid;
    rssdlast = 0;
    rssdloading = 0;

    $.ajaxSetup({ cache: false });
    var rssd_list_url = "apps/rssdetail/rssd_list.py?type=" + atype + "&id=" + hashid + "&showmode=" + show_mode;
    $.ajaxSettings.async = false;
    $.getJSON(rssd_list_url,
	  function(data) {
	      var rssd_list = data["detail"];
	      var rssd_list_str = "";

	      for (var i=0; i<rssd_list.length; i++) {
		  rssd_list_str += "<div id='rssd-list-" + rssd_list[i].id + "' style='border-bottom:2px solid #dddddd;'>";
		  if (rssd_list[i].star == 1) {
		      rssd_list_str += "<div class='star1' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
		  } else {
		      rssd_list_str += "<div class='star' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
		  }
		  rssd_list_str += "<div id='rssd-title' onclick='rssd_detail(" + rssd_list[i].id + ")'>";
		  if (atype == 1) {
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
	      }

	      var toolbar_str = "";
	      if (atype == 0) {
		  toolbar_str += "<button onclick='rssd_reload(\"" + hashid +"\")'>reload</button>&nbsp;";
		  toolbar_str += "<button onclick='rssd_markasread(\"" + hashid + "\")'>全部標示為已閱讀</button>&nbsp;";
		  toolbar_str += "<button id='showmode_button' onclick='showmode(this)'>show mode</button>";
		  toolbar_str += "<div id='showmode' style='display:none;'>";
		  toolbar_str += "<div class='showmode-item' onclick='showmode_choice(1)'><div id='showmode1'>&nbsp;</div>顯示全部</div>";
		  toolbar_str += "<div class='showmode-item' onclick='showmode_choice(2)'><div id='showmode2'>&nbsp;</div>僅顯示未閱讀</div>";
		  toolbar_str += "</div>&nbsp;";
		  toolbar_str += "<button class='rssd_cancel_button' onclick='rssd_cancel(\"" + hashid +"\")'>取消訂閱</button>&nbsp;";
	      } else if (atype == 1) {
		  toolbar_str += "<button onclick='rssd_list(1, \"\")'>reload</button>&nbsp;";
	      }

	      jQuery("#rss-toolbar").html(toolbar_str);
	      jQuery("#rss-title").html(data.title);
	      jQuery("#main").html(rssd_list_str);

	      // alert(jQuery(".rssd-main-title").html());
	      var title_title_width = jQuery("#rssd-title").outerWidth() - jQuery(".rssd-main-title").outerWidth() - jQuery(".rssd-title-date").outerWidth() - 40;
	      // alert(title_title_width);
	      jQuery("#rssd-title .rssd-title-title").css({"width":title_title_width});

	      // 更新 unreadcnt
	      if (atype == 0) {
		  if (data["unreadcnt"] != 0) {
		      jQuery("#unread-"+data["hashid"]).text(data["unreadcnt"]);
		  } else {
		      jQuery("#unread-"+data["hashid"]).text("");
		  }
	      }
	  });
    $.ajaxSettings.async = true;

    jQuery("#main-td").scrollTop(0);

    if (atype == 0) {
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
    }
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
		      jQuery("#unread-"+data["hashid"]).text(data["unreadcnt"]);
		  } else {
		      jQuery("#unread-"+data["hashid"]).text("");
		  }
	      });
}

function rssd_markasread(hashid) {
    // 將所有未讀 item 改為已閱讀
    show_message("全部標示為已閱讀");

    $.ajaxSetup({ cache: false });
    var rssd_markasread_url = "apps/rssdetail/rssd_markasread.py?id=" + hashid
    $.ajaxSettings.async = false;
    $.getJSON(rssd_markasread_url,
	  function(data) {

	  });
    $.ajaxSettings.async = true;

    rssd_list(0, hashid);
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

function showmode_choice(mode) {
    // 改變 showmode, 並重新顯示
    show_mode = mode;

    rssd_list(0, rss_hashid);
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
    if (rssdlast != 1) {
	var last_rssdlist = jQuery("#main").children(":last").attr("id");
	if (typeof(last_rssdlist) != "undefined") {
	    var lastid = last_rssdlist.split("-").reverse()[0];

	    $.ajaxSetup({ cache: false });
	    var rssd_loadmoredata_url = "apps/rssdetail/rssd_list.py?type=" + atype + "&id=" + rss_hashid + "&showmode=" + show_mode + "&lastid=" + lastid;
	    $.ajaxSettings.async = false;
	    $.getJSON(rssd_loadmoredata_url,
    		      function(data) {
			  var rssd_list = data["detail"];

			  if (rssd_list.length > 0) {
			      for (var i=0; i<rssd_list.length; i++) {
				  var rssd_list_str = "";
				  rssd_list_str += "<div id='rssd-list-" + rssd_list[i].id + "' style='border-bottom:2px solid #dddddd;'>";
				  if (rssd_list[i].star == 1) {
				      rssd_list_str += "<div class='star1' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
				  } else {
				      rssd_list_str += "<div class='star' onclick='starclick(this, " + rssd_list[i].id + ");'></div>";
				  }
				  rssd_list_str += "<div id='rssd-title' onclick='rssd_detail(" + rssd_list[i].id + ")'>";
				  if (atype == 1) {
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
