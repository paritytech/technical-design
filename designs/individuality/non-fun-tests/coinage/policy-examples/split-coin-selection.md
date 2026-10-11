# Split-coin selection

Policy: `wallet.payment_construction`

Strategy: **Split**

## Shared context

The exact-coin strategy has already failed. The wallet now tries to cover the payment by passing zero or more coins whole and splitting one larger coin into recipient denominations and change.

This strategy runs before voucher unloading. If it succeeds, no recycler vouchers are selected.

## Android behaviour

1. Order spendable coins by denomination, largest first, preferring older coins within a denomination.
2. Add a largest-first prefix while its total does not exceed the payment. Stop at the first coin that would exceed it.
3. Calculate the remaining uncovered value.
4. Among all unselected spendable coins larger than that remainder, select the smallest denomination.
5. Pass the prefix whole and split the selected coin into the uncovered recipient value and change.

If no unselected coin can cover the remainder, the split strategy fails and the wallet proceeds to voucher unloading.

## iOS behaviour

1. Look for any single coin larger than the entire payment.
2. If one or more exist, select the smallest such coin, split it alone, and produce the rest as change.
3. Otherwise, order coins by denomination, largest first.
4. Pass coins whole while the running total remains below the payment.
5. Split the first coin that makes the running total reach or exceed the payment.

If all coins are exhausted while the running total remains below the payment, the split strategy fails and the wallet proceeds to voucher unloading.

## Distinguishing examples

### Different split coin

Payment: `11¢`

Inventory: `8¢, 8¢, 4¢`

The inventory has no exact `11¢` combination.

**Android:** Takes one `8¢` coin whole. The next `8¢` coin would exceed the payment, so the prefix stops with a `3¢` remainder. Of the unselected coins, `4¢` is the smallest one covering that remainder. Android splits it into `3¢` for the recipient and `1¢` change.

**iOS:** No single coin covers the entire `11¢`. It takes one `8¢` coin whole, then uses the second `8¢` coin as the overflow coin. iOS splits it into `3¢` for the recipient and `5¢` change (`4¢ + 1¢`).

Both transfer `11¢`, but Android leaves an original `8¢` coin plus `1¢` change, while iOS leaves the original `4¢` coin plus `4¢ + 1¢` change.

### Single sufficient coin

Payment: `5¢`

Inventory: `8¢`

Both implementations split the `8¢` coin into `5¢` for the recipient (`4¢ + 1¢`) and `3¢` change (`2¢ + 1¢`). They diverge when Android's post-prefix search chooses a smaller split candidate than iOS's first overflow coin.

## Consequences

For the same payment and starting inventory, the implementations can:

- consume different input coins;
- produce different change denominations and coin counts;
- retain coins with different denominations and ages;
- create different inventory states for subsequent payments and recycling.

Tests asserting the selected coin, change composition, coin count, or post-payment inventory must therefore select the Android Community or iOS Community production variant explicitly.

## Brevity comparison

Brevity matches iOS for this decision. It first prefers the smallest single coin larger than the whole payment; otherwise it walks coins largest-first and splits the coin that makes the running total reach the payment. Brevity remains a comparison implementation, not production evidence.

## Code proof

| Implementation | Proven behaviour | Proof |
|---|---|---|
| Android Community | Builds a largest-first prefix and then selects the smallest unselected coin larger than the remainder. | [`tryGetSingleSplitPlan`](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/TransferPlanner.kt#L49-L73), [`findMaxCoinCoverage`](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/TransferPlanner.kt#L123-L146) |
| iOS Community | Prefers the smallest coin covering the whole payment; otherwise splits the overflow coin of a largest-first pass. | [`trySplitCoin`](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/CoinSelection/CoinSelector.swift#L85-L140) |
| Brevity | Uses the same split choice as iOS. | [`try_split_coin`](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/selection.rs#L212-L270) |

## Verified against

- Android Community commit `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community commit `b960f771049c07819de1f201b901b037613d42e9`;
- Brevity commit `0fb3fa214c8abeb7a33a7db0db60c257ea069c8e`.
