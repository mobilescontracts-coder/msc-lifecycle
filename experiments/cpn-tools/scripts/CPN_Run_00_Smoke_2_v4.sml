(* SPoS-MSC v4 two-replication smoke test. CPN'Replications requires n > 1. *)
ipSetBaseSeed(626);
ipResetSensitivityParameters();
ipSetScenario(1);
ipSetDesign("SMOKE","Q1","DEFAULT");
ipSetCSVFile("SPoS_MSC_v4_smoke_2.csv");
ipResetRunCounter();
ipCurrentSensitivity();
CPN'Replications.nreplications 2;
