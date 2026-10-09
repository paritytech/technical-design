"""Count verified unloads per block, block-authoring stop reasons and proof timings for the 8-9 October unload cases.

Run: python3 unload_blocks.py <path to coinage-test-evidence/cases>
Writes unload-blocks.json in the current directory. The raw evidence is kept locally, not on this site.
"""
import collections, glob, json, math, re, sys

ROOT = sys.argv[1]
OFF, PAY = "RecyclerUnloadedIntoExternalAsset", "RecyclerUnloadedIntoCoin"
CASES = {
    "quota-10000-burst-default": ("coinage-burst-case-10000-burst-default-quota-37733097599", "quota-pilot-wave-1", OFF),
    "quota-10000-paced-default-wave-1": ("coinage-burst-case-10000-paced-default-quota-37751232138", "quota-pilot-wave-1", OFF),
    "quota-10000-paced-default-wave-2": ("coinage-burst-case-10000-paced-default-quota-37751232138", "quota-pilot-wave-2", OFF),
    "quota-10000-burst-enlarged": ("coinage-burst-case-10000-burst-enlarged-quota-37772925410", "quota-pilot-wave-1", OFF),
    "quota-20000-burst-enlarged": ("coinage-burst-case-20000-burst-enlarged-quota-37800522275", "quota-pilot-wave-1", OFF),
    "offboard-20000-burst-enlarged": ("coinage-burst-case-20000-burst-enlarged-offboard-37694191834", "offboard-pilot-wave-1", OFF),
    "full-flow-100-payment-unload": ("coinage-burst-case-100-default-full-flow-37855938846", "full-flow-pilot-wave-1-payment", PAY),
    "full-flow-100-offboard": ("coinage-burst-case-100-default-full-flow-37855938846", "full-flow-pilot-wave-1", OFF),
    "full-flow-1000-payment-unload": ("coinage-burst-case-1000-default-full-flow-37858620774", "full-flow-pilot-wave-1-payment", PAY),
    "full-flow-1000-offboard": ("coinage-burst-case-1000-default-full-flow-37858620774", "full-flow-pilot-wave-1", OFF),
}


def nearest_rank(values, pct):
    values = sorted(values)
    return values[max(0, math.ceil(pct / 100 * len(values)) - 1)]


def block_number(header):
    n = header["number"]
    return int(n, 16) if isinstance(n, str) and n.startswith("0x") else int(n)


out = {"definitions": {
    "receiptsFile": "Original verified receipts in the run's own <wave>-receipts.json, grouped by block number.",
    "rawBlocks": "Independent pass over saved raw blocks: extrinsics with System.ExtrinsicSuccess and the expected Coinage unload event. Includes reconciled receipts. Saved blocks only.",
    "stopReasons": "Collator log 'Prepared block for proposing at N ... end: <reason>; extrinsics_count: K', matched to each saved canonical block by height and extrinsic count (the logged hash is taken before sealing).",
    "refTimeMs": "ref_time of each successful unload's ExtrinsicSuccess dispatch_info (post-dispatch weight), in milliseconds.",
    "proofs": "Client proof generation time per proof kind, nearest-rank, from <wave>-proofs.jsonl when present. Generated before release; not part of finality."}}
for name, (case, wave, op) in CASES.items():
    path = glob.glob(f"{ROOT}/{case}/coinage-*-pilot-*")[0]
    receipts = json.load(open(f"{path}/{wave}-receipts.json"))
    items = receipts if isinstance(receipts, list) else next(v for v in receipts.values() if isinstance(v, list))
    per_receipt_block = collections.Counter(x["block"]["number"] if isinstance(x.get("block"), dict) else x.get("blockNumber") for x in items)
    per_block, extrinsic_count, weights = {}, {}, set()
    for f in glob.glob(f"{path}/evidence/{wave}/block-*.json"):
        b = json.load(open(f))
        n = block_number(b["block"]["block"]["header"])
        extrinsic_count[n] = len(b["block"]["block"]["extrinsics"])
        events = collections.defaultdict(list)
        for e in b["events"]:
            if e["phase"]["type"] == "ApplyExtrinsic":
                events[e["phase"]["value"]].append(e["event"])
        count = 0
        for ev in events.values():
            ok = [e for e in ev if e["type"] == "System" and e["value"]["type"] == "ExtrinsicSuccess"]
            if ok and any(e["type"] == "Coinage" and e["value"]["type"] == op for e in ev):
                count += 1
                weights.add(round(int(ok[0]["value"]["value"]["dispatch_info"]["weight"]["ref_time"]) / 1e9, 3))
        if count:
            per_block[n] = count
    reasons = collections.defaultdict(set)
    for log in glob.glob(f"{path}/data/Collator-1502*/*.log"):
        for line in open(log, errors="replace"):
            m = re.search(r"Prepared block for proposing at (\d+) \((\d+) ms\) hash: (0x[0-9a-f]+);.*end: (\w+); extrinsics_count: (\d+)", line)
            if m and int(m[1]) in per_block and int(m[5]) == extrinsic_count[int(m[1])]:
                reasons[int(m[1])].add(m[4])
    full = max(per_block.values())
    stop = collections.Counter(("/".join(sorted(reasons[n])) if reasons.get(n) else "unmatched", "full" if c == full else "partial") for n, c in per_block.items())
    entry = {
        "receiptsFile": {"verified": sum(per_receipt_block.values()), "blocks": len(per_receipt_block), "maxPerBlock": max(per_receipt_block.values())},
        "rawBlocks": {"unloadSuccesses": sum(per_block.values()), "blocks": len(per_block), "maxPerBlock": full,
                      "blocksAtMax": sum(1 for c in per_block.values() if c == full), "refTimeMs": sorted(weights)},
        "stopReasons": {f"{r} ({kind} blocks)": k for (r, kind), k in sorted(stop.items())},
    }
    proof_files = glob.glob(f"{path}/{wave}-proofs.jsonl")
    if proof_files:
        proofs = [json.loads(line) for line in open(proof_files[0])]
        entry["proofs"] = {kind: {"count": len(v), "p50": round(nearest_rank(v, 50), 3), "max": round(max(v), 3)}
                           for kind in sorted({p["kind"] for p in proofs})
                           for v in [[p["durationMs"] / 1000 for p in proofs if p["kind"] == kind]]}
    out[name] = entry
    print(name, json.dumps(entry))
json.dump(out, open("unload-blocks.json", "w"), indent=1)
