"""Count verified unloads per block, block-authoring stop reasons and proof timings from saved evidence.

Run: python3 unload_blocks.py <path to coinage-test-evidence/cases>
Writes unload-blocks.json in the current directory. The raw evidence is kept locally, not on this site.
"""
import collections, glob, hashlib, json, math, re, sys

ROOT = sys.argv[1]
CASES = {
    "quota-100": ("coinage-burst-case-100-default-quota-37570768389/coinage-quota-100-burst-default-pilot-37570768389-1", "quota"),
    "offboard-100": ("coinage-burst-case-100-default-offboard-37590878841/coinage-offboard-100-burst-default-pilot-37590878841-1", "offboard"),
    "offboard-1000": ("coinage-burst-case-1000-default-offboard-37593396451/coinage-offboard-1000-burst-default-pilot-37593396451-1", "offboard"),
    "offboard-10000": ("coinage-burst-case-10000-burst-default-offboard-37606103903/coinage-offboard-10000-burst-default-pilot-37606103903-1", "offboard"),
    "quota-1000": ("coinage-burst-case-1000-default-quota-37690106740/coinage-quota-1000-burst-default-pilot-37690106740-1", "quota"),
    "offboard-10000-paced-wave-1": ("coinage-burst-case-10000-paced-default-offboard-37645548491/coinage-offboard-10000-paced-default-pilot-37645548491-1", "offboard", 1),
    "offboard-10000-paced-wave-2": ("coinage-burst-case-10000-paced-default-offboard-37645548491/coinage-offboard-10000-paced-default-pilot-37645548491-1", "offboard", 2),
}


def nearest_rank(values, pct):
    values = sorted(values)
    return values[max(0, math.ceil(pct / 100 * len(values)) - 1)]


def block_number(header):
    n = header["number"]
    return int(n, 16) if isinstance(n, str) and n.startswith("0x") else int(n)


out = {"definitions": {
    "receiptsFile": "Verified receipts in the run's own <scenario>-pilot-wave-<n>-receipts.json, grouped by block number (original watches only).",
    "rawBlocks": "Independent pass over saved raw blocks: extrinsics whose events include System.ExtrinsicSuccess and Coinage.RecyclerUnloadedIntoExternalAsset. Includes reconciled receipts.",
    "stopReasons": "Collator log line 'Prepared block for proposing at N ... end: <reason>; extrinsics_count: K', matched to each canonical block by height and extrinsic count (the logged hash is taken before sealing, so it differs from the final block hash).",
    "refTimeMs": "ref_time in the ExtrinsicSuccess dispatch_info of each successful unload (post-dispatch weight), in milliseconds.",
    "proofs": "Client proof generation time per proof kind, nearest-rank percentiles, from <scenario>-pilot-wave-<n>-proofs.jsonl. Generated before release; not part of finality."}}
for name, spec in CASES.items():
    rel, sc = spec[0], spec[1]
    wave = spec[2] if len(spec) > 2 else 1
    path = f"{ROOT}/{rel}"
    receipts = json.load(open(f"{path}/{sc}-pilot-wave-{wave}-receipts.json"))
    items = receipts if isinstance(receipts, list) else next(v for v in receipts.values() if isinstance(v, list))
    per_receipt_block = collections.Counter(x["block"]["number"] if isinstance(x.get("block"), dict) else x.get("blockNumber") for x in items)
    files = glob.glob(f"{path}/evidence/{sc}-pilot-wave-{wave}/block-*.json") or glob.glob(f"{path}/{sc}-pilot-block-*.json")
    per_block, extrinsic_count, weights, hashes = {}, {}, [], set()
    for f in files:
        b = json.load(open(f))
        n = block_number(b["block"]["block"]["header"])
        extrinsics = b["block"]["block"]["extrinsics"]
        extrinsic_count[n] = len(extrinsics)
        events = collections.defaultdict(list)
        for e in b["events"]:
            if e["phase"]["type"] == "ApplyExtrinsic":
                events[e["phase"]["value"]].append(e["event"])
        count = 0
        for i, raw in enumerate(extrinsics):
            ev = events[i]
            unload = any(e["type"] == "Coinage" and e["value"]["type"] == "RecyclerUnloadedIntoExternalAsset" for e in ev)
            ok = [e for e in ev if e["type"] == "System" and e["value"]["type"] == "ExtrinsicSuccess"]
            if unload and ok:
                count += 1
                weights.append(int(ok[0]["value"]["value"]["dispatch_info"]["weight"]["ref_time"]))
                hashes.add("0x" + hashlib.blake2b(bytes.fromhex(raw[2:]), digest_size=32).hexdigest())
        per_block[n] = count
    reasons = collections.defaultdict(set)
    for log in glob.glob(f"{path}/data/Collator-1502*/*.log"):
        for line in open(log, errors="replace"):
            m = re.search(r"Prepared block for proposing at (\d+) \((\d+) ms\) hash: (0x[0-9a-f]+);.*end: (\w+); extrinsics_count: (\d+)", line)
            if m and int(m[1]) in extrinsic_count and int(m[5]) == extrinsic_count[int(m[1])]:
                reasons[int(m[1])].add(m[4])
    full = max(per_block.values())
    stop = collections.Counter(("/".join(sorted(reasons[n])) if reasons.get(n) else "unmatched", "full" if c == full else "partial") for n, c in per_block.items())
    proofs = [json.loads(line) for line in open(f"{path}/{sc}-pilot-wave-{wave}-proofs.jsonl")]
    proof_summary = {}
    for kind in sorted({p["kind"] for p in proofs}):
        v = [p["durationMs"] / 1000 for p in proofs if p["kind"] == kind]
        proof_summary[kind] = {"count": len(v), "p50": round(nearest_rank(v, 50), 3), "p95": round(nearest_rank(v, 95), 3), "max": round(max(v), 3)}
    entry = {
        "receiptsFile": {"verified": sum(per_receipt_block.values()), "blocks": len(per_receipt_block), "maxPerBlock": max(per_receipt_block.values())},
        "rawBlocks": {"files": len(files), "unloadSuccesses": sum(per_block.values()), "blocks": len(per_block), "maxPerBlock": full,
                      "blocksAtMax": sum(1 for c in per_block.values() if c == full), "refTimeMs": sorted({round(w / 1e9, 3) for w in weights})},
        "stopReasons": {f"{r} ({kind} blocks)": k for (r, kind), k in sorted(stop.items())},
        "proofs": proof_summary,
    }
    if name == "offboard-10000":
        rec = json.load(open(f"{path}/offboard-pilot-wave-1-reconciliation.json"))
        ok = [t["txHash"] for t in rec["transactions"] if t["outcome"] == "reconciled-success"]
        rejected = [t["txHash"] for t in rec["transactions"] if t["outcome"] != "reconciled-success"]
        entry["independentReconciliationCheck"] = {"reconciled": len(ok), "foundAsSuccessfulUnload": sum(h in hashes for h in ok),
                                                   "rejectedAtPoolEntry": len(rejected), "rejectedFoundInSavedBlocks": sum(h in hashes for h in rejected)}
    out[name] = entry
json.dump(out, open("unload-blocks.json", "w"), indent=1)
print(json.dumps(out, indent=1))
