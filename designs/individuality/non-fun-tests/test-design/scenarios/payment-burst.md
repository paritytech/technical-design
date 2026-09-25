# Payment burst (Draft)

Many actors pay at the same time. This loads the send and claim flows together, from the payment plan to the recipient's finalised claims.

**User flows:** [Send](../../coinage/user-flows.md#send) and [Claim](../../coinage/user-flows.md#claim)

**Runtime path:** Split and claim use [coin operations](../../coinage/pallet-components.md#one-coin-transaction-client-to-runtime-and-back); voucher plans use [unload authorization and recycler proofs](../../coinage/pallet-components.md#recycler-load-ring-readiness-and-unload). Exact-coin send has no preparation call.

| Part | This scenario |
| ---- | ------------- |
| **Source** | A population of payers and recipients. |
| **Stimulus** | Each payer sends one payment at the same moment. The inventory gives a mix of exact, split and unload plans. |
| **Environment** | Performance: planned load. Stress: ramp the number of simultaneous payments. Policy: [payment construction](../../coinage/production-policies.md#payment-construction). Android and iOS differ, so each run selects one. |
| **Artifacts** | C2.payment, C3.extrinsics, C4.requests, R1.calls, R2.origins, R7.recyclers, N1.pool. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | Sender preparation lands, memos are delivered and every paid coin is claimed. |
| **Response measure** | Time from payment intent to finalised claim of every coin; partial payments; dropped transactions. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).
