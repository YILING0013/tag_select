import os
import json
import argparse

def extract_pairs(obj):
    """
    递归提取 obj 中所有键值对（仅当键和值均为字符串时）。
    返回一个字典，包含所有提取到的键值对。
    """
    pairs = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            # 如果键和值均为字符串，则记录该对
            if isinstance(key, str) and isinstance(value, str):
                if key in pairs and pairs[key] != value:
                    print(f"警告：键 '{key}' 重复，但值不同：'{pairs[key]}' 与 '{value}'。保留首次出现的值。")
                else:
                    pairs[key] = value
            # 无论 value 是否为字符串，都递归检查其内部结构
            sub_pairs = extract_pairs(value)
            for sub_key, sub_value in sub_pairs.items():
                if sub_key in pairs and pairs[sub_key] != sub_value:
                    print(f"警告：键 '{sub_key}' 重复，但值不同：'{pairs[sub_key]}' 与 '{sub_value}'。保留首次出现的值。")
                else:
                    pairs[sub_key] = sub_value
    elif isinstance(obj, list):
        for item in obj:
            sub_pairs = extract_pairs(item)
            for sub_key, sub_value in sub_pairs.items():
                if sub_key in pairs and pairs[sub_key] != sub_value:
                    print(f"警告：键 '{sub_key}' 重复，但值不同：'{pairs[sub_key]}' 与 '{sub_value}'。保留首次出现的值。")
                else:
                    pairs[sub_key] = sub_value
    return pairs

def merge_json_pairs(directory, output_file):
    """
    遍历指定目录下所有 JSON 文件，
    提取每个文件中所有层级的键值对（仅当键和值均为字符串时），
    并将它们合并到一个平面字典中，最后写入 output_file。
    """
    merged_pairs = {}
    
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                file_pairs = extract_pairs(data)
                for key, value in file_pairs.items():
                    if key in merged_pairs and merged_pairs[key] != value:
                        print(f"警告：文件 '{filename}' 中键 '{key}' 的值 '{value}' 与之前值 '{merged_pairs[key]}' 不同，保留首次出现的值。")
                    else:
                        merged_pairs[key] = value
            except Exception as e:
                print(f"读取文件 '{filename}' 时发生错误：{e}")
    
    try:
        with open(output_file, "w", encoding="utf-8") as out_f:
            json.dump(merged_pairs, out_f, ensure_ascii=False, indent=4)
        print(f"合并后的键值对已写入：{output_file}")
    except Exception as e:
        print(f"写入输出文件 '{output_file}' 时发生错误：{e}")

if __name__ == '__main__':
    directory = 'public\TagJson'
    output_file = 'TagJson.json'

    merge_json_pairs(directory, output_file)
