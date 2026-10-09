# Remaining-flow burst campaign

This campaign runs the four remaining scenarios with fixed, auditable plans. It supplements the broader scenario drafts; it does not claim to execute a native wallet or the sustained full-flow ramp.

## Run order

Each scenario and profile is its own workflow run ([`coinage-burst-case.yml`](https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-unload-campaign/.github/workflows/coinage-burst-case.yml)), with its own URL, logs, conclusion and artifacts. A failed case is retried alone. Run one disposable PreviewNet at a time: six relay validators, two People collators and no synthetic delay. Each measured run starts with its own one-actor smoke stage. Order: merchant fan-in, then free-quota exhaustion, offboarding and full-flow.

The [case queue](https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-unload-campaign/ci/previewnet/coinage-case-queue.py) dispatches one case, waits for it, records the run ID and conclusion in a ledger, then continues. It never retries on its own and resumes from the ledger. Preserve a failed case and continue independent cases; fix setup failures before calling them workload attempts.

| Case per scenario | Actors | Release | Pool |
| --- | ---: | --- | --- |
| 1 | 100 | One burst | Default, no override |
| 2 | 1,000 | One burst | Default, no override |
| 3 | 10,000 | One burst | Default, no override |
| 4 | 10,000 | 8,000, verify completion, then 2,000 | Default, no override |
| 5 | 10,000 | One burst | 11,000 entries; 256 MiB |
| 6 | 20,000 | One burst | 22,000 entries; 256 MiB |

All 24 cases are requested, including both 10,000 fallbacks even if the default burst passes. Save effective startup arguments for both collators. Enlarged pools are experimental settings. Actor count is not transaction count: record calls per actor and stage separately.

## Measured operations

- **Merchant fan-in:** one merchant driver receives fixture memos and claims each coin into a fresh merchant-controlled key. Record arrival, queue, submit and finality times. This is the fixed-burst variant of the sustained-arrival draft.
- **Free-quota exhaustion:** count the requested size as unload requests, grouped into people with up to the starting allowance of requests each; record the distinct-person count separately. This fixture avoids conflating 20,000 unload requests with 20,000 people each spending a full allowance. Use real People token proofs and recycler proofs. Observe success below the allowance and validation rejection at the boundary. Count expected policy rejections separately from unexpected losses. Record the actual allowance at submission and inclusion; it can change with the fee multiplier. Period recovery is a separate stage and requires a real accepted period; never manufacture a successful rollover by merely changing client time.
- **Offboarding:** unload one ready voucher per actor into an external-asset account. Verify external value delivered and backing released. Additional surplus and multi-voucher variants remain separately labelled.
- **Full-flow:** top-up, wait for a built ring, unload into a payment coin, claim, recycle, wait for a built ring, then offboard. Report each dependent stage and total completion. This fixed-plan burst is not the production planner or the mixed sustained-rate ramp.

A case may progress to a dependent stage only after its prerequisite receipts and state checks pass. In a paced case, release the second group only after the first finishes all required stages. Always write partial observations before failing a gate.

## Implementation scope

The offboarding fixture creates vouchers through real top-ups, including the Wrapped hold needed for external-asset release. Minting free backing alone is insufficient. Full-flow uses the same real top-up as its first measured stage.

The first quota pilot exhausts complete person cohorts, leaves any final partial cohort explicitly identified, then probes a consumed counter and the current out-of-range counter. The real-period rollover and native-wallet policy variants remain separate from these 24 burst cases. Policy-model rows must never be presented as observed Android or iOS executions.

The standalone `smoke` profile validates a driver on its own. Cases run sequentially, and a failed case does not block the next.

Setup top-ups use `author_submitAndWatchExtrinsic`, like the workload. PAPI's `submitAndWatch` uses `transaction_v1_broadcast`, which the node allows 16 times per connection; beyond that the transaction is silently never sent. Record every setup outcome. A setup failure is not a workload attempt.

## Evidence for recycling-unavailable handling

Link results to [the policy explanation](../coinage/policy-examples/recycling-unavailable-handling.md). Save one record per policy evaluation with:

- platform or explicit test policy; source revision; actor and chain block;
- allowance limit, period, accepted periods, consumed counters and remaining tokens;
- remaining fraction and whether the 20% reserve is engaged;
- coin age, forced threshold, proposed action and resulting action;
- discretionary loads withheld, forced loads submitted and each resulting receipt;
- unloads attempted, withheld or rejected, with reason and token counter;
- allowance-read failures and the policy response;
- next-period eligibility and actual recovery receipts, when observed.

Exercise above reserve, at reserve and exhausted states. Loading a coin does not spend a free unload token. A custom TypeScript decision model is labelled a policy model; it is not evidence that the native Android or iOS code ran. Native policy conformance and real chain execution are separate result fields.

## Verification and retained artifacts

For each submitted hash retain signed public extrinsic bytes, finalized block/index, System success or failure and expected Coinage events. Retain state snapshots, asset backing, token consumption and recycler membership/root revisions at pinned finalized blocks. Save original watch outcomes and later reconciliation separately.

Save configuration, runtime/binary revisions, proof preparation time, submit windows, per-stage p50/p95/p99/max with sample counts, readiness cutoffs, generator CPU/memory, node metrics and recovery observations. Save secrets only in private runner memory; never upload seeds or voucher entropy. Write machine-readable summaries even when setup, proof generation, submission, audits or shutdown fail. Preserve evidence outside expiring GitHub artifacts.
