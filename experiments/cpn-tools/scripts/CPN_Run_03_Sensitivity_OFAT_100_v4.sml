(* SPoS-MSC v4: full independent-group OFAT experiment, 8 x 3 x 100 = 2400 replications. *)
ipSetBaseSeed(626);
ipSetCSVFile("SPoS_MSC_v4_sensitivity_OFAT_2400.csv");

ipApplyOFAT("WORKLOAD","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("WORKLOAD","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("WORKLOAD","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;

ipApplyOFAT("CROSS_SHARD_PCT","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("CROSS_SHARD_PCT","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("CROSS_SHARD_PCT","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;

ipApplyOFAT("REQUEST_OFFLINE_PCT","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("REQUEST_OFFLINE_PCT","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("REQUEST_OFFLINE_PCT","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;

ipApplyOFAT("RECEIPT_DROP_PCT","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("RECEIPT_DROP_PCT","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("RECEIPT_DROP_PCT","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;

ipApplyOFAT("OWNER_CAP","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("OWNER_CAP","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("OWNER_CAP","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;

ipApplyOFAT("MOBILE_THRESHOLD","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("MOBILE_THRESHOLD","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("MOBILE_THRESHOLD","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;

ipApplyOFAT("COMMITTEE_QUORUM","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("COMMITTEE_QUORUM","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("COMMITTEE_QUORUM","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;

ipApplyOFAT("LOAD_THRESHOLD","LOW"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("LOAD_THRESHOLD","DEFAULT"); ipResetRunCounter(); CPN'Replications.nreplications 100;
ipApplyOFAT("LOAD_THRESHOLD","HIGH"); ipResetRunCounter(); CPN'Replications.nreplications 100;
