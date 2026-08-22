$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
$Manifest = Join-Path $Root "CHECKSUMS.sha256"
Get-Content $Manifest | ForEach-Object {
  if ($_ -match '^([0-9a-f]{64})  (.+)$') {
    $Expected = $Matches[1]
    $File = Join-Path $Root $Matches[2]
    $Actual = (Get-FileHash -Algorithm SHA256 $File).Hash.ToLower()
    if ($Actual -ne $Expected) { throw "Checksum mismatch: $($Matches[2])" }
  }
}
Write-Host "PASS: all checksums match."
