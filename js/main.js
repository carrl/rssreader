
var my_userid = "";		// userid

// 設定 #main 的高度
function setMainHeight() {
    var menu_height = jQuery(window).height() - jQuery("#my-banner").outerHeight() - jQuery("#addweb-div").outerHeight();
    var main_height = jQuery(window).height() - jQuery("#my-banner").outerHeight() - jQuery("#rss-toolbar").outerHeight();
    jQuery("#menu-td").css({"height": menu_height});
    jQuery("#main-td").css({"height": main_height});

    // 調整 rssdetail 中標題 (rssd-title-title) 的長度
    if (jQuery(".rssd-title-title").html() != null) {
	var title_title_width = jQuery("#rssd-title").outerWidth() - jQuery(".rssd-main-title").outerWidth() - jQuery(".rssd-title-date").outerWidth() - 40;
	jQuery("#rssd-title .rssd-title-title").css({"width":title_title_width});
    }
}

var menu_height = jQuery(window).height() - jQuery("#my-banner").outerHeight() - jQuery("#addweb-div").outerHeight() - 30;
var main_height = jQuery(window).height() - jQuery("#my-banner").outerHeight() - jQuery("#rss-toolbar").outerHeight() - 30;
jQuery("#menu-td").css({"height": menu_height});
jQuery("#main-td").css({"height": main_height});

// setMainHeight();
window.onresize=setMainHeight;	// 當視窗有改變大小時，執行 setMainHeight

// 判斷瀏覽器
var isOpera=(window.opera&&navigator.userAgent.match(/opera/gi))?true:false;
var isIE=(!this.isOpera&&document.all&&navigator.userAgent.match(/msie/gi))?true:false;
var isSafari=(!this.isIE&&navigator.userAgent.match(/safari/gi))?true:false;
var isGecko=(!this.isIE&&navigator.userAgent.match(/gecko/gi))?true:false;
var isFirefox=(!this.isIE&&navigator.userAgent.match(/firefox/gi))?true:false;

// 顯示訊息
function show_message(msg) {
    if (msg != "") {
	jQuery("#my-msg-span").html(msg);
	jQuery("#my-msg-span").show();
	setTimeout("hide_message()",3000);
    }
}

// 隱藏訊息
function hide_message() {
    jQuery("#my-msg-span").hide();
    jQuery("#my-msg-span").html("");
}

function HideAllPop(e) {
    // 關閉所有 pop 視窗
    // 當 click 不是在 [訂閱] 相關 div 時, 關閉 [訂閱] div
    if ((jQuery(e.target)[0].id == "addweb_btn") || (jQuery(e.target)[0].id == "addweb_input") || (jQuery(e.target).parent()[0].id == "addweb_input")) {
        return;
    } else {
	jQuery("#addweb_input").hide();
    }

    // 當 click 不是在 顯示模式 按鈕處, 就關閉 顯示模式 div
    if ((jQuery(e.target)[0].id == "showmode") || (jQuery(e.target)[0].id == "showmode_button")) {
	return;
    } else {
	jQuery("#showmode").hide();
    }
}

function start() {
    // 開啟視窗時執行

    // 將 訊息處 #my-msg-span 隱藏起來
    jQuery("#my-msg-span").hide();

    // 建立 addweb_input 的內容
    var addweb_btn_str = "";
    addweb_btn_str += "<button id='addweb_btn'>訂閱</button>";
    addweb_btn_str += "<div id='addweb_input'>";
    addweb_btn_str += "<span>請輸入網址</span><br />";
    addweb_btn_str += "<input type='text' id='addweb_url' size='24' />";
    addweb_btn_str += "<button onClick='addweb_submit()'>訂閱</button><br />";
    addweb_btn_str += "<span>ex: http://www.abc.com</span>";
    addweb_btn_str += "</div>";
    jQuery("#addweb-div").html(addweb_btn_str);
    jQuery("#addweb_btn").bind('click', addweb);
    jQuery("#addweb_input").hide();

    // 產生 menu
    menu_start();
}

jQuery(document).ready(function() {
    start();

    jQuery("#main").html("<div style='text-align:center; font-size:30px;'>Welcome</div>");

    $(document).bind('click', HideAllPop);
});