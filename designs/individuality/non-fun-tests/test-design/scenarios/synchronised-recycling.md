# Synchronised recycling (Draft)

Many coins reach the forced recycling age at the same time. This loads the recycling flow: one recycler load per coin, then ring builds for the new vouchers.

**User flow:** [Recycling](../../coinage/user-flows.md#recycling)

**Runtime path:** [Coin consumption, recycler loading and later Members OCW calls](../../coinage/pallet-components.md#recycler-load-ring-readiness-and-unload). This is distinct from [expired-state cleanup](../../coinage/pallet-components.md#ocw-cleanup-and-archive-recovery).

| Part | This scenario |
| ---- | ------------- |
| **Source** | A population whose coins age together. |
| **Stimulus** | Many coins reach the forced recycling age in the same evaluation window. |
| **Environment** | Performance: planned recycling rate. Stress: ramp the number of coins due at once. Policy: [recycling-unavailable handling](../../coinage/production-policies.md#recycling-unavailable-handling). Android and iOS differ, so each run selects one. |
| **Artifacts** | C2.recycle, R1.calls, R2.origins, R3.rings, R6.pots (sponsored instances), R7.recyclers, N1.pool. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | Each due coin is loaded into a recycler and its voucher joins a ring. |
| **Response measure** | Recycle loads included; ring build lag; time until the new vouchers are usable. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).
