# Production policy implementations

This file documents the production implementation of each Wallet policy listed in the parameter index.

Each entry must describe the implementation and provide a commit-pinned reference to its policy logic.

For execution order and the chain calls these policies produce, see [load paths](load-paths.md#operation-paths).

Production-policy investigation treats the following repos as the authoritative production implementations:
- [Android Community](https://github.com/paritytech/polkadot-android-community)
- [iOS Community](https://github.com/paritytech/polkadot-ios-community)

[Brevity](https://github.com/paritytech/brevity-dozer) is not treated as production evidence. When its behaviour matches both production applications, it will be documented as a supporting implementation and considered for reuse by the test harness.

## Top-up Composition

**Policy key:** `inventory.top_up.composition`

**Production status:** Confirmed — Android Community and iOS Community agree.

**Behaviour:**
During underlying-asset onboarding, the wallet processes the runtime-supported denominations from largest to smallest. It takes each denomination repeatedly while it fits into the remaining value and creates one recycler voucher for every selected denomination.

Valid profile-generated top-ups are whole-cent values and are expected to be represented completely. If a non-representable value is encountered, the wallet loads the largest representable value that does not exceed it and leaves the sub-denomination remainder in the underlying asset. A zero value produces no vouchers.

| Implementation | Agreement | Proof |
|---|---|---|
| Android Community | Production implementation; greedy largest-first decomposition with round-down support. | [policy](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/common/RealCoinAmountBreakdownContext.kt#L17-L43) |
| iOS Community | Production implementation; same composition, with any remainder omitted from the result. | [policy](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Denomination/Denomination.swift#L57-L72) |
| Brevity | Supporting implementation; matches the production policy and exposes the remainder explicitly. | [policy](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/denomination.rs#L68-L89) |

**Verified against:**

- Android Community commit `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community commit `b960f771049c07819de1f201b901b037613d42e9`;
- Brevity commit `0fb3fa214c8abeb7a33a7db0db60c257ea069c8e`.

## Payment Construction

**Policy key:** `wallet.payment_construction`

**Production status:** Confirmed — Android Community and iOS Community implement the same strategy ladder but differ in split-coin and voucher selection.

**Behaviour:**

Both production wallets evaluate these strategies in order and use the first one that can cover the payment:

1. **Exact coins.** Select an exact value using the largest denominations first and the oldest coin within each denomination. The selected coins pass whole to the recipient without a sender-side split or unload transaction.
2. **Split.** Pass zero or more coins whole and split one larger coin into recipient denominations and change.
3. **Unload and split.** Pass selected coins whole and cover the remainder by unloading recycler vouchers. Vouchers are grouped by denomination and recycler, and every unload call produces recipient and change denominations whose total equals its voucher input.

Both wallets first plan using immediately spendable assets. If those cannot cover the payment, they retry with privacy-held assets when the active recycling policy permits confirmed spending. Coins at or beyond the wallet's hard spend-age cutoff are excluded from both attempts.

The production implementations diverge as follows:

| Decision                                           | Android Community                                                                                                                       | iOS Community                                                                                                                                                     |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Split coin](examples/split-coin-selection.md)     | Takes a largest-first prefix of whole coins, then splits the smallest unselected coin larger than the remainder.                        | If one coin exceeds the whole payment, splits the smallest such coin alone; otherwise splits the coin at which a largest-first running total reaches the payment. |
| [Voucher selection](examples/voucher-selection.md) | Groups vouchers by denomination and recycler, orders groups by total value descending, then takes vouchers in that order until covered. | Takes the smallest single voucher that covers the remainder; if none does, takes vouchers largest-first until covered.                                            |

| Implementation | Finding | Proof |
|---|---|---|
| Android Community | Production variant. | [policy](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/TransferPlanner.kt#L23-L183) |
| iOS Community | Production variant. | [policy](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/CoinSelection/CoinSelector.swift#L34-L357) |
| Brevity | Comparison only. It follows iOS for split and voucher selection. | [policy](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/selection.rs#L95-L340) |

**Required selection:** Every test scenario must explicitly select either the Android Community or iOS Community production variant. There is no default.

**Verified against:**
- Android Community commit `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community commit `b960f771049c07819de1f201b901b037613d42e9`;
- Brevity commit `0fb3fa214c8abeb7a33a7db0db60c257ea069c8e`.

## Recycle Output Composition

**Policy key:** `wallet.recycling.output_composition`

**Production status:** Confirmed — Android Community and iOS Community use the same greedy denomination composition during payment construction. Neither uses the runtime's dedicated single-coin consolidation call or unloads vouchers solely to reshape its own inventory. They differ in handling compositions that exceed the runtime output limit.

**Behaviour:**

Composition occurs when vouchers are unloaded from a recycler.

An unload operation can combine vouchers only when they have the same denomination and recycler index. For `n` vouchers of denomination `2^k`, the value available to that operation is `n × 2^k`.

The runtime provides two ways to turn that value into coins:

1. **Single-coin consolidation.** `unload_recycler_into_coin` accepts a power-of-two number of vouchers and creates one coin of denomination `2^(k + log₂(n))`. The denomination must not exceed the runtime maximum. The resulting coin has age `0`.
2. **General output composition.** `unload_recycler_into_coins` accepts up to `MaxConsolidation` vouchers and a wallet-generated `split_into` composition. It can produce any protocol-valid collection of supported denominations, subject to `MaxSplitOutputs`. The resulting coins have age `1`.

With a prepaid unload token, output value must equal the complete voucher input value. When the fee is taken from the output, output value plus the reserved fee must equal the voucher input value.

Both production wallets use the general operation as part of Payment Construction:

1. group selected vouchers by denomination and recycler index;
2. divide each group according to `MaxConsolidation`;
3. allocate each group's value between recipient value and sender change;
4. greedily decompose each allocation from the largest supported denomination downward;
5. submit the resulting denominations and destination keys as `split_into`.

This can consolidate vouchers into a greater denomination. For example, two `32¢` vouchers from the same recycler can produce one `64¢` coin. Two `32¢` vouchers from different recyclers require separate unload calls and therefore produce at least one output from each `32¢` budget.

| Decision | Android Community | iOS Community |
|---|---|---|
| Denomination composition | Greedy largest-first decomposition, applied separately to recipient value and change. | Same. |
| Too many voucher inputs | Divides recycler groups according to `MaxConsolidation`. | Same. |
| Too many output coins | No explicit `MaxSplitOutputs` replanning was found; an oversized composition may reach runtime rejection. | Repeatedly divides a multi-voucher group until each call fits `MaxSplitOutputs`; reports failure if one voucher alone cannot fit. |
| Dedicated single-coin consolidation | Not used. | Not used. |
| Standalone inventory reshaping | Not performed. Vouchers are unloaded when needed by Payment Construction. | Same. |

| Implementation | Finding | Proof |
|---|---|---|
| Runtime | Supports both power-of-two single-coin consolidation and arbitrary valid `split_into` composition. | [single-coin consolidation](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L2806-L2875), [general composition](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3596-L3761) |
| Android Community | Production variant; greedy per-batch composition without explicit output-limit replanning. | [policy](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/strategies/VoucherBatchDistribution.kt#L32-L60) |
| iOS Community | Production variant; greedy per-batch composition with output-limit replanning. | [policy](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/CoinSelection/CoinSelector.swift#L214-L300) |
| Brevity | Comparison only; uses greedy per-recycler recipient/change composition. | [policy](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/selection.rs#L286-L365) |

**Required selection:** Scenarios exercising recycler output composition must select the Android Community or iOS Community variant. When composition is reached through Payment Construction, it should normally use the same platform variant selected for that policy.

**Verified against:**

- Coinage pallet commit `b5951a9784bdcc87539b793ed686fa6ae93f99ab`;
- Android Community commit `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community commit `b960f771049c07819de1f201b901b037613d42e9`;
- Brevity commit `0fb3fa214c8abeb7a33a7db0db60c257ea069c8e`.

## Recycling-Unavailable Handling

**Policy key:** `wallet.recycling.unavailable_handling`

**Production status:** Confirmed — Android Community and iOS Community share the same normal response: retain discretionary recycling candidates as spendable coins and provide no paid-unload fallback. They differ in allowance-read failure, allowance-period accounting, and how they obtain the forced-recycling threshold.

**Behaviour:**

The production wallets do not directly evaluate `privacy.recycling.paid_fee_limit`. They construct unloads only with free prepaid tokens and do not implement either paid-token or fee-from-output fallback. Their `max_fee = 0` call argument is part of that prepaid construction and, for unload-into-coins, is required by the runtime; it does not encode an actor fee preference.

Both wallets also apply a preventive quota reserve before the [Preferred Recycling Unavailable](runtime-conditions.md#preferred-recycling-unavailable) condition is satisfied:

1. When remaining free unloads are at or below 20% of the applicable allowance, discretionary recycling verdicts from the privacy preset are discarded.
2. A coin below the wallet's forced-recycling threshold is retained as `ALLOW_USE`, remains spendable, and can become a recycling candidate again after a later evaluation observes sufficient allowance. The wallet neither offboards it nor attempts a paid unload.
3. A coin at or above the forced-recycling threshold is still marked `MUST_RECYCLE` and loaded into a recycler because loading consumes no unload token.
4. Engaging the reserve does not prevent voucher unloading while valid free tokens remain. Only complete exhaustion satisfies the free-allowance part of Preferred Recycling Unavailable and causes production unload attempts to fail.
5. At complete exhaustion, a forced coin can still become a voucher, but neither production wallet can unload that voucher until a valid free token becomes available.

The forced-recycling threshold is currently `MaximumAge - 2`. It is distinct from the runtime's `MaximumAge` rejection threshold. The runtime rejects transfer and split at `age >= MaximumAge`, but recycler loading has no coin-age check.

Brevity is comparison only. It has no preventive quota valve: it recycles available coins at `age >= 14` and resolves free tokens only when unloading.

| Decision | Android Community | iOS Community |
|---|---|---|
| Allowance read fails | Treats the allowance as not low and continues to apply the privacy preset. | Aborts that complete evaluation; no recycling starts from it, and the previously published verdict remains. |
| Allowance periods | Counts the current period only. | Counts the periods selected by its one-hour lookback: normally the current period, plus the preceding period when the grace window crosses a boundary. |
| Forced-recycling threshold | Reads `MaximumAge` from the runtime, subtracts two, and falls back to `14` if the read fails. | Uses the hard-coded value `16 - 2 = 14`. |

| Implementation | Finding | Proof |
|---|---|---|
| Android Community | Production variant; a quota decorator suppresses discretionary recycling and an outer age guard forces old coins. | [policy](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/EnsureQuotaLimitsStrategy.kt#L11-L39) |
| iOS Community | Production variant; applies the same reserve and forced-age structure. | [policy](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Recycling/Strategy/RecyclingStrategyProvider.swift#L21-L64) |
| Brevity | Comparison only; no reserve valve and no paid fallback. | [policy](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/recycling.rs#L130-L146) |
| Runtime | Loading has no age restriction. Unloading supports free or paid prepaid tokens and fee-from-output; paid tokens can be funded with a coin, native currency, or an underlying asset. | [fee modes](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L1310-L1334) |

Detailed worked states and line-level proof: [Recycling-unavailable handling](examples/recycling-unavailable-handling.md).

**Required selection:** Every scenario resolving this policy must explicitly select either the Android Community or iOS Community production variant. There is no default.

**Verified against:**

- Android Community commit `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community commit `b960f771049c07819de1f201b901b037613d42e9`;
- Brevity commit `0fb3fa214c8abeb7a33a7db0db60c257ea069c8e`;
- Coinage pallet commit `b5951a9784bdcc87539b793ed686fa6ae93f99ab`.

## Offboarding Inventory Selection

**Policy key:** `wallet.offboarding.inventory_selection`

**Production status:** Confirmed — Android Community and iOS Community implement the same denomination-level inventory selection. Their external-payment execution differs when a recycler contributes more than `MaxConsolidation` vouchers: iOS chunks the recycler into several calls, while Android builds one oversized call whose bounded alias and proof vectors fail runtime decoding before pallet dispatch.

**Behaviour:**

The production wallets implement offboarding through their external-payment flow. In that flow, value leaves Coinage through recycler vouchers. The runtime's `direct_offboard_coin_into_external_asset` call bypasses the recycler, but neither production wallet calls it.

1. **Vouchers before coins.** The planner first tries locally tracked, free, in-recycler vouchers that the active recycling preset marks usable. If they cover the amount, it takes them largest first until covered. Otherwise it considers all locally tracked, free, in-recycler vouchers, taking usable vouchers first and then gaining-privacy vouchers, largest first within each class. Coins are considered only when those vouchers together fall short.
2. **Coins fill the deficit, then become vouchers.** The deficit is the amount minus the eligible voucher total. Every locally tracked, free, settled coin—on chain with known age—is a candidate regardless of its recycling verdict and even past the spend-age cutoff. Coins are taken largest first until the deficit is covered and are recycled one by one. The payment proceeds after all selected coins have reached recyclers.
3. **After recycling, the usability preference is dropped.** The final pick runs over the pre-existing vouchers plus the fresh ones, largest first, with no preferred set. A gaining-privacy voucher of larger denomination therefore precedes a usable smaller one.
4. **Greedy, no search.** Selection stops at the first prefix that covers the target. Neither wallet searches for an exact cover or minimises surplus.
5. **Surplus returns as vouchers in one call.** The overshoot is broken into denominations largest first and minted as fresh vouchers inside one `unload_recycler_into_external_asset_and_loaded_coins` call. Its host is the first planned unload call whose input value covers the surplus; every other call uses `unload_recycler_into_external_asset`. The implementations contain a defensive no-host error, but it is unreachable for planner-produced selections: the final crossing voucher is itself worth more than the surplus, so its group or chunk can host it.
6. **One unload token per call, `max_fee = 0`.** The wallets use the free-token behavior described under [Recycling-Unavailable Handling](#recycling-unavailable-handling).

Brevity uses the same largest-first progression over ready vouchers and then available coins, but differs in execution: it treats every in-recycler voucher as ready, reschedules when waiting vouchers or coins already recycling would cover the amount, and spreads surplus over the crossing and trailing groups instead of assigning it to one host.

| Decision | Android Community | iOS Community |
|---|---|---|
| Recycler group above `MaxConsolidation` | Builds one call per recycler with every selected alias. Oversized call and extension vectors fail bounded-vector decoding before pallet dispatch. Chunking exists only in the transfer path. | Reads `MaxConsolidation` and slices each recycler into chunks of at most that many vouchers, one call each. The surplus host is selected over chunks rather than unsplit recyclers. |

At the pinned People runtime commit, `MaxConsolidation` is `64`; this is [runtime configuration](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/runtimes/next-people-paseo/src/people.rs#L1665-L1670), not a protocol-wide constant. Oversized bounded vectors [fail to decode](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/tests/test_bounded_vec_decoding.rs#L17-L26) rather than reaching dispatch.

| Implementation | Finding | Proof |
|---|---|---|
| Android Community | Vouchers-before-coins ladder; preferred-then-largest voucher pick; largest-first coin pick; no preference after recycling; first-fit surplus host; greedy denomination breakdown; no consolidation chunking in the external-payment unload. | [plan ladder](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/externalPayment/RealExternalPaymentPlanner.kt#L41-L74), [voucher and coin picks](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/externalPayment/RealExternalPaymentPlanner.kt#L78-L126), [pick after recycling](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/externalPayment/state/AwaitRecyclingPaymentState.kt#L64-L81), [free settled coins are candidates](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/CoinageAssetSelector.kt#L76-L87), [one call per recycler, surplus host](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/externalPayment/usecase/UnloadRecyclerIntoExternalAssetUseCase.kt#L180-L233), [breakdown](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/common/RealCoinAmountBreakdownContext.kt#L17-L33) |
| iOS Community | Same ladder and picks; chunks each recycler by `MaxConsolidation`; first-fit surplus host over chunks; greedy denomination breakdown. | [plan ladder](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/ExternalPayment/Planner/ExternalPaymentPlanner.swift#L6-L54), [voucher and coin picks](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/ExternalPayment/Planner/ExternalPaymentPlanner.swift#L86-L114), [pick after recycling](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/ExternalPayment/StateMachine/States/OnboardCoinsPaymentState.swift#L66-L84), [free settled coins are candidates](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/ExternalPayment/Planner/ExternalPaymentAssetClassifier.swift#L32-L34), [surplus host and chunking](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/ExternalPayment/Service/OffboardVouchersForPaymentService.swift#L279-L327), [chunker](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/CoinSelection/RecyclerVoucherChunker.swift#L13-L44), [breakdown](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Denomination/Denomination.swift#L58-L72) |
| Brevity | Comparison only. Greedy largest-first over ready vouchers, then coins; reschedules instead of recycling when pending assets would cover; surplus assigned sequentially to trailing groups. | [plan](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/external_payment.rs#L199-L314), [group surplus](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/offboard.rs#L205-L262) |
| Runtime | The production wallets use voucher unload to asset and voucher unload to asset plus fresh loaded coins. The pallet additionally exposes single- and multi-recycler non-anonymous unloads, archived-recycler recovery, and direct coin offboarding with a documented privacy warning. | [unload to asset](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L2876-L2911), [unload to asset and loaded coins](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3186-L3250), [non-anonymous unloads](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3339-L3419), [archived-recycler recovery](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3485-L3528), [direct coin offboard](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3768-L3802) |

**Required selection:** None for denomination-level inventory selection itself. A scenario in which one recycler contributes more than `MaxConsolidation` vouchers must explicitly select the Android Community or iOS Community execution variant.

**Verified against:**
- Android Community commit `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community commit `b960f771049c07819de1f201b901b037613d42e9`;
- Brevity commit `0fb3fa214c8abeb7a33a7db0db60c257ea069c8e`;
- Coinage pallet commit `b5951a9784bdcc87539b793ed686fa6ae93f99ab`.
