# Measured runtime constants

Fee and quota values measured from a Coinage runtime with the tests shown below. They are measurements of one runtime version, not protocol constants, and must be re-measured on the runtime under test.

**Measured on:**

`people-polkadot` spec_version 2_005_000

## Summary

| Constant | Value | What it is |
| -------- | ----- | ---------- |
| [`UNLOAD_TOKEN_FEE_BASE`](#unload_token_fee_base) | 0.1634017754 DOT | The fee for one paid unload token when the chain is not congested. |
| [`FREE_UNLOAD_TOKENS_PER_PERIOD`](#free_unload_tokens_per_period) | person 122, lite person 61, hard cap 1000 | The number of free unloads a person or lite person gets in one 24-hour period. |

Both values were read at `NextFeeMultiplier = 1`, the genesis default. When the chain is congested, the multiplier rises. The fee then rises, and the free unload counts fall, because each count is an allowance divided by the current fee.

---

## UNLOAD_TOKEN_FEE_BASE

A wallet pays this fee to unload from a recycler when it has no free unload left.

**Runtime function:**

`get_paid_unload_token_fee_in_native`

**Result:**

UNLOAD_TOKEN_FEE_BASE = 0.1634017754 DOT

**Test that printed it:**

```rust
/// local test written inside: "https://github.com/polkadot-fellows/runtimes/blob/main/system-parachains/people/people-polkadot/src/tests.rs"
#[test]
fn print_paid_unload_token_fee() {
  use crate::{Coinage, RuntimeGenesisConfig};
  use sp_runtime::BuildStorage;

  let mut ext = sp_io::TestExternalities::new(
    RuntimeGenesisConfig::default().build_storage().expect("runtime genesis builds"),
  );
  ext.execute_with(|| {
    let fee = Coinage::get_paid_unload_token_fee_in_native();
    println!("paid unload token fee, uncongested (NextFeeMultiplier = 1)");
    println!("  {fee} plancks");
    println!("  {} DOT", fee as f64 / 1e10);
  });
}
```

---

## FREE_UNLOAD_TOKENS_PER_PERIOD

The number of unloads a person or lite person can make without paying the fee above, in each 24-hour period.

**Formula:**

`min(allowance / current_fee, MaxFreeUnloadTokensPerTimePeriod)`

**Hard cap:**

`MaxFreeUnloadTokensPerTimePeriod = 1000`

**Result:**

at `NextFeeMultiplier = 1` (genesis default)

```text
person:      122
lite person: 61
```

**Test that printed it:**

Printed by the same `print_paid_unload_token_fee` test as above, continuing
inside the `execute_with` block:

```rust
println!("free unload tokens per 24h period:");
println!("  person      {}", Coinage::free_unload_token_limit_for_people());
println!("  lite person {}", Coinage::free_unload_token_limit_for_lite_people());
println!("  hard cap    {}", Coinage::get_max_free_unload_tokens_per_time_period());
```
