# Appendix: Coinage measured results

The tables below preserve the detailed measurements and evidence references behind the [Coinage stress metrics report](coinage-stress-metrics.md). If you'd rather work with the numbers directly, you can [download the extracted data](evidence/stress-metrics-2026-10-05/metrics.json). All timings are seconds; N is the timing sample count. An em dash means the record does not establish that measurement. See the report’s [measurement definitions](coinage-stress-metrics.md#measurement-definitions) and [environment](coinage-stress-metrics.md#environment-and-pool-configuration) before comparing configurations.

Finality ends at successful finalized receipt lookup. Readiness ends at the first saved finalized observation of root coverage. Reconciled counts do not create new timing samples. Stage duration excludes fixtures, smoke and recovery; workflow-specific boundaries remain in the report.

## Top-up measurements

Timing populations remain original after reconciliation. The ready count can include later state observations; its timing population is shown separately.

| Run / configuration | Requested / submitted / verified | Finality p50 / p95 / max (N) | Ready; readiness p50 / p95 / max (N) | Stage |
| --- | --- | --- | --- | --- |
| [1,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36534910589/attempts/1) | 1,000 / 1,000 / 1,000 | — / 53.0 / — (1,000) | 1,000; — / 105.6 / — (1,000) | — |
| [7,000 + 3,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36560408065/attempts/1) | 10,000 / 10,000 / 10,000 | — / 183.0 / — (10,000) | 10,000; — / 262.1 / — (10,000) | 410.9 |
| [10,000 burst; 11,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36609355696/attempts/1) | 10,000 / 10,000 / 10,000 | — / 256.0 / — (10,000) | 10,000; — / 353.1 / — (10,000) | 420.7 |
| [10,000 burst; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36537079387/attempts/1) | 10,000 / 10,000 / 9,011 | 136.722 / 232.777 / 244.981 (8,971) | 9,011; 216.392 / 332.522 / 347.910 (9,011) | 628.256 |
| [8,500 + 1,500; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36619415692/attempts/1) | 10,000 / 8,500 / 8,500 | 128.507 / 224.546 / 236.602 (8,452) | 5,869; 155.974 / 231.603 / 236.728 (5,602) | 269.075 |
| [8,400 + 1,600; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36662212241/attempts/1) | 10,000 / 10,000 / 10,000 | 107.019 / 214.931 / 227.177 (10,000) | 10,000; 171.100 / 312.393 / 347.931 (10,000) | 405.548 |

## Claim measurements

Claims do not require ring readiness. Launch windows measure the client.

| Run / pool entries and bytes | Requested / submitted / verified | Client launch | Finality p50 / p95 / max (N) | Stage |
| --- | --- | --- | --- | --- |
| [10,000 burst; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36705343718/attempts/1) | 10,000 / 10,000 / 8,192 | 0.471 | 38.234 / 50.167 / 50.185 (8,192) | — |
| [8,000 + 2,000; default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719621433/attempts/1) | 10,000 / 10,000 / 10,000 | 0.350 + 0.084 | 38.970 / 50.680 / 50.697 (10,000) | 113.615 |
| [10,000 burst; 11,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36719745986/attempts/1) | 10,000 / 10,000 / 10,000 | 0.433 | 42.903 / 54.686 / 54.694 (10,000) | 88.275 |
| [20,000 burst; 22,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | 20,000 / 20,000 / 20,000 | 0.802 | 65.711 / 93.806 / 93.914 (20,000) | 151.428 |
| [40,000 burst; 44,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | 40,000 / 40,000 / 40,000 | 1.582 | 92.300 / 139.394 / 139.566 (40,000) | 182.521 |
| [100,000 burst; 110,000 / 40 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | 100,000 / 100,000 / 100,000 | 3.930 | 178.521 / 297.346 / 310.339 (100,000) | 410.385 |
| [150,000 burst; 165,000 / 256 MiB](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36900802673/attempts/1) | 150,000 / 150,000 / 150,000 | 6.662 | 275.769 / 489.735 / 507.262 (150,000) | 649.976 |

## Client notifications and receipt lookup

All timings are seconds, from each submission. Finalized RPC notification and successful receipt lookup are separate observations.

| Run | Observation | N | p50 / p95 / p99 / max (s) |
| --- | --- | --- | --- |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → first pool-ready | 20,000 | 1.542 / 2.809 / 2.915 / 2.941 |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → first inclusion | 20,000 | 29.142 / 62.284 / 62.584 / 68.152 |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → finalized RPC notification | 20,000 | 65.537 / 93.803 / 93.832 / 93.912 |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | Submit → successful receipt lookup | 20,000 | 65.711 / 93.806 / 93.898 / 93.914 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → first pool-ready | 40,000 | 3.321 / 6.399 / 6.868 / 7.033 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → first inclusion | 40,000 | 73.215 / 112.833 / 112.909 / 112.923 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → finalized RPC notification | 40,000 | 92.295 / 139.388 / 139.513 / 139.561 |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | Submit → successful receipt lookup | 40,000 | 92.300 / 139.394 / 139.516 / 139.566 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → first pool-ready | 100,000 | 7.435 / 15.268 / 16.088 / 16.441 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → first inclusion | 100,000 | 150.106 / 274.796 / 278.924 / 284.309 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → finalized RPC notification | 100,000 | 178.341 / 297.157 / 306.360 / 310.250 |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | Submit → successful receipt lookup | 100,000 | 178.521 / 297.346 / 306.367 / 310.339 |

## Claim resources

Host and pool metrics are approximately five-second samples. Driver memory uses burst observer samples. Proposal duration is authoring time, not PVF execution.

| Claims / run | Host busy peak | Min available RAM (GiB) | Ready queue peak, primary People node | Driver RSS / heap peak (GiB) | Max canonical proposal (s) |
| --- | --- | --- | --- | --- | --- |
| [20,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | 20.690% | 47.985 | 20,000 | 1.189 / 0.558 | 2.735 |
| [40,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | 25.173% | 46.985 | 37,637 | 1.688 / 0.946 | 2.764 |
| [100,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | 21.290% | 42.980 | 88,185 | 2.820 / 1.567 | 2.970 |

## Split-and-claim outcomes

Two extrinsics per actor. Workload outcome and CI shutdown outcome remain separate.

| Case / selected attempt | Actors / schedule | Pool entries / bytes | Submitted / verified extrinsics | Workload; CI distinction | Stage (s) |
| --- | --- | --- | --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | 100 / burst | 8,192 / 20 MiB (default) | 200 / 200 | workload-pass | 60.021 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 1,000 / burst | 8,192 / 20 MiB (default) | 2,000 / 2,000 | workload-pass | 60.029 |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 8,192 / 20 MiB (default) | 10,000 / 8,192 | incomplete | — |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / 8,000 + 2,000 paced | 8,192 / 20 MiB (default) | 20,000 / 20,000 | workload-pass | 240.062 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 11,000 / 256 MiB | 20,000 / 20,000 | workload-pass | 160.063 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 20,000 / burst | 22,000 / 256 MiB | 40,000 / 40,000 | launch-timing-failure | 225.207 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40,000 / burst | 44,000 / 256 MiB | 80,000 / 80,000 | workload-pass; shutdown failed | 435.545 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 100,000 / burst | 110,000 / 256 MiB | 200,000 / 200,000 | workload-pass | 1,041.877 |

## Split-and-claim wave timings

Client launches/s is submitted count divided by the unrounded submission window; it is not chain throughput.

| Case | Wave | Submitted | Launch (s) | Client launches/s | Finality N | p50 / p95 / max (s) |
| --- | --- | --- | --- | --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | split-split | 100 | 0.006 | 18,093.620 | 100 | 27.687 / 27.688 / 27.688 |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | split-claim | 100 | 0.004 | 26,702.063 | 100 | 31.710 / 31.712 / 31.714 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 1,000 | 0.064 | 15,674.771 | 1,000 | 29.805 / 29.822 / 29.822 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 1,000 | 0.051 | 19,451.906 | 1,000 | 26.155 / 26.173 / 26.186 |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 10,000 | 0.516 | 19,380.553 | 8,192 | 41.397 / 49.337 / 53.209 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-1-split | 8,000 | 0.383 | 20,863.676 | 8,000 | 49.067 / 53.008 / 60.930 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-1-claim | 8,000 | 0.370 | 21,615.986 | 8,000 | 46.637 / 50.734 / 58.501 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-2-split | 2,000 | 0.091 | 22,058.290 | 2,000 | 37.127 / 37.135 / 40.998 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-wave-2-claim | 2,000 | 0.085 | 23,554.426 | 2,000 | 44.557 / 44.626 / 44.650 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 10,000 | 0.532 | 18,811.278 | 10,000 | 49.233 / 61.232 / 65.056 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 10,000 | 0.508 | 19,687.561 | 10,000 | 50.848 / 62.524 / 62.537 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | split-split | 20,000 | 1.100 | 18,187.728 | 20,000 | 57.641 / 81.841 / 86.024 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | split-claim | 20,000 | 0.949 | 21,074.328 | 20,000 | 49.999 / 73.645 / 73.964 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 40,000 | 1.946 | 20,557.721 | 40,000 | 100.739 / 172.903 / 177.328 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 40,000 | 1.802 | 22,196.872 | 40,000 | 84.130 / 131.315 / 132.578 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-split | 100,000 | 4.956 | 20,179.017 | 100,000 | 207.971 / 371.987 / 389.557 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | split-claim | 100,000 | 4.365 | 22,909.419 | 100,000 | 172.573 / 318.680 / 332.599 |

## Recycling outcomes

One coin-load extrinsic per actor, followed by a separate root-coverage observation.

| Case / selected attempt | Actors / schedule | Pool entries / bytes | Submitted / verified extrinsics | Workload; CI distinction | Stage (s) |
| --- | --- | --- | --- | --- | --- |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 100 / burst | 8,192 / 20 MiB (default) | 100 / 100 | workload-pass | 55.343 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 1,000 / burst | 8,192 / 20 MiB (default) | 1,000 / 1,000 | workload-pass | 110.629 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 8,192 / 20 MiB (default) | 10,000 / 8,724 | incomplete | — |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / 8,000 + 2,000 paced | 8,192 / 20 MiB (default) | 10,000 / 10,000 | workload-pass | 480.183 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 / burst | 11,000 / 256 MiB | 10,000 / 10,000 | workload-pass | 389.279 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20,000 / burst | 22,000 / 256 MiB | 20,000 / 20,000 | workload-pass | 851.216 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | 40,000 / burst | 44,000 / 256 MiB | 40,000 / 40,000 | workload-pass; shutdown failed | 1,563.826 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 100,000 / burst | 110,000 / 256 MiB | 100,000 / 60,990 | incomplete | — |

## Recycling wave timings

Percentiles use original successful watches; reconciled receipts add no timing samples.

| Case | Wave | Submitted | Launch (s) | Client launches/s | Finality N | p50 / p95 / max (s) |
| --- | --- | --- | --- | --- | --- | --- |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | recycle-recycle | 100 | 0.006 | 17,828.808 | 100 | 35.676 / 35.677 / 35.677 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 1,000 | 0.044 | 22,618.230 | 1,000 | 41.873 / 53.894 / 53.915 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 10,000 | 0.383 | 26,115.716 | 8,479 | 133.680 / 217.971 / 229.942 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-wave-1-recycle | 8,000 | 0.316 | 25,330.817 | 8,000 | 121.806 / 197.826 / 205.913 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-wave-2-recycle | 2,000 | 0.073 | 27,349.204 | 2,000 | 46.644 / 66.690 / 70.694 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 10,000 | 0.394 | 25,383.404 | 10,000 | 137.158 / 233.401 / 245.434 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 20,000 | 0.799 | 25,021.593 | 20,000 | 363.694 / 615.855 / 636.100 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | recycle-recycle | 40,000 | 1.428 | 28,002.665 | 40,000 | 606.384 / 1,095.313 / 1,143.690 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | recycle-recycle | 100,000 | 3.692 | 27,083.397 | 60,982 | 925.565 / 1,709.561 / 1,794.058 |

## Recycling readiness

Readiness includes finalized polling delay and is not wallet privacy readiness. Unobserved readiness is not a proven failure.

| Case | Observed ready | Timing N | Readiness p50 / p95 / max (s) | Observation cutoff (s) |
| --- | --- | --- | --- | --- |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 100 | 100 | 50.339 / 50.341 / 50.341 | 50.341 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 1,000 | 1,000 | 80.517 / 105.595 / 105.597 | 105.627 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 5,002 | 5,002 | 150.951 / 226.736 / 231.871 | 247.079 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 | 10,000 | 165.930 / 317.952 / 343.236 | 475.169 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 10,000 | 10,000 | 216.573 / 353.636 / 384.043 | 384.264 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20,000 | 20,000 | 524.207 / 809.979 / 845.925 | 846.185 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | 40,000 | 40,000 | 910.867 / 1,485.140 / 1,558.509 | 1,558.766 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 39,917 | 39,917 | 992.583 / 1,718.515 / 1,797.529 | 1,797.949 |

## Lifecycle state and resources

Backing uses raw fixture asset units. Resource samples cover the driver step, potentially including fixtures and smoke; network cgroup memory includes multiple processes.

| Case | Backing before → after | Wave state checks | Recovery | Driver RSS GiB | Network cgroup GiB | Resource samples |
| --- | --- | --- | --- | --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | 401 → 401 | Pass (2 waves) | Pass | 0.304 | 14.308 | 73 |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 4001 → 4001 | Pass (2 waves) | Pass | 0.408 | 14.384 | 74 |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Incomplete | Pass | 0.803 | 15.432 | 88 |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 201 → 201 | Pass | True | 0.239 | 15.463 | 82 |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 2001 → 2001 | Pass | True | 0.381 | 14.663 | 93 |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20001 → 20001 | Incomplete | Pass | 1.002 | 16.293 | 133 |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Pass (4 waves) | Pass | 0.844 | 16.199 | 135 |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Pass (2 waves) | Pass | 0.901 | 16.046 | 119 |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20001 → 20001 | Pass (2 waves) | Pass | 0.887 | 16.631 | 178 |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 20001 → 20001 | Pass | True | 0.854 | 16.307 | 150 |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | 80001 → 80001 | Pass (2 waves) | Pass | 1.290 | 19.588 | 154 |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 160001 → 160001 | Pass (2 waves) | Pass | 2.033 | 30.416 | 2,160 |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 400001 → 400001 | Pass (2 waves) | Pass | 1.992 | 30.870 | 451 |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 40001 → 40001 | Pass | True | 1.558 | 19.287 | 275 |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | 80001 → 80001 | Pass | True | 2.431 | 25.027 | 484 |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | 200001 → 200001 | Incomplete | Pass | 4.390 | 31.964 | 673 |

## Lifecycle evidence references

Selected attempts were audited on 3 October 2026 UTC.

| Case / attempt | Test commit | Verification file |
| --- | --- | --- |
| [a100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/1) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a100-verification.json](evidence/lifecycle-2026-10-03/a100-verification.json) |
| [a1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a1000-attempt-2-verification.json](evidence/lifecycle-2026-10-03/a1000-attempt-2-verification.json) |
| [a10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [coinage-split-10000-burst-default-pilot-37029048758-2-split-pilot-split-subset-verification.json](evidence/lifecycle-2026-10-03/coinage-split-10000-burst-default-pilot-37029048758-2-split-pilot-split-subset-verification.json) |
| [b100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | [`ba4bdee5c1a4`](https://github.com/paritytech/polkadot-pop-e2e/commit/ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c) | [b100-targeted-verification.txt](evidence/lifecycle-2026-10-03/b100-targeted-verification.txt) |
| [b1000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b1000-attempt-2-verification.json](evidence/lifecycle-2026-10-03/b1000-attempt-2-verification.json) |
| [b10000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [coinage-recycle-10000-burst-default-pilot-37029048758-2-recycle-pilot-recycle-subset-verification.json](evidence/lifecycle-2026-10-03/coinage-recycle-10000-burst-default-pilot-37029048758-2-recycle-pilot-recycle-subset-verification.json) |
| [a_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a-paced-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a-paced-attempt-2-verification.txt) |
| [a_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a-pool-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a-pool-attempt-2-verification.txt) |
| [b_paced](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b-paced-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/b-paced-attempt-2-verification.txt) |
| [b_pool](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b-pool-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/b-pool-attempt-2-verification.txt) |
| [a20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37116007842/attempts/1) | [`ba4bdee5c1a4`](https://github.com/paritytech/polkadot-pop-e2e/commit/ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c) | [a20000-targeted-workload-verification.json](evidence/lifecycle-2026-10-03/a20000-targeted-workload-verification.json) |
| [a40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a40000-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a40000-attempt-2-verification.txt) |
| [a100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [a100000-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/a100000-attempt-2-verification.txt) |
| [b20000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b20000-attempt-2-verification.txt](evidence/lifecycle-2026-10-03/b20000-attempt-2-verification.txt) |
| [b40000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37121458129/attempts/1) | [`ba4bdee5c1a4`](https://github.com/paritytech/polkadot-pop-e2e/commit/ba4bdee5c1a4a7ed725e6a1f34653b7bb39b774c) | [b40000-targeted-verification.txt](evidence/lifecycle-2026-10-03/b40000-targeted-verification.txt) |
| [b100000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37029048758/attempts/2) | [`ed563b14f5bc`](https://github.com/paritytech/polkadot-pop-e2e/commit/ed563b14f5bc99c82c0158cd6ece6f9affff3f46) | [b100000-receipts-reconciliation.json](evidence/lifecycle-2026-10-03/b100000-receipts-reconciliation.json) |

## Claim evidence references

Original independent verification dates are retained below.

| Claim run (attempt 1) | Test commit | Verification date / source |
| --- | --- | --- |
| [36832069153](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | [`23a884c644db`](https://github.com/paritytech/polkadot-pop-e2e/commit/23a884c644dba50805f7b9373ad45d2529bb888f) | 2026-10-01T08:24:18.422021+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36836204912](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | [`39d2961bb794`](https://github.com/paritytech/polkadot-pop-e2e/commit/39d2961bb7940ee0dd07b970968bc4be034a9608) | 2026-10-01T08:57:55.492162+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36840043405](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | [`b7451cd74bbe`](https://github.com/paritytech/polkadot-pop-e2e/commit/b7451cd74bbe71799ab9bc8e01a69696ab043217) | 2026-10-01T10:05:49.982071+00:00; `verified-results.json`, `analysis.json`, `original/claim-burst-transactions.jsonl` |
| [36900802673](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36900802673/attempts/1) | [`932677d50e07`](https://github.com/paritytech/polkadot-pop-e2e/commit/932677d50e07052e62d45356a334801dc4630270) | 2026-10-02T03:05:11.110954+00:00; `claim-burst-summary.json`, `local-verification.json` |

## Merchant fan-in measurements

Run [37510457575, attempt 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1), test commit [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5). Each transfer is one claim into a fresh destination key of one merchant, from a fixture-prepared coin. Attempt 2 was queued automatically and cancelled before any job ran; it has no results. Launch windows measure the client, not chain throughput.

| Transfers | Pattern | Pool entries / bytes | Watch-finalized | Receipt-verified | State-verified | Client launch | Finality p50 / p95 / max (N) | Result | Job |
| ---: | --- | --- | ---: | --- | ---: | --- | --- | --- | --- |
| 100 | Burst | 8,192 / 20 MiB (default) | 100 | 100 | 100 | 0.006 | 35.72 / 35.72 / 35.73 (100) | Passed | [112480491326](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112480491326) |
| 1,000 | Burst | 8,192 / 20 MiB (default) | 1,000 | 1,000 | 1,000 | 0.080 | 30.42 / 30.45 / 30.45 (1,000) | Passed | [112487225834](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112487225834) |
| 10,000 | Burst | 8,192 / 20 MiB (default) | 8,193 | 8,193 original + 818 reconciled = 9,011 | 9,011 | 0.543 | 41.25 / 45.31 / 45.35 (8,193) | **Failed** completion target | [112493393120](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112493393120) |
| 10,000 | Waves 8,000 + 2,000 | 8,192 / 20 MiB (default) | 10,000 | 10,000 | 10,000 | 0.442 + 0.116 | 45.46 / 57.26 / 57.27 (10,000) | Passed | [112500858287](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112500858287) |
| 10,000 | Burst | 11,000 / 256 MiB | 10,000 | 10,000 | 10,000 | 0.474 | 49.47 / 61.18 / 61.21 (10,000) | Passed | [112509307852](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112509307852) |
| 20,000 | Burst | 22,000 / 256 MiB | 20,000 | 20,000 | 20,000 | 0.950 | 59.15 / 91.16 / 91.38 (20,000) | Passed | [112517391792](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112517391792) |

In the failed default-pool burst, 989 submissions were rejected at pool entry (`1016`, pool limit) and 818 watches were dropped. Reconciliation on 7 October 2026 found all 818 dropped transactions in saved canonical, finalized blocks 173195–173198, with `System.ExtrinsicSuccess` and `Coinage.CoinTransferred`. None of the 989 rejected transactions appears in a saved block. Finality stays on the original 8,193 timed transfers. The one-transfer smoke passed ([job 112430856228](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112430856228)).

## Free-quota and offboarding measurements

Each case is a single, independent run on the default pool. Quota 100, offboarding 100 and offboarding 1,000 used test commit [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55); offboarding 10,000 at once used [`4a652d912e9d`](https://github.com/paritytech/polkadot-pop-e2e/commit/4a652d912e9d38c02a9c41e7496bf1acca41cdbd); offboarding 10,000 in waves used [`42f2e8d99753`](https://github.com/paritytech/polkadot-pop-e2e/commit/42f2e8d997531e0731a8551147badca4bb55456e); quota 1,000 used [`fd826a3843e1`](https://github.com/paritytech/polkadot-pop-e2e/commit/fd826a3843e1a6a40990a616bcbf3de8be400fb2). Proof time is client preparation before release; it is not part of finality. Proof percentiles are nearest-rank over every proof of each kind (one of each per unload). The 8 October quota runs (10,000 and 20,000) used [`7f269bcf4f65`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419), and the offboarding 20,000 retry used [`e163be942607`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52); rows marked enlarged used the stated larger pool.

| Case / run | People / unloads | Setup top-ups | Receipt-verified | Finality p50 / p95 / max (N) | Recycler proof p50 / max | Free-token proof p50 / max | Result |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| [Quota 100, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37570768389/attempts/1) | 1 / 100 | 100 / 100 finalized | 100 | 43.08 / 55.02 / 55.02 (100) | 1.406 / 1.455 | 0.786 / 0.835 | Passed; preliminary |
| [Offboarding 100, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37590878841/attempts/1) | 100 / 100 | 100 / 100 finalized | 100 | 49.16 / 61.12 / 61.12 (100) | 1.411 / 1.479 | 0.827 / 0.880 | Passed; preliminary |
| [Offboarding 1,000, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37593396451/attempts/1) | 1,000 / 1,000 | 1,000 / 1,000 finalized | 1,000 | 152.5 / 272.6 / 284.5 (1,000) | 1.650 / 1.749 | 0.879 / 0.943 | Passed; preliminary |
| [Offboarding 10,000 at once, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37606103903/attempts/1) | 10,000 / 10,000 | 10,000 / 10,000 finalized | 8,922 original + 89 reconciled = 9,011; 989 rejected at pool entry | 2,673.2 / 3,333.1 / 3,341.9 (8,922) | 1.648 / 1.859 | 0.875 / 1.041 | **Failed** completion target; final state not observed |
| [Offboarding 10,000 in waves, default, wave 1 (8,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/attempts/1) | 8,000 / 8,000 | 10,000 / 10,000 finalized (both waves) | 8,000 original; 0 reconciled; 0 missing | 1,779.5 / 2,317.0 / 2,322.8 (8,000) | 1.672 / 1.869 | 0.890 / 1.030 | Passed; preliminary |
| [Offboarding 10,000 in waves, default, wave 2 (2,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/attempts/1) | 2,000 / 2,000 | (shared with wave 1) | 2,000 original; 0 reconciled; 0 missing | 287.9 / 520.0 / 544.1 (2,000) | 1.677 / 1.834 | 0.889 / 1.011 | Passed; preliminary |
| [Quota 1,000, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37690106740/attempts/1) | 1 / 1,000 | 1,000 / 1,000 finalized | 1,000 | 156.5 / 276.6 / 288.6 (1,000) | 1.664 / 1.835 | 0.797 / 0.911 | Passed; full allowance used; preliminary |
| [Quota 10,000 at once, default](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37733097599/attempts/1) | 10 / 10,000 | 10,000 / 10,000 finalized | 8,921 original + 90 reconciled = 9,011; 989 rejected at pool entry; 0 unresolved | 2,682.3 / 3,347.2 / 3,355.9 (8,921) | 1.654 / 1.845 | 0.789 / 0.946 | **Failed** completion target |
| [Quota 10,000 in waves, default, wave 1 (8,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37751232138/attempts/1) | 10 / 8,000 | 10,000 / 10,000 finalized (both waves) | 8,000 original; 0 reconciled; 0 unresolved | 1,787.0 / 2,324.0 / 2,329.6 (8,000) | 1.661 / 1.882 | 0.791 / 0.967 | Passed |
| [Quota 10,000 in waves, default, wave 2 (2,000)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37751232138/attempts/1) | (same 10) / 2,000 | (shared with wave 1) | 2,000 original; 0 reconciled; 0 unresolved | 288.2 / 524.3 / 548.3 (2,000) | 1.659 / 1.845 | 0.791 / 0.915 | Passed |
| [Quota 10,000 at once, enlarged (11,000 entries / 256 MiB)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37772925410/attempts/1) | 10 / 10,000 | 10,000 / 10,000 finalized | 10,000 original; 0 reconciled; 0 unresolved | 2,743.6 / 3,577.0 / 3,588.5 (10,000) | 1.680 / 1.916 | 0.804 / 0.952 | Passed |
| [Quota 20,000 at once, enlarged (22,000 entries / 256 MiB)](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37800522275/attempts/1) | 20 / 20,000 | 20,000 / 20,000 finalized | 4,823 original + 15,162 reconciled = 19,985; 0 rejected; 15 unresolved | 3,558.2 / 8,594.3 / 8,714.9 (4,823) | 1.654 / 1.860 | 0.793 / 0.975 | **Failed** |
| [Offboarding 20,000 at once, enlarged (22,000 entries), retry](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37694191834/attempts/1) | 20,000 / 20,000 | 20,000 / 20,000 finalized | 4,165 original + 2,614 reconciled = 6,779; 0 rejected; 13,221 unresolved | 2,596.9 / 6,306.9 / 7,630.7 (4,165) | 1.651 / 1.870 | 0.876 / 1.026 | **Failed**; incomplete receipt evidence |

Offboarding 1,000: client launch window 0.052 s; pilot stage 290.0 s; final held backing 0 and pallet backing 1, both as expected; fixture preparation 1,163.7 s (setup, not timing).

Offboarding 10,000 at once: client launch window 0.481 s. 989 submissions were rejected at pool entry (`1016`, pool limit) and 89 watches were dropped. Reconciliation found all 89 as successful unloads in saved canonical, finalized blocks; none of the 989 rejected transactions is in the saved block range 175287–175678, and no watch is left unresolved. Finality uses the 8,922 original watches; the reconciled receipts have no timing. The driver stopped at its receipt-audit assertion, so the final destination-balance, held-backing and token snapshot was **not observed**. Fixture preparation took 9,526 s (setup, not timing). Recovery passed. The effective pool was the node default: `network.toml` has no pool override, and `poolTransactions=11000` in the fixture is an inactive input. RPC subscriptions per connection were 20,050, a client-connection setting, not a pool change. An earlier dispatch, [run 37603781867](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37603781867/attempts/1), was cancelled and has no result. Offboarding 10,000 in waves ([run 37645548491](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/attempts/1)) has since completed; see below.

Offboarding 10,000 in waves: client launch windows 0.344 s (wave 1) and 0.093 s (wave 2); wave 2 was released after wave 1 settled. Held backing was 4,000 after wave 1 and 0 after wave 2; final free backing 1, all as expected. Receipts span 348 blocks (wave 1) and 87 blocks (wave 2), at most 23 per block. Preparation took 3,980 s (setup, not timing), with setup batch 250 and 8 proof workers. Recovery passed. The effective pool was the node default, with no pool startup overrides; `poolTransactions=11000` in the fixture is an inactive input. Each wave's percentiles are reported separately and not combined.

Quota 1,000: client launch window 0.049 s; 44 blocks, at most 23 per block. The allowance limit was 1,000, so one person made all 1,000 requests and used every free token in the period. After that, reusing a consumed token (counter 0) was rejected with custom error 57, and counter 1,000 was rejected with custom error 58. Final held backing 0 and pallet backing 1, as expected. Preparation took 465 s. Real period rollover was not exercised.

Quota 10,000 at once: client launch window 0.528 s. 989 rejected at pool entry (`1016`) and 90 watches dropped; reconciliation found all 90 as successful unloads in saved blocks 174187–174742, and no watch is left unresolved. Final state agrees with the receipts: 9,011 actors credited and 989 not, 9,011 tokens consumed, held backing 1,978 (989 × 2) and free backing 1. 392 blocks, at most 23 per block. Setup 3,028 s. Recovery passed.

Quota 10,000 in waves: client launch windows 0.372 s and 0.087 s. Ten people each used their whole allowance. 20 negative probes (two per person) were rejected as designed: 10 with custom error 57 and 10 with custom error 58. Held backing 4,000 after wave 1 and 0 after wave 2; free backing 1. 348 and 87 blocks, at most 23 per block. Setup 2,979 s. Recovery passed.

Quota 10,000 enlarged: client launch window 0.438 s; pool flags `--pool-limit=11000` and `--pool-kbytes=262144` on both People collators. 20 negative probes rejected as designed (10 × error 57, 10 × error 58). Held backing 0, free backing 1. 435 blocks, at most 23 per block. Setup 3,411 s. Recovery passed.

Quota 20,000 enlarged: client launch window 1.085 s; `--pool-limit=22000`. Watches: 4,823 finalized, 15,176 "invalid" and 1 RPC internal error. Reconciliation over 936 saved blocks (175190–176125) found 15,162 successful unloads; 15 were not found in the saved blocks. Final state: 19,985 tokens consumed and 15 unconsumed, on the same 15 actors as the unresolved watches; held backing 30 (15 × 2) and free backing 1. State is consistent with those 15 not completing, but it is not receipt evidence. Finality uses the 4,823 original watches only. Negative probes were not reached after the receipt assertion. The CI process then timed out at shutdown (120 s), after the workload; that is separate from the workload outcome. This run included the block-saving fix `7f269bc` ("preserve finalized blocks missed by Coinage watches"). Setup 5,865 s. Recovery passed.

Offboarding 20,000 enlarged retry: client launch window 1.038 s. Watches: 4,165 finalized, 15,831 "ready, then invalid" and 4 RPC internal errors. Reconciliation found 2,614 more successful unloads; 13,221 are unresolved. The run predates the block-saving fix and saved only blocks named by finalized watches: 295 of the 1,206 heights in 175556–176761, so 911 heights were never saved. Final state with complete observation of all 20,000 actors: held backing 0, free backing 1, every token consumed. That is consistent with all offboards completing, but it is not receipt evidence, so the result is **incomplete evidence**, not "6,779 of 20,000 succeeded". Finality uses the 4,165 original watches. CI also timed out at shutdown after the workload. Setup 7,858 s. Recovery passed.

The quota case's allowance limit was 1,000, so all 100 requests came from one person. Two negative probes were rejected as designed: a reused token with custom error 57 (`UnloadTokenAlreadyConsumed`) and a counter at the limit with custom error 58 (`UnloadTokenCounterOutOfRange`). Real period rollover was not exercised. Policy rows come from a separate model, not native iOS or Android code.

## Full-flow measurements

A fixed plan per person: top-up → readiness → unload into a payment coin → claim → recycle → readiness → offboard. It is not the wallet planner. All runs used test commit [`aa72510d3fbf`](https://github.com/paritytech/polkadot-pop-e2e/commit/aa72510d3fbf321b2946430db0264f50ae5d8785), the default pool and distinct people. Block counts are the blocks holding each stage's receipts; for non-unload stages, the most in one block is the maximum seen in this run, not block capacity.

| Run / stage | People | Requested / original / reconciled / rejected / unresolved | Client launch (s) | Finality p50 / p95 / max (N) | Blocks / most in one block | Result |
| --- | ---: | --- | ---: | --- | --- | --- |
| [Smoke](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37854332739/attempts/1), all five stages | 1 | 5 / 5 / 0 / 0 / 0 | — | Top-up 35.9; payment unload 34.4; claim 35.9; recycle 35.0; offboard 38.6 (1 each) | 1 / 1 per stage | Passed |
| [100](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37855938846/attempts/1) · top-up | 100 | 100 / 100 / 0 / 0 / 0 | 0.005 | 34.4 / 34.4 / 34.4 (100) | 1 / 100 | Passed |
| 100 · payment unload | 100 | 100 / 100 / 0 / 0 / 0 | 0.006 | 49.8 / 61.8 / 61.8 (100) | 5 / 23 | Passed |
| 100 · claim | 100 | 100 / 100 / 0 / 0 / 0 | 0.005 | 34.3 / 34.3 / 34.3 (100) | 1 / 100 | Passed |
| 100 · recycle | 100 | 100 / 100 / 0 / 0 / 0 | 0.004 | 34.4 / 34.4 / 34.4 (100) | 1 / 100 | Passed |
| 100 · offboard | 100 | 100 / 100 / 0 / 0 / 0 | 0.005 | 48.4 / 60.5 / 60.5 (100) | 5 / 23 | Passed |
| [1,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37858620774/attempts/1) · top-up | 1,000 | 1,000 / 1,000 / 0 / 0 / 0 | 0.042 | 45.0 / 53.0 / 57.0 (1,000) | 5 / 260 | Passed |
| 1,000 · payment unload | 1,000 | 1,000 / 1,000 / 0 / 0 / 0 | 0.049 | 164.4 / 296.5 / 308.5 (1,000) | 44 / 23 | Passed |
| 1,000 · claim | 1,000 | 1,000 / 1,000 / 0 / 0 / 0 | 0.039 | 31.4 / 31.4 / 31.4 (1,000) | 1 / 1,000 | Passed |
| 1,000 · recycle | 1,000 | 1,000 / 1,000 / 0 / 0 / 0 | 0.038 | 36.2 / 48.2 / 48.2 (1,000) | 4 / 287 | Passed |
| 1,000 · offboard | 1,000 | 1,000 / 1,000 / 0 / 0 / 0 | 0.052 | 152.2 / 272.3 / 284.3 (1,000) | 44 / 23 | Passed |
| [10,000 at once](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37863573263/attempts/1) · top-up | 10,000 | 10,000 / 0 / 0 / 0 / 10,000 | 0.123 | — (0) | — | Test-tool failure; no chain load |

Preparation (setup, not timing): 179.5 s (smoke), 179.8 s (100), 396.1 s (1,000) and 2,729.6 s (10,000). In the 10,000 run, the sender disconnected at every attempted top-up submission: 10,000 RPC errors (`WebSocket is not connected`) and no ready, in-block or finalized observation, so later stages were not reached. An earlier reconciliation misclassified 94 of these errors as pool rejections by matching "1016" inside the signed request hex; the corrected review excludes request payloads and is the one used here. The retry, [run 37899564808](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37899564808/attempts/1) at commit [`36231206012e`](https://github.com/paritytech/polkadot-pop-e2e/commit/36231206012e70b5eaf06df1ae983d44dee78012) ("check Coinage sender connection before each wave"), was running at this update and is not verified. Full flow 10,000 in waves, 10,000 enlarged and 20,000 enlarged have not run.

## Merchant and quota evidence references

Verified locally on 7 October 2026. Selected summaries are in the [remaining-flow evidence folder](evidence/remaining-flow-2026-10-07/SHA256SUMS.txt); they are not the full raw artifacts. Offboarding 1,000, 10,000 at once, 10,000 in waves, quota 1,000 and the no-result reviews are in the [8 October evidence folder](evidence/remaining-flow-2026-10-08/SHA256SUMS.txt). The larger quota cases, the offboarding 20,000 retry and the full-flow runs are in the [9 October evidence folder](evidence/remaining-flow-2026-10-09/SHA256SUMS.txt).

| Case | Run / attempt / job | Test commit | Evidence files | Local verification |
| --- | --- | --- | --- | --- |
| Merchant 100, 1,000, 10,000 paced, 10,000 enlarged, 20,000 enlarged | [37510457575 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1); jobs in [Merchant fan-in measurements](#merchant-fan-in-measurements) | [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5) | `claim-burst-summary.json`, `claim-burst-audit.json`, `handoff-verification.txt` per case in [merchant/](evidence/remaining-flow-2026-10-07/merchant/20000-burst-enlarged/handoff-verification.txt) | `verify-remaining-flow.py` recheck, 7 October 2026 |
| Merchant 10,000, default | [37510457575 / 1 / 112493393120](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/job/112493393120) | [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5) | [reconciliation](evidence/remaining-flow-2026-10-07/merchant/10000-burst-default/claim-burst-reconciliation.json), [summary](evidence/remaining-flow-2026-10-07/merchant/10000-burst-default/claim-burst-summary.json), [audit](evidence/remaining-flow-2026-10-07/merchant/10000-burst-default/claim-burst-audit.json) | Offline reconciliation of 818 dropped watches, 7 October 2026 |
| Quota 100, default | [37570768389 / 1 / 112628661431](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37570768389/job/112628661431) | [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55) | [summary](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-summary.json), [audit](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-wave-1-audit.json), [probes](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-negative-probes.json), [proofs](evidence/remaining-flow-2026-10-07/quota-100/quota-pilot-wave-1-proofs.jsonl) | [Verifier output](evidence/remaining-flow-2026-10-07/quota-100/local-verification.txt), 7 October 2026 |
| Offboarding 100, default | [37590878841 / 1 / 112691846783](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37590878841/job/112691846783) | [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55) | [summary](evidence/remaining-flow-2026-10-07/offboard-100/offboard-pilot-summary.json), [audit](evidence/remaining-flow-2026-10-07/offboard-100/offboard-pilot-wave-1-audit.json), [proofs](evidence/remaining-flow-2026-10-07/offboard-100/offboard-pilot-wave-1-proofs.jsonl) | [Verifier output](evidence/remaining-flow-2026-10-07/offboard-100/local-verification.txt), 7 October 2026 |
| Offboarding 1,000, default | [37593396451 / 1 / 112700138107](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37593396451/job/112700138107) | [`37b02ba65a52`](https://github.com/paritytech/polkadot-pop-e2e/commit/37b02ba65a52370e64c91b6809e1f2258ce48d55) | [summary](evidence/remaining-flow-2026-10-08/offboard-1000/offboard-pilot-summary.json), [audit](evidence/remaining-flow-2026-10-08/offboard-1000/offboard-pilot-wave-1-audit.json), [state](evidence/remaining-flow-2026-10-08/offboard-1000/offboard-pilot-wave-1-state.json), [proofs](evidence/remaining-flow-2026-10-08/offboard-1000/offboard-pilot-wave-1-proofs.jsonl) | [Verifier output](evidence/remaining-flow-2026-10-08/offboard-1000/local-verification.txt), 8 October 2026 |
| Offboarding 10,000 at once, default | [37606103903 / 1 / 112741880745](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37606103903/job/112741880745) | [`4a652d912e9d`](https://github.com/paritytech/polkadot-pop-e2e/commit/4a652d912e9d38c02a9c41e7496bf1acca41cdbd) | [wave summary](evidence/remaining-flow-2026-10-08/offboard-10000/offboard-pilot-wave-1-summary.json), [audit](evidence/remaining-flow-2026-10-08/offboard-10000/offboard-pilot-wave-1-audit.json), [reconciliation](evidence/remaining-flow-2026-10-08/offboard-10000/offboard-pilot-wave-1-reconciliation.json), [review](evidence/remaining-flow-2026-10-08/offboard-10000/continuation-review.json); proof summary in [unload-blocks.json](evidence/remaining-flow-2026-10-08/unload-blocks.json) | Review 7 October 2026; [receipt-only check](evidence/remaining-flow-2026-10-08/offboard-10000/independent-receipt-verification.txt) and [verifier note](evidence/remaining-flow-2026-10-08/offboard-10000/local-verification.txt); independent reconciliation check in `unload-blocks.json`, 8 October 2026 |
| Offboarding 10,000 in waves, default | [37645548491 / 1 / 112875289822](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37645548491/job/112875289822) | [`42f2e8d99753`](https://github.com/paritytech/polkadot-pop-e2e/commit/42f2e8d997531e0731a8551147badca4bb55456e) | [summary](evidence/remaining-flow-2026-10-08/offboard-10000-paced/offboard-pilot-summary.json), [wave 1 audit](evidence/remaining-flow-2026-10-08/offboard-10000-paced/offboard-pilot-wave-1-audit.json), [wave 2 audit](evidence/remaining-flow-2026-10-08/offboard-10000-paced/offboard-pilot-wave-2-audit.json), [wave 1 state](evidence/remaining-flow-2026-10-08/offboard-10000-paced/offboard-pilot-wave-1-state.json), [wave 2 state](evidence/remaining-flow-2026-10-08/offboard-10000-paced/offboard-pilot-wave-2-state.json), [review](evidence/remaining-flow-2026-10-08/offboard-10000-paced/continuation-review.json); proof summary in [unload-blocks.json](evidence/remaining-flow-2026-10-08/unload-blocks.json) | [Verifier output](evidence/remaining-flow-2026-10-08/offboard-10000-paced/local-verification.txt) and [review check](evidence/remaining-flow-2026-10-08/offboard-10000-paced/independent-verification.txt), 7–8 October 2026 |
| Quota 1,000, default | [37690106740 / 1 / 113027844444](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37690106740/job/113027844444) | [`fd826a3843e1`](https://github.com/paritytech/polkadot-pop-e2e/commit/fd826a3843e1a6a40990a616bcbf3de8be400fb2) | [summary](evidence/remaining-flow-2026-10-08/quota-1000/quota-pilot-summary.json), [audit](evidence/remaining-flow-2026-10-08/quota-1000/quota-pilot-wave-1-audit.json), [quota](evidence/remaining-flow-2026-10-08/quota-1000/quota-pilot-quota.json), [probes](evidence/remaining-flow-2026-10-08/quota-1000/quota-pilot-negative-probes.json), [state](evidence/remaining-flow-2026-10-08/quota-1000/quota-pilot-wave-1-state.json), [proofs](evidence/remaining-flow-2026-10-08/quota-1000/quota-pilot-wave-1-proofs.jsonl) | [Verifier output](evidence/remaining-flow-2026-10-08/quota-1000/local-verification.txt), 8 October 2026 |
| Unloads per block, all unload cases | Runs above | — | [unload-blocks.json](evidence/remaining-flow-2026-10-08/unload-blocks.json) and its [script](evidence/remaining-flow-2026-10-08/unload_blocks.py) | Saved raw blocks and collator logs, 8 October 2026 |
| Quota 10,000 at once, default | [37733097599 / 1 / 113166506357](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37733097599/job/113166506357) | [`7f269bcf4f65`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419) | [review](evidence/remaining-flow-2026-10-09/quota-10000-burst-default/continuation-review.json), [summary](evidence/remaining-flow-2026-10-09/quota-10000-burst-default/quota-pilot-wave-1-summary.json), [audit](evidence/remaining-flow-2026-10-09/quota-10000-burst-default/quota-pilot-wave-1-audit.json), [reconciliation](evidence/remaining-flow-2026-10-09/quota-10000-burst-default/quota-pilot-wave-1-independent-reconciliation.json), [failure state](evidence/remaining-flow-2026-10-09/quota-10000-burst-default/quota-pilot-failure-state.json) | [Receipt-only check](evidence/remaining-flow-2026-10-09/quota-10000-burst-default/independent-receipt-verification.txt) and review, 8 October 2026 |
| Quota 10,000 in waves, default | [37751232138 / 1 / 113224729583](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37751232138/job/113224729583) | [`7f269bcf4f65`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419) | [review](evidence/remaining-flow-2026-10-09/quota-10000-paced-default/continuation-review.json), [summary](evidence/remaining-flow-2026-10-09/quota-10000-paced-default/quota-pilot-summary.json), [quota](evidence/remaining-flow-2026-10-09/quota-10000-paced-default/quota-pilot-quota.json), [probes](evidence/remaining-flow-2026-10-09/quota-10000-paced-default/quota-pilot-negative-probes.json) | [Verifier output](evidence/remaining-flow-2026-10-09/quota-10000-paced-default/local-verification.txt), 9 October 2026 |
| Quota 10,000 at once, enlarged | [37772925410 / 1 / 113296708506](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37772925410/job/113296708506) | [`7f269bcf4f65`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419) | [review](evidence/remaining-flow-2026-10-09/quota-10000-burst-enlarged/continuation-review.json), [summary](evidence/remaining-flow-2026-10-09/quota-10000-burst-enlarged/quota-pilot-summary.json), [quota](evidence/remaining-flow-2026-10-09/quota-10000-burst-enlarged/quota-pilot-quota.json), [probes](evidence/remaining-flow-2026-10-09/quota-10000-burst-enlarged/quota-pilot-negative-probes.json) | [Verifier output](evidence/remaining-flow-2026-10-09/quota-10000-burst-enlarged/local-verification.txt), 9 October 2026 |
| Quota 20,000 at once, enlarged | [37800522275 / 1 / 113391234697](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37800522275/job/113391234697) | [`7f269bcf4f65`](https://github.com/paritytech/polkadot-pop-e2e/commit/7f269bcf4f65109d6eb84b29c6afb1821c48c419) | [review](evidence/remaining-flow-2026-10-09/quota-20000-burst-enlarged/continuation-review.json), [selected-evidence review](evidence/remaining-flow-2026-10-09/quota-20000-burst-enlarged/selected-evidence-review.json), [unresolved watches](evidence/remaining-flow-2026-10-09/quota-20000-burst-enlarged/unresolved-watch-details.json), [reconciliation summary](evidence/remaining-flow-2026-10-09/reconciliation-summaries.json), [shutdown timeout](evidence/remaining-flow-2026-10-09/quota-20000-burst-enlarged/unload-shutdown-error.json) | [Receipt-only check](evidence/remaining-flow-2026-10-09/quota-20000-burst-enlarged/independent-receipt-verification.txt) and reviews, 8 October 2026 |
| Offboarding 20,000 enlarged, retry | [37694191834 / 1 / 113041646266](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37694191834/job/113041646266) | [`e163be942607`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52) | [review](evidence/remaining-flow-2026-10-09/offboard-20000-burst-enlarged/continuation-review.json), [timing and coverage](evidence/remaining-flow-2026-10-09/offboard-20000-burst-enlarged/timing-and-coverage-review.json), [state review](evidence/remaining-flow-2026-10-09/offboard-20000-burst-enlarged/state-observation-review.json), [reconciliation summary](evidence/remaining-flow-2026-10-09/reconciliation-summaries.json) | [Original receipt check](evidence/remaining-flow-2026-10-09/offboard-20000-burst-enlarged/original-receipt-verification.txt) and reviews, 8 October 2026 |
| Full flow smoke, 100 and 1,000 | [37854332739 / 1 / 113574808083](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37854332739/job/113574808083), [37855938846 / 1 / 113580049322](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37855938846/job/113580049322), [37858620774 / 1 / 113588780506](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37858620774/job/113588780506) | [`aa72510d3fbf`](https://github.com/paritytech/polkadot-pop-e2e/commit/aa72510d3fbf321b2946430db0264f50ae5d8785) | Reviews and summaries for [smoke](evidence/remaining-flow-2026-10-09/full-flow-smoke/continuation-review.json), [100](evidence/remaining-flow-2026-10-09/full-flow-100/continuation-review.json) and [1,000](evidence/remaining-flow-2026-10-09/full-flow-1000/continuation-review.json) | Verifier output for [smoke](evidence/remaining-flow-2026-10-09/full-flow-smoke/local-verification.txt), [100](evidence/remaining-flow-2026-10-09/full-flow-100/local-verification.txt) and [1,000](evidence/remaining-flow-2026-10-09/full-flow-1000/local-verification.txt), 9 October 2026 |
| Full flow 10,000 at once | [37863573263 / 1 / 113604870154](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37863573263/job/113604870154) | [`aa72510d3fbf`](https://github.com/paritytech/polkadot-pop-e2e/commit/aa72510d3fbf321b2946430db0264f50ae5d8785) | [review](evidence/remaining-flow-2026-10-09/full-flow-10000-burst-default/continuation-review.json), [top-up summary](evidence/remaining-flow-2026-10-09/full-flow-10000-burst-default/full-flow-pilot-wave-1-topup-summary.json), [reconciliation summaries](evidence/remaining-flow-2026-10-09/reconciliation-summaries.json) | Corrected review, 9 October 2026 |
| Unloads per block, 8–9 October cases | Runs above | — | [unload-blocks.json](evidence/remaining-flow-2026-10-09/unload-blocks.json) and its [script](evidence/remaining-flow-2026-10-09/unload_blocks.py) | Saved raw blocks and collator logs, 9 October 2026 |
| Setup failures and skipped cases | [37510457575 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37510457575/attempts/1) | [`7373fe8c1def`](https://github.com/paritytech/polkadot-pop-e2e/commit/7373fe8c1def9c8a5ef6531859ac85a844945bd5) | [case ledger](evidence/remaining-flow-2026-10-07/case-ledger-remaining-flow.json) | Job conclusions and stages, 7 October 2026 |

## Unload cases with no workload result

None of these produced a workload result. GitHub conclusions on later attempts are not results. Links point to attempt 1.

| Case | Run / attempt | Commit | What happened | Evidence |
| --- | --- | --- | --- | --- |
| Offboarding 10,000, enlarged pool | [37672641924 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37672641924/attempts/1), pilot job [112968099614](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37672641924/job/112968099614) | [`7322395`](https://github.com/paritytech/polkadot-pop-e2e/commit/73223951e57549a88f20fd22033ed53575977976) | The self-hosted runner lost communication with GitHub during the smoke and pilot step. No workload artifact survived. Attempt 2 was started automatically by `cattery-scheduler[bot]` and cancelled under the no-automatic-retry rule. Cause not established. | [review](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37672641924/continuation-review.json), [annotation](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37672641924/attempt-1-annotations.json), [attempt 1 jobs](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37672641924/attempt-1-jobs.json), [attempt 2 jobs](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37672641924/attempt-2-jobs.json) |
| Offboarding 10,000, enlarged pool, second run | [37684376141 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37684376141/attempts/1), pilot job [113008352654](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37684376141/job/113008352654) | [`fd826a3`](https://github.com/paritytech/polkadot-pop-e2e/commit/fd826a3843e1a6a40990a616bcbf3de8be400fb2) | The runner lost communication again. Attempt 2, also started by `cattery-scheduler[bot]`, shows "success" on GitHub, but its pilot job was skipped and **no workload ran**; it is excluded. Cause not established. | [review](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37684376141/continuation-review.json), [annotation](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37684376141/attempt-1-annotations.json), [attempt 1 jobs](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37684376141/attempt-1-jobs.json), [attempt 2 jobs](evidence/remaining-flow-2026-10-08/not-run/offboard-10000-enlarged-37684376141/attempt-2-jobs.json) |
| Offboarding 20,000, enlarged pool (22,000 entries) | [37687780845 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37687780845/attempts/1), pilot job [113019981874](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37687780845/job/113019981874) | [`fd826a3`](https://github.com/paritytech/polkadot-pop-e2e/commit/fd826a3843e1a6a40990a616bcbf3de8be400fb2) | Setup failure while starting the six relay validators and two People collators. The zombienet orchestrator panicked (`lib.rs:842`): an automatically allocated Prometheus port, 30337, was Collator-1600's fixed p2p port. Fixed in [`e163be9`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52) by reserving fixed ports. 0 submitted. | [review](evidence/remaining-flow-2026-10-08/not-run/offboard-20000-enlarged-37687780845/continuation-review.json), [jobs](evidence/remaining-flow-2026-10-08/not-run/offboard-20000-enlarged-37687780845/attempt-1-jobs.json) |
| Offboarding 20,000, enlarged pool, retry | [37694191834 / 1](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/37694191834/attempts/1) | [`e163be9`](https://github.com/paritytech/polkadot-pop-e2e/commit/e163be9426078d59dc70e5c1ad846d48a4971e52) | Ran after this table was first written: incomplete receipt evidence (6,779 proven, 13,221 unresolved). See [Free-quota and offboarding measurements](#free-quota-and-offboarding-measurements). | [review](evidence/remaining-flow-2026-10-09/offboard-20000-burst-enlarged/continuation-review.json) |

All quota profiles have since run (see above). Full flow 10,000 in waves, 10,000 enlarged and 20,000 enlarged have not run, and the full flow 10,000-at-once retry was running at this update.

## Machine resources during claim bursts

All three runs used the `parity-large` runner (AMD EPYC 7B13, 32 logical CPUs, 62.8 GiB RAM). Machine CPU is the share of all 32 logical CPUs that were busy, from `/proc/stat` every ~5 s. Machine memory is MemTotal minus MemAvailable. Process memory is `ps` RSS every ~10 s. Process CPU is average cores in the window, from `ps` lifetime CPU and the process start time. "Idle" is the network running before fixture preparation; "burst" is first submission to last receipt. See the [host resource data](evidence/host-resources-2026-10-07/host-resources.json).

| Claims / run | Machine CPU average: idle / fixtures / burst (burst peak) | Machine memory average: idle / fixtures / burst (burst peak), GiB | Collator 1 / 2 cores in burst | Collator 1 / 2 RSS burst peak, GiB | Load generator cores: fixtures / burst |
| --- | --- | --- | --- | --- | --- |
| [20,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36832069153/attempts/1) | 4.5% / 5.4% / 8.6% (20.7%) | 11.9 / 12.6 / 14.2 (14.8) | 0.59 / 0.44 | 1.80 / 1.88 | 0.36 / 0.15 |
| [40,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36836204912/attempts/1) | 4.5% / 7.5% / 10.2% (25.2%) | 12.0 / 13.4 / 15.3 (15.8) | 0.98 / 0.60 | 2.17 / 2.16 | 0.97 / 0.18 |
| [100,000](https://github.com/paritytech/polkadot-pop-e2e/actions/runs/36840043405/attempts/1) | 4.6% / 7.4% / 12.4% (21.3%) | 11.9 / 15.1 / 18.8 (19.8) | 1.32 / 0.66 | 3.38 / 2.95 | 0.95 / 0.42 |

Both People collators used about 0.02 cores when idle and during fixture preparation. All claims were sent to collator 1 (RPC port 10010); collator 2 received them only through the network.
