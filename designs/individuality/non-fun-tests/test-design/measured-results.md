# Coinage stress-test findings

We verified a burst of **100,000 claims**. These experiments establish completed burst sizes, not the server’s physical maximum or sustainable production throughput.

Pacing and larger pool settings both produced successful 10,000-top-up runs. Later reconciliation verified all 88 dropped-watch transactions from the two incomplete runs. Those runs remain failed as 10,000-top-up experiments: one had 989 admission rejections, and the other never submitted its final 1,500 transactions.

## Measured results

These results apply to distinct actor keys performing one operation each on a disposable PreviewNet network. They do not measure a sustained real-user population. “Verified receipts” below means successful finalized receipts, including later reconciliation. Latency percentiles retain their original observation populations, shown where they differ.

| Scenario / evidence | Result | Verified receipts | Finality p95 | Ring readiness p95 |
| --- | --- | --- | --- | --- |
| [1,000 top-ups][topups-1000] | **PASS** | 1,000 / 1,000 | 53.0 s | 105.6 s |
| [1,000 claims][claims-1000] | **PASS** | 1,000 / 1,000 | 40.9 s | No ring construction required |
| [10,000 paced top-ups (7,000 + 3,000)][paced] | **PASS** | 10,000 / 10,000 | 183.0 s | 262.1 s |
| [10,000 simultaneous top-ups, default pool][topups-10000] | **FAIL** | 9,011 / 10,000 after reconciliation | 232.8 s; 8,971 timed receipts | 332.5 s; 9,011 timed vouchers |
| [10,000 simultaneous top-ups, enlarged pool][larger-pool] | **PASS** | 10,000 / 10,000 | 256.0 s | 353.1 s |
| [8,500 + 1,500 paced top-ups, default pool][paced-8500] | **FAIL — first-wave receipt gate** | 8,500 / 8,500 submitted after reconciliation; next 1,500 not submitted | 224.5 s; 8,452 timed receipts | 231.6 s; 5,602 timed vouchers |
| [8,400 + 1,600 paced top-ups, default pool][paced-8400] | **PASS** | 10,000 / 10,000, independently rechecked | 214.9 s | 312.4 s |

The 1,000-top-up run verified 1,000 actor debits and ready vouchers, with matching held backing. The 1,000-claim run verified that all source coins disappeared and recipient coins had the expected values and ages. **Claim source coins were seeded through privileged fixture setup: this tests claims, not the complete issuance/payment lifecycle.** Network recovery checks passed in these two 1,000-operation runs, the failed default-pool simultaneous burst, the 7,000 + 3,000 paced run the failed 8,500 first-wave run, and the 8,400 + 1,600 paced run.

### What limited the simultaneous 10,000-top-up run

All 10,000 submissions were launched; the generator was not the limiting factor. Outcomes were:

- **8,971** successful finalized receipts verified during the original run.
- **989** explicit pool-limit rejections.
- **40** dropped-watch transactions subsequently verified as successful finalized receipts in block **159734**, extrinsic indexes **2–41**; no failed dispatches or unresolved receipts in this group.

Reconciliation brings the verified receipt count to **9,011**, matching the observed actor debits and ready vouchers. The **989 admission rejections** remain, so this is still a failed 10,000-top-up run. No test was rerun.

Node startup logs reported effective ready-pool limits of **8,192 transactions and 20 MiB of transaction bytes**. The 8,971 verified successes are an outcome count across the run, not the pool's capacity. This run exposed admission pressure; it does not show that the chain broke. Network recovery checks passed.

## Paced result: 7,000 + 3,000 — PASS

[Run 36560408065][paced] completed successfully. **All 10,000 top-ups succeeded without manually increasing the transaction-pool limits.** Both People nodes retained ready-pool limits of 8,192 transactions and 20 MiB, confirmed in their startup logs. There were no automatic retries.

The first wave submitted 7,000 transactions in 282 ms. After their successful finalized receipts were verified, the second wave started at 196.0 seconds and submitted 3,000 in 103 ms. Both waves used the same prepared instance. Ring readiness did not gate the second wave.

The final audit verified 10,000 unique successful receipts with no errors. A separate local run of the artifact verifier also matched all 10,000 transaction hashes to the saved block bodies and successful dispatch events. State checks found 10,000 actor debits, 10,000 vouchers included in built roots, and 20,000 asset units held under Coinage.Wrapped, matching the expected backing. The pallet retained its separate minimum free balance of 1. Network recovery and both People-author checks passed.

Finality p95 was 183.0 seconds and ring readiness p95 was 262.1 seconds, each measured from the individual transaction's submission. The measured stage took 410.9 seconds (6 min 51 s), including the wait between waves and final state reads, excluding fixture preparation and the final receipt audit. This demonstrates completion with pacing on this test network; it does not demonstrate admission of 10,000 transactions at once.

## Simultaneous 10,000, enlarged pool — PASS

[Run 36609355696][larger-pool] completed the simultaneous burst. Both People collators used `--pool-limit=11000 --pool-kbytes=40960`; startup logs confirm **11,000 ready transactions / 40 MiB**. All 10,000 submissions launched in 380 ms. There were no retries.

The saved audit reports 10,000 unique verified successful receipts and no audit errors. State checks found 10,000 actor debits, 10,000 ready vouchers and matching held backing. Finality p95 was 256.0 seconds, ring readiness p95 was 353.1 seconds, and the measured stage took 420.7 seconds.

**This configuration completed the simultaneous burst.** Both the transaction-count and byte limits increased, so this run does not isolate which limit mattered. A larger queue does not itself increase block-processing capacity. This is a separate comparison from pacing with unchanged pool limits.

## Paced 8,500 + 1,500 — FAIL at first-wave receipt gate

[Run 36619415692][paced-8500] used the default pool settings and submitted 8,500 transactions in its first wave. It verified **8,452 successful finalized receipts**. Another **48 watches reported “dropped” after first reporting “ready”**; no explicit immediate pool-limit rejections were recorded.

State showed all 8,500 actor debits and matching held backing of 17,000 asset units, including debits for the 48 affected transactions. Later reconciliation verified all 48 as successful finalized receipts in block **173699**, extrinsic indexes **2–49**, bringing the total to **8,500**. There were no failed dispatches or unresolved receipts in this group; this conclusion comes from receipt evidence, not state changes alone.

The remaining 1,500 transactions were never submitted because the first-wave receipt gate failed. Network recovery passed. The original gate failure is retained: this was not a completed 10,000-top-up run. It exposed a gap between watch outcomes and execution evidence, not an 8,500-transaction capacity limit or a precise failure threshold.

## Paced 8,400 + 1,600 — PASS

[Run 36662212241][paced-8400] completed with default pool settings, the same first-wave receipt gate and no retries. The saved evidence was independently rechecked: all **10,000** submitted top-ups have successful finalized receipts, actor debits and ready vouchers, with **20,000** asset units held as backing. Finality p95 was **214.931 seconds**, readiness p95 **312.393 seconds**, and stage duration **405.548 seconds**. Network recovery passed.

## Reconciliation and readiness observations

Verification of saved evidence completed on **30 September 2026, approximately 09:51 UTC**. No tests were rerun. All **88** dropped watches have successful finalized receipts; none remain unresolved and none show failed dispatch. The original audit outputs are preserved separately from the later findings.

| Run | Originally verified receipts | After reconciliation | Original observed-ready count | Ready in saved final state |
| --- | ---: | ---: | ---: | ---: |
| [10,000 simultaneous][topups-10000] | 8,971 | **9,011** | 9,011 | **9,011**; 989 admission-rejected top-ups have no established vouchers |
| [8,500 + 1,500][paced-8500] | 8,452 | **8,500** | 5,602 | **5,869**; readiness remains unobserved for 2,631 submitted vouchers; another 1,500 actors never submitted |
| [8,400 + 1,600][paced-8400] | 10,000 | **10,000, independently rechecked** | 10,000 | **10,000** |

For the 8,500 run, the last readiness sample was at **20:37:34.964 UTC on September 29**, 236.919 seconds after stage start, at finalized block **173732**. It observed 5,602 ready vouchers. The later state at finalized block **173733** establishes **267 additional ready vouchers**, by matching member keys to included ring positions with saved roots. There is no exact query timestamp for this snapshot; it was collected before the stage summary at approximately **20:38:07.120 UTC**.

No later saved per-member state establishes readiness for the remaining **2,631** submitted vouchers. They are **unobserved, not failed**. Readiness polling stopped after the receipt gate failed, before the full observation window elapsed. Recovery shows chain progress, not voucher readiness or complete backlog drainage.

The simultaneous run's last readiness sample was **September 29 at 08:44:14.829 UTC**, block **159826**, with final state at **159827**. The 8,400 + 1,600 run's last sample was **September 30 at 04:18:17.531 UTC**, with both the sample and final state at **173800**.

### Original timing populations

All values below are seconds, independently recalculated from saved measurements. Percentiles use nearest rank over the stated population and exclude unobserved outcomes. **Reconciliation supplies receipts and state evidence, not missing timing samples.** The 40 and 48 reconciled receipts do not enter the original finality percentiles; the additional 267 ready vouchers do not enter the original readiness percentiles.

| Run | Timed finality population | Finality p50 / p95 / max | Timed readiness population | Readiness p50 / p95 / max |
| --- | ---: | --- | ---: | --- |
| [10,000 simultaneous][topups-10000] | 8,971 | 136.722 / 232.777 / 244.981 | 9,011 | 216.392 / 332.522 / 347.910 |
| [8,500 + 1,500][paced-8500] | 8,452 | 128.507 / 224.546 / 236.602 | 5,602 | 155.974 / 231.603 / 236.728 |
| [8,400 + 1,600][paced-8400] | 10,000 | 107.019 / 214.931 / 227.177 | 10,000 | 171.100 / 312.393 / 347.931 |

**Finality** measures submission to client result completion after the finalized notification and block/event lookup, including observation overhead. **Readiness** measures submission to the first sampled observation of the voucher inside a built root at finalized state, including polling delay.

| Run | Measured stage duration | Debited actors | Held backing (test-asset units) |
| --- | ---: | ---: | ---: |
| [10,000 simultaneous][topups-10000] | 628.256 s | 9,011 | 18,022 |
| [8,500 + 1,500][paced-8500] | 269.075 s | 8,500 | 17,000 |
| [8,400 + 1,600][paced-8400] | 405.548 s | 10,000 | 20,000 |

Held backing matches `Coinage.Wrapped`: two test-asset units per executed top-up. Each pallet asset account retained its separate free balance of 1. Stage duration includes submission, waits, between-wave audits where applicable, observer shutdown and final state reads. It excludes fixture preparation/signing, connection setup, the final aggregate receipt audit, offline verification and recovery.

Recovery passed in all three runs. Each People collator authored **32 of the 64** checked finalized blocks. This establishes liveness and author participation, not complete ring-backlog drainage.

## Claim experiments: 10,000 claims

Verified from preserved evidence on **30 September 2026 UTC**. Each actor submitted one signed `Coinage.transfer` for a pre-seeded source coin. These claim-only PreviewNet tests exclude onboarding, coin selection, voucher readiness and the full payment lifecycle. Fixture seeding bypasses normal issuance and held-backing setup. A separate smoke claim is excluded from all counts. **Ring readiness is not applicable.**

All three experiments requested and submitted 10,000 claims. Finality values below are seconds, measured over successful claims only.

| Claim experiment / evidence | Result | Receipt- and state-verified | Finality p50 / p95 / max | Watches settled |
| --- | --- | ---: | --- | ---: |
| [10,000 simultaneous, default pool][claims-default] | **FAIL — full completion** | 8,192 / 10,000 | 38.234 / 50.167 / 50.185 | 50.418 s |
| [8,000 + 2,000 paced, default pool][claims-paced] | **PASS** | 10,000 / 10,000 | 38.970 / 50.680 / 50.697 | 79.207 s |
| [10,000 simultaneous, enlarged pool][claims-enlarged] | **PASS** | 10,000 / 10,000 | 42.903 / 54.686 / 54.694 | 55.127 s |

- **Default-pool burst:** client submissions launched within **471.12 ms**. There were **989 immediate pool-limit rejections** and **819 dropped watches**. Those 819 source coins remained unchanged and their recipients were absent at finalized block **173754**. This is the saved observation cutoff, not a statement about every later block. No failed dispatch receipts were found in the saved receipt blocks. The **9,011 ready notifications are not successful-claim receipts**: 819 subsequently reported dropped. The exact cause of those dropped watches was not traced through pool internals.
- **Paced run:** 8,000 claims launched within **349.60 ms**, then 2,000 within **84.13 ms**. Wave two began **52.241 s** after wave one began, only after the first 8,000 successful finalized receipts passed the audit against both People nodes. Measured stage duration was **113.615 s**. Both collator logs confirm the unchanged default ready-pool limits: **8,192 transactions / 20 MiB**.
- **Enlarged-pool burst:** all 10,000 claims launched within **433.40 ms**. Both People collators used `--pool-limit=11000 --pool-kbytes=40960`; both startup logs confirm **11,000 ready transactions / 40 MiB**. Measured stage duration was **88.275 s**.

Both successful runs had **no rejections, dropped watches, failed dispatch receipts or unresolved receipts**, and **no retries**. Network recovery passed in all three experiments. Both People collators advanced **11 finalized blocks** during recovery for the paced run and **10** for the enlarged-pool run.

**Both pacing and the larger pool allowed all 10,000 claims to complete in these runs.** The default-pool simultaneous run did not complete all claims. A larger pool provides more buffering; both count and byte limits changed, so this comparison does not isolate which limit mattered. These individual observations do not establish increased block-processing capacity, production user capacity, correct weights, PVF deadline compliance or a universal capacity threshold.

### Claim evidence and timing boundaries

The experiments used the same PreviewNet snapshot and binary provenance, with two People collators and the required relay validators, without added network delay. Each verified receipt was checked against its raw extrinsic hash, finalized block/index, `System.ExtrinsicSuccess` and `Coinage.CoinTransferred`, with saved canonical/finalized observations from both People nodes. Successful claims removed the source coin and created the expected recipient coin with the same instance/value and age increased from **0 to 1**. The fixture asset balance remained **20,001 before and after each run**. This unchanged fixture asset balance does not prove normal held-backing accounting. Saved local RPC observations are not independent consensus or storage proofs.

- **Finality:** each claim's own submission until the client observes finalization and completes receipt lookup. The timing populations are 8,192, 10,000 and 10,000 respectively.
- **Submission window:** client launch time, not node acceptance time or chain throughput.
- **Watch settlement:** time from the first wave's start until all watch outcomes settle, including the inter-wave receipt gate in the paced run.
- **Stage duration:** also includes wave audits, observer shutdown and final state queries. It excludes fixture preparation, final aggregate receipt auditing, offline verification and recovery. Setup took roughly an hour and is excluded from burst timings.

Original run observations and subsequent offline checks are retained separately. These claim results do not inherit the successful dropped-watch reconciliation from the earlier top-up experiments.

## Claim capacity experiments — 1 October 2026

**We verified a burst of 100,000 claims. These experiments establish completed burst sizes, not the server’s physical maximum or sustainable production throughput.** All three runs passed: every requested claim has a successful finalized receipt and matching final coin state. There were no retries, failed dispatch receipts or unresolved receipts. Recovery passed, and both People collators continued authoring.

All times in the following table are seconds. Each finality population includes every successful claim in its run: 20,000, 40,000 or 100,000.

| Claims / run | Pool entries | Client launch | Last receipt from burst start | Finality p50 / p95 / max |
| --- | ---: | ---: | ---: | --- |
| [20,000][capacity-20000] | 22,000 | 0.802 | 94.263 | 65.711 / 93.806 / 93.914 |
| [40,000][capacity-40000] | 44,000 | 1.582 | 140.925 | 92.300 / 139.394 / 139.566 |
| [100,000][capacity-100000] | 110,000 | 3.930 | 312.867 | 178.521 / 297.346 / 310.339 |

Finality runs from each claim's own submission until finalized notification and receipt lookup complete. Client launch is not node acceptance time or simultaneous execution. Launch targets were **1, 5 and 10 seconds**, respectively; the larger runs were not one-second bursts. Pool byte capacity stayed at **40 MiB**.

| Claims | Launch target | Measured stage | Preparation |
| ---: | ---: | ---: | ---: |
| 20,000 | 1 s | 151.428 s | 1,138.347 s |
| 40,000 | 5 s | 182.521 s | 977.091 s |
| 100,000 | 10 s | 410.385 s | 2,440.797 s |

Stage duration includes final state queries but excludes preparation, final aggregate receipt auditing and recovery. **Ring readiness is not applicable** to these claim-only experiments.

### Hardware and observed constraint

The runner reported **AMD EPYC 7B13, 16 cores / 32 logical CPUs and approximately 62.8 GiB RAM**. The entire local PreviewNet network and driver shared that machine.

| Claims | Peak sampled host CPU busy | Minimum sampled available RAM | Peak sampled ready queue |
| ---: | ---: | ---: | ---: |
| 20,000 | 20.7% | 48.0 GiB | 20,000 |
| 40,000 | 25.2% | 47.0 GiB | 37,637 |
| 100,000 | 21.3% | 43.0 GiB | 88,185 |

These are approximately five-second samples, not instantaneous peaks. Host CPU is an average across logical CPUs. One logical CPU reached approximately **98%** in the 100,000 run; low average CPU does not rule out serial execution limits. Service-cgroup limits were not captured correctly for the 20,000 run, so host specifications alone do not establish its effective quota.

In the **100,000-claim run**:

- All client-observed ready notifications arrived within **20.371 s**. Watched transactions peaked at **100,000**, a different measure from ready-queue depth.
- There were **43 canonical receipt blocks**: 42 containing **2,363 claims** each, then **754** in the last block. All 42 full blocks reported `HitBlockWeightLimit`; the final block reported `NoMoreTransactions`.
- Maximum canonical proposal duration was **2,970 ms**. This is authoring time, not measured PVF execution time. No service-cgroup OOM events were observed.

Increasing the pool allowed more claims to wait; it did not increase claims per full block. **The next useful capacity measurement is a sustained submission rate with a stable queue.** This is a proposed measurement, not a completed result.

### Capacity evidence and scope

Downloaded evidence was checked again on **1 October 2026 UTC**: raw extrinsic hashes, block/index, `System.ExtrinsicSuccess` and expected `Coinage.CoinTransferred` events. Source coins disappeared; recipient coins had the expected instance/value and age increased from **0 to 1**. Fixture backing stayed unchanged. Root-seeded fixtures bypass normal issuance and held-backing setup; unchanged fixture backing does not prove normal held-backing accounting.

These are claims, not top-ups or full wallet flows. Runs used the same engine, binaries and snapshot bytes, with zero added network delay. Fixture batching, query concurrency and launch targets changed explicitly; the 100,000 run also separated fixture snapshot reads from signing. These single-run observations do not establish production capacity guarantees, correct weights or PVF deadline compliance. Saved local RPC observations are not independent cryptographic consensus proofs. The launch window must not be extrapolated into a physical maximum or transactions-per-second claim.

See the [pinned claim-capacity results guide][claim-capacity-guide] and the existing [claim scenario specification][claim-spec]. Download the hosted [compact summary and provenance JSON](evidence/claims-capacity-2026-10-01/summary-provenance.json) and its [SHA-256 checksum](evidence/claims-capacity-2026-10-01/SHA256SUMS.txt). The summary includes exact verification timestamps, test revisions, artifact IDs, parameters and source-file hashes; **it does not contain all raw evidence**.

Full evidence is preserved locally under `coinage-evidence/claims-capacity-2026-10-01/`, separately from the hosted summary. GitHub artifacts are temporary and expire after **30 days**; local archives survive that expiry. The multi-gigabyte archive is not a website download. Original observations remain separate from later verification and from earlier top-up reconciliations.

## Claim generator memory retention — 2 October 2026

The million-claim attempt exposed a **load-generator memory limit**. The memory fix then passed a verified 1,000-claim validation. These observations do not establish the chain's maximum capacity. “Claims” means one signed transfer per root-seeded source coin, not real app users or the full payment lifecycle. The smoke claim is separate and excluded.

| Experiment / run | Outcome | Requested | Submitted | Watch-finalized | Receipt-verified |
| --- | --- | ---: | --- | --- | --- |
| [Million-claim attempt][retention-million] | **Generator heap exhausted** | 1,000,000 | Not established | Not established | No complete audit |
| [Memory-fix validation][retention-validation] | **PASS** | 1,000 | 1,000 | 1,000 | 1,000 |
| [250,000-claim experiment][retention-250k] | **RUNNING — results pending** | 250,000 | Pending evidence | Pending evidence | Pending evidence |

**Million-claim attempt:** all claims were prepared, but the TypeScript driver exhausted its **24 GiB JavaScript heap**. The configured pool was **1,100,000 transactions / 262144 KiB**. Repeated broadcast notifications and decoded blocks were retained without bounds; no heap profile established their exact share of memory. No complete final receipt or state audit was produced. Recovery passed after the driver crashed. The submitted, successful and failed totals for the million requested claims remain unestablished.

The [memory-retention fix][retention-fix] ([PR #38](https://github.com/paritytech/polkadot-pop-e2e/pull/38)) aggregates broadcast notifications into counters and timestamps, caps retained watch observations and decoded-block caching, and writes non-broadcast watch transitions and observed block evidence during execution. It releases completed watch traces and signed wire data. Receipt verification and final-state requirements remain in place, with no added pacing, automatic retries or relaxed success criteria. A local regression test processed **one million repeated notifications under a 128 MiB heap limit**. This was a synthetic notification test, not a million-transaction chain test.

### Verified 1,000-claim validation

The saved receipt audit verifies **1,000 successful claims**. All saved source/recipient states were independently rechecked with **zero mismatches**. Fixture backing remained **2,001 → 2,001**, in the artifact's raw units; root seeding bypasses normal issuance and held-backing setup. This unchanged balance does not verify normal held-backing accounting. The run used the **default transaction pool**. Recovery and the overall workflow passed.

| Measurement | Milliseconds |
| --- | ---: |
| Client submission window | 71.915 |
| Per-claim finality p50 / p95 / max (all 1,000) | 34,482.891 / 34,498.700 / 34,504.053 |
| Last watch settled, from burst start | 34,558.428 |
| Summary elapsed time | 36,058.706 |

Finality measures each transaction's submission through client-observed finalized notification and receipt lookup. The [driver at the fix commit][retention-driver] starts its elapsed timer after preparation and before submission. Elapsed time includes watch settlement, observer shutdown, sender disconnection, final coin/balance queries and summary preparation. It excludes fixture preparation, the subsequent independent aggregate receipt audit and recovery. The client submission window is not node acceptance time or chain throughput.

All **1,000** claims emitted client-observed pool-ready notifications. **Pool-ready notifications are not voucher readiness**; ring readiness is not applicable to these claim-only tests. Receipts were rechecked against raw extrinsic hashes, block indexes, `System.ExtrinsicSuccess`, expected `Coinage.CoinTransferred` events, and saved canonical/finality observations from both People nodes. These are consistency checks on saved RPC evidence, not cryptographic consensus proofs.

### Pending 250,000-claim experiment

At **2026-10-01 17:37 UTC** (2 October locally), GitHub reported **in progress**, with no downloadable artifacts. Configuration only: **250,000 claims in one burst**, no pacing or retries; pool **275,000 transactions / 262144 KiB**; fixture batch **5,000**; client launch target **60 seconds**; watch deadline **60 minutes**. It uses the same [memory-fix commit][retention-fix] as the validation. Submitted, watch-finalized and receipt-verified counts, final state, memory measurements and recovery remain unavailable. Inspect those artifacts before assigning a result. A larger pool provides queue space; it does not establish higher chain execution capacity.

The validation evidence and checksum manifest are preserved locally under `coinage-evidence/claims-retention-2026-10-02/`; they are not public downloads. The recorded independent validation timestamp is **2026-10-01 17:18:52 UTC** (2 October locally). Original observations remain separate from later verification. See the existing [claim scenario][claim-spec] and [claim methodology][claim-capacity-guide] for workload and measurement boundaries.

## How verification works

Each verified receipt matches a transaction hash to raw extrinsic bytes, its block and index, `System.ExtrinsicSuccess`, and the expected Coinage event. The reconciled top-up receipts also match the event’s actor, instance, denomination and amount to the fixture. Both local People nodes report the block as canonical and finalized. Separate state checks verify actor debits, held backing and voucher inclusion in built roots for top-ups, or source and recipient coin state for claims. These are trusted local-node observations, not independent cryptographic consensus proofs.

The [evidence guide][guide] explains the reports, receipt audits, raw block evidence, state checks and local artifact verifier. Scenario specifications describe the workload and pass criteria: [top-up burst][topup-spec] and [claim burst][claim-spec].

## Limits of these measurements

- “Actors” means distinct keys performing one operation, not a sustained real-user population.
- The disposable PreviewNet network runs on one CI runner, including two People collators and six relay validators, with no added network delay.
- Submission launch time is not acceptance throughput. Launching the workload within one second does not establish that the nodes accepted it within one second.
- Latency percentiles are measured from each transaction’s submission. Measured stage duration excludes fixture preparation and the final receipt audit.
- Single runs do not establish production capacity, weight accuracy, PVF deadline compliance or a precise failure threshold.
- Claim fixtures bypass issuance. Top-up ring readiness is separate from finality and does not include a wallet's privacy delay.

## Evidence record

Saved evidence reconciled on **2026-09-30 at approximately 09:51 UTC**; no tests were rerun. Earlier findings are retained from the 2026-09-29 review. The commits below identify the test repository revision for each run; they are not runtime or node revisions. Those details belong to each artifact's runtime and provenance files.

| Run (attempt 1) | Test commit | Verification record |
| --- | --- | --- |
| [36534910589][topups-1000] | [`8bffb7d1583e`](https://github.com/paritytech/polkadot-pop-e2e/commit/8bffb7d1583ec6c97c17fe9fd93035c1ba8c40d0) | Top-up receipt audit, state checks and network recovery passed. |
| [36514698770][claims-1000] | [`4e64a30e0273`](https://github.com/paritytech/polkadot-pop-e2e/commit/4e64a30e02732154b4bbf97248e404610809320d) | Claim receipt audit, state checks and network recovery passed; privileged fixture boundary applies. |
| [36537079387][topups-10000] | [`8bffb7d1583e`](https://github.com/paritytech/polkadot-pop-e2e/commit/8bffb7d1583ec6c97c17fe9fd93035c1ba8c40d0) | 8,971 original receipts + 40 reconciled = 9,011 verified; 989 admission rejections remain. Preserved artifact: 11022336907. |
| [36560408065][paced] | [`e2952bc3cea2`](https://github.com/paritytech/polkadot-pop-e2e/commit/e2952bc3cea2cb1b01556663950862e5e9d78b9f) | 10,000 verified receipts; both wave gates, final state checks and network recovery passed. Default pool confirmed in both node logs. |
| [36609355696][larger-pool] | [`e2952bc3cea2`](https://github.com/paritytech/polkadot-pop-e2e/commit/e2952bc3cea2cb1b01556663950862e5e9d78b9f) | Saved audit: 10,000 unique verified receipts, no errors; final state checks passed. Enlarged pool confirmed in startup logs. |
| [36619415692][paced-8500] | [`28ff6d477179`](https://github.com/paritytech/polkadot-pop-e2e/commit/28ff6d47717904567aa2a97b1119b6cd6443f65f) | First-wave gate failed originally; all 8,500 submitted receipts now verified. Only 5,869 ready in saved state; final 1,500 never sent. Preserved artifact: 11060739103. |
| [36662212241][paced-8400] | [`28ff6d477179`](https://github.com/paritytech/polkadot-pop-e2e/commit/28ff6d47717904567aa2a97b1119b6cd6443f65f) | 10,000 receipts independently rechecked; all ready, backing matched, recovery passed. Preserved artifact: 11076898224. |
| [36705343718][claims-default] | [`0793ccc5df8b`](https://github.com/paritytech/polkadot-pop-e2e/commit/0793ccc5df8b4f6fbc410b68658ba4976466244d) | Claims; verified 2026-09-30 UTC: 8,192 receipts and matching states; 989 rejected, 819 dropped. Preserved full artifact: 11095640662. |
| [36719621433][claims-paced] | [`3e2552a841a2`](https://github.com/paritytech/polkadot-pop-e2e/commit/3e2552a841a20ee8d3f209e0e7390d1976bc3c89) | Claims; verified 2026-09-30 UTC: 10,000 receipts and matching states; first-wave gate and recovery passed. Preserved artifact: 11105025693. |
| [36719745986][claims-enlarged] | [`3e2552a841a2`](https://github.com/paritytech/polkadot-pop-e2e/commit/3e2552a841a20ee8d3f209e0e7390d1976bc3c89) | Claims; verified 2026-09-30 UTC: 10,000 receipts and matching states; enlarged pool confirmed, recovery passed. Preserved artifact: 11109621586. |
| [36832069153][capacity-20000] | [`23a884c644db`](https://github.com/paritytech/polkadot-pop-e2e/commit/23a884c644dba50805f7b9373ad45d2529bb888f) | Claims; verified 2026-10-01 UTC: 20,000 receipts and matching states; unchanged fixture backing, recovery passed. Full artifact: 11148628985. |
| [36836204912][capacity-40000] | [`39d2961bb794`](https://github.com/paritytech/polkadot-pop-e2e/commit/39d2961bb7940ee0dd07b970968bc4be034a9608) | Claims; verified 2026-10-01 UTC: 40,000 receipts and matching states; unchanged fixture backing, recovery passed. Full artifact: 11150407769. |
| [36840043405][capacity-100000] | [`b7451cd74bbe`](https://github.com/paritytech/polkadot-pop-e2e/commit/b7451cd74bbe71799ab9bc8e01a69696ab043217) | Claims; verified 2026-10-01 UTC: 100,000 receipts and matching states; unchanged fixture backing, recovery passed. Full artifact: 11154045167. |
| [36859278723][retention-million] | [`6c6ce86ad0da`](https://github.com/paritytech/polkadot-pop-e2e/commit/6c6ce86ad0dab94ea45a2bd9a589f459d168c92d) | Generator heap exhaustion after preparing 1,000,000 claims; no complete receipt/state audit; recovery passed. |
| [36895937059][retention-validation] | [`932677d50e07`][retention-fix] | 1,000 successful receipts; all final coin states rechecked without mismatches; unchanged fixture backing; recovery passed. |
| [36898423397][retention-250k] | [`932677d50e07`][retention-fix] | Running at this update; configuration recorded, results pending evidence. |

Claim evidence is retained locally in `coinage-evidence/claims-10000-36705343718/` and `coinage-evidence/claims-comparison-2026-09-30/`, including `experiments.json`, verification outputs, exact test code and SHA-256 manifests. The comparison directory contains full artifacts for both successful runs. These local copies survive GitHub artifact expiry; they are not website downloads.

### Preserved reconciliation evidence

- [Combined analysis](evidence/reconciliation-2026-09-30/analysis.json) and [checksums for these published files](evidence/reconciliation-2026-09-30/SHA256SUMS.txt).
- Run 36537079387: [40 reconciled receipts, CSV](evidence/reconciliation-2026-09-30/36537079387/reconciled/dropped-receipts.csv), [indexed events, JSON](evidence/reconciliation-2026-09-30/36537079387/reconciled/dropped-receipts.json), and [raw block 159734 with saved finality observations](evidence/reconciliation-2026-09-30/36537079387/original/evidence/burst/block-159734.json).
- Run 36619415692: [48 reconciled receipts, CSV](evidence/reconciliation-2026-09-30/36619415692/reconciled/dropped-receipts.csv), [indexed events, JSON](evidence/reconciliation-2026-09-30/36619415692/reconciled/dropped-receipts.json), and [raw block 173699 with saved finality observations](evidence/reconciliation-2026-09-30/36619415692/original/evidence/burst/block-173699.json).

GitHub artifacts expire after **30 days**, on **October 29–30** for these runs. The selected files linked above are retained with this documentation. The complete local archive `reconciliation-2026-09-30.tar.gz` also preserves original evidence, both People-node logs, exact test-source revisions, reconciliation scripts and per-file checksums; it is not hosted as a website download. Its SHA-256 is `2a350dc0db20d763c3c98fb3c26bce15addb71b7b95bb23d07f8d6e091b13d19`. Original results were not overwritten; derived findings remain under `reconciled/`. These checks establish consistency of saved local RPC evidence, not an independent cryptographic proof of consensus.

[topups-1000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36534910589
[claims-1000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36514698770
[topups-10000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36537079387
[paced]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36560408065
[larger-pool]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36609355696
[paced-8500]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36619415692
[paced-8400]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36662212241
[guide]: https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-top-up-burst/ci/previewnet/burst-results.md
[topup-spec]: https://github.com/paritytech/technical-design/blob/indiv-non-fn-testing/designs/individuality/non-fun-tests/test-design/scenarios/top-up-burst.md
[claim-spec]: https://github.com/paritytech/technical-design/blob/indiv-non-fn-testing/designs/individuality/non-fun-tests/test-design/scenarios/claim-burst.md

[claims-default]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36705343718
[claims-paced]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719621433
[claims-enlarged]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719745986

[capacity-20000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153
[capacity-40000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912
[capacity-100000]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405
[claim-capacity-guide]: https://github.com/paritytech/polkadot-pop-e2e/blob/dfdc44a75bc91ea1610742b42b4e5278f4ad42fd/ci/previewnet/burst-results.md

[retention-million]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36859278723
[retention-validation]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36895937059
[retention-250k]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36898423397
[retention-fix]: https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270
[retention-driver]: https://github.com/paritytech/polkadot-pop-e2e/blob/932677d50e07052e62d45356a334801dc4630270/packages/chain-tests/scripts/coinage-claim-burst.ts
