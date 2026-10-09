# Free-quota exhaustion (Draft)

Unload demand exceeds the free unload allowance. This tests what the wallet and the chain do when free unloads run out.

**User flows:** [Send with voucher unloads](../../coinage/user-flows.md#send) and [Offboarding](../../coinage/user-flows.md#offboarding)

**Runtime path:** [Free unload-token validation](../../coinage/pallet-components.md#recycler-load-ring-readiness-and-unload). A recycler load does not consume an unload token. The [recycling policy](../../coinage/production-policies.md#recycling-unavailable-handling) can react to low allowance, but that is a separate wallet decision. Period rollover permits new tokens within the allowance; cleanup only removes old consumed-token records.

| Part | This scenario |
| ---- | ------------- |
| **Source** | Actors whose unload demand exceeds their free allowance for the period. |
| **Stimulus** | Unload requests continue after the free allowance is used up. |
| **Environment** | Performance: not applicable. Stress: ramp free-token unload demand past the allowance. Use one platform's [payment construction](../../coinage/production-policies.md#payment-construction) and [offboarding selection](../../coinage/production-policies.md#offboarding-inventory-selection) policies. |
| **Artifacts** | C2.payment, C2.offboard, R2.origins, N1.pool. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | The wallet reacts as its policy defines. Submitted free-token requests outside the allowance are rejected during validation. |
| **Response measure** | Requests withheld by the wallet versus submitted; validation rejections by reason; recovery with valid tokens in the next period. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).

## Pilot: free-token exhaustion and period rollover

**Question:** When people use up their free unloads, are the extra requests rejected cleanly at validation, and do unloads work again in the next period?

The chain side is defined exactly, so this pilot tests it first with a fixed plan. The wallet side follows in the [policy variant](#policy-variant).

**How the allowance works** (re-read at the starting block):

- Each person may use counters `0` to `limit - 1` in each one-day period. A counter at or above the limit fails validation with `UnloadTokenCounterOutOfRange` ([validation][token-validate]).
- `limit = min(allowance / unload fee, 1000)`. The People allowance is 20 native units and the LitePeople allowance is 10 ([config][allowance]). Read both limits with the `Coinage.get_free_unload_token_info` view.
- The unload fee follows the transaction fee multiplier. Under congestion the fee rises and the limit falls, so a counter that was valid at the start of a burst can become invalid during it.
- Validation accepts the previous period for one hour after a boundary.

| Setting | Pilot |
| ------- | ----- |
| Network and people | The [shared unload fixture](../unload-fixture.md) with 10 people, then 100. Read the limit `L` at the starting block. |
| Inventory | Per person, `L + E` exponent-`1` vouchers in built rings, where `E = max(5, L / 10)`. Each person also keeps 5 counters unused for the rollover stage. |
| Exhaustion stage | Each person submits unloads for counters `0` to `L + E - 1`, except the 5 kept back, all at once. Use `unload_recycler_into_coin` with one alias each, into fresh keys. |
| Duplicate stage | For 100 tokens, submit two unloads that use the same `(person, period, counter)` with different vouchers. |
| Rollover stage | Schedule the run so the exhaustion stage ends at least 15 minutes before 00:00 UTC. In the first hour after the boundary, submit the 5 kept-back counters from the old period, plus the `E` rejected unloads with new-period counters. One hour after the boundary, submit one more old-period token per person. |

**Expected results and checks:**

- Exhaustion: per person, every counter below the limit succeeds and every counter at or above it is rejected with `UnloadTokenCounterOutOfRange`. None of the rejected calls reaches a block. Sample the limit every block during the stage. If it changes, report the counters affected.
- Duplicates: at most one unload per token reaches a block, because both transactions provide the same pool tag. Record whether the second one was rejected at entry, replaced or dropped, and whether its client was told.
- Rollover: kept-back old-period tokens succeed inside the grace hour. New-period tokens succeed. Old-period tokens after the grace hour fail with `InvalidUnloadTokenPeriod`.
- Any free token consumed by a failed dispatch is reported separately; it is not refunded.
- The fixture's [unload checks](../unload-fixture.md#checks-for-every-unload) for every successful unload, with `Coinage.RecyclerUnloadedIntoCoin` and an output coin at age `0`.

A silent result fails the pilot. Examples: a client that saw "ready" for a token that never reached a block and got no error, or a token counted as consumed with no successful unload.

## Policy variant

The production wallets react before the allowance runs out. When remaining free unloads fall to 20% of the allowance, both wallets stop discretionary recycling. Coins at the forced age are still loaded, because loading consumes no token. Once tokens run out, their unloads fail ([recycling-unavailable handling](../../coinage/production-policies.md#recycling-unavailable-handling)).

Run the same population through the wallet module, with one platform selected for `wallet.recycling.unavailable_handling` and `wallet.payment_construction`. Drive payment and offboarding intents until each person passes the reserve and then the limit. Report:

- operations withheld by the wallet versus submitted, before and after the reserve;
- forced-age loads that still happen after the reserve;
- unload attempts after exhaustion and how they fail;
- recovery in the next period.

The platforms differ here. Android counts only the current period and treats a failed allowance read as "not low". iOS also counts the previous period inside its one-hour lookback and aborts the evaluation when the read fails.

[token-validate]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/extension.rs#L452-L482
[allowance]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/runtimes/next-people-paseo/src/people.rs#L1672-L1682

## Requested burst campaign

The [remaining-flow campaign](../remaining-flow-campaign.md) specifies six sequential cases for this scenario, from 100 to 20,000 actors, including default-pool, paced and enlarged-pool comparisons. It also defines evidence for recycling-unavailable handling and distinguishes the fixed-plan pilot from the broader scenario above.
