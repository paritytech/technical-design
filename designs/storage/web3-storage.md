# Scalable Web3 Storage

|                        |                                                                                                                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Start Date**         | 2026-01-16                                                                                                                                                                                   |
| **Description**        | Decentralized storage with game-theoretic guarantees: providers lock stake and face slashing for data loss, while reads and writes stay off-chain and the chain handles setup, checkpoints, and disputes. |
| **Authors**            | eskimor                                                                                                                                                                                      |
| **Canonical location** | [`paritytech/web3-storage` → `docs/design/`](https://github.com/paritytech/web3-storage/tree/dev/docs/design)                                                                                |

## Summary

Storage providers register on a parachain with stake proportional to their
declared capacity. Clients buy storage through on-chain agreements, upload data
to provider nodes over plain HTTP, and periodically checkpoint the providers'
signed MMR commitments on chain. From that point the provider is liable: anyone
authorized may challenge it to produce a stored chunk, and a missing or invalid
response is slashed. The chain is a credible threat rather than the hot path —
normal operation touches it only for setup, checkpoints, and disputes.

## Where the design lives

The design is maintained next to its implementation in
[`paritytech/web3-storage`](https://github.com/paritytech/web3-storage), where
`docs/design/` is the review-gated source of truth (enforced via that repo's
`CODEOWNERS`). It still evolves with the implementation, so per this
repository's rule that unfinished designs stay in their PR — and finished
reference material stays with the code — this file is the `storage` topic's
index entry rather than a copy:

- [Architecture & economics](https://github.com/paritytech/web3-storage/blob/dev/docs/design/scalable-web3-storage.md)
  — the design proper: model, incentives, challenge game, comparisons with
  Filecoin/IPFS/Arweave, and rebuttals to common review concerns.
- [Implementation details](https://github.com/paritytech/web3-storage/blob/dev/docs/design/scalable-web3-storage-implementation.md)
  — pallet extrinsics, provider HTTP API, MMR layout, challenge mechanism,
  replica sync, client protocol semantics.

Changes go through PRs in `web3-storage`, reviewed by the design owners there.
Once individual decisions stabilize (for example the checkpoint/challenge
protocol), they are candidates for promotion into standalone designs in this
folder.
