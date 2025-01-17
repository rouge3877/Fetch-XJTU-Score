# 参数定义部分，放在文件的最上方
param (
    [string]$command
)

# 检查 Python 版本
function Check-PythonVersion {
    $pythonCmd = "python"
    
    # 检查 python3 是否存在
    # if (Get-Command python3 -ErrorAction SilentlyContinue) {
    #     $pythonCmd = "python3"
    # }

    Write-Host "Using Python: $pythonCmd"
    return $pythonCmd
}

# 设置虚拟环境
function Set-Env {
    $pythonCmd = Check-PythonVersion

    Write-Host "Setting up environment..."
    & $pythonCmd -m venv .venv
    
    # 激活虚拟环境
    .\.venv\Scripts\Activate.ps1

    # 安装依赖
    pip install -r requirements.txt

    Write-Host "Environment setup complete."
}

# 构建项目
function Build {
    Write-Host "Building project..."

    # 清理 dist 目录（先检查是否存在）
    if (Test-Path "dist") {
        Remove-Item -Recurse -Force "dist"
        Write-Host "Removed 'dist' directory."
    }

    # 使用 PyInstaller 构建项目
    pyinstaller --onefile --windowed src\main.py

    Write-Host "Build completed. Executable is in the 'dist' directory."
}

# 清理生成的文件
function Clean {
    Write-Host "Cleaning project..."

    # 删除生成的文件和目录（先检查是否存在）
    $dirsToRemove = @("dist", "build", ".venv", "__pycache__", "src\main.spec", "main.spec")
    foreach ($dirPath in $dirsToRemove) {
        if (Test-Path $dirPath) {
            if (Test-Path "$dirPath\*") {
                Remove-Item -Recurse -Force $dirPath
                Write-Host "Removed directory: $dirPath"
            } else {
                Remove-Item -Force $dirPath
                Write-Host "Removed file: $dirPath"
            }
        }
    }

    Write-Host "Clean completed."
}

# 运行项目
function Run {
    param (
        [string[]]$args
    )

    Write-Host "Running main.py with arguments: $args"

    # 激活虚拟环境
    .\.venv\Scripts\Activate.ps1

    # 运行 Python 脚本并传递参数
    python src\main.py @args
}

# 退出虚拟环境
function Deactivate-Env {
    Write-Host "Deactivating virtual environment..."
    deactivate
}

# 主程序：处理命令行输入
$pythonCmd = Check-PythonVersion

switch ($command) {
    "set_env" { Set-Env }
    "build" { Build }
    "clean" { Clean }
    "run" { 
        $args = $args[1..($args.Length - 1)]  # 获取除第一个命令外的所有参数
        Run -args $args
    }
    "deactivate" { Deactivate-Env }
    default {
        Write-Host "Usage: .\setup_windows.ps1 {set_env|build|clean|run|deactivate}"
        exit 1
    }
}
