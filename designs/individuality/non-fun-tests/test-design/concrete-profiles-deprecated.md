To define a useful profile mix, we start with real-world usage patterns and turn them into explicit, testable assumptions.

Each transaction has a sender and a recipient. Either party may act as a payer or a merchant, although the merchant will usually be the recipient.

> [!warning] Assumed distributions
> Every **Share** value in this document is an assumption, not a measured result. Treat these values as model inputs that must be revisited when real usage data becomes available.
### Payer Profile
#### Volume
**param_1: Payment frequency**

| Level    | Payments / day | Share |
| -------- | -------------- | ----- |
| **low**  | 0.2            | 80%   |
| **mid**  | 2              | 18%   |
| **high** | 10             | 2%    |
**param_4: Top-up amount**

For this model, a top-up restores the wallet to its target inventory value (`param_13`) rather than adding a fixed amount. The actual amount loaded therefore depends on the wallet's balance when the top-up is triggered.

**param_13: Initial inventory value**

We correlate the target inventory with payment frequency (`param_1`): actors who pay more often are assumed to hold a larger balance. To keep the initial model simple, the levels are linked one-to-one. For example, the high-volume profile makes 10 payments per day and targets an inventory worth 500 dotUSD.

| Level    | Target value (dotUSD) | Share |
| -------- | --------------------- | ----- |
| **low**  | 50                    | 80%   |
| **mid**  | 200                   | 18%   |
| **high** | 500                   | 2%    |
#### Privacy
**param_9: Recycle age threshold**

| Level      | Threshold | Meaning                 | Share |
| ---------- | --------- | ----------------------- | ----- |
| **low**    | age 16    | only when forced        | 70%   |
| **medium** | age 8     | mid-lifecycle           | 20%   |
| **high**   | age 1     | after every transaction | 10%   |

**param_10: Privacy budget**

| Level       | X                             | Behaviour under a ramp                                             | Share |
| ----------- | ----------------------------- | ------------------------------------------------------------------ | ----- |
| none        | 0                             | never pays beyond free quota                                       | 20%   |
| **default** | **2 × UNLOAD_TOKEN_FEE_BASE** | **degrades at multiplier 2, where budget and quota fail together** | 50%   |
| tolerant    | 5 × UNLOAD_TOKEN_FEE_BASE     | survives moderate congestion, isolates recycler limits             | 20%   |
| unbounded   | ∞                             | removes fees from the experiment entirely                          | 10%   |

See [constants](../coinage/constants.md#unload_token_fee_base)
> Under the baseline model, most payers with personhood status are unlikely to exhaust their free quota and therefore will rarely need to use their privacy budget.

**param_12: Personhood status**

Free quota is `min(allowance / current_fee, MaxFreeUnloadTokensPerTimePeriod)`,
per person, per 24-hour period.

| Level    | Allowance / period | Free unloads / period | Share |
| -------- | ------------------ | --------------------- | ----- |
| `none`   | —                  | **0**                 | 10%   |
| `lite`   | 10 DOT             | **61**                | 60%   |
| `person` | 20 DOT             | **122**               | 30%   |

Free unload counts: see [constants](../coinage/constants.md#free_unload_tokens_per_period)

> [!warning] Free quota falls as the fee rises
> The quota calculation divides the allowance by `current_fee`. As a result, congestion that raises the fee multiplier reduces the number of free unloads available in a period. This relationship was measured by sweeping `NextFeeMultiplier`:
>
> | `NextFeeMultiplier` | Fee per unload | `person` quota | `lite` quota |
> | ------------------- | -------------- | -------------- | ------------ |
> | 1  | 0.1634 DOT | 122 | 61 |
> | 2  | 0.3268 DOT | 61  | 30 |
> | 10 | 1.6340 DOT | 12  | 6  |
>
> The fee is exactly linear in the multiplier.
>
> **Open:** whether a stress ramp can actually drive `NextFeeMultiplier` that far. `FeeMultiplierUpdate = SlowAdjustingFeeUpdate`, which moves the multiplier gradually across many blocks rather than instantly with load. If it only responds to sustained fullness, this is an endurance concern rather than a stress-ramp one.


#### Spend shape

> [!info] _Initially I was thinking about making user focus on spending specific coin denominations. However, quickly the question arose: 'what to do after they are all spend'. We naturally would fall back to the remaining denominations. No matter which denomination we focus on, we only determine the start point by it, but still do a full sweep of all coins. A more realistic setup is to use a matching setup (for endurance tests) or a max coin setup (for stress tests)_ 

**param_2: Payment denomination focus**

This parameter selects the Coinage denomination level around which the actor's payments are concentrated. It is a denomination exponent, not a direct dotUSD amount.

For the production dotUSD Coinage instance:

- dotUSD has 6 decimals;
- `asset_unit = 10_000` base units = `0.01 dotUSD`; and
- denomination `d` has the value `coin_value(d) = 0.01 × 2^d dotUSD`.

For each payment, the generator selects a target denomination around this focus according to `param_3`. The wallet must then satisfy that value using its available coin composition. It may already hold a matching coin, need to split a larger coin, or need to transfer several smaller coins.

| Level    | Focus denomination | Reference value | Interpretation              | Share |
| -------- | ------------------- | --------------- | --------------------------- | ----- |
| **low**  | `d = 3`             | 0.08 dotUSD     | very small payments         | 70%   |
| **mid**  | `d = 7`             | 1.28 dotUSD     | low-value everyday payments | 25%   |
| **high** | `d = 11`            | 20.48 dotUSD    | higher-value payments       | 5%    |

**param_3: Denomination variance**

This parameter controls how far a payment's target denomination may vary from the focus denomination in `param_2`. The `±` values refer to denomination levels, not dotUSD amounts. Moving by one denomination level doubles or halves the reference value.

For example, focus `d = 7` with variance `d ± 3` covers denominations `d = 4` through `d = 10`, corresponding to reference values from 0.16 to 10.24 dotUSD.

> [!question] Wallet responsibility
> Confirm whether payment variance is user-driven or selected automatically by the wallet. If the wallet determines it, these profiles should reproduce the wallet's actual selection behavior instead of inventing a separate distribution.

| Level    | Denomination spread | Behaviour                                    | Share |
| -------- | ------------------- | -------------------------------------------- | ----- |
| **low**  | `d ± 1`             | payments remain close to the focus           | 50%   |
| **mid**  | `d ± 3`             | payments span a moderately broad value range | 35%   |
| **high** | `d ± 5`             | payments span a broad, multiplicative range  | 15%   |

> [!info] The resulting denomination is clamped to the runtime's `d = 0` through `d = 14` range. A focus near either boundary therefore produces an asymmetric range.
#### Wallet strategy

**param_5: Top-Up split**

| Level       | Split                          | What it exercises                          | Share |
| ----------- | ------------------------------ | ------------------------------------------ | ----- |
| **matched** | tracks `param_2` and `param_3` | baseline, assumes a competent wallet       | 50%   |
| **fine**    | many small coins               | high coin count, storage and transfer load | 25%   |
| **coarse**  | few large coins                | splits on every payment, fastest age grind | 25%   |

**param_6: Top-Up threshold**

| Level     | Trigger       | Effect                          | Share |
| --------- | ------------- | ------------------------------- | ----- |
| **late**  | 10% remaining | fewer, larger top-ups           | 25%   |
| **mid**   | 25% remaining | baseline                        | 50%   |
| **early** | 50% remaining | doubles the load rate vs `late` | 25%   |

**param_11: Recycle return split**

| Level           | Output                         | What it exercises                           | Share |
| --------------- | ------------------------------ | ------------------------------------------- | ----- |
| **consolidate** | one coin, `value + log2(N)`    | minimum coin count, forces splits later     | 25%   |
| **matched**     | tracks `param_2` and `param_3` | baseline                                    | 50%   |
| **fine**        | many small coins               | high coin count, more transfers per payment | 25%   |
This uses the same denomination strategy as `param_5`, but at a different entry point: `param_5` converts an external asset into coins, whereas `param_11` converts recycled coins into new coins. Every recycled output starts at age 0.
#### Exit policy

**param_7: Offboard threshold**
**param_8: Offboard selection**

In the baseline payer model, wallets do not proactively offboard; their inventory normally leaves through spending.

We model one exception:

- personhood status is `param_12 = none`; and
- privacy budget is `param_10 = 0`.

Under this policy, a coin that reaches `MaximumAge` can be loaded into the recycler, but not unloaded: the actor has neither a free unload quota nor permission to pay for an unload. Direct offboarding is therefore the fallback.


### Payer Population Spec

Every parameter is sampled. A payer draws one level from each distribution.

| Axis        | Param  | Level       | Value                    | Share |
| ----------- | ------ | ----------- | ------------------------ | ----- |
| Volume      | 1 + 13 | low         | 0.2 / day, 50 dotUSD     | 80%   |
|             |        | mid         | 2 / day, 200 dotUSD      | 18%   |
|             |        | high        | 10 / day, 500 dotUSD     | 2%    |
| Spend shape | 2      | low         | focus 2^3                | 70%   |
|             |        | mid         | focus 2^7                | 25%   |
|             |        | high        | focus 2^11               | 5%    |
|             | 3      | low         | ±1                       | 50%   |
|             |        | mid         | ±3                       | 35%   |
|             |        | high        | ±5                       | 15%   |
| Wallet      | 5      | matched     | tracks focus/variance    | 50%   |
|             |        | fine        | many small coins         | 25%   |
|             |        | coarse      | few large coins          | 25%   |
|             | 6      | late        | 10% remaining            | 25%   |
|             |        | mid         | 25% remaining            | 50%   |
|             |        | early       | 50% remaining            | 25%   |
|             | 11     | consolidate | one coin, `+ log2(N)`    | 25%   |
|             |        | matched     | tracks focus/variance    | 50%   |
|             |        | fine        | many small coins         | 25%   |
| Privacy     | 9      | low         | age 16                   | 70%   |
|             |        | medium      | age 8                    | 20%   |
|             |        | high        | age 1                    | 10%   |
|             | 10     | none        | 0                        | 20%   |
|             |        | default     | 2 × UNLOAD_TOKEN_FEE_BASE | 50%   |
|             |        | tolerant    | 5 × UNLOAD_TOKEN_FEE_BASE | 20%   |
|             |        | unbounded   | ∞                        | 10%   |
|             | 12     | none        | 0 free unloads           | 10%   |
|             |        | lite        | 61 free unloads          | 60%   |
|             |        | person      | 122 free unloads         | 30%   |

**Fixed or absent**

| Param | Status                                                        |
| ----- | ------------------------------------------------------------- |
| 4     | derived: restores inventory to the `param_13` target           |
| 7, 8  | absent, except for the `none` + zero-budget case described above |

#### Profile-space constraints and implications

- The sampled dimensions produce `3^8 × 4` = **26,244 distinct payer profiles**. The eight three-level choices include the combined volume level (`param_1` + `param_13`); `param_10` is the only four-level choice.
- The model samples personhood status (`param_12`) and privacy budget (`param_10`) independently. Therefore, `none` personhood (10%) combined with a zero budget (20%) represents **2% of the modeled population**. Under the stated policy, this group cannot recycle and is the only payer group expected to use direct offboarding as a fallback.
- The privacy budget (`param_10`) matters only after the free quota is exhausted. At the baseline fee and modeled payer volumes, the 90% of payers with `lite` or `person` status are unlikely to exceed their daily quota of 61 or 122 unloads. Their budget level will therefore have little or no effect in ordinary runs.
- That last assumption is load-dependent, not universal. Because the free quota falls as `NextFeeMultiplier` rises, sustained congestion may cause `lite` and `person` profiles to exhaust it. Congestion tests must report when the privacy budget begins to affect behavior.

---
### Merchant Profile [WIP]

A payer actively chooses its inventory by deciding when to top up and which denomination split to request. A merchant primarily receives inventory, so its denomination distribution emerges from the coins sent by customers. The same five axes still affect merchant behavior, but fewer of them are independent merchant choices.

Merchant volume is selected through the merchant archetype rather than sampled as an additional dial. Likewise, inbound wallet strategy is generated by the payer population rather than chosen by the merchant. The model currently uses these three assumed merchant sizes:

| Profile          | Payments / day | Peak rate      | Coins held |
| ---------------- | -------------- | -------------- | ---------- |
| Small shop       | 50             | 0.05 / s       | ~1k        |
| Busy venue       | 2,000          | 1 / s at lunch | ~5k        |
| Event or stadium | 20,000         | 10 / s         | ~10k       |

On top of the merchant archetype, the model varies two settlement-policy axes:

| Profile           | Privacy                   | Exit policy                    | What it exercises              |
| ----------------- | ------------------------- | ------------------------------ | ------------------------------ |
| `settle-daily`    | recycle within free quota | offboard everything each night | inventory never accumulates    |
| `settle-hoard`    | recycle within free quota | offboard at a high threshold   | large inventory, age pressure  |
| `settle-no-quota` | personhood none           | offboard is the only exit      | free-quota-less merchant path  |
> [!important] Merchants can also be payers
> Merchant profiles must include outgoing payments, potentially at high volume. Receiving and settlement alone do not describe the complete merchant lifecycle.

Whether `settle-no-quota` is an edge case or the default depends on whether a business entity can hold a `PEOPLE_IDENTIFIER` membership proof. If businesses cannot hold one, every merchant follows the no-quota path rather than only this profile.

---

> [!todo] Complete the merchant behavior model
> Define merchant outgoing-payment frequency and value distribution using the same profile parameters. The model should cover merchants that accept both small and large payments, receive more value than they onboard, settle through offboarding, and transact primarily in higher denominations.

