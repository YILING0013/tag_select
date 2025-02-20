# search.py
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, Blueprint
import json
import re
import jieba
import Levenshtein as lev

search_blueprint = Blueprint('search', __name__)

# 加载 JSON 数据
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

data = load_json('translations_converted.json')
if data is None:
    raise Exception("Failed to load JSON data. Please check the file path and format.")

# 预先对所有键和值进行分词，提升模糊搜索的性能
segmented_data = {}
for key, value in data.items():
    segmented_data[key] = {
         "key_words": list(jieba.cut(str(key))),
         "value_words": list(jieba.cut(str(value)))
    }

# 正则匹配搜索函数
def search_keywords(data, query, max_results):
    results = []
    # 构建正则模式，将查询的每个字符之间用 .* 连接
    pattern = '.*'.join(map(re.escape, query))
    regex = re.compile(pattern, re.IGNORECASE)
    for key, value in data.items():
        # 将键和值转换为字符串进行匹配
        if regex.search(str(key)) or regex.search(str(value)):
            results.append({key: value})
            if len(results) >= max_results:
                break
    return results

# 精确匹配搜索函数
def exact_search(data, query, max_results):
    results = []
    query_lower = query.lower()
    for key, value in data.items():
        if str(key).lower() == query_lower or str(value).lower() == query_lower:
            results.append({key: value})
            if len(results) >= max_results:
                break
    return results

# 模糊匹配搜索函数
def fuzzy_search(data, query, max_distance, max_results):
    results = []
    query_words = list(jieba.cut(query))
    for key, value in data.items():
        seg = segmented_data[key]
        key_words = seg["key_words"]
        value_words = seg["value_words"]
        # 当查询中所有词在键或值中均有匹配时，认为匹配成功
        key_match = all(any(lev.distance(qw, kw) <= max_distance for kw in key_words) for qw in query_words)
        value_match = all(any(lev.distance(qw, vw) <= max_distance for vw in value_words) for qw in query_words)
        if key_match or value_match:
            results.append({key: value})
            if len(results) >= max_results:
                break
    return results

# 限制返回最大数量不超过300
def limit_max_results(max_results):
    if max_results is None or max_results > 300:
        return 300
    return max_results

@search_blueprint.route('/regular_expression', methods=['GET'])
def regular_expression_api():
    query = request.args.get('query')
    max_results = request.args.get('max_results', type=int)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    max_results = limit_max_results(max_results)
    results = search_keywords(data, query, max_results)
    return jsonify(results)

@search_blueprint.route('/fuzzy_search', methods=['GET'])
def fuzzy_search_api():
    query = request.args.get('query')
    max_results = request.args.get('max_results', type=int)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    max_results = limit_max_results(max_results)
    # max_distance 可根据需求调整
    results = fuzzy_search(data, query, max_distance=1, max_results=max_results)
    return jsonify(results)

@search_blueprint.route('/exact_search', methods=['GET'])
def exact_search_api():
    query = request.args.get('query')
    max_results = request.args.get('max_results', type=int)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    max_results = limit_max_results(max_results)
    results = exact_search(data, query, max_results)
    return jsonify(results)
