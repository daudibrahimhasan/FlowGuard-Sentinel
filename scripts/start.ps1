param([switch]$Install, [switch]$Production)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
if ($Install) {
  if (!(Test-Path backend/.venv/Scripts/python.exe)) { python -m venv backend/.venv }
  & backend/.venv/Scripts/python.exe -m pip install --cache-dir backend/.pip-cache -r backend/requirements.txt
  if ($LASTEXITCODE -ne 0) { throw 'Backend installation failed' }
  Push-Location frontend
  try { npm install --cache .npm-cache; if ($LASTEXITCODE -ne 0) { throw 'Frontend installation failed' } } finally { Pop-Location }
}
if (!(Test-Path backend/.venv/Scripts/python.exe)) { throw 'Run scripts/start.ps1 -Install first' }
$pythonPath = Join-Path $projectRoot 'backend/.venv/Scripts/python.exe'
$api = Start-Process -FilePath $pythonPath -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000' -WorkingDirectory (Join-Path $projectRoot 'backend') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $projectRoot 'backend-server.log') -RedirectStandardError (Join-Path $projectRoot 'backend-error.log')
$apiReady = $false
for ($attempt = 0; $attempt -lt 40; $attempt++) {
  try { $health = Invoke-RestMethod 'http://127.0.0.1:8000/api/health' -TimeoutSec 1; if ($health.status -eq 'ok') { $apiReady = $true; break } } catch { Start-Sleep -Milliseconds 250 }
}
if (!$apiReady) { throw 'Backend did not become ready. Check backend-error.log before starting another copy.' }
$webCommand = if ($Production) { 'npm run start -- --hostname 127.0.0.1' } else { 'npm run dev -- --hostname 127.0.0.1' }
$web = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c',$webCommand -WorkingDirectory (Join-Path $projectRoot 'frontend') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $projectRoot 'frontend-server.log') -RedirectStandardError (Join-Path $projectRoot 'frontend-error.log')
@{backend=$api.Id;frontend=$web.Id} | ConvertTo-Json | Set-Content (Join-Path $projectRoot '.server-pids.json')
Write-Host 'FlowGuard Sentinel: http://localhost:3000 | API: http://127.0.0.1:8000/docs'
Write-Host 'Demo only. All financial events are synthetic. Logs and process IDs are in the project folder.'
