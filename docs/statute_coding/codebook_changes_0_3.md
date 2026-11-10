# Codebook 0.3.0 changes

These are descriptive mechanisms, not scores. Read `coded_value` together with `provision_status`, the education scope, English interpretation and exceptions. A candidate code with status `unclear` is not an established provincial rule.

The 0.2.0 permitted categories are retained. Earlier 96 decisions and 213 evidence records are unchanged apart from the shared codebook-version field. New categories below were introduced by the remaining-jurisdiction draft; they require team adjudication and any resulting back-application.

| Indicator | Added category | Interpretation |
| --- | --- | --- |
| AS02 | `appointment_after_transfer_priority` | Statutory transfer priority followed by direct appointment when transfer requests are absent; not assumed to be a ranked public competition. |
| AS02 | `ranked_credentials_with_exam` | Examination is explicitly required alongside the ranked credential/antecedent process in the coded scope. |
| AS04 | `appraisal_cessation_without_sumario` | Supplied text expressly allows cessation on a confirmed deficient appraisal without a disciplinary sumario; do not infer current enforceability. |
| PR01 | `competition_exam_or_promotion_course` | Opposition or an approved promotion course are express alternatives. |
| PR01 | `competition_with_promotion_course` | A promotion course is part of the prescribed route; it is not automatically classified as opposition. |
| PR01 | `competition_conditional_exam` | Whether opposition is required varies by post, category or route. Preserve the stated distinction. |
| PR01 | `competition_external_rules` | Competition is prescribed, but its procedure depends on an external framework not fully supplied. |
| PR04 | `attendance_additional_external_conditions` | A monetary attendance-related addition is explicit, but its creation, amount or complete eligibility rules are in other instruments. |
| MP01 | `annual_appraisal_suspended_or_mixed` | Annual appraisal clauses and suspension annotations coexist; the applicable mechanism is unresolved. |
| MP02 | `appraisal_rule_suspended` | The supplied compilation marks an appraisal/ranking provision suspended; its operative replacement is not established. |
| AS03, AS04, PR04, MP01, MP03, CT02 | `insufficient_documentation` | The supplied source set does not settle the mechanism. Use status `unclear`, explain the gap and obtain the missing instrument. |

The distinction between a leadership course, opposition, training ranking points, appraisal and attendance-based cash remuneration is preserved. Specific numeric schedules and thresholds remain in text rather than being compressed into a misleading province-level scalar.

Any coding of an additional education branch requires a separate case. National reference clauses require a provincial applicability link; this is unresolved for most Neuquén/Río Negro baseline rows. La Rioja secondary/higher is not used to fill a missing primary case.
