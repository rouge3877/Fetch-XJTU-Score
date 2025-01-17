import fetchScore
import fetchShowDo
import sys
import parse

def getScoreFromID(cookies_path, xh_value, parse_mode='course'):
    """
    Get the score data from the student id.
    Organize the workflow of the fetchShowDo, fetchScore and parse modules.
    :param cookies_path: The path of the cookies file.
    :param xh_value: The student id of the student.
    :param parse_mode: The parse mode of the parse module.
    :return: A tuple of (success, data or error message).
    """
    # print show_do
    success1, show_do = fetchShowDo.fetch_show_do(cookies_path, xh_value)
    if not success1:
        return False, show_do

    # print score_page
    success2, score_page = fetchScore.fetch_score_page(cookies_path, show_do)
    if not success2:
        return False, score_page
        
    # parse the semester tables
    semester_data = parse.parse_semester_tables(score_page, parse_mode)
    if not semester_data:
        return False, "Failed to parse the semester tables."
    else:
        return True, semester_data

def checkStudentID(student_id):
    """
    Check if the student id is valid.
    :param student_id: The student id of the student, a string.
    :return: A tuple of (success, error message).

    1. The student id should be 10 characters long.
    2. The student id should be a string of digits.
    3. The [1-2] characters of the student id should be less than 26 and greater than 10.
    4. The first character of the student id should be '2'.
    """
    if len(student_id) != 10:
        return False, "The student id should be 10 characters long."
    if not student_id.isdigit():
        return False, "The student id should be a string of digits."
    if int(student_id[1:3]) < 10 or int(student_id[1:3]) > 25:
        return False, "The [1-2] characters of the student id should be less than 26 and greater than 10."
    if student_id[0] != '2':
        return False, "The first character of the student id should be '2'."
    return True, ""

def printError(error_message):
    """
    Print the error message to stderr in red blod font.
    Get the console's background color:
        if the background color is not black, the font will be red and bold and the background color will be black;
        if the background color is black, the font will be red and bold and the background color will be write.
    :param error_message: The error message to print.
    """

    # get the console's background color
    import os
    import platform
    if platform.system() == "Windows":
        import ctypes
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        csbi = ctypes.create_string_buffer(22)
        res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        if res:
            bg_color = ord(csbi[4])
        else:
            bg_color = 0
    else:
        bg_color = int(os.popen('tput setab 0').read().strip())

    # print the error message
    if bg_color == 0:
        # black background
        # the font will be red and bold and the background color will be write
        print("\033[1;47;31m" + "Failed:" + error_message + "\033[0m", file=sys.stderr)
    else:
        # not black background
        # the font will be red and bold and the background color will be black
        print("\033[1;31;40m" + "Failed:" + error_message + "\033[0m", file=sys.stderr)

    # exit the script    
    sys.exit(1)

def main():
    """
    Main function of the script (just a simple demo).
    """
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print("Usage: python script.py [cookies_file_path] <student_id>")
        print("\tcookies_file_path: The path of the cookies file, default is ./cookies.txt.")
        print("\tstudent_id: The student id of the student.")
        sys.exit(1)
    elif len(sys.argv) == 3:
        cookies_path = sys.argv[1]
        xh_value = sys.argv[2]
    else:
        cookies_path = "cookies.txt"   # default cookies file path
        xh_value = sys.argv[1]

    # check the student id
    success, error_message = checkStudentID(xh_value)
    if not success:
        printError(error_message)
        
    success, score_data = getScoreFromID(cookies_path, xh_value)
    if not success:
        printError(score_data)
    else:
        print("Success!")
        print(score_data)
        sys.exit(0)

if __name__ == "__main__":
    main()
