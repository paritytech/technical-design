# Free-quota exhaustion (Draft)

Unload demand exceeds the free unload allowance. This tests what the wallet and the chain do when free unloads run out.

**User flow:** [Recycling](../../coinage/user-flows.md#recycling)

| Part | This scenario |
| ---- | ------------- |
| **Source** | Actors whose unload demand exceeds their free allowance for the period. |
| **Stimulus** | Unload requests continue after the free allowance is used up. |
| **Environment** | Performance: not applicable. Stress: ramp unload demand past the allowance. Policy: [recycling-unavailable handling](../../coinage/production-policies.md#recycling-unavailable-handling). Android and iOS differ, so each run selects one. |
| **Artifacts** | C2.recycle, R2.origins, R4.cleanup. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | The wallet reacts as its policy defines. Unloads fail until a free token is available again. |
| **Response measure** | Wallet behaviour when the quota runs out; failed unloads; recovery in the next period. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).
