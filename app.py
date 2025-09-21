import os
import json
import requests
from flask import Flask, jsonify, send_from_directory, request, abort
from flask_cors import CORS

from tag_extractor import tag_extractorbp
from search import search_blueprint

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求
TAG_JSON_DIR = os.path.join(os.getcwd(), 'public', 'TagJson')

TURNSTILE_SECRET_KEY = "xxx" 

app.register_blueprint(search_blueprint, url_prefix='/search')
app.register_blueprint(tag_extractorbp, url_prefix='/api')

@app.route('/')
def index():
    return send_from_directory('static/frontend', 'index.html')

# 用于Turnstile验证的新接口
@app.route('/api/verify-turnstile', methods=['POST'])
def verify_turnstile():
    data = request.get_json()
    token = data.get('token')
    
    if not token:
        return jsonify({"success": False, "message": "缺少Token。"}), 400

    # 使用Cloudflare进行验证
    try:
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={
                'secret': TURNSTILE_SECRET_KEY,
                'response': token,
            }
        )
        response.raise_for_status() # 如果请求失败 (状态码 4xx or 5xx), 抛出异常
        result = response.json()
        
        if result.get('success'):
            return jsonify({"success": True, "message": "验证成功。"}), 200
        else:
            error_codes = result.get('error-codes', [])
            return jsonify({"success": False, "message": "验证失败。", "error-codes": error_codes}), 400
            
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": f"连接验证服务器时出错: {e}"}), 500


# 列出TagJson目录中的所有JSON文件
@app.route('/api/json-files', methods=['GET'])
def get_json_files():
    try:
        # 获取目录下的所有文件名
        files = [f for f in os.listdir(TAG_JSON_DIR) if f.endswith('.json')]
        return jsonify(files), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 获取指定JSON文件中的字典键
@app.route('/api/json-files/<filename>/keys', methods=['GET'])
def get_json_file_keys(filename):
    if not filename.endswith('.json'):
        abort(400, description="Invalid file extension")
    
    file_path = os.path.join(TAG_JSON_DIR, filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        abort(404, description="File not found")
    
    try:
        # 打开文件并提取字典的键
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        keys = list(data.keys())  # 获取字典的所有键
        return jsonify(keys), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 获取指定JSON文件和字典键的内容
@app.route('/api/json-files/<filename>/keys/<key>', methods=['GET'])
def get_json_key_content(filename, key):
    if not filename.endswith('.json'):
        abort(400, description="Invalid file extension")
    
    file_path = os.path.join(TAG_JSON_DIR, filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        abort(404, description="File not found")
    
    try:
        # 打开文件并获取指定字典键的内容
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if key not in data:
            abort(404, description="Key not found in JSON file")
        
        return jsonify(data[key]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 设置Flask的静态文件目录
@app.route('/public/TagJson/<filename>')
def serve_json_file(filename):
    return send_from_directory(TAG_JSON_DIR, filename)


if __name__ == '__main__':
    # 运行Flask应用
    app.run(debug=True)
