import fetchScore
import fetchShowDo
import sys
import parse

def main():

    if len(sys.argv) != 3 and len(sys.argv) != 1:
        print("用法：python script.py [cookies_file_path] [STUDENT_ID]")
        sys.exit(1)
    elif len(sys.argv) == 3:
        cookies_path = sys.argv[1]
        xh_value = sys.argv[2]
    else:
        cookies_path = "cookies.txt"   # 这里替换为您的文件路径
        xh_value = "2204112914"        # 替换为您需要的学号
    

    success1, show_do = fetchShowDo.fetch_show_do(cookies_path, xh_value)
    if not success1:
        # print show_do
        print(show_do)
        sys.exit(1)

    success2, score_page = fetchScore.fetch_score_page(cookies_path, show_do)
    if not success2:
        # print score_page
        print(score_page)
        sys.exit(1)
        
    semester_data = parse.parse_semester_tables(score_page, 'course')
    if not semester_data:
        print("未解析到任何学期或课程成绩。")
        return

    print(semester_data)

if __name__ == "__main__":
    main()
