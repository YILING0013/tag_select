function loadTags(category) {
    fetch('/api_tag/get_tags/' + category)
        .then(response => response.json())
        .then(data => {
            var container = document.getElementById(category);

            if (!container) {
                console.error('Container for category ' + category + ' not found');
                return;
            }

            if (category === 'r18') {
                container.innerHTML += formatForR17_9(data);
            } else if (category === 'Illustrator') {
                for (let subcategory in data) {
                    let htmlContent = `<p>${subcategory}</p><form class="layui-form" style="display: flex; flex-wrap: wrap;">`;
                    let tags = data[subcategory];
                    Object.entries(tags).forEach(([chinese, english], index) => {
                        let id = `but${category}${subcategory}${index}`;
                        let cleanedEnglish = english.replace('artist:', ''); // 移除 "artist:"
                        let imageName = `${chinese}_${cleanedEnglish}.webp`; // 使用修改后的英文名称构造图像名称
                        let imagePath = `/static/images/artist_preview/${imageName}`; // 构造图像的路径

                        htmlContent += `
                    <div style="display: flex; flex-direction: column; align-items: center; margin-right: 10px; margin-bottom: 10px;">
                        <img src="${imagePath}" alt="${english}" class="illustrator-image"> <!-- 添加图像 -->
                        <div class="tagbutton" id="${id}">
                            <div class="buttext">
                                <span class="english">${english}</span>
                                <span class="chinese">${chinese}</span>
                            </div>
                        </div>
                    </div>`;
                    });
                    htmlContent += '</form><hr>';
                    container.innerHTML += htmlContent;
                }
            } else {
                for (let subcategory in data) {
                    let htmlContent = `<p>${subcategory}</p><form class="layui-form">`;
                    let tags = data[subcategory];
                    Object.entries(tags).forEach(([chinese, english], index) => {
                        let id = `but${category}${subcategory}${index}`;

                        htmlContent += `
                        <div class="tagbutton" id="${id}">
                            <div class="minus" style="display: none;">-</div>
                            <div class="plus" style="display: none;">+</div>
                            <div class="buttext">
                                <span class="english">${english}</span>
                                <span class="chinese">${chinese}</span>
                            </div>
                        </div>`;
                    });
                    htmlContent += '</form><hr>';
                    container.innerHTML += htmlContent;
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

// 为 "R17-9" 格式化数据
function formatForR17_9(data) {
    let htmlContent = '<form class="layui-form r18">';
    // 遍历数据以生成特定格式的HTML
    for (let subcategory in data) {
        let tags = data[subcategory];
        htmlContent += `<p>${subcategory}</p>`;
        Object.entries(tags).forEach(([english, chinese], index) => {
            //生成随机字符
            let id = `butr18${index}` + Math.random().toString(36).substring(2, 18);

            htmlContent += `
                <div class="tagbutton" id="${id}">
                    <div class="minus" style="display: none;">-</div>
                    <div class="plus" style="display: none;">+</div>
                    <div class="buttext">
                        <span class="english">${english}</span>
                        <span class="chinese">${chinese}</span>
                    </div>
                </div>`;
        });
    }
    htmlContent += '</form>';
    return htmlContent;
}



var flagminus = "none";
var flagenglish = "inline-block";
var flagchinese = "inline-block";
var flagplus = "none";
var flagdel = "none";
var flagweightl = "{";
var flagweightr = "}";

function toast(msg, type, time) {
    var oDiv = document.createElement("div");
    oDiv.setAttribute("id", "toast");
    oDiv.setAttribute("class", 'toast_' + type || 'toast_' + 'info');
    var oBody = document.getElementsByTagName('body')[0];
    oBody.append(oDiv);
    $('#toast').text(msg);
    $('#toast').fadeIn();
    setTimeout(function() {
        $('#toast').fadeOut();
    }, time);
}



layui.use('form', function() {
    var form = layui.form;

    form.on('switch(switchr18)', function(data) {
        if (this.checked) {
            console.log(this.checked);
            $(".r18").css("display", "block");
            $(".nr18").css("display", "none");
            // document.getElementById("badbad").value="lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst        quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, ";

        } else {
            $(".r18").css("display", "none");
            $(".nr18").css("display", "block");
            // document.getElementById("badbad").value="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst      quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, ";
        }

    });

    form.on('switch(switchchinese)', function(data) {
        if (this.checked) {
            console.log(this.checked);
            $(".chinese").css("display", "contents");
            flagchinese = "inline-block";
        } else {
            console.log(this.checked);
            $(".chinese").css("display", "none");
            flagchinese = "none";
        }
    });

    form.on('switch(switchenglish)', function(data) {
        if (this.checked) {
            $(".english").css("display", "contents");
            flagenglish = "none";
        } else {
            $(".english").css("display", "none");
            flagenglish = "none";
        }
    });

    form.on('switch(switchminus)', function(data) {
        if (this.checked) {
            $(".minus").css("display", "inline-block");
            flagminus = "inline-block";
        } else {
            $(".minus").css("display", "none");
            flagminus = "none";
        }
    });

    form.on('switch(switchplus)', function(data) {
        if (this.checked) {
            $(".plus").css("display", "inline-block");
            flagplus = "inline-block";
        } else {
            $(".plus").css("display", "none");
            flagplus = "none"
        }
    });

    form.on('switch(switchdel)', function(data) {
        if (this.checked) {
            $(".del").css("display", "inline-block");
            flagdel = "inline-block";
        } else {
            $(".del").css("display", "none");
            flagdel = "none";
        }
    });

    form.on('switch(switchicon)', function(data) {
        if (this.checked) {
            console.log("yes");
            $(".english").each(function() {
                console.log($(this).html());
                var reg1 = new RegExp("\\{", "g");
                var reg2 = new RegExp("\\}", "g");
                $(this).html($(this).html().replace(reg1, "("));
                $(this).html($(this).html().replace(reg2, ")"));
            });
            flagweightl = "(";
            flagweightr = ")";
        } else {
            $(".english").each(function() {
                console.log($(this).html());
                var reg1 = new RegExp("\\(", "g");
                var reg2 = new RegExp("\\)", "g");
                $(this).html($(this).html().replace(reg1, "{"));
                $(this).html($(this).html().replace(reg2, "}"));
            });
            flagweightl = "{";
            flagweightr = "}";
        }
        generate();
    });

    layui.form.render();

});


function generate() {
    var alltag = "";
    $("#elements-container .english").each(function() {
        alltag += $(this).html() + ", ";
    });
    document.getElementById("tagarea").value = alltag;
}


$(document).on('click', ".minus", function() {
    console.log("Minus-");
    var divid = $(this).parent().attr('id');
    divid = divid.replace("tag", "but");
    var str = $("#" + divid + " .english").html();

    if (str.substr(0, 1) == "{" || str.substr(0, 1) == "(") {
        str = str.slice(1, str.length - 1);
        $("#" + divid + " .english").html(str);
        divid = divid.replace("but", "tag");
        $("#" + divid + " .english").html(str);
        //$("#"+$(this).parent().attr('id')+" .english").html(str)
    } else {
        var str = "[" + $("#" + $(this).parent().attr('id') + " .english").html() + "]";

        $("#" + divid + " .english").html(str);
        divid = divid.replace("but", "tag");
        $("#" + divid + " .english").html(str);
        //toast("住手啊！不要再减了！", "warning","1000");
    }
    generate();
});

$(document).on('click', ".plus", function() {
    console.log("Plus-");
    var divid = $(this).parent().attr('id');
    divid = divid.replace("tag", "but");
    var str = $("#" + divid + " .english").html();
    if (str.substr(0, 1) == "[") {
        str = str.slice(1, str.length - 1);
        $("#" + divid + " .english").html(str);
        divid = divid.replace("but", "tag");
        $("#" + divid + " .english").html(str);

    } else {
        var str = flagweightl + str + flagweightr;
        $("#" + divid + " .english").html(str);
        divid = divid.replace("but", "tag");
        $("#" + divid + " .english").html(str);
        //toast("住手啊！不要再加了！", "warning","1000");
    }
    generate();
});

$(document).on('click', ".del", function() {
    var divid = $(this).parent().attr('id');
    $('#' + divid).remove();
    divid = divid.replace("tag", "but");
    $('#' + divid).children('.buttext').removeClass("checked");
    generate();
})


$(document).on('click', '.buttext', function() {
    var divid = $(this).parent().attr('id');
    divid = divid.replace("but", "tag");
    if ($(this).is('.checked')) {
        $(this).removeClass("checked");
        $("#" + divid).remove();
        generate();
    } else {
        var english = $(this).children('.english').html();
        $(this).addClass("checked");
        var newtag = "<div class='draggable-element' id='" + divid + "'><div class='minus' style='display:" + flagminus + "'>-</div><div class='plus' style='display:" + flagplus + "'>+</div><div class='tagtext'><span id='eng" + $(this).parent().attr('id') + "' class='english' style='display:" + flagenglish + "'>" + $(this).children('.english').html() + "</span><span class='chinese' style='display:" + flagchinese + "'>" + $(this).children('.chinese').html() + "</span></div><div class='del' style='display:" + flagdel + "'><i class='layui-icon'>&#xe640;</i></div></div>";
        $('#addtag').before(newtag);

        $(function() {
            $('.draggable-element').arrangeable();
            $('div').arrangeable({
                dragSelector: '.drag-area'
            });
        });

        generate();

    }

});

function copytag() {
    generate();
    document.getElementById("tagarea").select();
    document.execCommand("copy");
    toast("复制成功！", "success", "1000");
    submittag();
}

function cleartag() {
    $("#elements-container .tagtext").each(function() {
        console.log($(this).parent().attr('id'));
        var divid = $(this).parent().attr('id');
        console.log(divid);
        $('#' + divid).remove();
        console.log(divid);
        divid = divid.replace("tag", "but");
        console.log(divid);
        $('#' + divid).children('.buttext').removeClass("checked");
    });

    generate();
}


var verno = "5";
var jdno = "7";
if (localStorage.getItem("uid") == verno) {
    if (localStorage.getItem("jd") != jdno) {
        document.getElementById("jd").style.display = "block";
        localStorage.setItem("jd", jdno);
    }
}

if (localStorage.getItem("uid") != verno) {
    document.getElementById("hint").style.display = "block";
    localStorage.setItem("uid", verno);
}

document.getElementById("tagarea2").value = localStorage.getItem("tag2");

$(function() {
    $('.draggable-element').arrangeable();
    $('div').arrangeable({
        dragSelector: '.drag-area'
    });
});