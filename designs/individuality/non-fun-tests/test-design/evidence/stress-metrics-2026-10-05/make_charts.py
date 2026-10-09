"""Draw the Coinage stress metrics charts from metrics.json.

Run: python make_charts.py  (needs matplotlib; writes the SVG files next to this script)
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = Path(__file__).parent
DATA = json.loads((HERE / "metrics.json").read_text())

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
BLUE = "#2a78d6"  # finality, or the only series
ORANGE = "#eb6834"  # readiness, or the second series
GREY = "#b9b8b1"  # failed or incomplete

plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "svg.hashsalt": "coinage-stress-metrics",
        "font.family": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "text.color": INK,
        "axes.labelcolor": INK_2,
        "axes.edgecolor": AXIS,
        "axes.facecolor": SURFACE,
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "xtick.labelcolor": INK_2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
    }
)


def fmt_s(v):
    return f"{v:,.0f} s" if v >= 100 else f"{v:,.1f} s"


def style_hbar(ax, xmax):
    ax.set_xlim(0, xmax)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()


def label_bar(ax, y, value, text, xmax, colour=INK):
    ax.text(value + xmax * 0.01, y, text, va="center", ha="left", fontsize=9, color=colour)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def lifecycle(case):
    for item in DATA["lifecycle"]:
        if item["verifiedOutcome"]["case"] == case:
            return item
    raise KeyError(case)


def wave_p95(case, suffix):
    for wave in lifecycle(case)["measurements"]["waves"]:
        if wave["name"].endswith(suffix):
            return wave["finalitySeconds"]["p95"]
    return None


def grouped_hbar(ax, rows, series, xmax, unit_fmt=fmt_s):
    """rows: list of (label, [value or None per series], [status text or None per series], faded)."""
    height = 0.8 / len(series)
    for i, (label, values, notes, faded) in enumerate(rows):
        for j, (name, colour) in enumerate(series):
            value = values[j]
            y = i - 0.4 + height * (j + 0.5)
            if value is None:
                label_bar(ax, y, 0, notes[j] or "no data", xmax, MUTED)
                continue
            ax.barh(
                y,
                value,
                height=height - 0.06,
                color=GREY if faded else colour,
                hatch="////" if faded else None,
                edgecolor=SURFACE,
                linewidth=0,
            )
            text = unit_fmt(value) + (f"  ({notes[j]})" if notes[j] else "")
            label_bar(ax, y, value, text, xmax, INK_2 if faded else INK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    style_hbar(ax, xmax)


# Figure 1: top-up finality and readiness.
def topup_timing():
    earlier = DATA["earlierPublishedResults"]["topups"]
    recon = {t["run"]: t for t in DATA["topupReconciliation"]}
    r1, r2, r3 = recon[36537079387], recon[36619415692], recon[36662212241]
    rows = [
        ("1,000 at once\ndefault pool", [earlier[0]["finalityP95Seconds"], earlier[0]["readinessP95Seconds"]], [None, None], False),
        ("7,000 + 3,000 in waves\ndefault pool", [earlier[1]["finalityP95Seconds"], earlier[1]["readinessP95Seconds"]], [None, None], False),
        ("10,000 at once\nbigger pool (11,000)", [earlier[2]["finalityP95Seconds"], earlier[2]["readinessP95Seconds"]], [None, None], False),
        ("8,400 + 1,600 in waves\ndefault pool", [r3["originalFinalitySeconds"]["p95"], r3["originalReadinessSeconds"]["p95"]], [None, None], False),
        (
            "FAILED: 10,000 at once\ndefault pool",
            [r1["originalFinalitySeconds"]["p95"], r1["originalReadinessSeconds"]["p95"]],
            [f"{r1['originalFinalitySeconds']['count']:,} timed", f"{r1['originalReadinessSeconds']['count']:,} timed"],
            True,
        ),
        (
            "FAILED: 8,500 + 1,500 in waves\ndefault pool",
            [r2["originalFinalitySeconds"]["p95"], r2["originalReadinessSeconds"]["p95"]],
            [f"{r2['originalFinalitySeconds']['count']:,} timed", f"{r2['originalReadinessSeconds']['count']:,} timed"],
            True,
        ),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    grouped_hbar(ax, rows, [("Finality", BLUE), ("Readiness", ORANGE)], 460)
    ax.set_xlabel("Seconds for 95% of top-ups (p95). Shorter is better.")
    ax.set_title("Top-ups: time to settle (finality) and time to use (readiness)")
    ax.legend(
        handles=[
            Patch(color=BLUE, label="Finality p95: payment is settled"),
            Patch(color=ORANGE, label="Readiness p95: voucher can be unloaded"),
            Patch(facecolor=GREY, hatch="////", edgecolor=SURFACE, label="Failed run (timed part only)"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "topup-timing.svg")


# Figure 2: recycling finality and readiness.
def recycling_timing():
    cases = [
        ("b100", "100 at once\ndefault pool"),
        ("b1000", "1,000 at once\ndefault pool"),
        ("b_paced", "8,000 + 2,000 in waves\ndefault pool"),
        ("b_pool", "10,000 at once\nbigger pool (11,000)"),
        ("b20000", "20,000 at once\nbigger pool (22,000)"),
        ("b40000", "40,000 at once\nbigger pool (44,000)"),
        ("b10000", "INCOMPLETE: 10,000 at once\ndefault pool"),
        ("b100000", "INCOMPLETE: 100,000 at once\nbigger pool (110,000)"),
    ]
    rows = []
    for case, label in cases:
        m = lifecycle(case)["measurements"]
        incomplete = lifecycle(case)["verifiedOutcome"]["outcome"] == "incomplete"
        if case == "b_paced":
            # Wave 1 (8,000) is the slower wave and holds most of the actors.
            finality = wave_p95(case, "wave-1-recycle")
        else:
            finality = m["waves"][0]["finalitySeconds"]["p95"]
        readiness = m["readinessSeconds"]
        notes = [None, None]
        if incomplete:
            actors = lifecycle(case)["verifiedOutcome"]["requestedActors"]
            notes = [
                f"{m['waves'][0]['finalitySeconds']['count']:,} of {actors:,} timed",
                f"{readiness['count']:,} of {actors:,} seen",
            ]
        rows.append((label, [finality, readiness["p95"]], notes, incomplete))
    fig, ax = plt.subplots(figsize=(8.6, 6.8))
    grouped_hbar(ax, rows, [("Finality", BLUE), ("Readiness", ORANGE)], 2500)
    ax.set_xlabel("Seconds for 95% of recycled coins (p95). Shorter is better.")
    ax.set_title("Recycling: time to settle (finality) and time to use (readiness)")
    ax.legend(
        handles=[
            Patch(color=BLUE, label="Finality p95: load is settled"),
            Patch(color=ORANGE, label="Readiness p95: coin is in a ring root"),
            Patch(facecolor=GREY, hatch="////", edgecolor=SURFACE, label="Incomplete run (observed part only)"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "recycling-timing.svg")


# Figure 3: claim finality spread (p50, p95, p99).
def claim_finality():
    labels = ["20,000 claims", "40,000 claims", "100,000 claims"]
    fig, ax = plt.subplots(figsize=(8.6, 2.9))
    for i, item in enumerate(DATA["claimCapacityDerived"]):
        s = item["clientObservedSeconds"]["receiptLookup"]
        ax.plot([s["p50"], s["p99"]], [i, i], color=AXIS, linewidth=2, zorder=1)
        ax.scatter([s["p50"]], [i], s=70, color=SURFACE, edgecolor=BLUE, linewidth=2, zorder=3)
        ax.scatter([s["p95"]], [i], s=70, color=BLUE, edgecolor=SURFACE, linewidth=1.5, zorder=3)
        ax.scatter([s["p99"]], [i], s=70, marker="D", color=INK_2, edgecolor=SURFACE, linewidth=1.5, zorder=3)
        ax.text(s["p50"], i - 0.28, f"p50 {s['p50']:.0f} s", ha="center", fontsize=9, color=INK_2)
        ax.text(s["p99"] + 9, i, f"p95 {s['p95']:.0f} s · p99 {s['p99']:.0f} s", va="center", fontsize=9)
    ax.set_yticks(range(3), labels)
    ax.set_ylim(2.6, -0.6)
    ax.set_xlim(0, 420)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Seconds from submit to settled claim")
    ax.set_title("Claims: how long did the slowest claims wait?")
    ax.legend(
        handles=[
            plt.Line2D([], [], marker="o", linestyle="", markerfacecolor=SURFACE, markeredgecolor=BLUE, markeredgewidth=2, markersize=8, label="p50 (half were faster)"),
            plt.Line2D([], [], marker="o", linestyle="", color=BLUE, markersize=8, label="p95"),
            plt.Line2D([], [], marker="D", linestyle="", color=INK_2, markersize=7, label="p99"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.28),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "claim-finality.svg")


# Figure 4: ready queue over time.
def pool():
    titles = ["20,000 claims", "40,000 claims", "100,000 claims"]
    fig, axes = plt.subplots(3, 1, figsize=(8.6, 8.2), sharex=True)
    for ax, item, title in zip(axes, DATA["claimCapacityDerived"], titles):
        samples = item["readyPoolSamples"]
        t = [s["secondsFromBurstStart"] for s in samples]
        for node, colour, name in [("Collator-1502", BLUE, "Collator 1"), ("Collator-1502-2", ORANGE, "Collator 2")]:
            v = [s["readyTransactions"][node] for s in samples]
            ax.plot(t, v, color=colour, linewidth=2, label=name)
            peak = max(v)
            tp = t[v.index(peak)]
            ax.annotate(f"peak {peak:,.0f}", (tp, peak), xytext=(6, 2), textcoords="offset points", fontsize=9, color=INK)
        empty = next(
            s["secondsFromBurstStart"]
            for s in samples
            if s["secondsFromBurstStart"] > 10 and all(n == 0 for n in s["readyTransactions"].values())
        )
        ax.axvline(empty, color=MUTED, linewidth=1)
        ax.text(empty + 4, ax.get_ylim()[1] * 0.55, f"both empty\nat ~{empty:.0f} s", fontsize=9, color=INK_2)
        ax.set_title(title)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.set_ylim(bottom=0)
        ax.set_ylabel("Claims waiting")
    axes[0].legend(loc="upper right", frameon=False, fontsize=9)
    axes[-1].set_xlabel("Seconds since the burst started")
    axes[-1].set_xlim(0, 340)
    fig.tight_layout()
    save(fig, "pool.svg")


# Figure 5: claims per block.
def blocks():
    titles = ["20,000 claims", "40,000 claims", "100,000 claims"]
    exps = DATA["claimCapacity"]["experiments"]
    fig, axes = plt.subplots(3, 1, figsize=(8.6, 7.4), sharey=True)
    for ax, exp, title in zip(axes, exps, titles):
        counts = [c for _, c in sorted(exp["receiptCountsByBlock"].items(), key=lambda kv: int(kv[0]))]
        full = max(counts)
        xs = range(1, len(counts) + 1)
        ax.bar(xs, counts, width=0.8, color=[BLUE if c == full else GREY for c in counts], linewidth=0)
        ax.axhline(full, color=INK, linewidth=1)
        nfull = sum(c == full for c in counts)
        ax.text(0.4, full + 120, f"{full:,} claims in every full block ({nfull} full blocks)", fontsize=9, color=INK)
        ax.text(len(counts), counts[-1] + 80, f"{counts[-1]:,}", ha="center", fontsize=9, color=INK_2)
        ax.set_title(f"{title}: {len(counts)} blocks")
        ax.set_xlim(0.3, len(counts) + 0.7)
        ax.set_ylim(0, 3000)
        ax.set_yticks([0, 1000, 2000], ["0", "1,000", "2,000"])
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_ylabel("Claims in block")
        step = 1 if len(counts) <= 20 else 5
        ax.set_xticks([x for x in xs if x == 1 or x % step == 0])
    axes[-1].set_xlabel("Block in the run (1 = first block with workload claims)")
    fig.tight_layout()
    save(fig, "blocks.svg")


# Figure 6: split-and-claim finality.
def split_claim_timing():
    cases = [
        ("a100", "100 actors at once\ndefault pool"),
        ("a1000", "1,000 actors at once\ndefault pool"),
        ("a_paced", "8,000 + 2,000 in waves\ndefault pool (first wave)"),
        ("a_pool", "10,000 actors at once\nbigger pool (11,000)"),
        ("a20000", "LAUNCH TOO SLOW: 20,000\nbigger pool (22,000)"),
        ("a40000", "40,000 actors at once\nbigger pool (44,000)"),
        ("a100000", "100,000 actors at once\nbigger pool (110,000)"),
        ("a10000", "INCOMPLETE: 10,000 at once\ndefault pool"),
    ]
    rows = []
    for case, label in cases:
        outcome = lifecycle(case)["verifiedOutcome"]["outcome"]
        if case == "a_paced":
            split, claim = wave_p95(case, "wave-1-split"), wave_p95(case, "wave-1-claim")
        else:
            split, claim = wave_p95(case, "-split"), wave_p95(case, "-claim")
        notes = [None, None]
        if case == "a10000":
            notes = ["8,192 of 10,000 timed", "claims not sent"]
        rows.append((label, [split, claim], notes, outcome != "workload-pass"))
    fig, ax = plt.subplots(figsize=(8.6, 6.8))
    grouped_hbar(ax, rows, [("Split", BLUE), ("Claim", ORANGE)], 480)
    ax.set_xlabel("Seconds for 95% of extrinsics to settle (finality p95). Shorter is better.")
    ax.set_title("Split-and-claim: time to settle each step")
    ax.legend(
        handles=[
            Patch(color=BLUE, label="Split p95"),
            Patch(color=ORANGE, label="Claim p95"),
            Patch(facecolor=GREY, hatch="////", edgecolor=SURFACE, label="Not a workload pass"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    save(fig, "split-claim-timing.svg")


# Figure 7: lifecycle completion (verified / requested extrinsics).
def completion():
    order = ["a100", "a1000", "a_paced", "a_pool", "a20000", "a40000", "a100000", "a10000",
             "b100", "b1000", "b_paced", "b_pool", "b20000", "b40000", "b10000", "b100000"]
    names = {
        "a100": "Split-and-claim, 100",
        "a1000": "Split-and-claim, 1,000",
        "a_paced": "Split-and-claim, 10,000 in waves",
        "a_pool": "Split-and-claim, 10,000, bigger pool",
        "a20000": "Split-and-claim, 20,000",
        "a40000": "Split-and-claim, 40,000",
        "a100000": "Split-and-claim, 100,000",
        "a10000": "Split-and-claim, 10,000, default pool",
        "b100": "Recycling, 100",
        "b1000": "Recycling, 1,000",
        "b_paced": "Recycling, 10,000 in waves",
        "b_pool": "Recycling, 10,000, bigger pool",
        "b20000": "Recycling, 20,000",
        "b40000": "Recycling, 40,000",
        "b10000": "Recycling, 10,000, default pool",
        "b100000": "Recycling, 100,000",
    }
    status = {
        "workload-pass": "pass",
        "incomplete": "incomplete",
        "launch-timing-failure": "fail: launch too slow",
    }
    fig, ax = plt.subplots(figsize=(8.6, 7.0))
    for i, case in enumerate(order):
        v = lifecycle(case)["verifiedOutcome"]
        per_actor = 2 if case.startswith("a") else 1
        requested = v["requestedActors"] * per_actor
        pct = 100 * v["receiptVerified"] / requested
        ok = v["outcome"] == "workload-pass"
        ax.barh(i, pct, height=0.7, color=BLUE if ok else GREY, hatch=None if ok else "////", edgecolor=SURFACE, linewidth=0)
        text = f"{pct:.0f}%  {v['receiptVerified']:,} of {requested:,}  ·  {status[v['outcome']]}"
        if v["ciShutdownFailure"]:
            text += " (CI shutdown failed later)"
        label_bar(ax, i, pct, text, 160)
    ax.set_yticks(range(len(order)), [names[c] for c in order])
    style_hbar(ax, 160)
    ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.axhline(7.5, color=AXIS, linewidth=1)
    ax.set_xlabel("Verified receipts as a share of requested extrinsics")
    ax.set_title("Lifecycle cases: how many extrinsics have a verified receipt?")
    save(fig, "lifecycle-completion.svg")


def linear_fit(xs, ys):
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return my - slope * mx, slope


# Machine load during the 100,000-claim run (host-resources-2026-10-07).
def machine_resources():
    host_data = json.loads((HERE.parent / "host-resources-2026-10-07" / "host-resources.json").read_text())
    run = host_data["runs"]["100,000 claims"]
    prep, settled = run["fixturePreparationSeconds"], run["lastReceiptSeconds"]
    host, procs = run["host"], run["processRssGiB"]
    start = run["networkStartSeconds"] / 60
    fig, (cpu, mem) = plt.subplots(2, 1, figsize=(8.6, 7.4), sharex=True)
    for ax in (cpu, mem):
        ax.axvspan(-prep / 60, 0, color=GRID, alpha=0.45, linewidth=0)
        ax.axvspan(0, settled / 60, color=ORANGE, alpha=0.12, linewidth=0)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
    t = [h["t"] / 60 for h in host]
    cpu.plot(t, [h["maxCore"] for h in host], color=AXIS, linewidth=1, label="Busiest single CPU")
    cpu.plot(t, [h["busy"] for h in host], color=BLUE, linewidth=2, label="Whole machine (32 CPUs)")
    cpu.set_ylim(0, 105)
    cpu.set_ylabel("CPU busy (%)")
    cpu.set_title("CPU: the whole machine stayed below 22% busy")

    def phase(a, b, key):
        values = [h[key] for h in host if a <= h["t"] <= b]
        return sum(values) / len(values), max(values)

    idle = phase(run["networkStartSeconds"] + 60, -prep - 30, "busy")
    burst = phase(0, settled, "busy")
    cpu.text(start + 1, 30, f"Network idle:\naverage {idle[0]:.0f}%", fontsize=9, color=INK_2)
    cpu.text(-prep / 60 + 1, 30, "Fixture preparation", fontsize=9, color=INK_2)
    cpu.annotate(f"Burst: average {burst[0]:.0f}%,\npeak {burst[1]:.0f}%", (settled / 60, burst[1]), xytext=(8, 10),
                 textcoords="offset points", fontsize=9, color=INK)
    cpu.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), frameon=False, fontsize=9, ncol=2)

    tm = [h["t"] / 60 for h in host]
    mem.plot(tm, [h["usedGiB"] for h in host], color=BLUE, linewidth=2, label="Whole machine, used")
    series = [("Collator-1502", ORANGE, "People collator 1"), ("Collator-1502-2", "#1baf7a", "People collator 2"), ("driver", INK_2, "Load generator")]
    for key, colour, name in series:
        pts = [(p["t"] / 60, p[key]) for p in procs if key in p]
        burst_peak = max(b for a, b in pts if 0 <= a * 60 <= settled)
        mem.plot([a for a, _ in pts], [b for _, b in pts], color=colour, linewidth=2, label=f"{name} (burst peak {burst_peak:.1f} GiB)")
    used = [h for h in host if h["t"] <= -prep - 30 and h["t"] >= run["networkStartSeconds"] + 60]
    peak_used = max(host, key=lambda h: h["usedGiB"])
    mem.annotate(f"{peak_used['usedGiB']:.1f} GiB of 62.8", (peak_used["t"] / 60, peak_used["usedGiB"]), xytext=(4, 4),
                 textcoords="offset points", fontsize=9, color=INK)
    mem.text(start + 1, sum(h["usedGiB"] for h in used) / len(used) + 1, f"idle: {sum(h['usedGiB'] for h in used) / len(used):.0f} GiB",
             fontsize=9, color=INK_2)
    mem.set_ylim(0, 24)
    mem.set_ylabel("Memory (GiB)")
    mem.set_title("Memory: the load generator used about as much as a collator")
    mem.set_xlabel("Minutes from the first claim (0 = burst start; orange band = burst; grey band = fixture preparation)")
    mem.set_xlim(start, (settled + 420) / 60)
    mem.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=9)
    fig.tight_layout()
    save(fig, "machine-resources.svg")


# Top-up p95 against the largest batch that entered the pool at once.
def topup_trend():
    earlier = DATA["earlierPublishedResults"]["topups"]
    recon = {t["run"]: t for t in DATA["topupReconciliation"]}
    r1, r2, r3 = recon[36537079387], recon[36619415692], recon[36662212241]
    points = [
        ("1,000 at once", 1000, earlier[0]["finalityP95Seconds"], earlier[0]["readinessP95Seconds"], True),
        ("7,000 + 3,000", 7000, earlier[1]["finalityP95Seconds"], earlier[1]["readinessP95Seconds"], True),
        ("8,400 + 1,600", 8400, r3["originalFinalitySeconds"]["p95"], r3["originalReadinessSeconds"]["p95"], True),
        ("8,500 + 1,500 (failed)", 8500, r2["originalFinalitySeconds"]["p95"], None, False),
        ("10,000 at once, default (failed; 9,011 entered)", 9011, r1["originalFinalitySeconds"]["p95"], r1["originalReadinessSeconds"]["p95"], False),
        ("10,000 at once, bigger pool", 10000, earlier[2]["finalityP95Seconds"], earlier[2]["readinessP95Seconds"], True),
    ]
    passing = [p for p in points if p[4]]
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    for idx, colour, name in [(2, BLUE, "Finality p95"), (3, ORANGE, "Readiness p95")]:
        a, b = linear_fit([p[1] for p in passing], [p[idx] for p in passing])
        ax.plot([0, 10500], [a, a + b * 10500], color=colour, linewidth=1, linestyle=(0, (4, 3)), alpha=0.8)
        ax.text(10600, a + b * 10500, f"+{b * 1000:.0f} s per\n1,000 top-ups", va="center", fontsize=9, color=colour)
        for p in points:
            if p[idx] is None:
                continue
            filled = p[4]
            ax.scatter([p[1]], [p[idx]], s=60, zorder=3, color=colour if filled else SURFACE, edgecolor=colour, linewidth=2)
        base = points[0][idx]
        for p in passing:
            text = f"{p[idx]:.0f} s" if p[1] == 1000 else f"{p[idx]:.0f} s (+{100 * (p[idx] / base - 1):.0f}%)"
            if idx == 3:
                ax.annotate(text, (p[1], p[idx]), xytext=(-8, 6), textcoords="offset points", ha="right", fontsize=9, color=INK)
            else:
                ax.annotate(text, (p[1], p[idx]), xytext=(8, -14), textcoords="offset points", ha="left", fontsize=9, color=INK)
        ax.plot([], [], color=colour, marker="o", linestyle="", label=name)
    ax.scatter([], [], s=60, color=SURFACE, edgecolor=MUTED, linewidth=2, label="Failed run (not used for the line)")
    for p in points:
        if not p[4]:
            ax.annotate("failed", (p[1], p[2]), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=8, color=MUTED)
    ax.set_xlim(0, 12300)
    ax.set_ylim(0, 400)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_xticks([0, 2000, 4000, 6000, 8000, 10000])
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Top-ups that entered the pool in the largest single batch")
    ax.set_ylabel("Seconds (p95)")
    ax.set_title("Top-ups: time grows in a straight line with batch size")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, frameon=False, fontsize=9)
    save(fig, "topup-trend.svg")


# Recycling p95 as the burst doubles.
def recycling_growth():
    cases = [("b_pool", 10000), ("b20000", 20000), ("b40000", 40000)]
    rows = []
    for case, actors in cases:
        m = lifecycle(case)["measurements"]
        rows.append((actors, m["waves"][0]["finalitySeconds"]["p95"], m["readinessSeconds"]["p95"]))
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    for idx, colour, name in [(1, BLUE, "Finality p95"), (2, ORANGE, "Readiness p95")]:
        xs, ys = [r[0] for r in rows], [r[idx] for r in rows]
        ax.plot(xs, ys, color=colour, linewidth=2, marker="o", markersize=7, label=name)
        for x, y in zip(xs, ys):
            ax.annotate(f"{y:,.0f} s", (x, y), xytext=(8, -4 if idx == 1 else 6), textcoords="offset points", fontsize=9, color=INK)
        for (x0, y0), (x1, y1) in zip(zip(xs, ys), list(zip(xs, ys))[1:]):
            ax.annotate(f"+{y1 - y0:,.0f} s", ((x0 * x1) ** 0.5, (y0 + y1) / 2), xytext=(-10, 10) if idx == 2 else (12, -16),
                        textcoords="offset points", ha="right" if idx == 2 else "left", fontsize=9, color=colour, fontweight="bold")
    ax.set_xscale("log", base=2)
    ax.set_xticks([10000, 20000, 40000], ["10,000", "20,000", "40,000"])
    ax.minorticks_off()
    ax.set_xlim(8000, 52000)
    ax.set_ylim(0, 1700)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Recycling actors in one burst, bigger pool (each step doubles)")
    ax.set_ylabel("Seconds (p95)")
    ax.set_title("Recycling: each doubling added about 400–700 seconds")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    save(fig, "recycling-growth.svg")


# Merchant fan-in finality p95 (remaining-flow-2026-10-07).
def merchant_timing():
    root = HERE.parent / "remaining-flow-2026-10-07" / "merchant"
    cases = [
        ("100-burst-default", "100 at once\ndefault pool"),
        ("1000-burst-default", "1,000 at once\ndefault pool"),
        ("10000-paced-default", "8,000 + 2,000 in waves\ndefault pool"),
        ("10000-burst-enlarged", "10,000 at once\nbigger pool (11,000)"),
        ("20000-burst-enlarged", "20,000 at once\nbigger pool (22,000)"),
        ("10000-burst-default", "FAILED: 10,000 at once\ndefault pool"),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    for i, (case, label) in enumerate(cases):
        summary = json.loads((root / case / "claim-burst-summary.json").read_text())
        p95 = summary["finalityMs"]["p95"] / 1000
        timed = summary["finalityMs"]["count"]
        sent = summary["sent"]
        verified = summary["verified"]
        failed = not summary["passed"]
        ax.barh(i, p95, height=0.6, color=GREY if failed else BLUE, hatch="////" if failed else None, edgecolor=SURFACE, linewidth=0)
        text = f"{p95:.1f} s  ·  {verified:,} of {sent:,} verified"
        if failed:
            text += f"  ({timed:,} timed)"
        label_bar(ax, i, p95, text, 140, INK_2 if failed else INK)
    ax.set_yticks(range(len(cases)), [c[1] for c in cases])
    style_hbar(ax, 140)
    ax.set_xlabel("Seconds for 95% of transfers to settle (finality p95). Shorter is better.")
    ax.set_title("Merchant fan-in: time to settle each burst")
    ax.legend(
        handles=[
            Patch(color=BLUE, label="Finality p95, passed"),
            Patch(facecolor=GREY, hatch="////", edgecolor=SURFACE, label="Failed run (timed part only)"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=2,
        frameon=False,
        fontsize=9,
    )
    save(fig, "merchant-timing.svg")


if __name__ == "__main__":
    merchant_timing()
    machine_resources()
    topup_trend()
    recycling_growth()
    topup_timing()
    recycling_timing()
    claim_finality()
    pool()
    blocks()
    split_claim_timing()
    completion()
