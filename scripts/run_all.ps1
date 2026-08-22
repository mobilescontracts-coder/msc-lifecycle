$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
& "$PSScriptRoot\verify_checksums.ps1"
python -m pytest -q "$Root\tests"
& "$PSScriptRoot\run_analysis.ps1"
python "$Root\analysis\verify_reference_outputs.py" `
  --generated "$Root\analysis\reproduced" `
  --reference "$Root\analysis\reference_outputs"
& "$PSScriptRoot\build_manuscript.ps1"
