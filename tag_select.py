from flask import Blueprint, jsonify
import json
import os

tag_select_blueprint = Blueprint('tag_select', __name__)

def load_json_data(file_name):
    file_path = os.path.join('tag_json', f'{file_name}.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

@tag_select_blueprint.route('/get_tags/<category>')
def get_tags(category):
    data = load_json_data(category)
    if data is not None:
        return jsonify(data)
    else:
        return jsonify({"error": "Category not found"}), 404
