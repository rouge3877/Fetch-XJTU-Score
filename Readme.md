# Auto Fetch Score from ehall.xjtu.edu.cn

*(No need for target account authentication information)*

## 0. Announcement

**The script is only used for learning web knowledge. Please do not use this script to obtain unauthorized personal data !**

**The script is only used for learning web knowledge. Please do not use this script to obtain unauthorized personal data !**

**The script is only used for learning web knowledge. Please do not use this script to obtain unauthorized personal data !**

**The author of this script is not responsible for any legal disputes arising from the use of this script.**

## 1. Introduction

This script is used to automatically fetch the score from `ehall.xjtu.edu.cn`

## 2. Usage of the python script

***<u>Before running the script, a cookies file is required. The cookies file should be exported from the browser and saved to a file. The cookies file should contain the `_WEU` and `MOD_AMP_AUTH` cookies.</u> (see chapter 4 for more details)***

1. Install the required packages

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the script

```bash
python main.py [-c|-s] [cookies's path] <student_id>

mkdir -p score_pages
python3 src/main.py -s cookies.txt $1  | python3 src/generate_html.py $1 -s > score_pages/$1.html
google-chrome score_pages/$1.html
```

- `-c`: Parse the course mode, default is course mode.
- `-s`: Parse the semester mode.
- `cookies's path`: The path of the cookies file. You should export the cookies from the browser and save it to a file.
- `student_id`: The student id of the target student.

## 3. Usage of `setup.sh`  -  *There is a bug waiting to be fixed* :(

There are two setup scripts in the repository, `setup.sh` and `setup.ps1` for Linux and Windows respectively.
These scripts help in setting up the environment, building, cleaning, running, and deactivating the virtual environment for the project.

### Guide for setup.ps1:

```powershell
.\setup.ps1 {set_env|build|clean|run|deactivate}
```

#### Set up the environment
Sets up the Python virtual environment and installs dependencies.

```powershell
.\setup.ps1 set_env
```


#### Run the project
Runs the `main.py` script with optional arguments. The arguments are passed to the script. *See the usage of the python script.*

```powershell
.\setup.ps1 run [args]
```

#### Deactivate the virtual environment
Deactivates the Python virtual environment.

```powershell
.\setup.ps1 deactivate
```

#### Build the project (into an **executable**)
Builds the project using PyInstaller and creates an **executable** in the `dist` directory.

```powershell
.\setup.ps1 build
```

#### Clean the project
Cleans up generated files and directories such as `dist`, `build`, `.venv`, `__pycache__`, and `main.spec`.

```powershell
.\setup.ps1 clean
```

### Guide for setup.sh:

```bash
./setup.sh {set_env|build|clean|run|deactivate}
```

#### Set up the environment
Sets up the Python virtual environment and installs dependencies.

```bash
./setup.sh set_env
```


#### Run the project
Runs the `main.py` script with optional arguments. The arguments are passed to the script. *See the usage of the python script.*

```bash
./setup.sh run [args]
```

#### Deactivate the virtual environment
Deactivates the Python virtual environment.

```bash
./setup.sh deactivate
```

#### Build the project (into an **executable**)
Builds the project using PyInstaller and creates an **executable** in the `dist` directory.

```bash
./setup.sh build
```

#### Clean the project
Cleans up generated files and directories such as `dist`, `build`, `.venv`, `__pycache__`, and `main.spec`.

```bash
./setup.sh clean
```

## 4. Cookies

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


