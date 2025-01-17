# Auto Fetch Score from ehall.xjtu.edu.cn

*(No need for target account authentication information)*

## Announcement

**The script is only used for learning web knowledge. Please do not use this script to obtain unauthorized personal data !**

**The script is only used for learning web knowledge. Please do not use this script to obtain unauthorized personal data !**

**The script is only used for learning web knowledge. Please do not use this script to obtain unauthorized personal data !**

**The author of this script is not responsible for any legal disputes arising from the use of this script.**

## Introduction

This script is used to automatically fetch the score from `ehall.xjtu.edu.cn`

## Usage

1. Install the required packages

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the script

```bash
python main.py [-c|-s] [cookies's path] <student_id>
```

- `-c`: Parse the course mode, default is course mode.
- `-s`: Parse the semester mode.
- `cookies's path`: The path of the cookies file. You should export the cookies from the browser and save it to a file.
- `student_id`: The student id of the target student.

## Cookies

1. Open the browser and login to `ehall.xjtu.edu.cn`.
2. Rondomly choose a service, such as `个人方案查询`.
3. Click `进入服务` button on the bottom.
4. Now, you can see there are three buttons on the middle of the page: `学生`, `移动应用学生`, `学生组`. You could click any one button that you like.
 （*Sometimes and in some service you choosed in step 2, there are maybe less buttons, but anyway, just choose one of them.*）
5. Press `F12` to open the developer tools, and click the `Application` tab.
6. Click the `Cookies` item on the left, and then click the `https://ehall.xjtu.edu.cn` item.
7. Find the `_WEU` and `MOD_AMP_AUTH` cookies, and copy the value of them to a file. The file should be like this:

    ```text
    _WEU=rpoMoUyzA59m...o24tNX;
    MOD_AMP_AUTH=MOD_AMP_c77e...07e2;
    ```
    * The basic format of the cookies should be `key=value;`
    * Just copy the `_WEU` and `MOD_AMP_AUTH` cookies, other cookies are not necessary.
    * The value of the cookies should be separated by `;`, and space, tab or newline is allowed between the cookies, but not necessary. So just be free to copy the cookies.
    * A simple way to get the cookies is clicking the target cookie, and its cookies value will be shown on the bottom of the pine. You can copy it directly.

8. Save the file to a path, and use the path as the cookies's path in the script.


