#!/bin/bash

# 检查 Python 版本
function check_python_version() {
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
    echo "Using Python: $PYTHON_CMD"
}

# 设置虚拟环境
function set_env() {
    echo "Setting up environment..."
    $PYTHON_CMD -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "Environment setup complete."
}

# 构建项目
function build() {
    echo "Building project..."

    # 清理 dist 目录（先检查是否存在）
    if [ -d "dist" ]; then
        rm -rf dist
        echo "Removed 'dist' directory."
    fi

    # 使用 PyInstaller 构建项目
    pyinstaller --onefile --windowed src/main.py

    echo "Build completed. Executable is in the 'dist' directory."
}

# 清理生成的文件
function clean() {
    echo "Cleaning project..."

    # 删除生成的文件和目录（先检查是否存在）
    dirs_to_remove=("dist" "build" ".venv" "__pycache__" "src/main.spec" "main.spec")
    for dir_path in "${dirs_to_remove[@]}"; do
        if [ -e "$dir_path" ]; then
            if [ -d "$dir_path" ]; then
                rm -rf "$dir_path"
                echo "Removed directory: $dir_path"
            else
                rm "$dir_path"
                echo "Removed file: $dir_path"
            fi
        fi
    done

    echo "Clean completed."
}

# 运行项目
function run() {
    echo "Running main.py with arguments: $@"
    source .venv/bin/activate
    python src/main.py "$@"  # 传递参数给 Python 脚本
}

# 退出虚拟环境
function deactivate_env() {
    echo "Deactivating virtual environment..."
    deactivate
}

# 评分项目
function score() {
    #!/usr/bin/env zsh
    mkdir -p score_pages
    python3 src/main.py -s cookies.txt "$1" | python3 src/generate_html.py "$1" -s > score_pages/"$1".html
    google-chrome score_pages/"$1".html
}

# 检查 Python 版本
check_python_version

# 检查输入的命令
case "$1" in
    set_env)
        set_env
        ;;
    build)
        build
        ;;
    clean)
        clean
        ;;
    run)
        shift
        run "$@"  # 传递剩余的命令行参数
        ;;
    score)
        shift
        score "$@"
        ;;
    deactivate)
        deactivate_env
        ;;
    *)
        echo "Usage: $0 {set_env|build|clean|run|score|deactivate}"
        exit 1
        ;;
esac
