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

# 尝试加载数据，如果失败，则终止
data = load_json('converted_data.json')
if data is None:
    raise Exception("Failed to load JSON data. Please check the file path and format.")

# 正则匹配搜索函数
def search_keywords(data, query, max_results=None):
    results = []
    pattern = '.*'.join(map(re.escape, query))
    regex = re.compile(pattern, re.IGNORECASE)
    for key, value in data.items():
        if regex.search(key) or regex.search(value):
            results.append({key: value})
            if max_results is not None and len(results) >= max_results:
                break
    return results

# 精确匹配搜索函数
def exact_search(data, query, max_results=None):
    results = []
    for key, value in data.items():
        if key.lower() == query.lower() or value.lower() == query.lower():
            results.append({key: value})
            if max_results is not None and len(results) >= max_results:
                break
    return results

# 模糊匹配搜索函数
def fuzzy_search(data, query, max_distance=1, max_results=None):
    results = []
    query_words = list(jieba.cut(query))
    for key, value in data.items():
        key_words = list(jieba.cut(key))
        value_words = list(jieba.cut(value))
        
        # 仅当查询中多个词与键或值匹配时才考虑为有效匹配
        if all(any(lev.distance(query_word, key_word) <= max_distance for key_word in key_words) for query_word in query_words) \
           or all(any(lev.distance(query_word, value_word) <= max_distance for value_word in value_words) for query_word in query_words):
            results.append({key: value})
            if max_results is not None and len(results) >= max_results:
                break
    return results

@search_blueprint.route('/regular_expression', methods=['GET'])
def regular_expression_api():
    query = request.args.get('query')
    max_results = request.args.get('max_results', type=int)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = search_keywords(data, query, max_results)
    return jsonify(results)

@search_blueprint.route('/fuzzy_search', methods=['GET'])
def fuzzy_search_api():
    query = request.args.get('query')
    max_results = request.args.get('max_results', type=int)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = fuzzy_search(data, query, max_distance=1, max_results=max_results)
    return jsonify(results)

@search_blueprint.route('/exact_search', methods=['GET'])
def exact_search_api():
    query = request.args.get('query')
    max_results = request.args.get('max_results', type=int)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = exact_search(data, query, max_results)
    return jsonify(results)
