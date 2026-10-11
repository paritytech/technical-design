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

## Pilot: voucher unloads to the external asset

**Question:** When many people cash out at once, does every requested amount reach its external account, and does the instance backing fall by exactly that much?

Both apps offboard through recycler unloads with free tokens, never through `direct_offboard_coin_into_external_asset` ([offboarding selection](../../coinage/production-policies.md#offboarding-inventory-selection)). Each stage below follows one branch of that flow. Run them in order, each on fresh state, at 100, 1,000 and 10,000 actors on the default pool.

| Stage | Inventory per actor | Calls | What it adds |
| ----- | ------------------- | ----- | ------------ |
| A. Vouchers cover the amount | One exponent-`1` voucher in a built ring | One `unload_recycler_into_external_asset` with one alias, `max_fee = 0` ([call][unload-external]) | The basic exit path |
| B. Surplus | One exponent-`2` voucher; offboard half of it | One `unload_recycler_into_external_asset_and_loaded_coins` that releases the exponent-`1` amount and loads an exponent-`1` surplus voucher ([call][unload-surplus]) | New ring work during the exit |
| C. Coins first | Two exponent-`1` coins, no vouchers | Two `load_recycler_with_coin`, then one unload per ring the two vouchers landed in (one call if they share a ring) | Recycling, then unloading |
| D. Above `MaxConsolidation` | 65 exponent-`0` vouchers in one recycler | iOS shape: two calls of at most 64 aliases. Android shape: one call with 65 aliases | The platform difference |

All stages use the [shared unload fixture](../unload-fixture.md), with one free token per call. Stage D runs at 100 actors only, because each actor needs 65 vouchers.

**Required evidence and checks:**

- The fixture's [unload checks](../unload-fixture.md#checks-for-every-unload) with the stage's call event: `RecyclerUnloadedIntoExternalAsset` or `RecyclerUnloadedIntoExternalAssetAndLoadedCoins`.
- Each external account's asset balance rises by the event's `amount`. The Coinage pallet account's balance of that asset falls by the same total. Report delivered value per actor and in total.
- Stage B: each surplus voucher appears in the recycler collection and reaches ring readiness. Report surplus readiness separately from the exit.
- Stage C: report intent to recycling finality, recycling finality to ring readiness, and readiness to delivered value. Unloading needs ring membership, so it waits for a built ring. The apps start after the coins reach recyclers in the best block, but the chain still needs the built ring before the unload proof is valid.
- Stage D: the iOS shape succeeds in two calls per actor. The Android shape fails to decode, because the alias vector exceeds its bound, and never reaches dispatch. Record how the client learns of that failure.
- Partial offboards: an actor whose value only partly arrived by the deadline.

Stop on wrong value, unresolved receipt, node failure or a 60-second finality stall. A sponsored instance adds deposit settlement on every unload; check it with the [sponsored-instance variant](synchronised-recycling.md#sponsored-instance-variant) checks.

[unload-external]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L2803-L2812
[unload-surplus]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L3131-L3142

## Requested burst campaign

The [remaining-flow campaign](../remaining-flow-campaign.md) specifies six sequential cases for this scenario, from 100 to 20,000 actors, including default-pool, paced and enlarged-pool comparisons. It also defines evidence for recycling-unavailable handling and distinguishes the fixed-plan pilot from the broader scenario above.
