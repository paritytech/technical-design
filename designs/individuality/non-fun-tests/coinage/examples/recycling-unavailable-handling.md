# Recycling-unavailable handling

## Scope

Recycler loading and recycler unloading consume different resources:

- loading a coin into a recycler does not consume an unload token;
- unloading the resulting voucher requires a valid unload origin.

The production wallets therefore manage free-unload capacity before it is completely exhausted. This preventive reserve is related to, but distinct from, the [Preferred Recycling Unavailable](../runtime-conditions.md#preferred-recycling-unavailable) condition.

## Shared production behaviour

Android Community and iOS Community use only free prepaid unload tokens. They do not construct paid-token or fee-from-output unload origins, and they do not compare an unload-fee quote with `privacy.recycling.paid_fee_limit`.

Both wallets reserve 20% of the free-unload allowance. When the remaining allowance is at or below that reserve:

1. discretionary recycling decisions from the selected privacy preset are discarded;
2. coins below the wallet's forced-recycling threshold remain in the wallet as spendable coins;
3. those coins may become recycling candidates again after a later evaluation observes sufficient allowance;
4. coins at or above the forced-recycling threshold are still loaded into recyclers because loading consumes no unload token.

Engaging the reserve does not itself make vouchers unspendable. Any remaining valid free unload tokens can still be used for payments. Only complete exhaustion prevents the production wallets from unloading a voucher, because neither wallet has a paid fallback.

The production unload calls use a free prepaid origin and `max_fee = 0`. For a prepaid origin, this call argument does not represent the actor's paid-fee preference: the runtime requires or ignores it because the unload fee has already been settled by the origin.

## Worked states

Assume a free-unload limit of `100`, a 20% reserve, and a coin that the privacy preset would recycle.

| Remaining free unloads | Coin below forced threshold | Coin at or above forced threshold |
|---:|---|---|
| `21` | Follow the selected privacy preset. | Load into a recycler. |
| `20` | Retain as a spendable coin and defer discretionary recycling. | Load into a recycler; the remaining free unloads can still unload its voucher. |
| `0` | Retain as a spendable coin and defer discretionary recycling. | Load into a recycler; the voucher cannot be unloaded by the production wallet until a valid free token becomes available. |

The final row is the production case covered by **Preferred Recycling Unavailable**. The preceding reserve state is preventive handling rather than satisfaction of that condition.

## Preferred age versus forced recycling

Both production wallets apply their forced-recycling guard outside the selected privacy policy. Consequently, a configured preferred recycle age greater than the forced-recycling threshold cannot independently take effect: the outer guard marks the coin `MUST_RECYCLE` first. With the currently verified runtime configuration, preferred age `15` is therefore behaviorally equivalent to `14` in both production variants.

The implementations obtain that threshold differently:

- **Android Community** reads `MaximumAge` from the runtime and subtracts a hard-coded offset of `2`: [offset](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/data/repository/CoinRepository.kt#L46), [runtime-derived threshold](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/data/repository/CoinRepository.kt#L99-L127), [forced guard](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/EnsureChainLimitsStrategy.kt#L38-L49). If the runtime read fails, Android falls back to `14`.
- **iOS Community** hard-codes both `coinMaxAge = 16` and `recycleAtAge = coinMaxAge - 2`: [constants](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/CoinageConstants.swift#L23-L27), [forced guard](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Recycling/Strategy/EnsureChainLimitsStrategy.swift#L23-L30).

This creates a compatibility risk: after a runtime `MaximumAge` change, Android follows the new value when its runtime read succeeds, while iOS continues forcing at `14` until its constants are updated. The profile schema retains values through `MaximumAge - 1` because a custom wallet policy may use them; recycler loading itself has no runtime age restriction.

## Platform differences

| Decision | Android Community | iOS Community |
|---|---|---|
| Allowance read fails | Treats the allowance as not low and continues to apply the privacy preset. | Aborts that complete evaluation. No recycling starts from that failed evaluation, and the previously published verdict remains. |
| Allowance periods | Counts the current period only. | Counts every period accepted by its one-hour lookback calculation: normally the current period, plus the preceding period when the grace window crosses a boundary. |
| Forced-recycling threshold | Reads `MaximumAge` from the runtime, subtracts two, and falls back to `14` if the read fails. | Uses the hard-coded value `16 - 2 = 14`. |

## Runtime capabilities not used by the production wallets

The runtime supports more than the production clients expose:

- `Prepaid` unloading with either a free or paid unload token;
- fee-from-output unloading, where `max_fee` is expressed in the unloaded underlying asset;
- entering the paid unload-token ring by consuming a coin, paying native currency, or paying the underlying asset of a Coinage instance.

Consequently, an actor's paid fee limit must identify both an asset and an amount. The limit cannot universally be denominated in the chain's native asset.

Recycler loading itself has no coin-age validation. Transfer and split reject a coin at `age >= MaximumAge`, but `load_recycler_with_coin` can still accept it if its other validity requirements are satisfied.

## Line-level proof

### Android Community

- The quota decorator suppresses discretionary verdicts when the quota is low and treats read failure as “not low”: [EnsureQuotaLimitsStrategy](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/EnsureQuotaLimitsStrategy.kt#L11-L39).
- The reserve is 20%: [UnloadQuotaTracker](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/UnloadQuotaTracker.kt#L35-L60).
- The outer decorator forces old coins and maps otherwise-unjudged coins to `ALLOW_USE`: [EnsureChainLimitsStrategy](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/EnsureChainLimitsStrategy.kt#L22-L50).
- Android reads `MaximumAge`, subtracts two, and falls back to `14`: [CoinRepository](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/data/repository/CoinRepository.kt#L99-L127), [ForcedRecyclingAgeProvider](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/ForcedRecyclingAgeProvider.kt#L19-L35).
- The free-token resolver fails when it cannot satisfy the requested number of unloads: [FreeUnloadTokenResolver](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/data/helpers/FreeUnloadTokenResolver.kt#L90-L110).

### iOS Community

- The provider applies the 20% reserve and wraps it in the forced-age guard: [RecyclingStrategyProvider](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Recycling/Strategy/RecyclingStrategyProvider.swift#L21-L64).
- A failed quota read aborts the complete evaluation: [CoinRecyclingEvaluator](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Recycling/CoinRecyclingEvaluator.swift#L124-L133).
- The tracker sums free counters over the periods selected by the one-hour lookback: [UnloadQuotaTracker](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/UnloadToken/UnloadQuotaTracker.swift#L65-L91), [UnloadTokenPeriodCalculator](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/UnloadToken/UnloadTokenPeriodCalculator.swift#L15-L33).
- The forced threshold is hard-coded as `16 - 2`: [CoinageConstants](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/CoinageConstants.swift#L21-L27).

### Runtime

- `UnloadFee` distinguishes prepaid and fee-from-output modes: [pallet source](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L1310-L1334).
- `max_fee` for fee-from-output unloading is denominated in the unloaded asset: [pallet source](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L2880-L2899).
- Paid unload tokens can be funded with a coin, native currency, or an underlying asset: [coin](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3000-L3072), [native](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3074-L3113), [underlying asset](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L3115-L3180).
- Split and transfer enforce `MaximumAge`, while recycler loading does not: [split validation](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L4978-L4991), [transfer validation](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L5048-L5057), [load validation](https://github.com/paritytech/individuality-community/blob/b5951a9784bdcc87539b793ed686fa6ae93f99ab/pallets/coinage/src/lib.rs#L5075-L5101).

## Verified commits

- Android Community: `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community: `b960f771049c07819de1f201b901b037613d42e9`;
- Coinage pallet: `b5951a9784bdcc87539b793ed686fa6ae93f99ab`.
