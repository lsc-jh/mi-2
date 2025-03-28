$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VenvPath = Join-Path $ScriptDir "venv"

if (-Not (Test-Path $VenvPath)) {
    python -m venv $VenvPath
}

& "$VenvPath\Scripts\Activate.ps1"
pip install --upgrade pip
pip install blessed

$env:RUNNING_INSIDE_VENV = "1"
python "$ScriptDir\main.py"