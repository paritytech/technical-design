# Coinage stress-test findings

We verified a burst of **150,000 claims**, including a local re-audit of its saved receipts and final coin states. These experiments establish completed burst sizes, not the server’s physical maximum or sustainable production throughput.

Pacing and larger pool settings both produced successful 10,000-top-up runs. Later reconciliation verified all 88 dropped-watch transactions from the two incomplete runs. Those runs remain failed as 10,000-top-up experiments: one had 989 admission rejections, and the other never submitted its final 1,500 transactions.

Merchant fan-in later verified up to **20,000 transfers to one merchant**; its default-pool 10,000 burst failed in the same way. The first free-quota and offboarding cases each verified 100 unloads and are preliminary. Offboarding then passed at 1,000 people; 10,000 at once failed its completion target with 9,011 verified receipts, a p95 of about 56 minutes and only 23 unloads per block. Sent in two waves (8,000 then 2,000), all 10,000 offboards verified, and one person used a full 1,000-token allowance with every unload verified. Later, all six free-quota profiles produced results, the full lifecycle (top-up to offboard) verified end to end for 1,000 people, and an offboarding retry at 20,000 left incomplete receipt evidence.

## Consolidated stress metrics — 5 October 2026

The [detailed stress-metrics report](coinage-stress-metrics.md) brings together the saved top-up, claim, split-and-claim and recycling measurements, with timing populations, pool settings, resource samples and [downloadable extracted data](evidence/stress-metrics-2026-10-05/metrics.json).

| Flow | Verified finding | Qualification |
| --- | --- | --- |
| Top-up | Pacing and enlarged pools each completed 10,000 | Reconciled receipts retain their original latency populations. |
| Claim | 150,000 receipts and saved states independently checked | One transfer per root-seeded coin; not a full wallet flow. |
| Split-and-claim | 100,000 actors; 200,000 receipts | Two operation waves, experimental 110,000-entry pool. |
| Recycling | 40,000 receipts and ready members | Workload passed; CI shutdown failed. The 100,000 case remains incomplete. |

The lifecycle campaign records 12 workload passes, one launch-timing failure and three incomplete workloads. Two passes had CI shutdown failures. These finite bursts do not establish a production throughput ceiling. Historical observations below retain their original verification context; the detailed report includes the later independent 150,000-claim verification.

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

The million-claim attempt exposed a **load-generator memory limit**. The memory fix then passed a verified 1,000-claim validation and a successful 150,000-claim workload. These observations do not establish the chain's maximum capacity. “Claims” means one signed transfer per root-seeded source coin, not real app users or the full payment lifecycle. The smoke claim is separate and excluded.

| Experiment / run | Outcome | Requested | Submitted | Watch-finalized | Receipt-verified |
| --- | --- | ---: | --- | --- | --- |
| [Million-claim attempt][retention-million] | **Generator heap exhausted** | 1,000,000 | Not established | Not established | No complete audit |
| [Memory-fix validation][retention-validation] | **PASS** | 1,000 | 1,000 | 1,000 | 1,000 |
| [150,000-claim burst][retention-150k] | **PASS — CI and local re-audit** | 150,000 | 150,000 | 150,000 | 150,000 (CI and local verifier) |
| [250,000, attempt 3][retention-250k] | **Cancelled workflow; see attempt history** | 250,000 | 250,000 (CI summary) | 250,000 (CI summary) | 250,000 (CI verifier log; not locally re-audited) |
| [500,000, attempt 4][retention-500k] | **Cancelled workflow; see attempt history** | 500,000 | 500,000 (CI summary) | 500,000 (CI summary) | 500,000 (CI verifier log; not locally re-audited) |

**Million-claim attempt:** all claims were prepared, but the TypeScript driver exhausted its **24 GiB JavaScript heap**. The configured pool was **1,100,000 transactions / 262144 KiB**. Repeated broadcast notifications and decoded blocks were retained without bounds; no heap profile established their exact share of memory. No complete final receipt or state audit was produced. Recovery passed after the driver crashed. The submitted, successful and failed totals for the million requested claims remain unestablished.

The [memory-retention fix][retention-fix] ([PR #38](https://github.com/paritytech/polkadot-pop-e2e/pull/38)) aggregates broadcast notifications into counters and timestamps, caps retained watch observations and decoded-block caching, and writes non-broadcast watch transitions and observed block evidence during execution. It releases completed watch traces and signed wire data. Discarded individual broadcast timestamps and peer lists were not used by the existing reports or receipt audits. Receipt verification and final-state requirements remain in place, with no added pacing, automatic retries or relaxed success criteria. A local regression test processed **one million repeated notifications under a 128 MiB heap limit**. This was a synthetic notification test, not a million-transaction chain test.

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

### Successful 150,000-claim burst

[Run 36900802673][retention-150k] used the [memory-fix commit][retention-fix]: one burst, no pacing or automatic retries; pool **165,000 entries / 262144 KiB (256 MiB)**; fixture batch **5,000**; client launch target **60 seconds**; watch deadline **60 minutes**. Two People collators and the required relay validators shared one CI runner. The separate smoke claim is excluded.

| Measurement | Seconds |
| --- | ---: |
| Client submission window | 6.662 |
| Last watch receipt from burst start | 509.979 |
| Per-claim finality p50 / p95 / max (all 150,000) | 275.769 / 489.735 / 507.262 |
| Summary elapsed time | 649.976 |

CI reported **150,000 requested, submitted and finalized watch outcomes**. Its saved-evidence verifier checked 150,000 unique transactions against raw block bodies, indexed successful dispatch events and the expected Coinage event. Final coin-state checks passed for all 150,000 actors with **zero mismatches**; backing stayed **300,001 raw asset units** before and after. Recovery and the overall workflow passed. A subsequent local re-audit of result artifact **11189200900** also passed: the pinned verifier checked all **150,000 unique receipts**, and all saved source/recipient states were rechecked with zero mismatches. Receipt event recipient, instance, value and age matched those states. This checks consistency of saved RPC evidence, not cryptographic consensus.

Submission measures client launch, not node acceptance or throughput. Finality measures each claim's submission through finalized notification and receipt lookup. Summary elapsed time includes post-burst state checks but excludes fixture preparation, the subsequent aggregate receipt audit and recovery. These definitions follow the [measurement boundaries above](#verified-1000-claim-validation).

Each claim transfers a root-seeded coin: it removes the source coin and creates its replacement, adding **no net live coin**. Setup bypasses issuance and the full wallet lifecycle. This successful workload is not “150,000 users”, a server maximum, weight validation, measured execution cost or PVF deadline verification. Pool enlargement changes backlog capacity, not block-weight limits. Workload size, pool settings and harness implementation changed across experiments, so these runs do not isolate a causal performance improvement.

### Larger attempts — inconclusive failures; testing stopped

GitHub now confirms both workflows **completed with conclusion cancelled**. Cancellation and force-cancellation had been requested, and the local deferred dispatcher was stopped. No additional tests were launched for this update.

| Run | Pool entries / byte budget | Earlier attempts | Final attempt |
| --- | --- | --- | --- |
| [250,000][retention-250k] | 275,000 / 256 MiB | Attempts 1–2 lost runner communication during the combined preparation/submission step; no result artifacts from those attempts are available. | Attempt 3 cancelled; CI verifier and recovery steps passed; result artifact 11204043184 is now available. |
| [500,000][retention-500k] | 550,000 / 256 MiB | Attempt 1 lost communication during dependency/client validation, before PreviewNet started; attempts 2–3 lost communication during the combined preparation/submission step. No result artifacts from those attempts are available. | Attempt 4 cancelled; CI verifier and recovery steps passed; result artifact 11204154579 and full artifact 11204891083 are now available. |

**Later observations do not resolve the earlier disconnects.** Final-attempt logs report the submitted/watch-finalized/CI-verified totals shown above, zero coin-state mismatches and unchanged fixture backing. These are CI reports, not a local re-audit of the larger artifacts, and the cancelled workflows are not labelled full-run passes. Their attempt histories remain separate from the earlier failed attempts. A disconnect annotation cannot distinguish resource exhaustion, runner termination or infrastructure/network problems. Those failures are inconclusive: they do not establish OOM, pool failure, chain failure or a capacity limit. Testing has stopped; no chain maximum or production readiness has been established.

See the site-relative [claim scenario](scenarios/claim-burst.md#measurements-and-limits) and [receipt methodology](#how-verification-works). The [small evidence report](evidence/claims-retention-2026-10-02/summary-provenance.json) and [checksum](evidence/claims-retention-2026-10-02/SHA256SUMS.txt) preserve selected summaries, provenance and attempt observations. They are not full raw artifacts. GitHub artifacts expire after 30 days; downloaded evidence is retained locally outside the repository.

The validation evidence and checksum manifest are preserved locally under `coinage-evidence/claims-retention-2026-10-02/`; they are not public downloads. The recorded independent validation timestamp is **2026-10-01 17:18:52 UTC** (2 October locally). Original observations remain separate from later verification. See the existing [claim scenario][claim-spec] and [claim methodology][claim-capacity-guide] for workload and measurement boundaries.

## Completed lifecycle campaign — 3 October 2026

**The split-and-claim pilot completed 100,000 fixed-plan actors across two waves, with 200,000 verified successful transaction receipts, using the experimental 110,000-entry pool configuration.** Across the campaign, all **16** requested configurations reached real submissions: **12 workload passes, one launch-timing failure and three incomplete workloads**. Two workload passes have separate CI shutdown failures; the campaign and its CI jobs did not all pass.

- **Scenario A — [split and claim](scenarios/payment-burst.md#next-pilot-split-and-claim):** each actor splits a predefined coin into payment and change, then claims the payment output into a recipient account. A complete case has N splits followed by N claims: **two transactions per actor**.
- **Scenario B — [recycling](scenarios/synchronised-recycling.md#next-pilot-coin-loads-into-one-recycler-collection):** each actor loads one existing coin into a recycler. Ring-root coverage is observed separately: **one transaction per actor, plus readiness observation**.

These fixed-plan chain tests do not exercise a production wallet planner, chat delivery, TrUAPI or the full mobile-app payment experience. Fixtures seed sufficient-instance coins and backing before measurement, bypassing issuance and wrapped-asset hold setup. These operations do not perform external-asset top-up debits.

### Lifecycle outcome matrix

Pool entries below apply to each People collator. **Recovered** means a later run succeeded after an earlier setup or runner failure; the earlier attempt remains failed. Per-case links identify the relevant job. The [full report's original-attempt column](lifecycle-campaign-results.md#outcomes) preserves the earlier outcomes separately.

| Scenario / job | Actors / scheduling | Pool entries | Final outcome |
| --- | --- | --- | --- |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/110910965456) | 100 burst | Default | Pass: 100 splits + 100 claims |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111088217155) | 1,000 burst | Default | Recovered pass: 1,000 splits + 1,000 claims |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111091066111) | 10,000 burst | Default | Incomplete: 8,192 split receipts; claims withheld |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/job/111191304293) | 100 burst | Default | Recovered pass: 100 receipts and ready members |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111094675197) | 1,000 burst | Default | Pass: 1,000 receipts and ready members |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111097683539) | 10,000 burst | Default | Incomplete: 8,724 verified receipts; 5,002 observed ready |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111101176047) | 8,000 + 2,000 paced | Default | Pass: 10,000 splits + 10,000 claims |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111104686208) | 10,000 burst | 11,000 | Recovered pass: 20,000 total receipts |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111108401107) | 8,000 + 2,000 paced | Default | Pass: 10,000 receipts and ready members |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111112313624) | 10,000 burst | 11,000 | Pass: 10,000 receipts and ready members |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/job/111193589926) | 20,000 burst | 22,000 | All 40,000 receipts and state checks verified; launch-timing failure |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111118958519) | 40,000 burst | 44,000 | All 80,000 receipts verified; workload passed, CI shutdown timeout |
| [Split + claim](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111148834636) | 100,000 burst | 110,000 | All 200,000 receipts verified; workload and CI passed |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111156205276) | 20,000 burst | 22,000 | Pass: 20,000 receipts and ready members |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/job/111198244482) | 40,000 burst | 44,000 | All 40,000 receipts and ready members verified; workload passed, CI shutdown failure |
| [Recycling](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/job/111181352051) | 100,000 burst | 110,000 | Incomplete: 60,990 receipts verified; 39,917 observed ready |

### Incomplete workloads, timing and shutdown

- **Default recycling, 10,000:** 8,479 original watched receipts plus **245 reconciled = 8,724 verified**; **1,276** have no verified receipt. Readiness was observed for **5,002** members; **4,998** remained unobserved at **247.079 s**. Finality percentiles retain the original **8,479** population; reconciliation supplies no new latency samples.
- **Split and claim, 20,000 / 22,000-entry pool:** the corrected rerun verified **20,000 splits + 20,000 claims** and expected state. Split launch took **1,099.643 ms** against a **1,000 ms** target: a generator-limited timing failure, not failed transaction execution. The correction let claims proceed after valid split receipts/state while retaining the failed timing criterion. The earlier attempt-2 timing gate had withheld claims; it remains a separate observation.
- **Recycling, 40,000 / 44,000-entry pool:** all **40,000 receipts, expected states and ready members** were independently checked in the final audit, with no unresolved receipts or readiness. Backing stayed at **80,001** units. The workload passed; CI failed because a TCP socket remained after the two-minute shutdown deadline. Socket ownership and root cause are unestablished. Recovery passed in **64.917 s**, after the shutdown guard. Split-and-claim at 40,000 also passed its workload but hung until the CI timeout; recovery was checked afterward.
- **Recycling, 100,000 / 110,000-entry pool:** all **100,000** calls were submitted. **60,982** original watched receipts plus **eight reconciled = 60,990 verified**; **39,010** lack verified receipts. Readiness was observed for **39,917** members; **60,083** remained unobserved at **1,797.949 s**. State showed **61,851 member entries**, including **861 state-only outcomes without receipts**; this is not a receipt count. Saved block evidence omits **173363, 173365 and 173366**. Finality uses the original **60,982** population. Completed stage duration is **unavailable**; the per-wave settlement window is not a substitute. Recovery passed and backing stayed unchanged.

Missing receipts do not prove that transactions never executed. Unobserved readiness does not prove that members never became ready. State changes alone do not establish successful transaction receipts.

### Selected lifecycle timings and resources

All timing values are **seconds**. Rows use main campaign attempt 2 unless marked targeted. Each percentile uses only its stated observed population; no latency is assigned to reconciled receipts or unobserved members.

| Case / measurement | Population | Launch | p50 / p95 / max |
| --- | ---: | ---: | --- |
| Split + claim 100,000 / split finality | 100,000 receipts | 4.956 | 207.971 / 371.987 / 389.557 |
| Split + claim 100,000 / claim finality | 100,000 receipts | 4.365 | 172.573 / 318.680 / 332.599 |
| Recycling 10,000 default / finality | 8,479 watched receipts | 0.383 | 133.680 / 217.971 / 229.942 |
| Recycling 10,000 default / readiness | 5,002 observed members | — | 150.951 / 226.736 / 231.871 |
| Recycling 40,000 targeted / finality | 40,000 receipts | 1.428 | 606.384 / 1095.313 / 1143.690 |
| Recycling 40,000 targeted / readiness | 40,000 observed members | — | 910.867 / 1485.140 / 1558.509 |
| Recycling 100,000 / finality | 60,982 watched receipts | 3.692 | 925.565 / 1709.561 / 1794.058 |
| Recycling 100,000 / readiness | 39,917 observed members | — | 992.583 / 1718.515 / 1797.529 |

| Case | Stage duration (s) | Readiness cutoff (s) | Driver sampled peak RSS (GiB) | Runner cgroup sampled peak (GiB) |
| --- | ---: | --- | ---: | ---: |
| Split + claim 100,000 | 1041.877 | Not applicable | 1.992 | 30.870 |
| Recycling 40,000 targeted | 1563.826 | 1558.766 | 2.431 | 25.027 |
| Recycling 100,000 | Unavailable | 1797.949 | 4.390 | 31.964 |

“Burst” describes a submission window, not simultaneous execution in one block. Finality measures client submission to observation of a successful finalized receipt, including client/RPC overhead. Readiness measures submission to the first finalized poll showing root coverage; it includes polling delay and is **not wallet privacy readiness**. Stage duration includes workload audits, applicable inter-wave signing and readiness observation; it excludes network setup, fixture preparation, the one-actor smoke and post-workload recovery. Recovery duration measures the check, not automatically queue-drain time.

Resource values are sampled peaks. Driver RSS can include fixture preparation and smoke; runner cgroup memory includes multiple processes. [Full timing/resource tables](lifecycle-campaign-results.md#resource-observations) retain the observation windows. Pool-maintenance counters cover those windows and are not direct runtime execution timings. Different pool settings and measurement windows prevent a simple causal comparison.

### Lifecycle configuration and evidence

Evidence was audited on **2026-10-03 UTC**, as recorded in the [final report](lifecycle-campaign-results.md) ([pinned audited revision](https://github.com/paritytech/technical-design/blob/e26a47902fa1cbc1a9dd5dca80d1dc5a2657a508/designs/individuality/non-fun-tests/test-design/lifecycle-campaign-results.md)). This page summarizes that audit; publishing it did not rerun the workloads or independently repeat the full raw-data audit.

- **Main campaign:** [attempt 2](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2), test commit [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46). The generic run page may show cancelled attempt 3, which stopped before network preparation or workload submission; it does not replace attempt-2 findings.
- **Targeted reruns:** [recycling-100 and split-and-claim-20,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842), and [recycling-40,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129), test commit [`ba4bdee5c1a4`](https://github.com/paritytech/polkadot-pop-e2e/commit/ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c).
- **Environment:** PreviewNet engine `7907a3bfa7b2e47535a74b7920086a05ca94773a`, snapshot bundle run **36614342201**; six relay validators, two People collators and the snapshot's other parachains on one runner; zero synthetic delay. Both People collators used the stated enlarged entry limits and **262,144 KiB** byte budget. Default cases applied no pool override. No individual transaction retries.
- **Scheduling:** the [configuration check](evidence/lifecycle-2026-10-03/saved-configuration-verification.json) and [schedule check](evidence/lifecycle-2026-10-03/sequential-schedule-verification.json) record sequential scheduling and no overlap among **27** saved driver executions. Lost-runner records cannot establish orphaned-process lifetime.

Download the committed [completion audit](evidence/lifecycle-2026-10-03/campaign-completion-audit.json), [case inventory](evidence/lifecycle-2026-10-03/case-inventory-check.json), [observation snapshot](evidence/lifecycle-2026-10-03/observations.json) and [evidence manifest](evidence/lifecycle-2026-10-03/manifest.json). Detailed checks cover [corrected split-and-claim-20,000](evidence/lifecycle-2026-10-03/a20000-targeted-workload-verification.json), [recycling-40,000 receipts/state](evidence/lifecycle-2026-10-03/b40000-targeted-verification.txt), [its readiness](evidence/lifecycle-2026-10-03/b40000-targeted-readiness-verification.json), [shutdown diagnostic](evidence/lifecycle-2026-10-03/b40000-targeted-shutdown-error.json), and recycling-100,000 [receipts](evidence/lifecycle-2026-10-03/b100000-receipts-reconciliation.json), [readiness](evidence/lifecycle-2026-10-03/b100000-readiness-verification.json), [state](evidence/lifecycle-2026-10-03/b100000-state-observation.json) and [block coverage](evidence/lifecycle-2026-10-03/b100000-block-coverage.json).

The final audit records **24 raw archives preserved locally with hashes checked**; the final recycling-40,000 archive also matched GitHub's published digest. The manifest supplies artifact IDs, SHA-256 hashes, expiry dates and additional GitHub download links. GitHub artifacts have **30-day retention**. The committed summaries are served with this site; the raw archives are only retained locally and are not public website downloads. Summaries and hashes alone cannot reproduce the full receipt audit.

Saved local RPC observations are not independent cryptographic consensus proofs. The campaign establishes neither a production capacity ceiling nor unlimited scalability, measured runtime-weight accuracy, block execution wall time or PVF deadline compliance.

## Remaining-flow burst tests — 6–7 October 2026

**Merchant fan-in verified up to 20,000 transfers to one merchant.** Five of six cases passed. The default-pool burst of 10,000 failed, as earlier claim and top-up bursts did. The first free-quota and offboarding cases each verified **100 unloads**; both are preliminary single cases.

### Merchant fan-in outcomes

[Run 37510457575, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1), test commit [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5). Each transfer is a claim into a fresh destination key of one merchant, from a fixture-prepared coin. It does not include chat delivery or the production wallet. Attempt 2 was queued automatically and cancelled before any job ran; it has no results.

| Transfers / job | Pattern | Pool | Watch-finalized | Receipt-verified | State-verified | Finality p50 / p95 / max (N) | Result |
| --- | --- | --- | ---: | --- | ---: | --- | --- |
| [100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112480491326) | Burst | Default | 100 | 100 | 100 | 35.72 / 35.72 / 35.73 s (100) | **PASS** |
| [1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112487225834) | Burst | Default | 1,000 | 1,000 | 1,000 | 30.42 / 30.45 / 30.45 s (1,000) | **PASS** |
| [10,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112493393120) | Burst | Default | 8,193 | 8,193 original + 818 reconciled = 9,011 | 9,011 | 41.25 / 45.31 / 45.35 s (8,193) | **FAIL** — completion target |
| [10,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112500858287) | Waves 8,000 + 2,000 | Default | 10,000 | 10,000 | 10,000 | 45.46 / 57.26 / 57.27 s (10,000) | **PASS** |
| [10,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112509307852) | Burst | Enlarged: 11,000 entries / 256 MiB | 10,000 | 10,000 | 10,000 | 49.47 / 61.18 / 61.21 s (10,000) | **PASS** |
| [20,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112517391792) | Burst | Enlarged: 22,000 entries / 256 MiB | 20,000 | 20,000 | 20,000 | 59.15 / 91.16 / 91.38 s (20,000) | **PASS** |

Client launch windows were 0.006, 0.080, 0.543, 0.442 + 0.116 (paced), 0.474 and 0.950 s. They measure the client, not chain throughput. The [one-transfer smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112430856228) passed. The five passing cases were rechecked locally with `verify-remaining-flow.py`.

**Default-pool 10,000 reconciliation.** All 10,000 transfers were sent. 989 were rejected immediately at pool entry (`1016`, pool limit) and 818 watches were dropped. The run's receipt audit verified 8,193. On **7 October 2026** all 818 dropped watches were reconciled offline: each was in a saved, canonical, finalized block (173195–173198, both People nodes' views), with a matching extrinsic hash, `System.ExtrinsicSuccess` and `Coinage.CoinTransferred`. None of the 989 rejected transactions appears in a saved block. Receipt-verified is therefore 8,193 + 818 = **9,011**, equal to the state-check count. Reconciliation adds receipts, not timing samples, so finality stays on N = 8,193. The case **remains failed** as a 10,000-transfer experiment and was not rerun.

Pacing and an enlarged pool each completed the tested merchant bursts; a single 10,000 burst on the default pool did not. This matches the earlier claim and top-up pattern. These separate runs do not establish a latency trend, sustainable throughput or production capacity.

### Free-quota exhaustion and offboarding — preliminary

All runs used the default pool unless marked enlarged. Quota 100, offboarding 100 and offboarding 1,000 used test commit [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55); offboarding 10,000 at once used [`4a652d912e9d`](https://github.com/paritytech/polkadot-pop-e2e/commit/4a652d912e9d38c02a9c41e7496bf1acca41cdbd); offboarding 10,000 in waves used [`42f2e8d99753`](https://github.com/paritytech/polkadot-pop-e2e/commit/42f2e8d997531e0731a8551147badca4bb55456e); quota 1,000 used [`fd826a3843e1`](https://github.com/paritytech/polkadot-pop-e2e/commit/fd826a3843e1a6a40990a616bcbf3de8be400fb2). Receipts were re-verified offline from saved raw blocks with `verify-remaining-flow.py` on 7–8 October 2026.

| Case / run | People / unloads | Setup top-ups | Receipt-verified | Finality p50 / p95 / max (N) | Result |
| --- | --- | --- | ---: | --- | --- |
| [Free quota, 100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37570768389/attempts/1) | 1 / 100 | 100 / 100 finalized | 100 | 43.08 / 55.02 / 55.02 s (100) | **PASS** — preliminary |
| [Offboarding, 100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37590878841/attempts/1) | 100 / 100 | 100 / 100 finalized | 100 | 49.16 / 61.12 / 61.12 s (100) | **PASS** — preliminary |
| [Offboarding, 1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37593396451/attempts/1) | 1,000 / 1,000 | 1,000 / 1,000 finalized | 1,000 | 152.5 / 272.6 / 284.5 s (1,000) | **PASS** — preliminary |
| [Offboarding, 10,000 at once](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37606103903/attempts/1) | 10,000 / 10,000 | 10,000 / 10,000 finalized | 8,922 original + 89 reconciled = 9,011 | 2,673.2 / 3,333.1 / 3,341.9 s (8,922) | **FAIL** — completion target; final state not observed |
| [Offboarding, 10,000 in waves (8,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/attempts/1) | 8,000 / 8,000 | 10,000 / 10,000 finalized (both waves) | 8,000 | 1,779.5 / 2,317.0 / 2,322.8 s (8,000) | **PASS** — preliminary |
| [Offboarding, 10,000 in waves (2,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/attempts/1) | 2,000 / 2,000 | (shared with wave 1) | 2,000 | 287.9 / 520.0 / 544.1 s (2,000) | **PASS** — preliminary |
| [Free quota, 1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37690106740/attempts/1) | 1 / 1,000 | 1,000 / 1,000 finalized | 1,000 | 156.5 / 276.6 / 288.6 s (1,000) | **PASS** — full allowance used; preliminary |
| [Free quota, 10,000 at once](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37733097599/attempts/1) | 10 / 10,000 | 10,000 / 10,000 finalized | 8,921 original + 90 reconciled = 9,011; 989 rejected | 2,682.3 / 3,347.2 / 3,355.9 s (8,921) | **FAIL** — completion target |
| [Free quota, 10,000 in waves (8,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37751232138/attempts/1) | 10 / 8,000 | 10,000 / 10,000 finalized (both waves) | 8,000 | 1,787.0 / 2,324.0 / 2,329.6 s (8,000) | **PASS** |
| [Free quota, 10,000 in waves (2,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37751232138/attempts/1) | (same 10) / 2,000 | (shared with wave 1) | 2,000 | 288.2 / 524.3 / 548.3 s (2,000) | **PASS** |
| [Free quota, 10,000 at once, enlarged (11,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37772925410/attempts/1) | 10 / 10,000 | 10,000 / 10,000 finalized | 10,000 | 2,743.6 / 3,577.0 / 3,588.5 s (10,000) | **PASS** |
| [Free quota, 20,000 at once, enlarged (22,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37800522275/attempts/1) | 20 / 20,000 | 20,000 / 20,000 finalized | 4,823 original + 15,162 reconciled = 19,985; 15 unresolved | 3,558.2 / 8,594.3 / 8,714.9 s (4,823) | **FAIL** |
| [Offboarding, 20,000 at once, enlarged (22,000), retry](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37694191834/attempts/1) | 20,000 / 20,000 | 20,000 / 20,000 finalized | 4,165 original + 2,614 reconciled = 6,779; 13,221 unresolved | 2,596.9 / 6,306.9 / 7,630.7 s (4,165) | **FAIL** — incomplete receipt evidence |

**Offboarding 10,000 at once.** 989 unloads were rejected at pool entry (`1016`, pool limit) and 89 watches were dropped. Reconciliation found all 89 as successful unloads in saved finalized blocks; none of the 989 rejected transactions is in the saved blocks (175287–175678). Finality stays on the 8,922 original watches. The driver stopped at its receipt-audit assertion, so the final balance, held-backing and token snapshot was **not observed**; no state-correctness claim is made. This is a valid overload result and is not rerun for a pass. An earlier dispatch (run 37603781867) was cancelled and has no result. Every full unload block held **23 unloads** and ended with `HitBlockWeightLimit`, so this burst needed 392 blocks; see the [report](coinage-stress-metrics.md#how-many-unloads-fit-in-a-block). Offboarding 10,000 in waves ([run 37645548491](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/attempts/1)) has since completed.

**Offboarding 10,000 in waves.** Wave 2 was released after wave 1 settled. All 10,000 receipts are original; none were reconciled and none are missing. Held backing was 4,000 after wave 1 and 0 after wave 2, with free backing 1, as expected. Recovery passed. Each wave's percentiles are reported separately. Pacing completed 10,000 offboards on the default pool, where one burst of 10,000 did not, the same pattern as top-up, claim and merchant fan-in. This is not a sustained unload rate.

**Free quota 1,000: first full allowance.** The allowance limit was 1,000, so one person made all 1,000 requests and used every free token in the period: 1 person, 1,000 transactions. Both negative probes ran after that: reusing a consumed token was rejected with custom error 57, and counter 1,000 with custom error 58. This shows a complete allowance used up. It does not show period rollover or wallet behaviour when the quota is gone.

**Free quota 10,000 and 20,000 (commit [`7f269bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419)).** People = requests ÷ 1,000. The default-pool 10,000 burst repeated the 989-rejected, 9,011-admitted pattern; all 90 dropped watches reconciled, and the final state agrees (9,011 credited, 989 not, held backing 1,978). The paced and enlarged 10,000 runs verified every receipt, and all 20 negative probes in each were rejected as designed (errors 57 and 58). At 20,000 enlarged, only 4,823 watches finalized and 15,176 reported "invalid"; reconciliation showed 15,162 of those succeeded, leaving 15 unresolved. The 15 unconsumed tokens in final state are on the same 15 actors, which is consistent with, but not proof of, those 15 not completing. Negative probes were not reached, and CI timed out at shutdown after the workload, a separate outcome. With all six quota profiles measured, the burst measurements are no longer preliminary; period rollover and native policy remain untested.

**Offboarding 20,000 enlarged retry (commit [`e163be9`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52)).** 4,165 watches finalized, 15,831 reported "ready, then invalid" and 4 hit RPC errors. Reconciliation added 2,614, so 6,779 receipts are proven and 13,221 are unresolved. The run predates the block-saving fix, so 911 of 1,206 block heights in range were never saved. Final state (held backing 0, free backing 1, every actor observed) is consistent with all offboards completing but is not receipt evidence: this is incomplete evidence, not "6,779 of 20,000 succeeded". In both 20,000 enlarged runs, client watch status was unreliable; the cause is not established.

- **One person, 100 transactions.** The quota allowance limit was 1,000, so all 100 quota requests came from one person. This is not 100 users.
- **Negative probes.** Reusing a consumed token was rejected with custom error 57 (`UnloadTokenAlreadyConsumed`). A counter at the limit was rejected with custom error 58 (`UnloadTokenCounterOutOfRange`).
- **Proof generation, first measurement.** Each unload needs two ring-VRF proofs, one for the recycler alias and one for the free token: two proofs per unload. Recycler proofs took 1.406 s at p50 and 1.455 s at most in the quota case (1.411 / 1.479 s for offboarding). Free-token proofs took 0.786 / 0.835 s (0.827 / 0.880 s). At 1,000 offboards, recycler proofs took 1.650 / 1.749 s and free-token proofs 0.879 / 0.943 s; at 10,000, 1.648 / 1.859 s and 0.875 / 1.041 s. In the paced run, recycler proofs took 1.672 / 1.869 s (wave 1) and 1.677 / 1.834 s (wave 2), and free-token proofs 0.890 / 1.030 s and 0.889 / 1.011 s. For quota 1,000 they took 1.664 / 1.835 s and 0.797 / 0.911 s. Proofs were generated before release, so this is client preparation cost, not submission-to-receipt time.
- **Limits.** Real period rollover was not exercised. Policy rows come from a separate model, not native iOS or Android code. All six quota profiles have now run; offboarding 10,000 enlarged has no workload result and offboarding 20,000 enlarged has incomplete receipts, so there is no offboarding conclusion, and quota rollover remains untested.

### Full flow — 8–9 October 2026

A fixed plan per person: top-up → readiness → unload into a payment coin → claim → recycle → readiness → offboard (not the wallet planner). Commit [`aa72510`](https://github.com/paritytech/polkadot-pop-e2e/commit/aa72510d3fbf321b2946430db0264f50ae5d8785), default pool, verified offline with `verify-remaining-flow.py` on 9 October 2026.

| Case / run | People | Receipts | Stage p95 (s) | Result |
| --- | ---: | --- | --- | --- |
| [Smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37854332739/attempts/1) | 1 | 5 / 5 | — | **PASS** |
| [100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37855938846/attempts/1) | 100 | 500 / 500 (100 per stage) | Top-up 34.4; payment unload 61.8; claim 34.3; recycle 34.4; offboard 60.5 | **PASS** |
| [1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37858620774/attempts/1) | 1,000 | 5,000 / 5,000 (1,000 per stage) | Top-up 53.0; payment unload 296.5; claim 31.4; recycle 48.2; offboard 272.3 | **PASS** |
| [10,000 at once](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37863573263/attempts/1) | 10,000 | 0 | — | **Test-tool failure**; no chain load |

The two unload stages dominate the time: each needed 44 blocks at 1,000 people, at 23 per block. In the 10,000 run, the sender disconnected at every top-up submission (10,000 RPC errors; nothing ready, in a block or finalized), so it is not a chain result; an earlier reconciliation misclassified 94 of these errors as pool rejections and was corrected. The retry, [run 37899564808](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37899564808/attempts/1), was running at this update and is not verified. 10,000 in waves, 10,000 enlarged and 20,000 enlarged have not run.

### Setup failures, now fixed

| Scenario | What happened | What it establishes |
| --- | --- | --- |
| Free-quota exhaustion | First campaign: [smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112436114495) passed; all six measured cases ([100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112526429833), [1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112532845219), [10,000 burst](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112539289683), [10,000 paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112545534951), [10,000 enlarged](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112551090694), [20,000 enlarged](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112556615978)) stopped during fixture top-ups. The 100- and 1,000-request cases have since passed independently. | Four profiles still to run; no burst-capacity conclusion yet |
| Offboarding | Same setup failure; [smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112440932803) passed. Measured cases: [100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112561845169), [1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112567282589), [10,000 burst](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112572580926), [10,000 paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112577483596), [10,000 enlarged](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112582692332), [20,000 enlarged](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112587829742). Since then, 100, 1,000 and 10,000 paced passed independently, and 10,000 at once ran and failed its completion target (9,011 verified). | The two enlarged profiles have no result (next rows); no burst-capacity conclusion yet |
| Offboarding 10,000 enlarged | Runner lost communication twice: [run 37672641924, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37672641924/attempts/1) (attempt 2 auto-queued by `cattery-scheduler[bot]` and cancelled) and [run 37684376141, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37684376141/attempts/1). The latter's automatic attempt 2 shows "success" on GitHub, but its pilot was skipped and no workload ran; it is not a result. | No workload result; cause of the runner loss not established |
| Offboarding 20,000 enlarged | [Run 37687780845, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37687780845/attempts/1): zombienet orchestrator panic at network start (`lib.rs:842`) after an automatically allocated Prometheus port (30337) collided with a collator's fixed p2p port. Fixed in [`e163be9`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52). Retry [run 37694191834](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37694191834/attempts/1) has since run: incomplete receipt evidence (6,779 proven, 13,221 unresolved). | Retry reached the workload; see above |
| Full flow | [Smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112446686310) failed while preparing the network: GitHub reports the self-hosted runner lost communication. Six cases skipped. Independent runs since then passed smoke, 100 and 1,000; 10,000 at once hit a test-tool failure and its retry was running (see Full flow above). | Cause of the first runner loss not established; three profiles passed |

The test client sent setup top-ups through a path the node allows only 16 at a time per connection. Above that, the extra transactions were silently never sent, so only 16 of 100 setup top-ups reached the pool. This was a test-harness bug, not a chain result. The [fix](https://github.com/paritytech/polkadot-pop-e2e/commit/e9c982bb296a344d8c6629dcc8a82971c107438e) sends setup through the same submission path as the workload. A sustained-load test is in development and is not yet reportable.

Download the [case ledger](evidence/remaining-flow-2026-10-07/case-ledger-remaining-flow.json), the [merchant reconciliation](evidence/remaining-flow-2026-10-07/merchant/10000-burst-default/claim-burst-reconciliation.json) and the other selected summaries listed in the [checksum file](evidence/remaining-flow-2026-10-07/SHA256SUMS.txt). The [detailed report](coinage-stress-metrics.md#merchant-fan-in-many-payments-to-one-merchant) and [appendix](coinage-stress-metrics-appendix.md#merchant-fan-in-measurements) give the full field split. Offboarding 1,000, 10,000 at once and 10,000 in waves files, quota 1,000 files, the 10,000 reconciliation, the no-result reviews and the unloads-per-block counts are in the [8 October evidence folder](evidence/remaining-flow-2026-10-08/SHA256SUMS.txt). The larger quota cases, the offboarding 20,000 retry and the full-flow runs are in the [9 October evidence folder](evidence/remaining-flow-2026-10-09/SHA256SUMS.txt). These are selected files, not full raw artifacts.

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
| [36900802673][retention-150k] | [`932677d50e07`][retention-fix] | 150,000 CI-verified receipts and matching coin states; unchanged backing and recovery passed. Result artifact: 11189200900. Local receipt/state re-audit passed; see the evidence report for its timestamp. |
| [36898423397][retention-250k] | [`932677d50e07`][retention-fix] | Attempts 1–2 inconclusive runner disconnects; attempt 3 cancelled, with later CI verifier/recovery success and result artifact 11204043184. Not locally re-audited. |
| [36902568601][retention-500k] | [`932677d50e07`][retention-fix] | Attempts 1–3 inconclusive runner disconnects; attempt 4 cancelled, with later CI verifier/recovery success and result artifact 11204154579. Not locally re-audited. |

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

[retention-150k]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36900802673
[retention-500k]: https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36902568601
