param(
    [Parameter(Position=0)]
    [ValidateSet("start","stop","restart","status")]
    [string]$action = "start",
    [int]$Port = 8000,
    [switch]$Foreground,
    [switch]$Reload
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$venvPython = Join-Path $root "venv\Scripts\python.exe"
$appDir = $root
$pidFile = Join-Path $root "uvicorn.pid"

function Start-Server {
    if (Test-Path $pidFile) {
        Write-Output "PID file exists at ${pidFile}. Server may already be running. Use 'status' or 'stop'."
        return
    }
    if (-not (Test-Path $venvPython)) {
        Write-Output "venv python not found at: ${venvPython}"
        Write-Output "Activate your venv or create it with: python -m venv venv"
        exit 1
    }
    $args = @('-m','uvicorn','main:app','--host','0.0.0.0','--port',"$Port",'--app-dir',$appDir)
    if ($Reload) { $args = $args + '--reload' }
    if ($Foreground) {
        Write-Output "Launching uvicorn in foreground (port $Port). Press Ctrl+C to stop."
        & $venvPython @args
        return
    }

    $proc = Start-Process -FilePath $venvPython -ArgumentList $args -PassThru -WindowStyle Normal
    $proc.Id | Out-File -FilePath $pidFile -Encoding ascii
    Write-Output "Started uvicorn (PID $($proc.Id)). PID saved to ${pidFile}"
}

function Stop-Server {
    if (-not (Test-Path $pidFile)) {
        Write-Output "PID file not found (${pidFile}). Server may not be running."
        return
    }
    $serverPid = Get-Content $pidFile
    if (-not $serverPid) { Remove-Item $pidFile -ErrorAction SilentlyContinue; Write-Output "Empty PID file removed."; return }
    try {
        if (Get-Process -Id $serverPid -ErrorAction SilentlyContinue) {
            Stop-Process -Id $serverPid -Force -ErrorAction Stop
            Remove-Item $pidFile -ErrorAction SilentlyContinue
            Write-Output "Stopped process ${serverPid} and removed pid file."
        } else {
            Remove-Item $pidFile -ErrorAction SilentlyContinue
            Write-Output "Removed stale PID file (process ${serverPid} not running)."
        }
    } catch {
        Write-Output "Failed to stop process ${serverPid}: $_"
    }
}

function Status-Server {
    if (Test-Path $pidFile) {
        $serverPid = Get-Content $pidFile
        if (Get-Process -Id $serverPid -ErrorAction SilentlyContinue) {
            Write-Output "Server running (PID ${serverPid})"
        } else {
            Write-Output "PID file exists but process ${serverPid} is not running."
        }
    } else {
        Write-Output "Server not running."
    }
}

switch ($action) {
    'start' { Start-Server }
    'stop' { Stop-Server }
    'restart' { Stop-Server; Start-Sleep -Seconds 1; Start-Server }
    'status' { Status-Server }
    default { Write-Output "Unknown action: $action" }
}
