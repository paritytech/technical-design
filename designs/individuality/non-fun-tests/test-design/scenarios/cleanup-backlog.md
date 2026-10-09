# Cleanup backlog (Draft)

A large amount of expired state needs cleaning while users keep transacting. Offchain workers submit the cleanup calls, and those calls share the pool and the block with user transactions.

**User flow:** none directly. This is background work caused by earlier flows.

**Runtime path:** [OCW cleanup and archive recovery](../../coinage/pallet-components.md#ocw-cleanup-and-archive-recovery). The Coinage OCW runs every 4 blocks in this runtime ([config][ocw-interval]). The Members OCW runs every block.

| Part | This scenario |
| ---- | ------------- |
| **Source** | Expired state left by earlier activity: consumed free tokens from past periods and expired recycler rings. |
| **Stimulus** | A large backlog of eligible cleanup work, while a steady user load runs. |
| **Environment** | Performance: a normal daily backlog with planned user load. Stress: ramp the backlog size. |
| **Artifacts** | R4.cleanup, R3.rings, R6.pots, R7.recyclers, N1.pool, N2.execution, N3.storage. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | The workers drain the backlog in bounded calls. User transactions keep their latency. Value in expired recyclers stays recoverable. |
| **Response measure** | Backlog size over time; time to drain; cleanup calls per block and their share of block weight; user latency against a no-backlog baseline; archived value recovered. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).

## Pilot: seeded expired state under a steady claim load

**Question:** Does a large cleanup backlog drain without slowing user transactions or losing value?

The network uses the real clock, and recyclers expire 90 days after they become immutable ([config][expiry]). The pilot cannot wait that long, so it seeds expired state with root `System.set_storage`, encoded against the run's metadata. Before measuring, check that the workers actually propose cleanup calls for the seeded state. Seeded state stands in for history; it is not history produced by real use.

| Backlog | How it is seeded | Cleanup calls |
| ------- | ---------------- | ------------- |
| Consumed free tokens | `ConsumedFreeUnloadTokens` entries in past periods: 10,000, then 100,000 | `clean_consumed_free_token(period)`, at most 1,000 entries per call ([limit][token-limit]) |
| Expired recyclers | Fill and build real recycler rings with loads, unload part of each ring, then move each ring's `immutable_since` back by more than 90 days | `clean_recycler`, then dust cleanup and Members ring-page deletion |

| Setting | Pilot |
| ------- | ----- |
| Network | Same as the claim burst, with real Coinage and Members OCWs and the default pool. |
| User load | A steady claim stream at a fixed rate the claim burst has shown the network can sustain, starting 10 minutes before the backlog appears. The first 10 minutes are the baseline. |
| Observation | Until the backlog is empty, or 60 minutes. |

**Required evidence and checks:**

- Remaining backlog every block, per backlog type.
- Every cleanup call: block, weight and how long it waited from proposal to inclusion.
- Claim latency before, during and after cleanup, at p50, p95 and max. Also why block authoring stopped in each block.
- The Coinage OCW checks only the last 10 expired periods for consumed tokens. Seed some entries older than that, and report whether they are ever removed.
- Expired recyclers with unspent vouchers are archived, not deleted. For a sample of 10 unspent vouchers, recover the value with `unload_archived_recycler_into_external_asset` and check the amount received.
- Sponsored instances: cleanup settles the remaining load deposits. Check the pot before and after.

Cleanup calls only accept local or in-block sources, so the load generator cannot submit them. It can only seed the state and observe the workers.

[ocw-interval]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/runtimes/next-people-paseo/src/people.rs#L1690
[expiry]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/runtimes/next-people-paseo/src/people.rs#L1671
[token-limit]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L170-L173
