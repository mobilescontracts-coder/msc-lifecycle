(* SPoS-MSC v4 declaration-only check. Run only after syntax checking finishes. *)
ipSetBaseSeed(626);
ipResetSensitivityParameters();
ipSetScenario(1);
ipSetDesign("CHECK","Q1","DEFAULT");
ipCurrentSensitivity();
