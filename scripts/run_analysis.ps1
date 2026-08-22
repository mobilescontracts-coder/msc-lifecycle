$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
python "$Root\analysis\analyze_spos_msc_v4.py" `
  --smoke-csv "$Root\data\raw\cpn\SPoS_MSC_v4_smoke_2.csv" `
  --pilot-csv "$Root\data\raw\cpn\SPoS_MSC_v4_sensitivity_pilot_72.csv" `
  --default-csv "$Root\data\raw\cpn\SPoS_MSC_v4_default_configuration_audit_700.csv" `
  --ofat-csv "$Root\data\raw\cpn\SPoS_MSC_v4_sensitivity_OFAT_2400.csv" `
  --output-dir "$Root\analysis\reproduced"
