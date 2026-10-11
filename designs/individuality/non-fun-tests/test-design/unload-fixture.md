# Shared unload fixture (Draft)

Every pilot that unloads a voucher needs the same setup: people who hold free unload tokens, vouchers in built rings, retained voucher secrets and two ring-VRF proofs per call. This file defines that setup once. The [payment burst](scenarios/payment-burst.md#next-pilot-voucher-unload-and-claim), [synchronised recycling](scenarios/synchronised-recycling.md#next-pilot-forced-age-selection-and-voucher-use), [free-quota exhaustion](scenarios/free-quota-exhaustion.md#pilot-free-token-exhaustion-and-period-rollover) and [offboarding burst](scenarios/offboarding-burst.md#pilot-voucher-unloads-to-the-external-asset) pilots reference it.

No current harness submits an unload. The lifecycle and top-up drivers create voucher keys in memory and do not keep their secrets, so their vouchers cannot be unloaded later. This fixture closes that gap.

**Runtime path:** [Recycler load, ring readiness and unload](../coinage/pallet-components.md#recycler-load-ring-readiness-and-unload). Values below were read at `individuality-community` [`fce93ef3`][rt-config] for `next-people-paseo`. Record the executed runtime and re-read every value at the run's starting block.

## People and free tokens

A free unload token needs a People or LitePeople membership proof. The production wallets use free tokens only, with `max_fee = 0` ([production policies](../coinage/production-policies.md#recycling-unavailable-handling)).

| Step | Fixture |
| ---- | ------- |
| Create people | Submit `People.force_recognize_personhood` through Sudo; its `ManagerOrigin` is root ([call][force-recognize]). For a LitePeople variant, use the permissionless `PeopleLite.register_with_fee` ([call][lite-register]), which costs 75 native units per person in this runtime. |
| Wait for rings | Members OCWs onboard each person key and build the People ring. Reuse the recycler readiness check against the People collection: a built root whose `included` count covers the member's position. |
| Read the allowance | Call the `Coinage.get_free_unload_token_info` view at the starting block ([view][token-info]). It returns `(people, lite_people)`, each `min(allowance / unload fee, 1000)`. The cap of 1,000 is marked "bumped temporarily" in the runtime. |
| Assign tokens | Each token is a unique `(person, period, counter)` with `counter < limit` ([validation][token-validate]). The period is `unix_time / 86,400`. Validation also accepts the previous period for one hour after a boundary. Give every unload its own triple. |
| Avoid boundaries | Start a stage only if its whole observation window fits in the current period, unless the pilot tests rollover. |

A pilot may give one person several unloads, up to that person's limit. That is a fixture simplification: production gives each user their own allowance. Report the number of people and unloads per person, so it is clear how much allowance each person used.

## Vouchers

1. Create vouchers with the top-up fixture (`load_recycler_with_external_asset_unpaid`) or with coin loads (`load_recycler_with_coin`). Keep each voucher's entropy on the runner. Do not upload it.
2. Wait until every fixture voucher is covered by a built recycler root. Recycler rings hold 1,024 members (`RecyclerRingExponent = R2e10`).
3. Stop loading into that recycler collection before generating proofs. Record each voucher's instance, denomination, ring index and revision.
4. For a sponsored instance, record pot contributions and held load deposits before the stage. Unloads settle those deposits.

## Proofs and calls

Each anonymous unload carries two ring-VRF proofs:

- **Recycler alias proof:** membership of the voucher's 1,024-member recycler ring, in context `pop:polkadot.network/coinrecyclr` ([context][recycler-context]). Unloading marks this alias spent.
- **Token proof:** membership of the People or LitePeople ring, in the free-token context for that period and counter ([context][token-context]).

Both proofs are bound to the signed call. Build every call first, then generate its proofs, then release.

No existing driver builds a free-token unload. Two pieces exist and must be combined:

- [`paritytech/coinage` `crates/chain`][coinage-chain] builds the recycler alias proof and a complete unload, but only with a **paid** token (`AsUnloadTokenPaid`).
- The e2e TypeScript helpers build People ring proofs for other calls. Their ring helper hard-codes the People ring exponent.

The driver needs the `AsUnloadTokenPeople` extension payload: the token proof, period, counter and the recycler alias proofs. A paid-token variant can reuse the Rust path unchanged, but it does not match the production wallets.

Generating these proofs is client work the earlier pilots never measured. Record it as its own result:

- time to open each prover and generate each proof, with p50/p95/max;
- total proving time, CPU and memory for the stage;
- whether proving happened before release (the default) or inside the measured window (a client-cost variant).

## Checks for every unload

- Verify the raw extrinsic, finalized block and index, `System.ExtrinsicSuccess`, one `RecyclerAliasUnloaded` per alias and the call's own event. Each pilot names its call event.
- Check `ConsumedFreeUnloadTokens(period, token_alias)` is present and `PeopleFreeUnloadTokenConsumed` (or the LitePeople event) was emitted.
- Record validation rejections by their exact reason. The ones these pilots expect are `InvalidUnloadTokenPeriod`, `UnloadTokenCounterOutOfRange`, `InvalidUnloadTokenProof`, `UnloadTokenAlreadyConsumed` and `InvalidRecyclerRevision`.
- A dispatch failure after `prepare` does not refund a free token. Count tokens consumed by failed dispatches separately from successful unloads.
- Each free-token transaction provides the pool tag `Coinage:ppl-unload-token` plus its token alias ([validity][token-validate]). Two transactions with the same token conflict in the pool. Record which one survives.

## Boundary

The fixture skips issuance, the wallet's privacy delay and the app's own token bookkeeping. Root-created people are not real personhood onboarding. Record these as fixture choices in every result, next to the counts they affect.

[rt-config]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/runtimes/next-people-paseo/src/people.rs#L1643-L1691
[force-recognize]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/people-multi/src/lib.rs#L540-L555
[lite-register]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/people-lite/src/lib.rs#L455-L506
[token-info]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L1716-L1725
[token-validate]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/extension.rs#L452-L482
[recycler-context]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L88-L89
[token-context]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L156-L164
[coinage-chain]: https://github.com/paritytech/coinage/blob/ffb1bb1937b8d4dd8061306ae0501bc0f87f9e3d/crates/chain/src/lib.rs#L1628-L1810
