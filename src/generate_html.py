import argparse
import ast
import sys

def generate_html(data, data_type, student_id):
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>课程成绩表 - 学号 {student_id}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
        </style>
    </head>
    <body>
        <h1>课程成绩表 - 学号 {student_id}</h1>
    """

    if data_type == "c":
        html += """
        <table>
            <thead>
                <tr>
                    <th>课程名称</th>
                    <th>学分</th>
                    <th>成绩</th>
                    <th>学期</th>
                </tr>
            </thead>
            <tbody>
        """
        for course, details in data[1].items():
            html += f"""
                <tr>
                    <td>{course}</td>
                    <td>{details['学分']}</td>
                    <td>{details['成绩']}</td>
                    <td>{details['学期']}</td>
                </tr>
            """
        html += """
            </tbody>
        </table>
        """
    elif data_type == "s":
        for semester, courses in data[1].items():
            html += f"""
            <h2>{semester}</h2>
            <table>
                <thead>
                    <tr>
                        <th>课程名称</th>
                        <th>学分</th>
                        <th>成绩</th>
                    </tr>
                </thead>
                <tbody>
            """
            for course, details in courses.items():
                html += f"""
                    <tr>
                        <td>{course}</td>
                        <td>{details['学分']}</td>
                        <td>{details['成绩']}</td>
                    </tr>
                """
            html += """
                </tbody>
            </table>
            """

    html += """
    </body>
    </html>
    """

    return html

def main():
    parser = argparse.ArgumentParser(description="生成课程成绩表的HTML文件")
    parser.add_argument("student_id", type=str, help="学生的学号")
    parser.add_argument("-c", action="store_true", help="使用课程为键的数据格式")
    parser.add_argument("-s", action="store_true", help="使用学期为键的数据格式")
    args = parser.parse_args()

    if not (args.c or args.s):
        print("请指定数据格式：-c 或 -s")
        sys.exit(1)

    data_type = "c" if args.c else "s"

    # 从标准输入读取数据
    input_data = sys.stdin.read().strip()
    try:
        data = ast.literal_eval(input_data)
    except (ValueError, SyntaxError) as e:
        print(f"输入数据格式错误：{e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, tuple) or len(data) != 2 or not isinstance(data[1], dict):
        print("输入数据格式不正确", file=sys.stderr)
        sys.exit(1)

    # 替换学号
    data = (args.student_id, data[1])

    html = generate_html(data, data_type, args.student_id)

    # 将生成的HTML输出到标准输出
    print(html)

if __name__ == "__main__":
    main()
