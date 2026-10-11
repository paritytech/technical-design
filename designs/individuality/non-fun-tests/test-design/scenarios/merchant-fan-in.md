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

## Pilot: one merchant claims a stream of payments

**Question:** When payments to one merchant arrive faster than its wallet can settle them, does the backlog stay bounded, and does it drain?

On chain, each claim is independent: every received coin moves to a fresh merchant key, so the runtime has no shared merchant record to contend on. What differs from [claim burst](claim-burst.md) is the client side. One wallet watches and submits every claim, so its connections, subscriptions and detection passes become the limit. This pilot measures that.

| Setting | Pilot |
| ------- | ----- |
| Network | Same as the claim burst: six relay validators, two People collators, zero added delay, default pool. Record `--rpc-max-connections` and `--rpc-max-subscriptions-per-connection`. The current network sets 1,024 and 20,050. |
| Fixture | Root-seeded payment coins as in the claim burst, one per incoming payment, with exponent `1` and age `0`. They stand for coins the payers have already handed over. |
| Merchant | One submitter process with a fixed number of RPC connections. Start with one connection, then four. Every claim targets a fresh merchant key. |
| Arrival | Memos arrive at a constant rate for 10 minutes. Steps: 10, 50, 100, 200, 400 and 800 payments per second, each on fresh state. Stop at the first failing step. |
| Claiming | Claim the way the apps do: when a memo arrives, claim the coins already visible, one `transfer` per coin. Group claims that arrive within one detection pass. A pass waits at most 30 seconds. |

**Required evidence and checks:**

- Per claim: memo arrival to submission, submission to finality, and memo arrival to finality. Report p50, p95 and max for each step.
- The merchant's backlog over time: memos received but not yet submitted, and claims submitted but not yet final. Sample every second.
- Claims still unsettled when arrivals stop, and the time until the backlog reaches zero.
- Every claim verified as in the claim burst: `Coinage.CoinTransferred`, the source absent and the merchant key holding the coin at age `1`.
- Merchant process CPU and memory, open subscriptions per connection and any RPC errors, such as subscription or connection limits.
- At the end, count the merchant's coins, by denomination and age. A merchant ends with many small coins, which feeds later recycling and offboarding load.

A step fails if any claim is lost or wrong, if the backlog is still growing when arrivals stop, or if it has not drained 10 minutes after arrivals stop. A failure caused by the submitter, such as hitting a subscription limit, is a client result. Report it as that, not as a chain limit.

The [claim burst](claim-burst.md) already gives the chain-side reference at the same sizes. Compare the merchant's finality with it to separate client delay from chain delay.

## Requested burst campaign

The [remaining-flow campaign](../remaining-flow-campaign.md) specifies six sequential cases for this scenario, from 100 to 20,000 actors, including default-pool, paced and enlarged-pool comparisons. It also defines evidence for recycling-unavailable handling and distinguishes the fixed-plan pilot from the broader scenario above.
