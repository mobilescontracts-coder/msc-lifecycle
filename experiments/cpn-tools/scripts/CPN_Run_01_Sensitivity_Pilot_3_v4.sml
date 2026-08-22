(* SPoS-MSC v4 pilot: 8 factors x 3 levels x 3 replications = 72 runs. *)
ipSetBaseSeed(626);
ipSetCSVFile("SPoS_MSC_v4_sensitivity_pilot_72.csv");

(* WORKLOAD, anchored to Q1. *)
ipResetSensitivityParameters(); ipSetScenario(1); ipSetDesign("OFAT","WORKLOAD","LOW"); ipSetTxOverride(16); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(1); ipSetDesign("OFAT","WORKLOAD","DEFAULT"); ipSetTxOverride(24); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(1); ipSetDesign("OFAT","WORKLOAD","HIGH"); ipSetTxOverride(40); ipResetRunCounter(); CPN'Replications.nreplications 3;

(* CROSS_SHARD_PCT, anchored to Q3. *)
ipResetSensitivityParameters(); ipSetScenario(3); ipSetDesign("OFAT","CROSS_SHARD_PCT","LOW"); ipSetCrossShardPct(20); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(3); ipSetDesign("OFAT","CROSS_SHARD_PCT","DEFAULT"); ipSetCrossShardPct(60); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(3); ipSetDesign("OFAT","CROSS_SHARD_PCT","HIGH"); ipSetCrossShardPct(80); ipResetRunCounter(); CPN'Replications.nreplications 3;

(* REQUEST_OFFLINE_PCT, anchored to Q4. *)
ipResetSensitivityParameters(); ipSetScenario(4); ipSetDesign("OFAT","REQUEST_OFFLINE_PCT","LOW"); ipSetRequestOfflinePct(10); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(4); ipSetDesign("OFAT","REQUEST_OFFLINE_PCT","DEFAULT"); ipSetRequestOfflinePct(20); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(4); ipSetDesign("OFAT","REQUEST_OFFLINE_PCT","HIGH"); ipSetRequestOfflinePct(30); ipResetRunCounter(); CPN'Replications.nreplications 3;

(* RECEIPT_DROP_PCT, anchored to Q4. *)
ipResetSensitivityParameters(); ipSetScenario(4); ipSetDesign("OFAT","RECEIPT_DROP_PCT","LOW"); ipSetReceiptDropPct(10); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(4); ipSetDesign("OFAT","RECEIPT_DROP_PCT","DEFAULT"); ipSetReceiptDropPct(29); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(4); ipSetDesign("OFAT","RECEIPT_DROP_PCT","HIGH"); ipSetReceiptDropPct(40); ipResetRunCounter(); CPN'Replications.nreplications 3;

(* OWNER_CAP, anchored to Q5. *)
ipResetSensitivityParameters(); ipSetScenario(5); ipSetDesign("OFAT","OWNER_CAP","LOW"); ipSetOwnerCap(1500); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(5); ipSetDesign("OFAT","OWNER_CAP","DEFAULT"); ipSetOwnerCap(3000); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(5); ipSetDesign("OFAT","OWNER_CAP","HIGH"); ipSetOwnerCap(6000); ipResetRunCounter(); CPN'Replications.nreplications 3;

(* MOBILE_THRESHOLD, anchored to Q6. *)
ipResetSensitivityParameters(); ipSetScenario(6); ipSetDesign("OFAT","MOBILE_THRESHOLD","LOW"); ipSetMobileThreshold(25); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(6); ipSetDesign("OFAT","MOBILE_THRESHOLD","DEFAULT"); ipSetMobileThreshold(35); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(6); ipSetDesign("OFAT","MOBILE_THRESHOLD","HIGH"); ipSetMobileThreshold(65); ipResetRunCounter(); CPN'Replications.nreplications 3;

(* COMMITTEE_QUORUM, anchored to Q6. *)
ipResetSensitivityParameters(); ipSetScenario(6); ipSetDesign("OFAT","COMMITTEE_QUORUM","LOW"); ipSetCommitteeQuorum(3,2); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(6); ipSetDesign("OFAT","COMMITTEE_QUORUM","DEFAULT"); ipSetCommitteeQuorum(4,3); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(6); ipSetDesign("OFAT","COMMITTEE_QUORUM","HIGH"); ipSetCommitteeQuorum(5,4); ipResetRunCounter(); CPN'Replications.nreplications 3;

(* LOAD_THRESHOLD, anchored to Q7. *)
ipResetSensitivityParameters(); ipSetScenario(7); ipSetDesign("OFAT","LOAD_THRESHOLD","LOW"); ipSetLoadThresholdOverride(45); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(7); ipSetDesign("OFAT","LOAD_THRESHOLD","DEFAULT"); ipSetLoadThresholdOverride(55); ipResetRunCounter(); CPN'Replications.nreplications 3;
ipResetSensitivityParameters(); ipSetScenario(7); ipSetDesign("OFAT","LOAD_THRESHOLD","HIGH"); ipSetLoadThresholdOverride(75); ipResetRunCounter(); CPN'Replications.nreplications 3;

