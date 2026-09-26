# Offboarding burst (Draft)

Many actors offboard to the external asset at the same time. This loads the offboarding flow: voucher unloads into the external asset, after any coins are recycled first.

**User flow:** [Offboarding](../../coinage/user-flows.md#offboarding)

**Runtime path:** [Unload authorization, recycler proofs and external-asset release](../../coinage/pallet-components.md#recycler-load-ring-readiness-and-unload). Coin recycling may precede unloading; surplus vouchers can require later ring work. This draft follows app offboarding, not the direct-coin or archived-recovery calls.

| Part | This scenario |
| ---- | ------------- |
| **Source** | A population of actors who cash out together. |
| **Stimulus** | Each actor offboards an amount at the same moment. |
| **Environment** | Performance: planned load. Stress: ramp the number of simultaneous offboards. Policy: [offboarding inventory selection](../../coinage/production-policies.md#offboarding-inventory-selection). Select a platform when one recycler contributes more than `MaxConsolidation` vouchers. |
| **Artifacts** | C2.offboard, R1.calls, R2.origins, R7.recyclers, N1.pool. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | The requested value reaches each external account. |
| **Response measure** | Value delivered to external accounts; partial offboards; unload throughput. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).
