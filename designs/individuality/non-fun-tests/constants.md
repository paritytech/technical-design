`people-polkadot` spec_version 2_005_000

## UNLOAD_TOKEN_FEE_BASE
`get_paid_unload_token_fee_in_native`

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

UNLOAD_TOKEN_FEE_BASE = 0.1634017754 DOT

---
## FREE_UNLOAD_TOKENS_PER_PERIOD
`min(allowance / current_fee, MaxFreeUnloadTokensPerTimePeriod)`
`MaxFreeUnloadTokensPerTimePeriod = 1000`

Printed by the same `print_paid_unload_token_fee` test as above, continuing
inside the `execute_with` block:

```rust
println!("free unload tokens per 24h period:");
println!("  person      {}", Coinage::free_unload_token_limit_for_people());
println!("  lite person {}", Coinage::free_unload_token_limit_for_lite_people());
println!("  hard cap    {}", Coinage::get_max_free_unload_tokens_per_time_period());
```

at `NextFeeMultiplier = 1` (genesis default)
person:      122
lite person: 61