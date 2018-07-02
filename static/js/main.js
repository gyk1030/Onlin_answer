window.onload = function() {
	var ul = document.getElementById("form_lg");
	var hc =　document.getElementById("helloC");　　　
	var li = document.createElement("input");　　　　
	li.setAttribute("name", "titleTxt");

	li.setAttribute("value", "管理员登录");
	　　　
	li.setAttribute("readonly", "readonly");

	li.className = "titleStyle";

	ul.insertBefore(li,hc);　　
}

function changeT(e) {
	var spanT = document.getElementById("span_txt");
	var TitleT = document.getElementById("Title");
	var personT = document.getElementById("form_person");
	var questionT = document.getElementById("questionList");
	if(e.innerHTML == "修改资料") {
		e.innerHTML = "返回问题列表";
		questionT.style.display = "none";
		personT.style.display = "";
		TitleT.innerHTML = "修 改 资 料";
	} else if(e.innerHTML == "返回问题列表") {
		e.innerHTML = "修改资料";
		questionT.style.display = "";
		personT.style.display = "none";
		TitleT.innerHTML = "问 题 列 表 ";
	}
}
