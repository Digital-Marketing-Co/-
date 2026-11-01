# Run records and reusable templates

## Search log (CSV)
Use columns: pass_id, searched_at, platform, query_exact, filters, results_returned, records_inspected, source_id, eligibility, decision_reason, retrieval_status, new_material_finding, affected_claim_ids. Unknown result counts remain blank. One row per inspected record; use a query-only row for zero results or unavailable retrieval.

## Evidence matrix (CSV)
Use columns: claim_id, claim_text, claim_type, source_id, locator, locator_verified, evidence_grade, directness, risk_of_bias, consistency, alternatives, transfer_limits, training_ids, note_numbers. One row per claim-source relationship. Distinguish missing evidence from evidence of no effect.

## Individual dog profile (JSON)
Record profile_id, date, age, breed_or_morphology, medical_status, veterinary_review, medication_context_if_supplied, sensory_status, mobility, household, safety_constraints, bite_history, observed_behavior, antecedents, consequences, baseline, preferred_rewards, equipment, owner_constraints and missing_information. Use null for unavailable details. Do not collect unnecessary identifying information.

## Individual training plan (JSON)
Record id, profile_id, category, purpose, prerequisites, baseline, success_criteria, environment, equipment, reinforcement, steps, progression, regression, generalization, maintenance, troubleshooting, welfare, evidence_ids, designer_selected_criteria, review_date and referral_conditions. Make each step observable. Specify stop conditions and an easier fallback. Never invent case results.

## Session record (CSV)
Use columns: session_id, date, plan_id, setting, trigger_intensity, trigger_distance, opportunities, successes, latency_seconds, prompt_level, reinforcement, observed_stress, recovery, opt_out, next_adjustment. Include an empty writable copy with the curriculum.

## Image inventory (JSON)
Record id, type, heading_id, path, sha256, perceptual_hash, prompt, generation_method, generated_at, purpose, page, word_position, width, height, alpha_extrema, native_composition_verified, anatomical_review, contextual_review, uniqueness_review, compositing_review, conceptual_caption and status. Missing checks remain unresolved.

## QA report (JSON)
Record gates as name, status, evidence, reviewer, checked_at, correction and remaining_limit. Include search_coverage, stopping_reason, saturation_reached, inaccessible_sources, missing_domains and artifact_versions. A script reports structure only; completion is a separately reviewed assertion requiring all acceptance gates. Never auto-promote a run because JSON or CSV files exist.
