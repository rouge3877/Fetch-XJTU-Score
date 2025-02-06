# Check Python version
function Check-PythonVersion {
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        $global:PYTHON_CMD = "python3"
    }
    else {
        $global:PYTHON_CMD = "python"
    }
    Write-Output "Using Python: $global:PYTHON_CMD"
}

# Setup virtual environment
function Set-Env {
    Write-Output "Setting up environment..."
    & $global:PYTHON_CMD -m venv .venv
    # Install requirements using the venv pip
    if (Test-Path ./.venv/bin/pip) {
        & ./.venv/bin/pip install -r requirements.txt
    }
    else {
        Write-Error "pip not found in virtual environment."
    }
    Write-Output "Environment setup complete."
}

# Build project
function Build-Project {
    Write-Output "Building project..."
    if (Test-Path ./dist) {
        Remove-Item -Recurse -Force ./dist
        Write-Output "Removed 'dist' directory."
    }
    # Use pyinstaller (assumes it is installed)
    pyinstaller --onefile --windowed src/main.py
    Write-Output "Build completed. Executable is in the 'dist' directory."
}

# Clean generated files
function Clean-Project {
    Write-Output "Cleaning project..."
    $pathsToRemove = @("dist", "build", ".venv", "__pycache__", "src/main.spec", "main.spec")
    foreach ($path in $pathsToRemove) {
        if (Test-Path $path) {
            Remove-Item -Recurse -Force $path
            Write-Output "Removed: $path"
        }
    }
    Write-Output "Clean completed."
}

# Run project
function Run-Project {
    param (
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$ArgsList
    )
    Write-Output "Running main.py with arguments: $ArgsList"
    # Execute using the venv python if available, otherwise fallback to $PYTHON_CMD
    if (Test-Path ./.venv/bin/python) {
        & ./.venv/bin/python src/main.py @ArgsList
    }
    else {
        & $global:PYTHON_CMD src/main.py @ArgsList
    }
}

# Score project
function Score-Project {
    param (
        [string]$Param
    )
    # Create score_pages directory if it doesn't exist
    if (-not (Test-Path score_pages)) {
        New-Item -ItemType Directory -Path score_pages | Out-Null
    }
    # Generate the score HTML
    $command1 = { & $global:PYTHON_CMD src/main.py -s cookies.txt $using:Param }
    $command2 = { & $global:PYTHON_CMD src/generate_html.py $using:Param -s }
    $scoreHtml = & $command1 | & $command2
    $outputFile = "score_pages/$Param.html"
    $scoreHtml | Out-File -Encoding utf8 $outputFile
    # Open the generated HTML file in google-chrome
    google-chrome $outputFile
}

# Deactivate virtual environment
function Deactivate-Env {
    Write-Output "Deactivating virtual environment..."
    Write-Output "To leave the virtual environment, close the current shell."
}

# Begin script execution
Check-PythonVersion

if ($args.Count -eq 0) {
    Write-Output "Usage: .\setup.ps1 {set_env|build|clean|run|score|deactivate} [additional arguments]"
    exit 1
}

switch ($args[0]) {
    "set_env" { Set-Env }
    "build" { Build-Project }
    "clean" { Clean-Project }
    "run" { 
        $remainingArgs = $args[1..($args.Count - 1)]
        Run-Project @remainingArgs 
    }
    "score" { 
        if ($args.Count -lt 2) {
            Write-Output "Usage: .\setup.ps1 score <parameter>"
            exit 1
        }
        Score-Project -Param $args[1]
    }
    "deactivate" { Deactivate-Env }
    default {
        Write-Output "Usage: .\setup.ps1 {set_env|build|clean|run|score|deactivate}"
        exit 1
    }
}