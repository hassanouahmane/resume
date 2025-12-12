Write-Output "--- run.ps1 status ---"
& "$PSScriptRoot\..\run.ps1" status

$pidFile = Join-Path $PSScriptRoot "..\uvicorn.pid"
Write-Output "--- PID file ---"
if (Test-Path $pidFile) {
    $pid = (Get-Content $pidFile).Trim()
    Write-Output "PID: $pid"
    try {
        Get-Process -Id $pid -ErrorAction Stop | Format-List Id,ProcessName,Path,StartTime
    } catch {
        Write-Output "Process $pid not running"
    }
} else {
    Write-Output "No PID file"
}

Write-Output "--- netstat for ports 8000/8001 ---"
netstat -ano | findstr ":8000"
netstat -ano | findstr ":8001"

Write-Output "--- HTTP /docs checks (8000,8001) ---"
foreach ($p in 8000,8001) {
    try {
        $r = Invoke-WebRequest -Uri ("http://localhost:$p/docs") -UseBasicParsing -TimeoutSec 2
        Write-Output ("http://localhost:$p/docs -> " + $r.StatusCode)
    } catch {
        Write-Output ("http://localhost:$p/docs -> failed: " + $_.Exception.Message)
    }
}
