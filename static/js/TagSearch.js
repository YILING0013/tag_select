function sendApiRequest(endpoint) {
    var query = document.getElementById("tagselect").value;
    var maxResults = document.getElementById("max_results").value;

    var params = new URLSearchParams({
        query: query
    });
    if (maxResults) {
        params.append('max_results', maxResults);
    }

    fetch('search/' + endpoint + '?' + params, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // 定位到插入点
        var insertionPoint = document.getElementById('insertion-point');

        // 清除旧的结果
        while (insertionPoint.nextSibling) {
            insertionPoint.parentNode.removeChild(insertionPoint.nextSibling);
        }

        // 为每个返回的结果创建新的div元素
        data.forEach((item, index) => {
            var key = Object.keys(item)[0];
            var value = item[key];
            var randomString = generateRandomString(6); // 生成随机字符串

            var div = document.createElement('div');
            div.className = 'tagbutton';
            div.id = 'butsearch' + index + "_" + randomString; // 加入随机字符串

            div.innerHTML = `
                <div class="minus" style="display: none;">-</div>
                <div class="plus" style="display: none;">+</div>
                <div class="buttext">
                    <span class="english">${key}</span>
                    <span class="chinese">${value}</span>
                </div>
            `;

            // 将新创建的div元素插入到插入点之后
            insertionPoint.parentNode.insertBefore(div, insertionPoint.nextSibling);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function generateRandomString(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

// 正则搜索
function regular_expression() {
    sendApiRequest('regular_expression');
}
// 模糊搜索
function fuzzy_search() {
    sendApiRequest('fuzzy_search');
}
// 精确搜索
function exact_search() {
    sendApiRequest('exact_search');
}