# Merchant fan-in (Draft)

One recipient receives many payments. Each received coin needs its own claim transaction, so claims pile up on one wallet.

**User flow:** [Claim](../../coinage/user-flows.md#claim)

**Runtime path:** [Coin authorization, transfer and owner-keyed storage](../../coinage/pallet-components.md#one-coin-transaction-client-to-runtime-and-back). Each claim targets a fresh coin key; the runtime does not append all merchant coins to one account record.

| Part | This scenario |
| ---- | ------------- |
| **Source** | Many payers and one merchant recipient. |
| **Stimulus** | Many payments arrive at the merchant in a short window. |
| **Environment** | Performance: planned merchant load. Stress: ramp the payment arrival rate. |
| **Artifacts** | C4.requests, R1.calls, R2.origins, N1.pool, N3.storage. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | The merchant claims every received coin with one transfer per coin. |
| **Response measure** | Claim latency; claims still unsettled when the burst stops; time to drain. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).
