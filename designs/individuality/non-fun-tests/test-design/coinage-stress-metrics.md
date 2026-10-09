# Coinage stress metrics

*How far we pushed five Coinage flows on a local PreviewNet, and what the numbers tell us.*

Stress testing a chain is not like stress testing a web server. A web server sends a response, and you are done. A chain transaction waits in a pool, goes into a block and then becomes final. Only then do we know if it worked.

So I use a strict rule. A workload **passed** only when every transaction has a verified receipt and the final coin state is correct. Some cases also had a launch-time target.

We ran five flows with 100 to 150,000 actors. We also tried one million. Some runs passed, some failed and some are incomplete. Here's what we found.

The exact numbers are in the [measurement appendix](coinage-stress-metrics-appendix.md). You can also [download the extracted data](evidence/stress-metrics-2026-10-05/metrics.json) and check it yourself.

Presenting this? The main insights are also in a [slide deck](coinage-stress-metrics-slides.html).

## The short version

- **10,000 top-ups and 10,000 claims.** One burst of 10,000 on the default pool did not complete. The pool rejected 989 submissions in each flow. Waves and a bigger pool both fixed this.
- **Claims at scale.** The largest verified burst was **150,000 claims**. A second, independent check found zero errors.
- **One block holds 2,363 claims.** This was true for every full block. A bigger pool lets more claims wait. It does not put more claims in a block.
- **Lifecycle campaign.** We selected 16 cases. 12 passed, one failed its launch-time target and three are incomplete. Split-and-claim with 100,000 actors verified all **200,000 receipts**.
- **Recycling is the slowest flow.** 40,000 actors passed. 100,000 actors is **incomplete**: 60,990 verified receipts and 39,917 coins seen as ready.
- **One million claims did not run.** The load generator ran out of memory. This is a limit of our tool, not of the chain.
- **Merchant fan-in.** Up to 20,000 transfers to one merchant were verified. As with top-ups and claims, one burst of 10,000 on the default pool failed, and waves and a bigger pool both completed it.
- **Unloads, preliminary.** The first free-quota and offboarding cases each verified 100 unloads. These are single small cases, not quota or offboarding conclusions.
- **Unloads are slow at scale.** One block holds only 23 unloads, against 2,363 claims. 1,000 offboards passed. 10,000 offboards at once took 56 minutes at p95, and 9,011 of 10,000 have verified receipts.
- **Waves completed 10,000 offboards, and one person used a full allowance.** Sent as 8,000 then 2,000 on the default pool, all 10,000 unloads verified. Separately, one person used all 1,000 free tokens in a period, and every unload verified.
- **The full lifecycle works end to end at 1,000, and the 10,000 pattern repeats.** 1,000 people completed top-up, payment unload, claim, recycle and offboard, with all 5,000 receipts verified. Free quota's 10,000 burst on the default pool also admitted 9,011 and rejected 989.

> These are finite bursts. They do not show a sustainable production TPS or a maximum capacity.

* * *

## What did we test?

Each test sends signed Coinage extrinsics from many test accounts. I call these accounts **actors**. The target is a local PreviewNet with two People collators.

| Flow | What one actor does | Extrinsics per actor |
| --- | --- | ---: |
| [Top-up](scenarios/top-up-burst.md) | Pays with an external test asset and gets a voucher. | 1 |
| [Claim](scenarios/claim-burst.md) | Transfers one coin. The old coin goes away and a new coin replaces it. | 1 |
| [Split-and-claim](scenarios/payment-burst.md) | Splits a coin, then claims it. | 2 |
| [Recycling](scenarios/synchronised-recycling.md) | Loads a coin into a recycler. We then wait for the coin to become ready. | 1 |
| [Merchant fan-in](scenarios/merchant-fan-in.md) | Transfers one coin to the same merchant, into a fresh destination key. | 1 |

Let me be clear: **these tests do not cover the whole wallet**. They do not include the production wallet planner, chat delivery, TrUAPI or the mobile payment screens.

Some test coins are created directly, not through normal issuance. So these tests do not prove the normal backing accounting. Setup transactions and smoke transactions are not in any count.

### Which scenarios did we cover?

We have not tested every scenario yet. Here's where each one stands.

| Scenario | Status | What we ran |
| --- | --- | --- |
| [Top-up burst](scenarios/top-up-burst.md) | Measured | 1,000 to 10,000 top-ups |
| [Claim burst](scenarios/claim-burst.md) | Measured | 1,000 to 150,000 claims |
| [Payment burst](scenarios/payment-burst.md) | Partly measured | Split-and-claim only, 100 to 100,000 actors. Exact and unload payment plans are still to come. |
| [Merchant fan-in](scenarios/merchant-fan-in.md) | Measured | 100 to 20,000 transfers to one merchant |
| [Synchronised recycling](scenarios/synchronised-recycling.md) | Measured | 100 to 100,000 coin loads into one recycler |
| [Free-quota exhaustion](scenarios/free-quota-exhaustion.md) | Measured (burst profiles) | All six profiles have results: 100, 1,000, 10,000 in waves and 10,000 with a bigger pool passed; 10,000 at once failed its target (9,011 verified); 20,000 with a bigger pool failed (19,985 verified, 15 unresolved). Period rollover and native wallet policy are not tested. |
| [Offboarding burst](scenarios/offboarding-burst.md) | Preliminary | 100, 1,000 and 10,000 in waves passed; 10,000 at once failed its completion target. 10,000 with a bigger pool lost its runner twice, with no result. 20,000 with a bigger pool has incomplete receipts: 6,779 proven, with state consistent with completion. |
| [Full-flow ramp](scenarios/full-flow-ramp.md) | Partly measured | Smoke, 100 and 1,000 people passed all five stages. 10,000 at once hit a test-tool failure; its retry is running. Three profiles not run yet. |
| [Sponsored-pot exhaustion](scenarios/sponsored-pot-exhaustion.md) | Not run yet | Loads that exceed what a sponsored pot can hold |
| [Cleanup backlog](scenarios/cleanup-backlog.md) | Not run yet | Expired-state cleanup while users keep paying |
| [Instance proliferation](scenarios/instance-proliferation.md) | Not run yet | Many Coinage instances at once |
| [Sustained load](sustained-pool-campaign.md) | In development | A three-minute full pool. Not reportable yet. |

### What machine did we test on?

Every run used the self-hosted `parity-large` GitHub runner. We saved the hardware details for the 20,000 to 100,000-claim runs:

| Part | Value |
| --- | --- |
| Machine | Google Cloud VM, Linux 6.17 |
| CPU | AMD EPYC 7B13: 16 cores, 32 logical CPUs |
| RAM | 62.8 GiB |
| Disk | 193 GB system disk |
| Chain nodes | 11 in total: 6 relay validators, 2 People collators, and 1 collator each for Asset Hub, Bulletin and Web3 Storage |
| Load generator | One Node.js process |
| Network delay | None added |

All of this runs on **one machine**. So the load generator shares the CPU and memory with the nodes that it tests.

### How busy was the machine?

We don't have a CPU or memory metric inside each node. But we saved two things every few seconds: the machine's total CPU and memory, and a process list with each process's memory and CPU time. From those, I can show how the load changed from an idle network to the burst.

#### Figure 1: What did the machine do during the 100,000-claim run?

[![Two line charts over time for the 100,000-claim run. Upper: whole-machine CPU is about 5% busy when idle, 5 to 9% during fixture preparation and averages 12% with a 21% peak during the burst; the busiest single CPU often reaches 100%. Lower: machine memory grows from about 12 GiB idle to a 19.8 GiB peak; the People collators peak at 3.4 and 2.9 GiB and the load generator at 2.8 GiB.](evidence/stress-metrics-2026-10-05/machine-resources.svg)](evidence/stress-metrics-2026-10-05/machine-resources.svg)

*Figure 1. Time runs from the network start to after the burst. The grey band is fixture preparation and the orange band is the burst. Upper panel: share of all 32 logical CPUs that were busy, and the busiest single CPU. Lower panel: memory used by the whole machine, by each People collator and by the load generator.*

So what changed? The whole machine went from about **5% busy when idle to 12% on average during the burst, with a 21% peak**. That is about 4 of the 32 CPUs on average. The machine never came close to full.

Memory went from about **12 GiB idle to a 19.8 GiB peak**. Be careful with this number. **The load generator adds to it.** It keeps every signed transaction and every watch in memory, so it grows with the burst. During fixture preparation, the machine's memory went up by about 4 GiB, and the load generator alone took about 2.5 GiB of that.

The busiest single CPU often hit 100%, also during fixture preparation, when the collators were almost idle. So a full single CPU here does not always mean a busy chain. The load generator signs on one thread, and we can't tell from these samples which process used that CPU.

Here are the three large claim bursts side by side:

| Claims | Machine CPU: idle → burst average (peak) | Machine memory: idle → burst peak | Collator 1 / 2 CPU during burst | Collator 1 / 2 memory, burst peak |
| ---: | --- | --- | --- | --- |
| 20,000 | 4.5% → 8.6% (20.7%) | 11.9 → 14.8 GiB | 0.59 / 0.44 cores | 1.80 / 1.88 GiB |
| 40,000 | 4.5% → 10.2% (25.2%) | 12.0 → 15.8 GiB | 0.98 / 0.60 cores | 2.17 / 2.16 GiB |
| 100,000 | 4.6% → 12.4% (21.3%) | 11.9 → 19.8 GiB | 1.32 / 0.66 cores | 3.38 / 2.95 GiB |

"Cores" is the average number of CPU cores that the collator process used during the burst. When idle, each People collator used about 0.02 cores and 1.4 to 1.6 GiB. So the burst made collator 1 work much harder, and its memory grew with the size of its queue. I explain why collator 1 works harder than collator 2 under [Figure 5](#figure-5-how-full-did-the-queue-get).

The [host resource data](evidence/host-resources-2026-10-07/host-resources.json) has every sample and the definitions.

### Words I use

- **Default pool:** 8,192 entries and 20 MiB for each People collator. A **bigger pool** has a larger limit for one run, for example 11,000 entries.
- **At once (burst):** we send all transactions together. **In waves (paced):** we send them in groups, for example 8,000 then 2,000.
- **Verified receipt:** we found the transaction in a finalized block, and it shows success and the correct Coinage event.
- **Finality:** the time from sending a transaction to finding its successful, finalized receipt.
- **Readiness:** the time from sending to the first time we see the coin in a finalized ring root. This includes our polling delay.
- **p95:** 95% of transactions finished in this time or less. **N** is the number of transactions that we timed.
- **Reconciliation:** a later check of saved evidence. It can find more receipts. It cannot add more timing samples.

The full definitions are in [Measurement definitions](#measurement-definitions).

## Why do these metrics matter?

You might ask, "Why not just count how many transactions the node accepted?" Let me explain.

Acceptance only tells us that a transaction got in the door. Coinage moves money. So I want to know three things: did the money move, how long did people wait, and what broke first?

- **Verified receipts and coin state** tell us if the money moved. A node can accept a transaction and then lose it. For a wallet, a payment that disappears is the worst result.
- **Finality** tells us how long a person waits for a settled payment. I use p95, not the average. The average hides the people at the back of the queue.
- **Readiness** matters for top-ups and recycling. You cannot use a new coin until it is in a ring root. Finality says the coin landed. Readiness says you can use it.
- **Pool rejections and the ready queue** show what happens when a spike arrives. A rejected transaction fails immediately. A queued transaction waits.
- **Claims per block** shows the real speed limit. A block can only hold a fixed amount of work. This limit sets how fast a queue drains.
- **Launch time and driver memory** tell us if a problem came from the chain or from our test tool.

> Acceptance tells us a transaction got in the door. **A verified receipt tells us the money moved.**

* * *

## How did each flow do?

### Top-ups: waves and bigger pools both got us to 10,000

We did six top-up runs. Four passed and two failed.

- **Passed:** 1,000 at once; 7,000 + 3,000 in waves; 10,000 at once with a bigger pool; and 8,400 + 1,600 in waves on the default pool.
- **Failed:** 10,000 at once on the default pool. The pool rejected 989 submissions, so only 9,011 have receipts.
- **Failed:** 8,500 + 1,500 in waves. We held back the second wave, so only 8,500 top-ups have receipts.

Reconciliation on 30 September 2026 found 40 and 48 more receipts in the two failed runs. This does not change the result. They **stay failed**.

The three newer runs all recovered after the test, and their backing matched the verified top-ups. The earlier runs' recovery records are in the [top-up results](measured-results.md#measured-results). The [top-up measurements table](coinage-stress-metrics-appendix.md#top-up-measurements) has the full numbers.

#### Figure 2: How long did top-ups take?

[![Grouped bar chart of top-up finality p95 and readiness p95 for six runs. The four passing runs settle in 53 to 256 seconds and become ready in 106 to 353 seconds. The two failed runs are grey.](evidence/stress-metrics-2026-10-05/topup-timing.svg)](evidence/stress-metrics-2026-10-05/topup-timing.svg)

*Figure 2. Each run has two bars. Blue is finality p95: the payment is settled. Orange is readiness p95: the voucher can be used. Grey bars are failed runs, and they show only the transactions that we timed.*

So what does this chart tell us? For the larger passing runs, 95% of top-ups settled in 183 to 256 seconds. The vouchers became ready about 80 to 100 seconds after that.

Each run has a different size, schedule and pool. The two failed runs also have fewer timed transactions, so their bars are not the full story. But when I put the runs side by side by batch size, a clear pattern shows up.

#### Figure 3: Does top-up time grow with the batch size?

[![Scatter chart of top-up p95 against the largest batch that entered the pool at once. Finality rises from 53 s at 1,000 to 256 s at 10,000, about 22 s per 1,000 top-ups. Readiness rises from 106 s to 353 s, about 28 s per 1,000. The two failed runs sit close to the same lines.](evidence/stress-metrics-2026-10-05/topup-trend.svg)](evidence/stress-metrics-2026-10-05/topup-trend.svg)

*Figure 3. The horizontal axis is the number of top-ups that entered the pool in the largest single batch: 7,000 for the 7,000 + 3,000 run, and 9,011 for the failed 10,000 burst. Filled dots are passing runs; the dashed lines are a straight-line fit through them. Hollow dots are failed runs, which are not used for the lines.*

This is the most interesting top-up result. **Time grows in a straight line with the batch size.** Each extra 1,000 top-ups in the batch added about **22 seconds** to finality p95 and about **28 seconds** to readiness p95. Every passing run is within 4 seconds of the finality line and within 8 seconds of the readiness line. The two failed runs also sit close to the lines.

In percentages: 10 times more top-ups (1,000 to 10,000) made finality p95 **383% longer** (53 to 256 seconds) and readiness p95 **234% longer** (106 to 353 seconds). Time grew slower than the batch, because part of the time is a fixed cost: about 29 seconds for finality and 76 seconds for readiness, even for a small batch.

Why a straight line? A block can only hold a fixed amount of work, so a queue drains at a steady rate. For finality, 22 seconds per 1,000 top-ups is about 45 top-ups per second. We see the same steady drain for claims in [Figure 6](#figure-6-how-many-claims-fit-in-one-block).

Keep this in proportion. There are only four passing runs. They differ in pool, schedule and harness version, and the p95 for a run in waves covers both waves. So this is a strong pattern, not a proven model.

### Claims: the lightest flow, and the biggest bursts

Claims are where we pushed the hardest. Let's start with the run that didn't work.

The 10,000 burst on the default pool verified only **8,192** claims. The pool rejected 989 submissions immediately, and we lost the watch on 819 more. At the saved cutoff, those 819 coins had not changed.

Every other claim run passed. Each claim removed the old coin and created the correct new coin. The fixture backing did not change in any run.

We checked the **150,000** run again on **2 October 2026 at 03:05 UTC**, with a separate verifier. It found 150,000 receipts and 150,000 correct coin states, with zero errors.

> 150,000 claims, 150,000 verified receipts, **zero errors**.

What about one million? We tried. The load generator used all of its 24 GiB of memory before it finished. So we have no receipts to check. **This is a limit of our tool, not of the chain.** The [fix](https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270) makes the tool keep less data in memory. We tested the fix with one million fake notifications, not with one million real transactions.

The [claim measurements](coinage-stress-metrics-appendix.md#claim-measurements) table has all launch times and stage times.

#### Figure 4: How long did the slowest claims wait?

[![Range plot of claim finality. At 20,000 claims p50 is 66 s and p95 is 94 s. At 40,000 claims p50 is 92 s and p95 is 139 s. At 100,000 claims p50 is 179 s, p95 is 297 s and p99 is 306 s.](evidence/stress-metrics-2026-10-05/claim-finality.svg)](evidence/stress-metrics-2026-10-05/claim-finality.svg)

*Figure 4. Each line goes from p50 (the open circle) to p99 (the diamond). The filled circle is p95. Every run timed all of its claims.*

What do the three marks mean?

- **p50:** half of the claims settled faster than this. It's the typical wait.
- **p95:** 95% settled faster. Only the slowest 1 in 20 took longer.
- **p99:** 99% settled faster. Only the slowest 1 in 100 took longer.

So why are p95 and p99 almost the same, like 139 and 140 seconds at 40,000? Because the slowest claims all leave in the last block. The slowest 5% of 40,000 claims is 2,000 claims, and one block holds up to 2,363 ([Figure 6](#figure-6-how-many-claims-fit-in-one-block)). So the slowest 5% and the slowest 1% settle together in the same final block. At 20,000 it's the same: the slowest 5% is 1,000 claims, all in the last block.

At 100,000 the slowest 5% is 5,000 claims, which is more than two blocks. So p95 and p99 land in different blocks near the end, and they're 9 seconds apart: 297 and 306 seconds. In every run, there was no long tail of very slow claims. Claims waited in a queue, and the queue drained at a steady rate.

These are three separate setups with different pool limits. Don't draw a line through them.

#### Figure 5: How full did the queue get?

[![Three line charts of claims waiting in each collator's ready queue. Collator 1 peaks at 20,000, 37,637 and 88,185 claims. Both queues are empty at about 75, 116 and 293 seconds.](evidence/stress-metrics-2026-10-05/pool.svg)](evidence/stress-metrics-2026-10-05/pool.svg)

*Figure 5. One panel for each burst size. The lines show how many claims waited in each People collator's ready queue. The grey line shows when both queues were empty.*

The queue filled up in the first 10 to 50 seconds. Then it went down at a steady rate until it was empty. That steady rate matches the fixed number of claims in each block (Figure 6).

We sampled the queue every five seconds, so we can miss short peaks.

Why does collator 1 hold so many more claims than collator 2? At 100,000 claims it peaked at 88,185, and collator 2 at only 18,821. **Our load generator sends every claim to collator 1.** Its RPC address is collator 1 (port 10010), and that's the only node it talks to. Collator 2 only gets the claims that collator 1 passes on over the peer-to-peer network. The node passes transactions on in batches, and collator 2 must check each one before it enters its own queue. So collator 2 holds fewer at any moment. This is our reading of the setup; we did not measure the gossip itself.

The CPU numbers agree. During the 100,000 burst, collator 1 used 1.32 cores and collator 2 used 0.66 cores (see [How busy was the machine?](#how-busy-was-the-machine)).

Can we split the work evenly? Yes, but it's a test change, not a chain change: the load generator could send half of the claims to each collator. Both queues still empty at the same time, because a claim leaves both queues as soon as it is in a block. A real wallet population would also spread over many RPC nodes, so the even split is closer to production.

#### Figure 6: How many claims fit in one block?

[![Three bar charts of verified claims in each block. Every full block holds 2,363 claims. The last block in each run holds fewer: 1,096, 2,192 and 754.](evidence/stress-metrics-2026-10-05/blocks.svg)](evidence/stress-metrics-2026-10-05/blocks.svg)

*Figure 6. Each bar is one finalized block. Blue bars are full blocks. The grey bar is the last block, which held the claims that were left.*

This is the clearest result in the report. **Every full block held exactly 2,363 claims.** In the 100,000 run, all 42 full blocks stopped because they hit the block weight limit.

This also explains Figure 5. The pool decides how many claims can wait. The block weight limit decides how fast they leave. Each new block takes about 2,363 claims out of the queue, so the lines in Figure 5 go down in a straight line.

> A bigger pool lets more claims wait. **It doesn't make blocks hold more claims.**

What about the machine? Average CPU use peaked at 21–25%. That looks relaxed. But one CPU core reached about 98% in the 100,000 run. So a low average does not rule out a single-thread limit.

The test tool also used more memory as the bursts got larger:

| Claims | Driver memory (RSS) | JavaScript heap |
| ---: | ---: | ---: |
| 20,000 | 1.189 GiB | 0.558 GiB |
| 40,000 | 1.688 GiB | 0.946 GiB |
| 100,000 | 2.820 GiB | 1.567 GiB |

This is the test tool's memory, not the chain's memory. See the [claim resources table](coinage-stress-metrics-appendix.md#claim-resources).

### Split-and-claim and recycling: the lifecycle campaign

The lifecycle campaign ran 16 cases: eight for split-and-claim and eight for recycling. Before we look at timing, let's see what finished.

#### Figure 7: How many extrinsics have a verified receipt?

[![Bar chart of verified receipts as a share of requested extrinsics for 16 lifecycle cases. 13 cases reach 100%. Split-and-claim at 10,000 on the default pool reaches 41%, recycling at 10,000 on the default pool 87% and recycling at 100,000 61%.](evidence/stress-metrics-2026-10-05/lifecycle-completion.svg)](evidence/stress-metrics-2026-10-05/lifecycle-completion.svg)

*Figure 7. Each bar shows verified receipts divided by requested extrinsics. Split-and-claim requests two extrinsics for each actor. Grey bars are cases that did not pass.*

Most cases reached 100%. Three did not:

- **Split-and-claim, 10,000 at once, default pool:** 8,192 of 10,000 splits verified. We did not send the claims.
- **Recycling, 10,000 at once, default pool:** 8,724 of 10,000 verified.
- **Recycling, 100,000:** 60,990 of 100,000 verified.

One case reached 100% and still failed. Split-and-claim with 20,000 actors verified all 40,000 receipts. But our tool took 1.10 seconds to launch the splits, and the target was 1.00 second. So it is a **launch-time failure**. This is why I keep each outcome separate.

Two cases passed, but CI did not shut down cleanly after the test. These are split-and-claim at 40,000 and recycling at 40,000. The workload result and the CI result are separate.

#### Figure 8: How long did split-and-claim take?

[![Grouped bar chart of split p95 and claim p95 for eight split-and-claim cases. At 100,000 actors split p95 is 372 s and claim p95 is 319 s.](evidence/stress-metrics-2026-10-05/split-claim-timing.svg)](evidence/stress-metrics-2026-10-05/split-claim-timing.svg)

*Figure 8. Blue is the split step and orange is the claim step. Both bars show finality p95. For the run in waves, the bars show the first wave of 8,000. Grey bars are cases that did not pass.*

Up to 10,000 actors, both steps settled in about 25 to 65 seconds. At 100,000 actors, splits took 372 seconds and claims took 319 seconds.

The [split-and-claim wave timings](coinage-stress-metrics-appendix.md#split-and-claim-wave-timings) table has every wave.

#### Figure 9: How long did recycling take?

[![Grouped bar chart of recycling finality p95 and readiness p95. Readiness p95 grows from 50 s at 100 actors to 1,485 s at 40,000 actors. The two incomplete cases are grey.](evidence/stress-metrics-2026-10-05/recycling-timing.svg)](evidence/stress-metrics-2026-10-05/recycling-timing.svg)

*Figure 9. Blue is finality p95: the load is settled. Orange is readiness p95: the coin is in a ring root. Grey bars are incomplete cases, and they show only the part that we observed.*

Recycling is much slower than the other flows. At 40,000 actors, 95% of coins became ready in 1,485 seconds. That is almost 25 minutes.

Be careful with the 100,000 bar. It shows 1,719 seconds, but only for the 39,917 coins that we saw before we stopped looking at 1,798 seconds. The other 60,083 coins have no timing. So the real p95 for 100,000 is not known.

Here's the tricky part with the 100,000 case. **A missing receipt does not prove that a transaction failed.** But a state change alone does not prove a successful receipt either. Three blocks are also missing from the saved evidence. So I call it incomplete, and I don't guess in either direction.

See the [recycling outcomes](coinage-stress-metrics-appendix.md#recycling-outcomes) and [recycling readiness](coinage-stress-metrics-appendix.md#recycling-readiness) tables.

#### Figure 10: What happens to recycling time when the burst doubles?

[![Line chart of recycling p95 at 10,000, 20,000 and 40,000 actors with a bigger pool. Finality goes 233, 616 and 1,095 s, adding 382 then 479 s. Readiness goes 354, 810 and 1,485 s, adding 456 then 675 s.](evidence/stress-metrics-2026-10-05/recycling-growth.svg)](evidence/stress-metrics-2026-10-05/recycling-growth.svg)

*Figure 10. Passing recycling cases with a bigger pool. Each step on the horizontal axis doubles the number of actors. The coloured numbers are the added seconds for each doubling. The incomplete 100,000 case is not shown, because its p95 covers only part of the burst.*

There's an interesting pattern here. Each time the burst doubled, finality p95 went up by about **400 to 500 seconds** (+382, then +479) and readiness p95 by about **450 to 700 seconds** (+456, then +675).

The step is not the same each time; it grew. And three points can't tell us the exact shape of the curve. To know, we need a passing case between 40,000 and 100,000, such as 80,000.

Split-and-claim grows more slowly. Its split p95 went from 61 seconds at 10,000 actors to 372 seconds at 100,000: about 3.5 seconds per 1,000 actors (Figure 8).

### What happens when 10,000 arrive at once on the default pool?

Every flow ran one burst of 10,000 on the default pool. **Every one of them rejected exactly 989 transactions at the door.** Here's what happened to all 10,000 in each flow:

| Flow | Rejected at pool entry | Watch lost | Verified receipts | No verified receipt |
| --- | ---: | --- | ---: | ---: |
| Top-up | 989 (9.9%) | 40, all found later | 9,011 (90.1%) | 989 (9.9%) |
| Claim | 989 (9.9%) | 819; the coins had not changed at the cutoff | 8,192 (81.9%) | 1,808 (18.1%) |
| Merchant fan-in | 989 (9.9%) | 818, all found later | 9,011 (90.1%) | 989 (9.9%) |
| Split (first step of split-and-claim) | 989 (9.9%) | 819, none found | 8,192 (81.9%) | 1,808 (18.1%) |
| Recycling | 989 (9.9%) | 532, of which 245 found later | 8,724 (87.2%) | 1,276 (12.8%) |
| Offboarding (run later, 7 October) | 989 (9.9%) | 89, all found later | 9,011 (90.1%) | 989 (9.9%) |
| Free quota (run later, 8 October) | 989 (9.9%) | 90, all found later | 9,011 (90.1%) | 989 (9.9%) |

Why exactly 989? Because 10,000 − 989 = 9,011, and 9,011 = 8,192 + 819. The default pool has 8,192 slots for ready transactions. Substrate also keeps a second queue for transactions that can't run yet, [one tenth of that size](https://github.com/paritytech/polkadot-sdk/blob/master/substrate/client/transaction-pool/src/builder.rs): 819. So the pool took 9,011 and turned the rest away immediately. The 819 lost watches in the claim and split runs are the same size as that second queue, but we have not confirmed that they are the same transactions.

So, on the default pool, about **1 in 10 transactions failed straight away**, in every flow. Between 10% and 18% ended with no verified receipt. Waves and a bigger pool both avoided this.

### Merchant fan-in: many payments to one merchant

Merchant fan-in sends many coin transfers to one merchant. Each transfer goes into a fresh destination key, from a coin that the fixture prepared. It does not include chat delivery or the production wallet.

We ran six cases in [run 37510457575, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1). Five passed and one failed.

#### Figure 11: How long did merchant transfers take?

[![Bar chart of merchant fan-in finality p95 for six cases. 100 transfers settle in 35.7 s, 1,000 in 30.5 s, 10,000 in waves in 57.3 s, 10,000 with a bigger pool in 61.2 s and 20,000 with a bigger pool in 91.2 s. The failed default-pool 10,000 burst is grey: 45.3 s over 8,193 timed transfers, 9,011 of 10,000 verified.](evidence/stress-metrics-2026-10-05/merchant-timing.svg)](evidence/stress-metrics-2026-10-05/merchant-timing.svg)

*Figure 11. Each bar is finality p95 for one case. The label also gives verified receipts out of transfers sent. The grey bar is the failed case, and it shows only the 8,193 transfers that we timed.*

All five passing cases verified every transfer. The largest, 20,000 at once on a bigger pool, settled 95% of transfers in 91 seconds. That is close to the 94 seconds for 20,000 claims (Figure 4), which makes sense: each merchant transfer is a claim.

Now the case that failed. We sent 10,000 transfers at once on the default pool. The pool rejected 989 immediately, and we lost the watch on 818 more. The run's own audit verified 8,193 receipts.

On 7 October 2026 we reconciled the 818 lost watches from saved blocks. All 818 were in canonical, finalized blocks, with success and the `Coinage.CoinTransferred` event. None of the 989 rejected transfers is in a saved block. So the total is 8,193 + 818 = **9,011 verified receipts**, which matches the 9,011 correct coin states.

This case **stays failed**. Reconciliation adds receipts, not timing samples, so its p95 still uses the 8,193 timed transfers.

> Same pattern, new flow: one 10,000 burst on the default pool fell short. **Waves and a bigger pool both completed it.**

The appendix has the [full merchant measurements](coinage-stress-metrics-appendix.md#merchant-fan-in-measurements), with p50, p95 and max, launch windows and job links. As with the other flows, each bar is a separate setup. Don't read Figure 11 as a trend.

### Free-quota and offboarding: first unload cases (preliminary)

Both of these flows unload coins into the external asset. All six free-quota profiles now have workload results, so I no longer call its burst measurements preliminary; the scenario is still incomplete, because a real period rollover and native wallet policy are not tested. Offboarding has five profiles with a result, one of them with incomplete receipts, so it stays preliminary.

**Free-quota exhaustion, 100 requests.** [Run 37570768389](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37570768389/attempts/1) sent 100 unload requests on the default pool. All 100 setup top-ups finalized first. We verified all 100 unload receipts, and we checked them again offline from the saved blocks. Finality p50 / p95 / max was 43.08 / 55.02 / 55.02 seconds, with N = 100.

The free-token allowance was 1,000. So all 100 requests came from **one person**. This is 100 transactions from 1 person, not 100 users.

We also tried two requests that must fail, and both failed as designed:

- Reusing a consumed token was rejected with custom error 57 (`UnloadTokenAlreadyConsumed`).
- A counter at the limit was rejected with custom error 58 (`UnloadTokenCounterOutOfRange`).

**Free-quota exhaustion, 1,000 requests: the first full allowance.** [Run 37690106740](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37690106740/attempts/1) sent 1,000 unload requests on the default pool, in a 0.049-second launch window. The allowance is 1,000, so all 1,000 came from **one person**, who used every free token in the period. That is 1 person and 1,000 transactions. All 1,000 setup top-ups finalized first. We verified all 1,000 unload receipts locally, and the final state matched: held backing 0 and pallet backing 1. Finality p50 / p95 / max was 156.5 / 276.6 / 288.6 seconds, with N = 1,000. Setup took 465 seconds, and it is not part of the timing.

With the allowance used up, both must-fail requests failed as designed. Reusing a consumed token was rejected with custom error 57. Counter 1,000, one past the last valid counter, was rejected with custom error 58.

This is the first case that uses up a whole allowance. It does not show what happens when the period rolls over, or how a wallet behaves when its free quota is gone.

**Free quota at 10,000 and 20,000 requests.** The allowance is 1,000 per person, so 10,000 requests come from 10 people and 20,000 from 20. All four runs used test commit [`7f269bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419), and every setup top-up finalized first.

| Case | People / requests | Verified receipts | Finality p50 / p95 / max (N) | Result |
| --- | --- | --- | --- | --- |
| [10,000 at once, default pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37733097599/attempts/1) | 10 / 10,000 | 8,921 original + 90 reconciled = 9,011; 989 rejected at pool entry | 2,682.3 / 3,347.2 / 3,355.9 s (8,921) | **Failed** completion target |
| [10,000 in waves (8,000 + 2,000), default pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37751232138/attempts/1) | 10 / 10,000 | 10,000 original | Wave 1: 1,787.0 / 2,324.0 / 2,329.6 s (8,000); wave 2: 288.2 / 524.3 / 548.3 s (2,000) | Passed |
| [10,000 at once, bigger pool (11,000 entries)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37772925410/attempts/1) | 10 / 10,000 | 10,000 original | 2,743.6 / 3,577.0 / 3,588.5 s (10,000) | Passed |
| [20,000 at once, bigger pool (22,000 entries)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37800522275/attempts/1) | 20 / 20,000 | 4,823 original + 15,162 reconciled = 19,985; 15 unresolved | 3,558.2 / 8,594.3 / 8,714.9 s (4,823) | **Failed** |

- **10,000 at once on the default pool** repeats the pattern of every other default-pool 10,000 burst: 989 rejected at the door, 9,011 admitted. We reconciled the 90 lost watches from saved blocks, and none is left unresolved. The final state agrees with the receipts: 9,011 people's coins credited and 989 not, 9,011 tokens used, and held backing 1,978 (989 × 2). It **failed its completion target**; it's a valid overload result.
- **10,000 in waves and 10,000 with a bigger pool** both verified every receipt. In each, 10 people used their whole allowance, and all 20 must-fail requests (two per person) were rejected as designed, with custom errors 57 and 58.
- **20,000 with a bigger pool** failed. Only 4,823 watches finalized; 15,176 reported "invalid" and one hit an RPC error. Reconciliation from the saved blocks showed that 15,162 of them succeeded, so **19,985 have verified receipts** and **15 are unresolved**. The final state has exactly 15 unused tokens, on the same 15 people, and held backing 30 (15 × 2). That is **consistent with** those 15 not completing, but state is not receipt evidence, so I don't call it proven. The must-fail requests were not reached. CI also timed out while shutting down after the workload; that is separate from the workload result.

This run included [`7f269bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419), which saves finalized blocks that the watches missed. That's why we could reconcile nearly every lost watch here. Setup took 3,028, 2,979, 3,411 and 5,865 seconds for the four runs, and it is not part of the timing.

**Offboarding, 100 people.** [Run 37590878841](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37590878841/attempts/1) sent 100 unloads from 100 different people on the default pool. All 100 setup top-ups finalized. We verified all 100 unload receipts locally from the saved artifact. Finality p50 / p95 / max was 49.16 / 61.12 / 61.12 seconds, with N = 100.

**Offboarding, 1,000 people.** [Run 37593396451](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37593396451/attempts/1) sent 1,000 unloads from 1,000 people on the default pool, in a 0.052-second client launch window. All 1,000 setup top-ups finalized first. We verified all 1,000 unload receipts locally from the saved artifact. Finality p50 / p95 / max was 152.5 / 272.6 / 284.5 seconds, with N = 1,000. The final state matched: held backing 0 and pallet backing 1, as expected. Fixture setup took 1,163.7 seconds, and it is not part of the timing.

**Offboarding, 10,000 people at once.** [Run 37606103903](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37606103903/attempts/1) sent 10,000 unloads on the default pool, in a 0.481-second launch window. All 10,000 setup top-ups finalized first. (An earlier dispatch of this case, run 37603781867, was cancelled. It has no result.)

- The pool rejected 989 immediately (`1016`, pool limit), and we lost the watch on 89 more.
- The run's own audit verified 8,922 receipts. We reconciled the 89 lost watches from the saved blocks, and all 89 were successful unloads. None of the 989 rejected unloads is in a saved block (175287–175678). So **9,011 of 10,000** have verified receipts, and no watch is left unresolved.
- It was very slow. Finality p50 / p95 / max was 2,673.2 / 3,333.1 / 3,341.9 seconds: about 45, 56 and 56 minutes. N = 8,922; the 89 reconciled receipts have no timing.
- **We did not observe the final state.** The driver stopped at its receipt-audit check, so it never saved the final balances, held backing or tokens. I make no claim about state correctness for this case.

This case **failed its completion target**. It is a valid overload result, not a test bug, so we won't rerun it to get a pass. The 989 rejected and 9,011 admitted repeat the pattern of the other default-pool 10,000 bursts. Fixture setup took 9,526 seconds (about 2.6 hours), and it is not part of the timing. Recovery passed. The pool was the node default: the network config has no pool override.

**Offboarding, 10,000 people in waves.** [Run 37645548491](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/attempts/1) sent 10,000 unloads from 10,000 people on the default pool, in two waves: 8,000, then 2,000 after the first wave settled. All 10,000 setup top-ups finalized first. We verified all **10,000** receipts locally: 10,000 original, none reconciled and none missing. The state matched after each wave: held backing 4,000 after wave 1 and 0 after wave 2, with pallet backing 1. Recovery passed.

| Wave | Unloads | Client launch | Finality p50 / p95 / max | N |
| --- | ---: | ---: | --- | ---: |
| 1 | 8,000 | 0.344 s | 1,779.5 / 2,317.0 / 2,322.8 s | 8,000 |
| 2 | 2,000 | 0.093 s | 287.9 / 520.0 / 544.1 s | 2,000 |

Wave 1 took about 39 minutes at p95, and wave 2 under 9 minutes. I report each wave on its own; they don't combine into one p95. Setup took 3,980 seconds (about 66 minutes), and it is not part of the timing. The pool was the node default.

So pacing completed 10,000 offboards on the default pool, where one burst of 10,000 did not. That's the same pattern as top-ups, claims and merchant fan-in. It is still a finite test, not a sustained rate.

**Offboarding, 20,000 people at once, bigger pool: incomplete evidence.** The retry, [run 37694191834](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37694191834/attempts/1) at commit [`e163be9`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52), sent 20,000 unloads after all 20,000 setup top-ups finalized.

- Only 4,165 watches finalized. 15,831 were reported "ready, then invalid", and 4 hit an RPC error.
- Reconciliation found 2,614 more successful unloads, so **6,779 have verified receipts** and **13,221 are unresolved**.
- The final state shows held backing 0 and free backing 1, and every one of the 20,000 people was observed with their tokens used. That is **consistent with every offboard completing**, but it is not receipt evidence.
- This run predates the block-saving fix. It only saved blocks named by a finalized watch, so 911 of the 1,206 block heights in the range were never saved. We can't prove the missing receipts.
- Finality for the original watches was p50 / p95 / max 2,596.9 / 6,306.9 / 7,630.7 seconds (N = 4,165).

I report this as **incomplete evidence**, not as "6,779 of 20,000 succeeded".

**What we saw at 20,000 on a bigger pool.** In both 20,000 runs, most client watches reported "invalid", even though reconciliation and the final state show that most transactions completed. So the client's watch status was not reliable at this size. We have not established why.

**Proof generation, a first measurement.** Each unload needs two ring-VRF proofs: one for the recycler alias and one for the free token. So each case made two proofs per unload.

| Case | Recycler proof p50 / max | Free-token proof p50 / max |
| --- | --- | --- |
| Free quota, 100 | 1.406 / 1.455 s | 0.786 / 0.835 s |
| Offboarding, 100 | 1.411 / 1.479 s | 0.827 / 0.880 s |
| Offboarding, 1,000 | 1.650 / 1.749 s | 0.879 / 0.943 s |
| Offboarding, 10,000 | 1.648 / 1.859 s | 0.875 / 1.041 s |
| Free quota, 1,000 | 1.664 / 1.835 s | 0.797 / 0.911 s |
| Offboarding, 10,000 in waves, wave 1 | 1.672 / 1.869 s | 0.890 / 1.030 s |
| Offboarding, 10,000 in waves, wave 2 | 1.677 / 1.834 s | 0.889 / 1.011 s |

So one unload took about 2.2 to 2.6 seconds of proof work. The client made the proofs before it sent anything. This is the client's preparation cost, not part of finality.

What these cases don't show: we did not test a real period rollover. The policy rows come from a separate model, not from native iOS or Android code. All six quota profiles have now run. Offboarding 10,000 with a bigger pool lost its runner twice and has no result, and offboarding 20,000 with a bigger pool has incomplete receipt evidence. See the [quota and offboarding table](coinage-stress-metrics-appendix.md#free-quota-and-offboarding-measurements).

### How many unloads fit in a block?

We counted the verified unloads in each saved block.

| Case | Verified receipts | Blocks | Unloads per full block |
| --- | ---: | ---: | ---: |
| Quota 100 | 100 | 5 | 23 |
| Offboarding 100 | 100 | 5 | 23 |
| Offboarding 1,000 | 1,000 | 44 | 23 |
| Offboarding 10,000 | 8,922 original + 89 reconciled = 9,011 | 392 | 23 |
| Quota 1,000 | 1,000 | 44 | 23 |
| Offboarding 10,000 in waves, wave 1 | 8,000 | 348 | 23 |
| Offboarding 10,000 in waves, wave 2 | 2,000 | 87 | 23 |
| Quota 10,000 at once | 8,921 original + 90 reconciled = 9,011 | 392 | 23 |
| Quota 10,000 in waves, wave 1 | 8,000 | 348 | 23 |
| Quota 10,000 in waves, wave 2 | 2,000 | 87 | 23 |
| Quota 10,000, bigger pool | 10,000 | 435 | 23 |
| Quota 20,000, bigger pool | 4,823 original + 15,162 reconciled = 19,985 | 870 saved | 23 |
| Offboarding 20,000, bigger pool (incomplete) | 6,779 proven | 295 saved | 23 |
| Full flow 100, payment unload | 100 | 5 | 23 |
| Full flow 100, offboard | 100 | 5 | 23 |
| Full flow 1,000, payment unload | 1,000 | 44 | 23 |
| Full flow 1,000, offboard | 1,000 | 44 | 23 |

**Every full block held exactly 23 unloads.** A full claim block holds 2,363 (Figure 6), about 100 times more. So a large unload burst needs hundreds of blocks to clear. 10,000 offboards at once needed 392 blocks, which fits the 45-minute p50.

Why 23? Each successful unload recorded 62.9 ms of ref time. 23 × 62.9 ms = 1.45 seconds. This runtime gives normal transactions 1.5 seconds of ref time per block, so a 24th unload (1.51 seconds) would not fit. The collator logs agree: every full block ended with `HitBlockWeightLimit`, and the last block of each run ended with `NoMoreTransactions`. The pattern held in every newer case too: quota 1,000 and both waves of the paced run.
It also held in every 8–9 October unload case: every full block held 23 unloads and ended with `HitBlockWeightLimit`. That includes the full flow's payment unloads, which unload into a coin and use 62.99 ms each. For the two 20,000 runs, we counted only the saved blocks.

Two limits on this. We matched log lines to blocks by height and transaction count, because the logged hash is taken before the block is sealed. And 62.9 ms is the weight recorded after dispatch; the block builder checks the declared weight before dispatch, which we did not read. So the weight limit stopped these blocks, but we have not shown the exact weight the builder used. The counts and stop reasons are in [unload-blocks.json](evidence/remaining-flow-2026-10-08/unload-blocks.json). The 8–9 October counts are in a [second file](evidence/remaining-flow-2026-10-09/unload-blocks.json).

### Full flow: the whole lifecycle

The full flow runs one fixed plan per person, through every stage: top-up → readiness → unload into a payment coin → claim → recycle → readiness → offboard. It is a fixed plan, not the wallet's planner. All runs used test commit [`aa72510`](https://github.com/paritytech/polkadot-pop-e2e/commit/aa72510d3fbf321b2946430db0264f50ae5d8785) on the default pool.

- **Smoke, 1 person:** [run 37854332739](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37854332739/attempts/1) passed. All five stages verified.
- **100 people:** [run 37855938846](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37855938846/attempts/1) passed. Every stage verified 100 of 100 receipts, 500 in total. Stage p95: top-up 34.4 s, payment unload 61.8 s, claim 34.3 s, recycle 34.4 s and offboard 60.5 s.
- **1,000 people:** [run 37858620774](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37858620774/attempts/1) passed. Every stage verified 1,000 of 1,000 receipts, 5,000 in total.

| Stage (1,000 people) | Finality p50 / p95 / max | Blocks | Most in one block |
| --- | --- | ---: | ---: |
| Top-up | 45.0 / 53.0 / 57.0 s | 5 | 260 |
| Payment unload | 164.4 / 296.5 / 308.5 s | 44 | 23 |
| Claim | 31.4 / 31.4 / 31.4 s | 1 | 1,000 |
| Recycle | 36.2 / 48.2 / 48.2 s | 4 | 287 |
| Offboard | 152.2 / 272.3 / 284.3 s | 44 | 23 |

The two unload stages take most of the time: each needs 44 blocks for 1,000 people, because a block fits only 23 unloads. The other stages fit in one to five blocks. For those stages, "most in one block" is just the most we saw in this run, not the block's capacity.

**10,000 at once: a test-tool failure.** [Run 37863573263](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37863573263/attempts/1) never put load on the chain. Our sender lost its connection at every top-up it tried to send: 10,000 RPC errors, and not one transaction was seen as ready, in a block or finalized. There are no receipts. This is not a chain result. (An earlier reconciliation counted 94 of these errors as pool rejections, because it matched "1016" inside the request bytes. The corrected review ignores request payloads.) A retry, [run 37899564808](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37899564808/attempts/1) with a sender-connection check, was running at this update and is not yet verified.

10,000 in waves, 10,000 with a bigger pool and 20,000 with a bigger pool have not run yet. See the [full-flow table](coinage-stress-metrics-appendix.md#full-flow-measurements).

### Which tests did not reach their measured load?

Some tests stopped before their measured workload began. These have no result yet.

| Scenario | What happened | What it establishes |
| --- | --- | --- |
| Free-quota exhaustion | First campaign: smoke passed; all six measured cases stopped during fixture top-ups. Cause found and fixed (below). The 100- and 1,000-request cases have since passed independently, and so have the four larger profiles (two passed, two failed; see above). | All six profiles have results |
| Offboarding | Same setup failure as quota; smoke passed. Since then, 100, 1,000 and 10,000 in waves passed independently, and 10,000 at once ran and failed its completion target (9,011 verified). | The 10,000 bigger-pool profile has no result, and 20,000 has incomplete receipts (next rows); no burst-capacity conclusion yet |
| Offboarding 10,000, bigger pool | Runner failure, twice. [Run 37672641924, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37672641924/attempts/1), commit [`7322395`](https://github.com/paritytech/polkadot-pop-e2e/commit/73223951e57549a88f20fd22033ed53575977976): the self-hosted runner lost communication with GitHub during the pilot step. Attempt 2 was queued automatically by `cattery-scheduler[bot]` and cancelled. [Run 37684376141, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37684376141/attempts/1), commit [`fd826a3`](https://github.com/paritytech/polkadot-pop-e2e/commit/fd826a3843e1a6a40990a616bcbf3de8be400fb2): the runner lost communication again. GitHub shows its automatic attempt 2 as "success", but the pilot job was skipped and **no workload ran**, so it is not a result. | No workload result; cause of the runner loss not established |
| Offboarding 20,000, bigger pool | Setup failure before any workload. [Run 37687780845, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37687780845/attempts/1), commit [`fd826a3`](https://github.com/paritytech/polkadot-pop-e2e/commit/fd826a3843e1a6a40990a616bcbf3de8be400fb2): the network orchestrator (zombienet) panicked at start (`lib.rs:842`), because a Prometheus port that it picked automatically (30337) was a collator's fixed p2p port. [`e163be9`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52) fixed this by reserving the fixed ports. The retry, [run 37694191834](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37694191834/attempts/1), ran: 6,779 receipts proven and 13,221 unresolved, with state consistent with completion (see above). | Incomplete receipt evidence |
| Full flow | First campaign: smoke failed while preparing the network: GitHub reports the self-hosted runner lost communication. Six cases skipped. Since then, independent runs passed smoke, 100 and 1,000 (see [Full flow](#full-flow-the-whole-lifecycle)). | Cause of the first runner loss not established; three profiles passed |
| Full flow 10,000 at once | [Run 37863573263, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37863573263/attempts/1): our sender lost its connection at every top-up submission; no transaction reached the chain. The retry, [run 37899564808](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37899564808/attempts/1), was running at this update. | No measured workload result; a test-tool failure, not a chain result |

Why did quota and offboarding stop? The test client sent its setup top-ups through a path that the node allows only 16 at a time on each connection. Above that, the extra transactions were silently never sent. Only 16 of the 100 setup top-ups reached the pool. This was a bug in our test harness, not a chain result. The [fix](https://github.com/paritytech/polkadot-pop-e2e/commit/e9c982bb296a344d8c6629dcc8a82971c107438e) sends setup through the same path as the workload.

The jobs are in [run 37510457575, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1):

- **Quota:** [smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112436114495), [100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112526429833), [1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112532845219), [10,000 at once](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112539289683), [10,000 in waves](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112545534951), [10,000 bigger pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112551090694), [20,000 bigger pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112556615978).
- **Offboarding:** [smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112440932803), [100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112561845169), [1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112567282589), [10,000 at once](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112572580926), [10,000 in waves](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112577483596), [10,000 bigger pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112582692332), [20,000 bigger pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112587829742).
- **Full flow:** [smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112446686310); the six cases were skipped.

A sustained-load test is also in development. It is not reportable yet.

* * *

## So what do the results tell us?

It's easy to read too much into these numbers. Here's what I think they do and don't show.

- **The pool sets how many can wait. The block limit sets how fast they leave.** A bigger pool gave more space to wait. It did not make the chain process more.
- **Waves and bigger pools both work.** Each one completed some workloads that a single burst on the default pool did not.
- **A passed run is not a maximum.** It does not show production capacity, sustainable TPS, runtime-weight accuracy, block execution time or PVF deadline compliance.
- **A receipt and a coin state are different checks.** We need both. Our evidence comes from local RPC nodes. It is consistent, but it is not a cryptographic proof.
- **This report does not rerun anything.** It reads the saved measurements again. Original runs, reruns, CI results and later checks stay separate. Their dates are in the appendix.
- **Unloads hit the block weight limit early.** Every full unload block held 23 unloads and stopped at the weight limit, so 10,000 offboards needed 392 blocks and most of an hour.
- **Pacing also completed 10,000 offboards.** In two waves on the default pool, all 10,000 unloads verified, where one burst of 10,000 did not. These are still finite tests, not a sustained unload rate.
- **The full lifecycle works end to end at 1,000, and unloads set its pace.** All five stages verified for 1,000 people. The two unload stages took most of the time. Free quota's default-pool 10,000 burst repeated the 9,011-admitted pattern.
- **Merchant fan-in follows the same pattern.** Waves and a bigger pool each completed 10,000 transfers to one merchant, and one default-pool burst did not. These separate runs do not show a latency trend, sustainable throughput or production capacity.

> A burst that passed tells us the chain handled that burst. **It isn't a capacity ceiling.**

In the end, Coinage on this setup verified a 150,000-claim burst and a 100,000-actor split-and-claim burst. We checked every receipt. We also know where runs stopped short: single 10,000 bursts on the default pool, and recycling with 100,000 actors. That's a solid baseline, not the final word.

* * *

## Measurement notes and evidence

If you want to check my work, this is where to look.

### Measurement definitions

- All times are in **seconds**. Finality includes client and RPC time. Readiness includes polling delay.
- Percentiles are nearest-rank values over the stated population. We never average them across runs or nodes.
- Reconciliation adds receipts. It never adds timing samples. In the appendix, an em dash means that the record does not give that value.
- Launch time and launch rate measure the client. They do not measure how fast the node accepts or runs transactions. A burst does not run in one block.
- **Stage duration.** Lifecycle stages include audits, signing between waves and readiness observation. They do not include setup, fixtures, smoke or recovery. Top-up and claim stages include waits, observer shutdown and final state reads. They do not include fixture setup, the final receipt audit or recovery.
- Recovery checks show that the chain is live and both authors make blocks. Recovery time is not a queue-drain time.
- Claim timings come from the saved `claim-burst-transactions.jsonl` file. They start at each call's own send time. The finalized notification and the receipt lookup are separate timestamps.
- Queue charts use each collator's own `substrate_ready_transactions_number` gauge. Driver memory comes from the burst observer samples.
- Proposal duration is block authoring time, not PVF execution time. The longest proposal took 2.970 seconds.

### Environment and pool configuration

The lifecycle campaign used engine `7907a3bfa7b2e47535a74b7920086a05ca94773a` and snapshot bundle run 36614342201. It had six relay validators, two People collators and the other snapshot parachains, all on one runner, with no added delay. Bigger lifecycle pools used 256 MiB for each People collator. Default cases did not change the pool. We did not retry any transaction.

The saved records show 27 driver runs that did not overlap. They cannot show if a process stayed alive after a runner was lost. The 16 cases are the selected attempts from the completion audit. Earlier setup failures are in the [original-attempt record](lifecycle-campaign-results.md#outcomes).

The 20,000 to 100,000 claim runs used the same engine and snapshot, the `polkadot-weekly2026w33-rc2` binaries and the People runtime `next-people-paseo` (spec 3003000, transaction version 5). The runner had an AMD EPYC 7B13 with 16 cores, 32 logical CPUs and about 62.8 GiB of RAM. The network and the driver shared this machine. Pool size stayed at 40 MiB. Entry limits, fixture batching, query concurrency and launch targets changed between runs.

Exact hashes, runtime limits and settings are in the download. Earlier run settings are in the [evidence record](measured-results.md#evidence-record). Do not assume that settings are the same across series.

### Evidence and downloads

- **Data:** [metrics.json](evidence/stress-metrics-2026-10-05/metrics.json) and its [checksum](evidence/stress-metrics-2026-10-05/SHA256SUMS.txt). The file has the selected measurements, source files and hashes, run attempts, runtime and binary details, and the sampled time series. Time fields are in seconds. Fields that we converted from milliseconds end in `Seconds`.
- **Charts:** [make_charts.py](evidence/stress-metrics-2026-10-05/make_charts.py) draws every figure from `metrics.json`, the host resource data and the saved merchant summaries.
- **Machine resources:** [host-resources.json](evidence/host-resources-2026-10-07/host-resources.json), its [extraction script](evidence/host-resources-2026-10-07/extract_host_resources.py) and [checksum](evidence/host-resources-2026-10-07/SHA256SUMS.txt). They come from the saved `/proc/stat`, `/proc/meminfo` and process lists of the three large claim runs.
- **Raw archives:** these small files are not the full raw receipt archives. GitHub artifacts expire after 30 days. We keep the raw archives locally, but they are not public.
- **Lifecycle audit:** done on **3 October 2026 UTC**. Artifact IDs, archive digests and expiry dates are in the [manifest](evidence/lifecycle-2026-10-03/manifest.json). Original attempts and job links are in the [pinned audited report](https://github.com/paritytech/technical-design/blob/e26a47902fa1cbc1a9dd5dca80d1dc5a2657a508/designs/individuality/non-fun-tests/test-design/lifecycle-campaign-results.md).
- **Commits and verification sources:** see the [lifecycle evidence references](coinage-stress-metrics-appendix.md#lifecycle-evidence-references) and [claim evidence references](coinage-stress-metrics-appendix.md#claim-evidence-references).
- **Earlier runs:** top-up and 10,000-claim commits, verification dates and artifact IDs are in the [existing evidence record](measured-results.md#evidence-record). Earlier records also include the [1,000-claim baseline](measured-results.md#measured-results), the [memory-fix check](measured-results.md#verified-1000-claim-validation) and the [million-claim tool failure](measured-results.md#claim-generator-memory-retention--2-october-2026).
- **Merchant, quota and offboarding (7 October 2026):** selected summaries, audits, the merchant reconciliation, proof timings, verifier output and the case ledger are in the [remaining-flow evidence folder](evidence/remaining-flow-2026-10-07/SHA256SUMS.txt). Commits and jobs are in the [merchant and quota evidence references](coinage-stress-metrics-appendix.md#merchant-and-quota-evidence-references).
- **Offboarding 1,000 and 10,000 (7–8 October 2026):** summaries, audits, the 10,000 reconciliation and review, proof timings, verifier output and the per-block counts are in the [8 October evidence folder](evidence/remaining-flow-2026-10-08/SHA256SUMS.txt).
- **Offboarding 10,000 in waves, quota 1,000 and the cases with no result (8 October 2026):** summaries, audits, state, the quota and probe files, reviews, verifier output and the per-block counts are in the same [8 October evidence folder](evidence/remaining-flow-2026-10-08/SHA256SUMS.txt).
- **Quota, full flow and offboarding 20,000 (8–9 October 2026):** reviews, summaries, audits, quota and probe files, reconciliation summaries, verifier output and per-block counts are in the [9 October evidence folder](evidence/remaining-flow-2026-10-09/SHA256SUMS.txt).
- **Methods:** the [claim method](https://github.com/paritytech/polkadot-pop-e2e/blob/dfdc44a75bc91ea1610742b42b4e5278f4ad42fd/ci/previewnet/burst-results.md) and the [top-up evidence guide](https://github.com/paritytech/polkadot-pop-e2e/blob/feat/th-coinage-top-up-burst/ci/previewnet/burst-results.md).
