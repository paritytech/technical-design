# Top-up burst (Draft)

Many actors top up at the same time. This loads the onboarding flow: each top-up becomes voucher loads, and the chain must add every new voucher to a ring.

**User flow:** [Top-up / Onboarding](../../coinage/user-flows.md#top-up--onboarding)

**Runtime path:** [Recycler loading and member-ring construction](../../coinage/pallet-components.md#recycler-load-ring-readiness-and-unload). A sponsored instance also uses [load-deposit accounting](../../coinage/pallet-components.md#instances-and-sponsored-deposits).

| Part | This scenario |
| ---- | ------------- |
| **Source** | A population of actors whose top-up trigger fires together. |
| **Stimulus** | Each actor tops up its target amount at the same moment. |
| **Environment** | Performance: planned load. Stress: ramp the number of simultaneous top-ups. Policy: [top-up composition](../../coinage/production-policies.md#top-up-composition) (Android and iOS agree). Select the submission shape: iOS batches loads, Android sends one load per voucher. |
| **Artifacts** | C2.topup, C4.requests, R1.calls, R2.origins, R3.rings, R6.pots (sponsored instances), R7.recyclers, N1.pool. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | Loads are included and finalised. New vouchers join a built ring revision. |
| **Response measure** | Loads finalised versus submitted; pool rejections by reason; time until the new vouchers are in a built ring revision. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).
