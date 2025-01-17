import re
import sys
from bs4 import BeautifulSoup

import re
from bs4 import BeautifulSoup

def parse_semester_tables_main_semester(html_content):
    """
    解析HTML，返回结构化数据：学期 -> {课程名称 -> {学分: 'xx', 成绩: 'xx'}}
    
    格式：
    {
        "2022-2023学年 第一学期": {
            "高等数学": {"学分": "3", "成绩": "A", "学期": "2022-2023学年 第一学期"},
            "计算机基础": {"学分": "2", "成绩": "B", "学期": "2022-2023学年 第一学期"}
        },
        "2022-2023学年 第二学期": {
            "英语": {"学分": "3", "成绩": "A-", "学期": "2022-2023学年 第二学期"}
        }
    }
    """
    try:
        # 使用 html.parser 解析器
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有的 <tr> 行
        all_trs = soup.find_all('tr')

        # 用于存储解析结果
        semester_data = {}

        # 当前学期标题
        current_semester = None
        current_courses = {}

        # 用于检测学期标题的正则表达式
        semester_pattern = re.compile(r"\d{4}-\d{4}学年\s+第.+学期")

        for tr in all_trs:
            # 提取该行的所有 <td> 标签
            tds = tr.find_all('td')

            # 解析学期标题
            if len(tds) == 1 and tds[0].get('colspan') == '9':
                semester_text = tds[0].get_text(strip=True)
                if semester_pattern.search(semester_text):
                    # 如果已存在当前学期，则将其数据保存在字典中
                    if current_semester:
                        semester_data[current_semester] = current_courses

                    # 更新当前学期标题
                    current_semester = semester_text
                    current_courses = {}

            # 解析课程记录
            elif len(tds) == 3:
                colspans = [td.get('colspan') for td in tds]
                if colspans == ['5', '2', '2']:
                    course_name = tds[0].get_text(strip=True)
                    credit = tds[1].get_text(strip=True)
                    grade = tds[2].get_text(strip=True)

                    # 如果当前学期已识别，记录课程信息
                    if current_semester:
                        # 每个课程的结构：{学分: 'xx', 成绩: 'xx'}
                        current_courses[course_name] = {'学分': credit, '成绩': grade}

        # 处理最后一个学期的数据
        if current_semester and current_courses:
            semester_data[current_semester] = current_courses

        return (True, semester_data)
    
    except Exception as e:
        return (False, f"Error parsing semester tables: {e}")


def parse_semester_tables_main_course(html_content):
    """
    解析HTML，返回结构化数据：课程名称 -> {学分: 'xx', 成绩: 'xx', 学期: '学期名称'}
    
    格式：
    {
        "高等数学": {"学分": "3", "成绩": "A", "学期": "2022-2023学年 第一学期"},
        "计算机基础": {"学分": "2", "成绩": "B", "学期": "2022-2023学年 第一学期"},
        "英语": {"学分": "3", "成绩": "A-", "学期": "2022-2023学年 第二学期"}
    }
    """
    try:
        # 使用 html.parser 解析器
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有的 <tr> 行
        all_trs = soup.find_all('tr')

        # 用于存储解析结果
        course_data = {}

        # 当前学期标题
        current_semester = None

        # 用于检测学期标题的正则表达式
        semester_pattern = re.compile(r"\d{4}-\d{4}学年\s+第.+学期")

        for tr in all_trs:
            # 提取该行的所有 <td> 标签
            tds = tr.find_all('td')

            # 解析学期标题
            if len(tds) == 1 and tds[0].get('colspan') == '9':
                semester_text = tds[0].get_text(strip=True)
                if semester_pattern.search(semester_text):
                    # 更新当前学期标题
                    current_semester = semester_text

            # 解析课程记录
            elif len(tds) == 3:
                colspans = [td.get('colspan') for td in tds]
                if colspans == ['5', '2', '2']:
                    course_name = tds[0].get_text(strip=True)
                    credit = tds[1].get_text(strip=True)
                    grade = tds[2].get_text(strip=True)

                    # 如果当前学期已识别，记录课程信息
                    if current_semester:
                        # 每个课程的结构：{学分: 'xx', 成绩: 'xx', 学期: '学期名称'}
                        course_data[course_name] = {'学分': credit, '成绩': grade, '学期': current_semester}

        return (True, course_data)
    
    except Exception as e:
        return (False, f"Error parsing course tables: {e}")


def parse_semester_tables(html_content, main_mode='semester'):
    """
    解析HTML，返回指定模式的结构化数据。
    
    支持模式：
    - 'semester': 按学期分组
    - 'course': 按课程分组
    """
    try:
        if main_mode == 'semester':
            return parse_semester_tables_main_semester(html_content)
        elif main_mode == 'course':
            return parse_semester_tables_main_course(html_content)
        else:
            raise ValueError(f"Unsupported mode: {main_mode}")
    
    except Exception as e:
        return (False, f"Error in parse_semester_tables: {e}")


if __name__ == "__main__":
    """
    Main function to parse HTML content and return structured data.
    """

    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python parse.py [-s|-c] [html_file_path]")
        print("  -s: origanized by semester")
        print("  -c: origanized by course")
        sys.exit(1)

    # Parse command line arguments
    if sys.argv[1] not in ['-s', '-c']:
        print("Invalid mode. Use -s or -c.")
        sys.exit(1)

    main_mode = 'semester' if sys.argv[1] == '-s' else 'course'
    html_file_path = sys.argv[2]

    # Read HTML content from the specified file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Call parse_semester_tables function
    success, result = parse_semester_tables(html_content, main_mode)

    if success:
        print(result)
    else:
        print(result)
        sys.exit(1)    
