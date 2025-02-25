import json

# 读取 JSON 文件
def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# 调换字典内的键值对
def swap_dict_keys_values(data):
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = {v: k for k, v in value.items()}  # 调换键值对
    return data

# 保存新的 JSON 文件
def save_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 主函数
def main():
    input_filename = 'public\TagJson\角色.json'  # 输入的 JSON 文件名
    output_filename = 'output.json'  # 输出的 JSON 文件名

    # 读取原始 JSON 文件
    data = read_json_file(input_filename)

    # 调换字典内部的键值对
    swapped_data = swap_dict_keys_values(data)

    # 保存调换后的数据到新的 JSON 文件
    save_json_file(output_filename, swapped_data)

    print("键值对调换完毕，结果已保存至", output_filename)

if __name__ == "__main__":
    main()
