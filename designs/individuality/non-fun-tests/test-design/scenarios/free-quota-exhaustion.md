# Free-quota exhaustion (Draft)

Unload demand exceeds the free unload allowance. This tests what the wallet and the chain do when free unloads run out.

**User flows:** [Send with voucher unloads](../../coinage/user-flows.md#send) and [Offboarding](../../coinage/user-flows.md#offboarding)

**Runtime path:** [Free unload-token validation](../../coinage/pallet-components.md#recycler-load-ring-readiness-and-unload). A recycler load does not consume an unload token. The [recycling policy](../../coinage/production-policies.md#recycling-unavailable-handling) can react to low allowance, but that is a separate wallet decision. Period rollover permits new tokens within the allowance; cleanup only removes old consumed-token records.

| Part | This scenario |
| ---- | ------------- |
| **Source** | Actors whose unload demand exceeds their free allowance for the period. |
| **Stimulus** | Unload requests continue after the free allowance is used up. |
| **Environment** | Performance: not applicable. Stress: ramp free-token unload demand past the allowance. Use one platform's [payment construction](../../coinage/production-policies.md#payment-construction) and [offboarding selection](../../coinage/production-policies.md#offboarding-inventory-selection) policies. |
| **Artifacts** | C2.payment, C2.offboard, R2.origins, N1.pool. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | The wallet reacts as its policy defines. Submitted free-token requests outside the allowance are rejected during validation. |
| **Response measure** | Requests withheld by the wallet versus submitted; validation rejections by reason; recovery with valid tokens in the next period. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).
