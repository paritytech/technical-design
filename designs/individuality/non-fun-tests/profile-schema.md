# Profile parameter schema
## Parameter kinds

- Profile input — actor behaviour, intent, or preferences configured by the profile.
- Wallet policy — wallet decision logic requiring a production or custom implementation.
- Provisioned state — actor or wallet state established by the test environment.

## Parameter index

| Parameter                                                           | Key                                      | Kind              |
| ------------------------------------------------------------------- | ---------------------------------------- | ----------------- |
| [Rate](#rate)                                                       | `payment_demand.rate`                    | Profile input     |
| [Timing](#timing)                                                   | `payment_demand.timing`                  | Profile input     |
| [Distribution](#distribution)                                       | `payment_demand.value_distribution`      | Profile input     |
| [Top-Up Trigger](#top-up-trigger)                                   | `inventory.top_up.trigger`               | Profile input     |
| [Top-Up Sizing](#top-up-sizing)                                     | `inventory.top_up.sizing`                | Profile input     |
| [Top-up Composition](#top-up-composition)                           | `inventory.top_up.composition`           | Wallet policy     |
| [Payment Construction](#payment-construction)                       | `wallet.payment_construction`            | Wallet policy     |
| [Preferred Recycle Age](#preferred-recycle-age)                     | `privacy.recycling.preferred_age`        | Profile input     |
| [Paid Recycling Fee Limit](#paid-recycling-fee-limit)               | `privacy.recycling.paid_fee_limit`       | Profile input     |
| [Recycle Output Composition](#recycle-output-composition)           | `wallet.recycling.output_composition`    | Wallet policy     |
| [Recycling-Unavailable Handling](#recycling-unavailable-handling)   | `wallet.recycling.unavailable_handling`  | Wallet policy     |
| [Personhood Status](#personhood-status)                             | `actor.personhood_status`                | Provisioned state |
| [Offboarding Trigger](#offboarding-trigger)                         | `exit.offboarding.trigger`               | Profile input     |
| [Offboarding Sizing](#offboarding-sizing)                           | `exit.offboarding.sizing`                | Profile input     |
| [Offboarding Inventory Selection](#offboarding-inventory-selection) | `wallet.offboarding.inventory_selection` | Wallet policy     |
| [Initial Inventory Coins](#initial-inventory-coins)                 | `initial_inventory.coins`                | Provisioned state |

## Payment demand
**Payment**: One payment is one business-level request to transfer a specified value from an actor to a recipient
**Payment timing:** The rule used to distribute payment intents over simulated time. It affects when payments occur
**Payment value:** The quantity of the underlying asset that the recipient is intended to receive, excluding fees and independent of the coins used to construct the payment.

### Rate

**Meaning:**
The expected number of distinct outgoing payment intents initiated by one actor during a unit of simulated time.

**Type/unit:**
Non-negative rate, expressed as payments / simulated day.
### Timing

**Meaning:**
How the payment intents represented by `payment_demand.rate` are distributed over simulated time.

**Type/unit:**
Timing strategy, with no unit.
### Distribution

**Meaning:**
The probability distribution from which each payment value is sampled.

**Type/unit:**  
A discrete probability distribution over payment values. Payment values are represented in the asset's smallest unit.

For each possible payment value `x`, the distribution assigns a probability `P(X = x)`, where:

- `X` is the payment value to be generated;
- `x` is one specific payment value;
- `P(X = x)` is a number between `0` and `1`;

For example:

- `P(X = 30 dotUSD) = 0.70` means that 70% of payments have a value of 30 dotUSD;
- `P(X = 100 dotUSD) = 0.20` means that 20% have a value of 100 dotUSD;
- `P(X = 500 dotUSD) = 0.10` means that 10% have a value of 500 dotUSD.

For each payment intent, the test harness draws one concrete payment value from this distribution.
## Inventory and wallet strategy
### Top-Up Trigger

The conversion of underlying assets into Coinage inventory for an actor’s wallet

**Meaning:** 
The condition under which the wallet initiates a top-up. It determines when a top-up occurs.

**Type/unit:** 
A predicate over the wallet's inventory state.

### Top-Up Sizing

The conversion of underlying assets into Coinage inventory for an actor’s wallet

**Meaning:**
The rule used to determine the value added to the wallet when its top-up trigger is met.

**Type/unit:**
A function over the wallet's inventory state that returns a non-negative integer number of cents. A positive result must be at least `0.01 dotUSD`.

### Top-up Composition

**Meaning:**
The strategy used to divide a requested top-up value into the Coinage denominations requested by the wallet. The resulting denominations represent the largest loadable value that does not exceed the requested top-up value. Any remaining value smaller than the minimum supported denomination remains in the underlying asset.

**Type/unit:**
A denomination-composition strategy. Its result is a collection of denomination levels and counts whose combined value equals the loaded value.

### Payment Construction

**Meaning:**
The strategy used to construct a payment of the requested value from the wallet's current coin inventory. The strategy may select existing coins, split larger coins, or combine multiple coins. It must produce a protocol-valid plan whose transferred value equals the requested payment value.

**Type/unit:**
A payment-construction strategy, with no unit.

## Privacy preferences
### Preferred Recycle Age

**Meaning:**
The coin age at which the actor prefers recycling to begin. A lower value represents a stronger privacy preference.

Reaching this age makes the coin a candidate for recycling. It does not require the wallet to offboard the coin when recycling is unavailable.

**Type/unit:**
A positive integer number of transfers between `1` and `MaximumAge - 1`.

> [!info]
> If neither free allowance nor an acceptable paid-unload method is available when this age is reached, the [Preferred Recycling Unavailable](runtime-conditions.md#preferred-recycling-unavailable) runtime condition applies.
>
> In the verified production wallets, a preferred age above the wallet's forced-recycling threshold cannot affect behaviour: the outer age guard recycles the coin first. Android derives the threshold as runtime `MaximumAge - 2`; iOS hard-codes `16 - 2 = 14`. The wider range remains available to custom policy implementations because the runtime itself permits recycler loading at later ages. See [Preferred age versus forced recycling](examples/recycling-unavailable-handling.md#preferred-age-versus-forced-recycling).

### Paid Recycling Fee Limit

**Meaning:**
The maximum fee the actor is willing to pay for one recycler unload when no free-recycling allowance is available.

**Type/unit:**
A non-negative fee value represented by an asset identifier and an integer amount in that asset's smallest unit, per recycler unload. Fee comparisons must quote the current unload fee in the same asset.

### Recycle Output Composition

**Meaning:**
The strategy used to choose the denominations and counts of new coins when recycler vouchers are unloaded into coins. It may consolidate multiple vouchers from the same recycler into larger coins or divide their combined value into smaller coins.

**Type/unit:**
A denomination-composition strategy. For each unload operation, it produces denomination levels and counts whose total equals the unloaded voucher value minus any fee taken from the output, while respecting runtime consolidation and output limits.

### Recycling-Unavailable Handling

**Meaning:**
The wallet decision applied to a coin while the Preferred Recycling Unavailable condition is satisfied. The policy determines whether an operation should be performed or whether the coin should remain in the wallet.

**Type/unit:**
A recycling-unavailable handling policy, with no unit.

### Personhood Status

**Meaning:**
The personhood class assigned to the actor in the test environment and recognized by the target runtime. The runtime uses this status when calculating the actor's free-recycling allowance.

**Type/unit:**
An enum with no unit:
- `none` — the actor has no personhood-based allowance;
- `lite` — the actor has the lite-person allowance;
- `person` — the actor has the full-person allowance.

## Exit preferences
### Offboarding Trigger

**Meaning:**
The condition under which the actor wants the wallet to begin converting Coinage inventory back into the underlying asset. The trigger determines when offboarding begins.

**Type/unit:**
An offboarding-trigger condition. It evaluates to either satisfied or not satisfied. Any values and units used by the condition are defined by the concrete profile.
### Offboarding Sizing

**Meaning:**
The rule used to determine the total value to offboard when the offboarding trigger is satisfied. It determines how much value should leave Coinage, but not which inventory assets are used.

**Type/unit:**
An offboarding-sizing rule. Its result is a non-negative asset value, limited by the wallet's available inventory.

### Offboarding Inventory Selection

**Meaning:**
The strategy used to select eligible wallet inventory to satisfy the requested offboarding value. It determines which existing recycler vouchers are unloaded and, when those vouchers are insufficient, which settled coins are first converted into vouchers.

**Type/unit:**
An inventory-selection strategy with no unit. Its result is a protocol-valid offboarding plan identifying the selected vouchers and any coins that must first be recycled.

## Initial Inventory

### Initial Inventory Coins

**Meaning:**
The coins held by the wallet at the start of the measured test.

**Type/unit:**
A list of `(denomination, age, count)` tuples:
- `denomination` is a valid Coinage denomination level;
- `age` is the coin's non-negative age, measured in transfers.
- `count` is a positive integer specifying how many coins have that denomination and age.
