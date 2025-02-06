import sys
import json
from collections import defaultdict

# 数据存储文件名
DATA_FILE = "student_data.json"

def load_data():
    """加载数据文件，如果文件不存在则返回空字典"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    """保存数据到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def update_or_upload(student_id, input_data):
    """更新或上传学生数据"""
    data = load_data()
    if student_id in data:
        print(f"Updating data for student {student_id}...")
    else:
        print(f"Adding new data for student {student_id}...")
    data[student_id] = input_data
    save_data(data)
    print("Operation completed successfully.")

def delete(student_id):
    """删除指定学号的数据"""
    data = load_data()
    if student_id in data:
        del data[student_id]
        save_data(data)
        print(f"Data for student {student_id} deleted successfully.")
    else:
        print(f"Student {student_id} not found.")

def get(student_id):
    """获取指定学号的数据，并按学期排序输出"""
    data = load_data()
    if student_id in data:
        student_data = data[student_id]
        # 检查每条课程数据是否包含 "学期" 字段
        valid_data = {k: v for k, v in student_data.items() if "学期" in v}
        invalid_data = {k: v for k, v in student_data.items() if "学期" not in v}

        if invalid_data:
            print(f"Warning: The following courses are missing the '学期' field and will be ignored: {list(invalid_data.keys())}")

        # 按学期排序
        sorted_data = sorted(valid_data.items(), key=lambda x: x[1]["学期"])
        # 转换为目标格式
        output_data = {k: v for k, v in sorted_data}
        print((student_id, output_data))
    else:
        print(f"Student {student_id} not found.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python student_records.py <operation> <student_id>")
        print("Operations: update/upload, delete, get")
        sys.exit(1)

    operation = sys.argv[1].lower()
    student_id = sys.argv[2]

    if operation in ["update", "upload"]:
        # 从标准输入读取数据
        input_data = sys.stdin.read().strip()
        try:
            # 解析输入数据
            data_tuple = eval(input_data)
            if isinstance(data_tuple, tuple) and data_tuple[0] is True:
                update_or_upload(student_id, data_tuple[1])
            else:
                print("Invalid input format. Expected a tuple starting with True.")
        except Exception as e:
            print(f"Error parsing input data: {e}")
    elif operation == "delete":
        delete(student_id)
    elif operation == "get":
        get(student_id)
    else:
        print(f"Unknown operation: {operation}")

if __name__ == "__main__":
    main()
