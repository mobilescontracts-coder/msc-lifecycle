(* SPoS-MSC v4: default-configuration audit, 7 x 100 = 700 replications. *)
ipSetBaseSeed(626);
ipSetCSVFile("SPoS_MSC_v4_default_configuration_audit_700.csv");

ipResetSensitivityParameters(); ipSetDesign("DEFAULT_EQ","Q1","DEFAULT"); ipSetScenario(1); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipResetSensitivityParameters(); ipSetDesign("DEFAULT_EQ","Q2","DEFAULT"); ipSetScenario(2); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipResetSensitivityParameters(); ipSetDesign("DEFAULT_EQ","Q3","DEFAULT"); ipSetScenario(3); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipResetSensitivityParameters(); ipSetDesign("DEFAULT_EQ","Q4","DEFAULT"); ipSetScenario(4); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipResetSensitivityParameters(); ipSetDesign("DEFAULT_EQ","Q5","DEFAULT"); ipSetScenario(5); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipResetSensitivityParameters(); ipSetDesign("DEFAULT_EQ","Q6","DEFAULT"); ipSetScenario(6); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipResetSensitivityParameters(); ipSetDesign("DEFAULT_EQ","Q7","DEFAULT"); ipSetScenario(7); ipResetRunCounter(); CPN'Replications.nreplications 100;
