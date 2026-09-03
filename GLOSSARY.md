# Glossary

Short, strict definitions of terms used in the technical docs: common
terminology across projects. A new definition must not introduce ambiguity
into the glossary: conflicting terminology must be resolved. An entry links
at most one external reference — the most authoritative source to research
further. Definitions should include the exact names a term goes by in other
places — code identifiers, crate or method names.

Entries are alphabetical.

---

**Levity** (a.k.a Bulletin) — The Polkadot Bulletin chain
([polkadot-bulletin-chain](https://github.com/paritytech/polkadot-bulletin-chain)):
a *system chain* that provides storage. Calls are feeless; instead they are
gated by an authorization model —
an account is authorized in advance to upload, and authorizations expire.
Data is uploaded by submitting extrinsics; the uploaded data itself is kept
in off-chain storage, not in the runtime state, and has a retention period.

**Fellowship runtimes** — The production runtimes of Polkadot and Kusama, maintained by the Polkadot Technical Fellowship in
[polkadot-fellows/runtimes](https://github.com/polkadot-fellows/runtimes) and
enacted via on-chain referenda. The runtimes developed there are based on a
specific *SDK release* and released on their own cycle.

**HOP** — Hand-Off Protocol: a JSON-RPC protocol (`sc-hop`) exposed by
*Bulletin* collators. Bulletin-authorized accounts submit data that resides
on that one collator node only, addressed to one or more recipients (one-time
public keys) who claim it. Data not claimed within a configurable retention
period is promoted best-effort: submitted to *Bulletin* as an extrinsic.

**Node** — The binary running a chain: networking, database, consensus, RPC.
Runtime state is opaque data to it; a chain spec defines what it runs —
genesis state, including the runtime, chain id and bootnodes. It exposes
JSON-RPC on one port for external clients and the P2P protocols on another
for other nodes. It can run in different modes — collator/validator, bootnode,
or a regular RPC node; whether it prunes block history and runtime state, or
keeps all of it (archive node), is an orthogonal choice.

**Pallet** — A FRAME module implementing one domain of runtime logic — its
storage, calls, events and errors. A runtime is composed of pallets
(`pallet-balances`, `pallet-staking`, …).

**Runtime API** — A versioned interface (`sp-api`) the Wasm runtime exposes
to the node, invoked on a specific block's state (block building, transaction
validation, metadata, …). Not the node's JSON-RPC: RPC is served by the node
to external clients, a runtime API is called by the node into the runtime.

**SDK release** — A versioned release (`stableYYMM`) of
[polkadot-sdk](https://github.com/paritytech/polkadot-sdk), the crate set that
node and runtime implementations build against. Ships on a regular cadence,
independent of *Fellowship runtimes* releases.

**System chain** — A parachain that is part of the network's protocol itself.
Runs on behalf of the network; its runtime lives in the *Fellowship
runtimes*. Uses a para ID below 2000 — the range that is not publicly
registrable (`LOWEST_PUBLIC_ID` in polkadot-sdk).
