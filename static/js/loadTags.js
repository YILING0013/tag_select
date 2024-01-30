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
        }else {
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

// 为 "R18" 格式化数据
function formatForR17_9(data) {
    let htmlContent = '<form class="layui-form r18">';
    // 遍历数据以生成特定格式的HTML
    for (let subcategory in data) {
        let tags = data[subcategory];
        Object.entries(tags).forEach(([chinese, english], index) => {
            let id = `butr18${index}`;
            
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



var flagminus="none";
var flagenglish="inline-block";
var flagchinese="inline-block";
var flagplus="none";
var flagdel="none";
var flagweightl="{";
var flagweightr="}";

function toast(msg, type, time ){
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

layui.use('form', function(){
    var form = layui.form;
    
    function toggleDisplay(className, displayStyle, flagVariable) {
        $("." + className).css("display", displayStyle);
        window[flagVariable] = displayStyle;
    }

    form.on('switch(switchr18)', function(data){
        if(this.checked)
            {
                console.log(this.checked);
                $(".r18").css("display","block");$(".nr18").css("display","none");
                document.getElementById("badbad").value="lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst        quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, ";
        
            }
            else{
                $(".r18").css("display","none");$(".nr18").css("display","block");
                document.getElementById("badbad").value="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst      quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, ";}
            
          });

    form.on('switch(switchenglish)', function(data){
        toggleDisplay('english', data.elem.checked ? 'contents' : 'none', 'flagenglish');
    });

    form.on('switch(switchchinese)', function(data){
        toggleDisplay('chinese', data.elem.checked ? 'contents' : 'none', 'flagchinese');
    });
    form.on('switch(switchminus)', function(data){
        toggleDisplay('minus', data.elem.checked ? 'inline-block' : 'none', 'flagminus');
    });
    form.on('switch(switchplus)', function(data){
        toggleDisplay('plus', data.elem.checked ? 'inline-block' : 'none', 'flagplus');
    });
    form.on('switch(switchdel)', function(data){
        toggleDisplay('del', data.elem.checked ? 'inline-block' : 'none', 'flagdel');
    });
    form.on('switch(switchicon)', function(data){
        $(".english").each(function(){
            var isChecked = data.elem.checked;
            var reg1 = isChecked ? /\{/g : /\(/g;
            var reg2 = isChecked ? /\}/g : /\)/g;
            var replaceWith1 = isChecked ? "(" : "{";
            var replaceWith2 = isChecked ? ")" : "}";
            $(this).html($(this).html().replace(reg1, replaceWith1).replace(reg2, replaceWith2));
        });
        window.flagweightl = data.elem.checked ? "(" : "{";
        window.flagweightr = data.elem.checked ? ")" : "}";
        generate();
    });

    form.render();
});

function generate(){
var alltag=""; 
$("#elements-container .english").each(function(){ 
alltag+=$(this).html()+", ";
});
document.getElementById("tagarea").value=alltag;
}


function updateTextContent(id, newText) {
    $("#"+id+" .english").html(newText);
}

$(document).on('click', ".minus", function () {
    console.log("Minus-");
    let divid = $(this).parent().attr('id').replace("tag", "but");
    let str = $("#"+divid+" .english").html();

    if(str.startsWith('{') || str.startsWith('(')){
        str = str.slice(1, -1);
    } else {
        str = "[" + str + "]";
    }

    updateTextContent(divid, str);
    updateTextContent(divid.replace("but", "tag"), str);
    generate();
});

$(document).on('click', ".plus", function () {
    console.log("Plus+");
    let divid = $(this).parent().attr('id').replace("tag", "but");
    let str = $("#"+divid+" .english").html();

    if(str.startsWith('[')){
        str = str.slice(1, -1);
    } else {
        str = flagweightl + str + flagweightr;
    }

    updateTextContent(divid, str);
    updateTextContent(divid.replace("but", "tag"), str);
    generate();
});

$(document).on('click', ".del", function () {
    let divid = $(this).parent().attr('id');
    $('#'+divid).remove();
    $('#'+divid.replace("tag", "but")).children('.buttext').removeClass("checked");
    generate();
});



$(document).on('click', '.buttext', function() {
    const $button = $(this);
    const buttonId = $button.parent().attr('id');
    let divid = buttonId.replace("but", "tag");

    if ($button.hasClass('checked')) {
        // 如果已经被选中，移除状态并删除对应元素
        $button.removeClass("checked");
        $("#" + divid).remove();
    } else {
        // 如果未被选中，添加状态并添加新元素
        $button.addClass("checked");
        const englishText = $button.children('.english').html();
        const chineseText = $button.children('.chinese').html();
        const newTagHtml = `
            <div class='draggable-element' id='${divid}'>
                <div class='minus' style='display:${flagminus}'>-</div>
                <div class='plus' style='display:${flagplus}'>+</div>
                <div class='tagtext'>
                    <span id='eng${buttonId}' class='english' style='display:${flagenglish}'>${englishText}</span>
                    <span class='chinese' style='display:${flagchinese}'>${chineseText}</span>
                </div>
                <div class='del' style='display:${flagdel}'><i class='layui-icon'>&#xe640;</i></div>
            </div>`;

        if (!$('#' + divid).length) {
            // 仅在对应元素不存在时添加新元素
            $('#addtag').before(newTagHtml);
            makeElementsArrangeable();
        }
    }

    generate();
});

function makeElementsArrangeable() {
    $('.draggable-element').arrangeable();
    $('div').arrangeable({ dragSelector: '.drag-area' });
}



function copytag()
{
generate();
document.getElementById("tagarea").select();
document.execCommand( "copy" );
toast("复制成功！", "success","1000");
submittag();
}

function cleartag()
{
    $("#elements-container .tagtext").each(function(){ 
        console.log($(this).parent().attr('id'));
        var divid=$(this).parent().attr('id');
        console.log(divid);
        $('#'+divid).remove();
        console.log(divid);
        divid=divid.replace("tag","but");
        console.log(divid);
        $('#'+divid).children('.buttext').removeClass("checked");
    });

    generate();
}


// var verno="5";
// var jdno="7";
// if (localStorage.getItem("uid") == verno) {
//     if (localStorage.getItem("jd") != jdno) {
//     document.getElementById("jd").style.display="block";
//     localStorage.setItem("jd", jdno);
//     }
// }

// if (localStorage.getItem("uid") != verno) {
//     document.getElementById("hint").style.display="block";
//     localStorage.setItem("uid", verno);
// }

// document.getElementById("tagarea2").value=localStorage.getItem("tag2");

// $(function() {
//     $('.draggable-element').arrangeable();
//     $('div').arrangeable({dragSelector: '.drag-area'});
//   });