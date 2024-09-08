from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
import hashlib
import random
import yaml

# 从yaml文件加载配置
def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

config = load_config('config.yaml')
# 百度翻译API信息
BAIDU_TRANSLATE_URL = config['baidu_translate_url']
# 百度翻译de多个APP_ID和SECRET_KEY
BAIDU_TRANSLATE_CREDENTIALS = config['baidu_translate_credentials']

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

def translate_texts(texts, from_lang='auto', to_lang='zh'):
    """
    使用百度翻译API翻译文本列表。
    如果翻译失败，则返回未翻译的原始文本。
    """
    credentials = get_next_credentials()
    app_id = credentials['app_id']
    secret_key = credentials['secret_key']

    salt = random.randint(32768, 65536)
    query = '\n'.join(texts)
    sign = hashlib.md5((app_id + query + str(salt) + secret_key).encode('utf-8')).hexdigest()

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
            return texts
    except Exception as e:
        return texts

# 创建蓝图
tag_extractorbp = Blueprint('tag_extractor', __name__)

@tag_extractorbp.route('/extract_tags', methods=['GET'])
def extract_tags():
    # 从请求参数中获取URL
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    # 发送GET请求到指定的URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    # 解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 提取所需的数据并翻译
    tags = []
    tag_names = []
    for li in soup.select('ul.general-tag-list > li'):
        # 提取标签名，并将下划线替换为空格
        tag_name = li.get('data-tag-name').replace('_', ' ')
        tag_names.append(tag_name)
        tag_info = {
            'tag_name': tag_name,
            'is_deprecated': li.get('data-is-deprecated') == 'true',
            'links': [a.text.strip() for a in li.find_all('a')],
            'post_count': li.find('span', class_='post-count').get('title') if li.find('span', class_='post-count') else None
        }
        tags.append(tag_info)
    
    translated_tag_names = translate_texts(tag_names)  # 翻译标签名称列表

    # 将翻译后的标签名添加到标签信息中
    for tag, translated_tag_name in zip(tags, translated_tag_names):
        tag['translated_tag_name'] = translated_tag_name

    # 将提取和翻译的数据组装为JSON格式返回
    return jsonify(tags)

@tag_extractorbp.route('/Tagtranslate', methods=['POST'])
def translate():
    data = request.get_json()
    texts = data.get('texts')
    if not texts:
        return jsonify({"error": "Missing texts parameter"}), 400

    translated_texts = translate_texts(texts)
    return jsonify({"translated_texts": translated_texts})
