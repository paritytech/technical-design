

Confirmed at lib.rs:2543-2545 — transfer requires "the destination account must not already have a coin" and "the coin's age must be less than MaximumAge". So rotation is not an extrinsic; it's a precondition of every transfer. k = 2 from "claim plus rotation" has no basis.

Here's what the code does support. k decomposes into three terms:

k = s + c + (s + c)/MaximumAge × r

  s = splits per payment        1 extrinsic, free, ages outputs by 1
  c = coins transferred         1 extrinsic each, free, ages by 1
  r = recycling cost per coin   1 load + 1 unload, amortised by batching

r is bounded by runtime constants: worst case 2 extrinsics per coin, best case 1/10 + 1/64 ≈ 0.12 with MaxBatchUnpaidLoad = 10 and MaxConsolidation = 64. With MaximumAge = 16 that third term is between 0.7% and 13% of the first two.

So k ≈ s + c, within 13%. Recycling is nearly free in extrinsic terms. The entire unknown is how many splits and coins a payment costs — which is a profile output, not a constant.

Paste-ready replacement for the parameters paragraph:

**Other parameters.** Grouped by how much we actually know.

*Verified from the People-Polkadot runtime config:*
`MaximumAge` 16, `MaxSplitOutputs` 32, `MaxConsolidation` 64,
`MaxBatchUnpaidLoad` 10, denominations 2^0 to 2^14,
`MaxFreeUnloadTokensPerTimePeriod` 1000 per 1-day period.

*Assumed, and load-bearing:*
peak factor 10x the daily mean; 0.72 payments and 0.055 loads per user per day.
Open question 3 in the source PRD asks whether these are believable. Every tier
number depends on them.

*Unmeasured — to come out of the tests:*

- **k, extrinsics per payment.** `k = s + c + (s + c)/MaximumAge × r`, where `s
  is splits per payment, `c` is coins transferred, and `r` is the amortised
  recycling cost per coin. `r` is bounded by the batching constants above at
  between 0.12 and 2, which makes the recycling term 0.7% to 13% of the total.
  So `k` is dominated by `s + c`, and `s + c` is an output of the consumption
  profile. It cannot be stated as a constant. The tier tables below use k = 2 a
  a placeholder only.
- **Coins per payment.** Expected to be right-skewed with most mass at 1, since
  `split` produces change and a payment only needs a coin at or above the
  amount. The mean, not the median, is what feeds k.
- **Same-ring batch size.** `RecyclerManager::load` takes no `RingIndex` — the
  member service appends to whichever ring is currently open. A merchant cannot
  choose to keep coins together, so the achievable consolidation batch is a
  random variable set by global traffic at that denomination.

Two things I'd drop from the author's paragraph entirely: "claim plus rotation"RECYCLING_SWEEP_BASE_INTERVAL with its 25% jitter (a client-side constant in arepo we can't locate — S9 is built on it and can't be specified without it).