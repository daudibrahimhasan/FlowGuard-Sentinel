$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $projectRoot '.server-pids.json'
if (!(Test-Path -LiteralPath $pidFile)) { Write-Host 'No saved startup processes.'; exit }
$saved = Get-Content -LiteralPath $pidFile -Raw | ConvertFrom-Json
$inventory = @(Get-CimInstance Win32_Process)
foreach ($kind in @('backend','frontend')) {
  $savedId = [int]$saved.$kind
  $parent = $inventory | Where-Object ProcessId -EQ $savedId
  if (!$parent) { continue }
  $valid = if ($kind -eq 'backend') { $parent.CommandLine.Contains($projectRoot) -and $parent.CommandLine.Contains('uvicorn') } else { $parent.CommandLine -match 'cmd.exe.*npm run (dev|start)' }
  if (!$valid) { throw "Saved $kind process no longer matches this launcher; refusing to stop it." }
  $pending = @($savedId)
  $found = @($savedId)
  while ($pending.Count) {
    $children = @($inventory | Where-Object { $_.ParentProcessId -in $pending } | Select-Object -ExpandProperty ProcessId)
    $pending = @($children | Where-Object { $_ -notin $found })
    $found += $pending
  }
  [array]::Reverse($found)
  foreach ($processId in $found) { Stop-Process -Id $processId -ErrorAction SilentlyContinue }
}
Remove-Item -LiteralPath $pidFile
Write-Host 'Stopped the saved local FlowGuard server processes.'
