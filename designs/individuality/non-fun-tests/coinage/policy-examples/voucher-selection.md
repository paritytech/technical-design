# Voucher selection

Policy: `wallet.payment_construction`

Strategy: **Unload and split**

## Shared context

The exact-coin and split strategies have already failed. Whole coins cover part of the payment, and recycler vouchers must cover the remaining gap.

Only vouchers made selectable by the active recycling policy participate in this decision. Both implementations stop as soon as the selected vouchers cover the gap; any excess becomes change.

## Android behaviour

1. Group vouchers by denomination and recycler.
2. Calculate the total value held by each group.
3. Order groups by total value, largest first.
4. Walk the ordered groups voucher by voucher until their combined value covers the gap.

Android does not first ask whether one voucher can cover the gap. It starts with the highest-value group.

## iOS behaviour

1. Look for a single voucher that covers the gap.
2. If one or more exist, select the smallest covering voucher and stop.
3. Otherwise, order all vouchers by denomination, largest first, and take them until their combined value covers the gap.

Recycler membership does not affect which vouchers iOS initially selects.

## Distinguishing examples

### Single-voucher choice

Gap: `3¢`

- Recycler A holds one `8¢` voucher.
- Recycler B holds one `4¢` voucher.

**iOS:** The smallest single voucher covering `3¢` is `4¢`. It produces `3¢` for the recipient and `1¢` change.

**Android:** Recycler A has the larger group total, so its `8¢` voucher is selected first. It produces `3¢` for the recipient and `5¢` change.

### Ordering across recyclers

Gap: `6¢`

- Recycler A holds four `2¢` vouchers, worth `8¢` in total.
- Recycler B holds one `4¢` voucher.

No single voucher covers the gap.

**iOS:** Takes `4¢` from recycler B and then `2¢` from recycler A. The two selected vouchers cover the gap exactly and require two recycler groups to be unloaded.

**Android:** Recycler A has the larger group total, so it takes three `2¢` vouchers from A. They cover the gap exactly using one recycler group.

Assuming the runtime consolidation limit permits all three vouchers in one call, iOS uses two unload calls in this example and Android uses one.

## Consequences

For the same payment and starting inventory, the implementations can:

- unload different vouchers;
- produce different change denominations and values;
- touch different recyclers;
- require different numbers of unload calls.

Neither implementation performs a global subset search to minimize excess value or change. Tests asserting the selected vouchers or resulting inventory must therefore select the Android Community or iOS Community production variant explicitly.

## Brevity comparison

Brevity matches iOS for this decision: it selects the smallest single voucher that covers the gap, or otherwise takes vouchers largest-first until covered. Brevity remains a comparison implementation, not production evidence.

## Code proof

| Implementation | Proven behaviour | Proof |
|---|---|---|
| Android Community | Groups by denomination and recycler, orders groups by total value descending, and takes vouchers until covered. | [`findMinimalVoucherCover` and `orderForUnload`](https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/TransferPlanner.kt#L149-L185) |
| iOS Community | Selects the smallest single covering voucher, otherwise vouchers largest-first. | [`findMinimalCover` and `findVoucherCombination`](https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/CoinSelection/CoinSelector.swift#L316-L357) |
| Brevity | Selects the smallest single covering voucher, otherwise vouchers largest-first. | [`try_unload`](https://github.com/paritytech/brevity-dozer/blob/0fb3fa214c8abeb7a33a7db0db60c257ea069c8e/core/crates/brevity-coinage/src/selection.rs#L285-L313) |

## Verified against

- Android Community commit `f875be37451f5282a92dec2aa9bf764ac5e64f43`;
- iOS Community commit `b960f771049c07819de1f201b901b037613d42e9`;
- Brevity commit `0fb3fa214c8abeb7a33a7db0db60c257ea069c8e`.
