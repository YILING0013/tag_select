import hashlib
import hmac
import json
import random
import time
from datetime import datetime
import requests
from flask import Blueprint, request, jsonify
import yaml

# 从yaml文件加载配置
def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

config = load_config('config.yaml')

# 百度翻译API信息
BAIDU_TRANSLATE_URL = config['baidu_translate_url']
BAIDU_TRANSLATE_CREDENTIALS = config['baidu_translate_credentials']

# 腾讯翻译API信息
TENCENT_SECRET_ID = config['tencent_secret_id']
TENCENT_SECRET_KEY = config['tencent_secret_key']
TENCENT_TRANSLATE_URL = config['tencent_translate_url']

# 用于轮询的索引
current_index = 0

def get_next_credentials():
    """
    获取下一个 APP_ID 和 SECRET_KEY 的组合，自动轮询。
    """
    global current_index
    credentials = BAIDU_TRANSLATE_CREDENTIALS[current_index]
    current_index = (current_index + 1) % len(BAIDU_TRANSLATE_CREDENTIALS)
    return credentials

def sign(key, msg):
    """
    使用HMAC-SHA256算法生成签名。
    """
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def generate_tc3_signature(secret_key, date, service, string_to_sign):
    """
    生成腾讯云TC3-HMAC-SHA256签名。
    """
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    return hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

def translate_with_tencent(texts, from_lang='auto', to_lang='zh'):
    """
    使用腾讯翻译API翻译文本列表。
    """
    service = "tmt"
    host = "tmt.tencentcloudapi.com"
    action = "TextTranslate"
    version = "2018-03-21"
    region = "ap-beijing"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    algorithm = "TC3-HMAC-SHA256"  # 在这里定义 algorithm

    # 构造请求参数
    payload = {
        "SourceText": "\n".join(texts),
        "Source": from_lang,
        "Target": to_lang,
        "ProjectId": 0
    }
    payload_str = json.dumps(payload)

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = f"content-type:{ct}\nhost:{host}\nx-tc-action:{action.lower()}\n"
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    signature = generate_tc3_signature(TENCENT_SECRET_KEY, date, service, string_to_sign)

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + TENCENT_SECRET_ID + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # ************* 步骤 5：构造并发起请求 *************
    headers = {
        "Authorization": authorization,
        "Content-Type": ct,
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version,
        "X-TC-Region": region
    }

    try:
        response = requests.post(TENCENT_TRANSLATE_URL, headers=headers, data=payload_str)
        response.raise_for_status()
        result = response.json()
        if "Response" in result and "TargetText" in result["Response"]:
            return result["Response"]["TargetText"].split("\n")
        else:
            return None
    except Exception as e:
        print(f"腾讯翻译API请求失败: {e}")
        return None

def translate_with_baidu(texts, from_lang='auto', to_lang='zh'):
    """
    使用百度翻译API翻译文本列表。
    """
    credentials = get_next_credentials()
    app_id = credentials['app_id']
    secret_key = credentials['secret_key']

    salt = random.randint(32768, 65536)
    query = '\n'.join(texts)
    sign_str = app_id + query + str(salt) + secret_key
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    params = {
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'appid': app_id,
        'salt': salt,
        'sign': sign
    }

    try:
        response = requests.get(BAIDU_TRANSLATE_URL, params=params)
        response.raise_for_status()
        result = response.json()
        if 'trans_result' in result:
            return [item['dst'] for item in result['trans_result']]
        else:
            return None
    except Exception as e:
        print(f"百度翻译API请求失败: {e}")
        return None

def translate_texts(texts, from_lang='auto', to_lang='zh'):
    """
    优先使用腾讯翻译API翻译文本列表，失败后使用百度翻译API。
    如果两者都失败，则返回未翻译的原始文本。
    """
    # 优先使用腾讯翻译API
    translated_texts = translate_with_tencent(texts, from_lang, to_lang)
    if translated_texts is not None:
        return translated_texts

    # 腾讯翻译失败后使用百度翻译API
    translated_texts = translate_with_baidu(texts, from_lang, to_lang)
    if translated_texts is not None:
        return translated_texts

    # 两者都失败，返回原始文本
    return texts

# 创建蓝图
tag_extractorbp = Blueprint('tag_extractor', __name__)

# 移除原来的 extract_tags 接口，因为现在前端直接获取和解析HTML

@tag_extractorbp.route('/Tagtranslate', methods=['POST'])
def translate():
    """
    翻译文本列表接口
    接收格式: {"texts": ["text1", "text2", ...]}
    返回格式: {"translated_texts": ["译文1", "译文2", ...]}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求体为空"}), 400
            
        texts = data.get('texts')
        if not texts:
            return jsonify({"error": "缺少texts参数"}), 400
            
        if not isinstance(texts, list):
            return jsonify({"error": "texts参数必须是数组"}), 400
            
        if len(texts) == 0:
            return jsonify({"translated_texts": []}), 200
            
        # 过滤空字符串
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        if len(valid_texts) == 0:
            return jsonify({"translated_texts": []}), 200
            
        print(f"开始翻译 {len(valid_texts)} 个文本...")
        translated_texts = translate_texts(valid_texts)
        print(f"翻译完成")
        
        return jsonify({"translated_texts": translated_texts})
        
    except Exception as e:
        print(f"翻译接口错误: {e}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

@tag_extractorbp.route('/translate_batch', methods=['POST'])
def translate_batch():
    """
    批量翻译接口，支持更多参数
    接收格式: {
        "texts": ["text1", "text2", ...],
        "from_lang": "auto",  // 可选，默认auto
        "to_lang": "zh"       // 可选，默认zh
    }
    返回格式: {"translated_texts": ["译文1", "译文2", ...]}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求体为空"}), 400
            
        texts = data.get('texts')
        if not texts:
            return jsonify({"error": "缺少texts参数"}), 400
            
        if not isinstance(texts, list):
            return jsonify({"error": "texts参数必须是数组"}), 400
            
        from_lang = data.get('from_lang', 'auto')
        to_lang = data.get('to_lang', 'zh')
        
        if len(texts) == 0:
            return jsonify({"translated_texts": []}), 200
            
        # 过滤空字符串
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        if len(valid_texts) == 0:
            return jsonify({"translated_texts": []}), 200
            
        print(f"开始批量翻译 {len(valid_texts)} 个文本 ({from_lang} -> {to_lang})...")
        translated_texts = translate_texts(valid_texts, from_lang, to_lang)
        print(f"批量翻译完成")
        
        return jsonify({
            "translated_texts": translated_texts,
            "from_lang": from_lang,
            "to_lang": to_lang,
            "count": len(translated_texts)
        })
        
    except Exception as e:
        print(f"批量翻译接口错误: {e}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500