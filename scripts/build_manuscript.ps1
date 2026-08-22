$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
Push-Location "$Root\manuscript"
$env:SOURCE_DATE_EPOCH = "1787011200"
try { latexmk -pdf Manuscript_SMPT.tex } finally { Pop-Location }
