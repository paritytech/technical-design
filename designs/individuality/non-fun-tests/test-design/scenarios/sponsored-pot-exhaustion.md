# Sponsored-pot exhaustion (Draft)

Loads into a sponsored instance run out of pot collateral. Every voucher loaded into a sponsored instance holds a deposit from the instance's pot. This tests what happens when more loads arrive than the pot can cover.

**User flows:** [Top-up / Onboarding](../../coinage/user-flows.md#top-up--onboarding) and [Recycling](../../coinage/user-flows.md#recycling) on a sponsored instance

**Runtime path:** [Instances and sponsored deposits](../../coinage/pallet-components.md#instances-and-sponsored-deposits). The pot check runs in transaction validation and again when the block applies the call. Unloads and recycler cleanup release deposits.

| Part | This scenario |
| ---- | ------------- |
| **Source** | Actors loading vouchers into one sponsored instance, and the sponsor who funds its pot. |
| **Stimulus** | Load demand exceeds the deposits the pot can hold. |
| **Environment** | Performance: not applicable. Stress: ramp loads past the pot's capacity, then fund the pot or release deposits. |
| **Artifacts** | R1.calls, R2.origins, R6.pots, R7.recyclers, N1.pool. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | Loads the pot can cover succeed. The rest are rejected with a clear reason. Loads work again after funding or unloads. |
| **Response measure** | Loads accepted versus the pot's capacity; rejections by reason and stage; loads the client saw as ready that never landed; time to recover after funding. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).

## Pilot: overfill one pot

**Question:** If a pot can cover K deposits and 2K loads arrive at once, do exactly K succeed, and does every other load fail visibly?

The pot check uses `can_hold` at validation ([check][pot-check]) and does not reserve anything. Many loads can pass pool validation against the same pot balance. The block then applies them one by one, and the later ones fail. This pilot finds where they fail and whether the client is told.

| Setting | Pilot |
| ------- | ----- |
| Network | Same as the top-up burst, with real Members OCWs and the default pool. |
| Instance | One instance from `create_sponsored_instance`, a signed call that the runtime currently allows for any account ([call][sponsored-create]). Fund it with `fund_pot` ([call][fund-pot]) for exactly K deposits. The deposit per key is `CoinageLoadDeposit`, 7 native units in this runtime ([config][load-deposit]); read it at the starting block. |
| Load | K = 100, then 1,000. Each stage submits 2K single-voucher top-ups (`load_recycler_with_external_asset_unpaid`) at once, from 2K funded accounts. |
| Recovery | After the burst settles, fund the pot for K more deposits and resubmit the rejected loads. Then unload 100 of the loaded vouchers with the [shared unload fixture](../unload-fixture.md) and submit 100 new loads. |

**Expected results and checks:**

- Exactly K loads succeed with `RecyclerLoadedWithExternalAsset` and `LoadDepositsHeld`. The pot's held balance equals K deposits.
- Every other load ends with a known reason. Count each of: rejected at pool entry with `PotCannotCoverLoadDeposit`, accepted into the pool and later dropped as invalid, and included but failed in dispatch.
- Any load the client saw as "ready" that never landed and was never reported as failed is a silent result and fails the pilot.
- No actor is debited for a load that failed. Check every actor's asset balance.
- After funding, resubmitted loads succeed up to the new capacity. After the unloads, each unload releases its deposit ([settlement][settle-deposits]) and the same number of new loads succeed.

Batched loads (`load_recycler_with_external_asset_unpaid_batch`, up to 10 items) charge deposits for the whole batch at once. Run a batch variant only after the single-load stages pass.

[pot-check]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/pot.rs#L330-L345
[sponsored-create]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L3784-L3789
[fund-pot]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L3842-L3850
[load-deposit]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/runtimes/next-people-paseo/src/people.rs#L1638-L1639
[settle-deposits]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/pot.rs#L427
