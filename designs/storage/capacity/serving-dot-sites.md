# Serving `.dot` sites from Capacity

|                 |                   |
| --------------- | ----------------- |
| **Start Date**  | 2026-08-31        |
| **Description** | Publish new `.dot` sites to Capacity and let DotNS clients fetch and verify them from Capacity storage providers. |
| **Authors**     | Francisco Aguirre |
| **Relates to**  | [Web3 Storage - Issue #132](https://github.com/paritytech/web3-storage/issues/132) |

## Summary

`.dot` sites are published today as static bundles stored on Levity (Bulletin Chain) and referenced from DotNS by their IPFS CID.
This document proposes publishing new sites to Capacity (Web3 Storage) instead.
Sites keep their current CAR file format and are stored as a single blob.
DotNS gains a new content record that carries the Capacity `bucket_id`, the content's `data_root` and its length.
Clients look up the bucket's storage providers on Asset Hub, download the content over HTTPS, rebuild the Merkle tree from the chunks and check the root against `data_root`.

Capacity does not gain IPFS or bitswap support. The DotNS reference format changes instead.

## Motivation

### Background

Within the Trinity platform, `.dot` sites are deployed to Levity by `bulletin-deploy`,
pointed to by CID from a DotNS record, and rendered by the User Agents: Polkadot App, Polkadot Web (dotli) and Polkadot Desktop, which resolve the name and load the site.

Levity was built for ephemeral storage, originally for Proof-of-Ink video evidence, while sites are generally long-lived.
Its free tier is tied to Personhood and the authorization expires roughly every 14 days.
Even with auto-renewal the publisher has to re-authenticate on that cadence or the site is lost.
Storage is also limited: every collator stores every blob, so the system does not scale, and there is no way to buy more space.

Capacity storage agreements have a duration chosen by the publisher.
The only constraint is the provider's `min_duration` and `max_duration`, which the chain does not cap.
Publishers could reasonably store a site for a year or more.
Payment in Capacity is of the form `payment = price_per_byte * bytes * duration` but the actual price of storing a site for a year will depend on the market.
Storage agreements can be extended by paying more and neither `bucket_id` nor `data_root` changes.
A publisher can therefore pay for a site once and leave it alone until the agreement is about to expire, and the DotNS record never needs updating on extension.

### Goals

- New `.dot` sites are hosted on Capacity: published by `bulletin-deploy` (potentially renamed), referenced by DotNS,
  resolved and verified by the User Agents.
- Existing `.dot` sites hosted on Levity can still be fetched during the transition period.

### Non-goals

- Free `.dot` sites for users with proven Personhood. This is covered by the upcoming Humanity Free Tier design.
- IPFS or bitswap support in Capacity.

## Stakeholders

- DotNS team (dotns and dotns-cli)
- Applied Engineering (Polkadot Web, Polkadot Desktop, `bulletin-deploy`)
- Mobile team (Polkadot App)
- Storage team (Levity and Capacity)

No one listed here has been consulted yet. The Storage team is writing this design and will be its first reviewer.

## Explanation

### Content addressing in the two systems

Levity identifies content by IPFS CID. Small content is a single raw block hashed with blake2b-256.
Larger content is chunked client-side into 1 MiB raw blocks with a UnixFS dag-pb root that ties them together.

Capacity identifies content by `data_root`: blake2b-256 over 256 KiB chunks today, with content-defined chunking planned, committed to a zero-padded binary Merkle tree.

The two identifiers are incompatible in general, and neither says where the data lives.
On Levity that does not matter because every collator has every blob.
On Capacity only the providers with an agreement for the bucket have the data, so the identifier has to carry the `bucket_id`.
That is why the design changes the DotNS record format rather than adding IPFS functionality to Capacity.

### Site format

A site is published as the same CAR file `bulletin-deploy` produces today, stored on Capacity as a single blob with one `data_root`.
This keeps the publishing pipeline and the User Agents' existing CAR decoding unchanged, and is the most compatible choice available now.
The record carries a `format` field so that a Capacity-native filesystem format can be introduced later.
The User Agents do not support such a format today and [might potentially change](https://github.com/paritytech/web3-storage/issues/51), so this document provides the most compatible option with a path forward for better ones.

### The new DotNS record

The DotNS `ContentResolver` gains a new `contenthash` kind.
The value is an EIP-1577 `protoCode` followed by a SCALE-encoded payload:

| Field            | Type           | Meaning                                                  |
| ---------------- | -------------- | -------------------------------------------------------- |
| `version`        | `u8`           | Payload layout version. This document defines version 0. |
| `format`         | `u8`           | Content format. 0 means a CAR file stored as one blob.   |
| `bucket_id`      | `u64`          | Capacity bucket that holds the content.                  |
| `data_root`      | `[u8; 32]`     | Merkle root of the content chunks.                       |
| `content_length` | `Compact<u64>` | Byte length of the content.                              |

The fixed fields take 42 bytes and the compact length 1 to 9, so the payload is 43 to 51 bytes.

`content_length` is required for verification: a zero-padded Merkle tree cannot be rebuilt without knowing how many chunks it has,
and the chunk count also fixes the depth of the tree.
`version` exists so the payload layout can change without a new `protoCode`.

### Client fetch flow

The plan is to deploy Capacity's pallets on Asset Hub, which the User Agents already connect to through a light client.
Resolving a site works as follows:

1. Resolve the name to a record through the DotNS `ContentResolver` on Asset Hub and decode the new record kind.
2. Call the Capacity runtime APIs on Asset Hub with the `bucket_id` from the record:
   `bucket_agreements(bucket_id)` returns the providers that hold the bucket,
   `provider_info(account)` returns each provider's multiaddr,
   and `bucket_info(bucket_id)` returns the bucket's MMR commitment.
3. Pick one of the available providers, any of them if there is more than one, decode its multiaddr into an HTTPS URL and connect to it.
4. Request from the provider the MMR inclusion proof for the leaf identified by `data_root` and verify it against the commitment from step 2.
   This establishes that the provider has checkpointed exactly this content and is liable for it.
5. Derive the chunk count and tree depth from `content_length`, download every chunk, rebuild the Merkle tree and compare its root to `data_root`.
   Per-chunk inclusion proofs are deliberately not used: the client downloads every chunk anyway, so rebuilding the tree costs nothing extra and needs no proof data from the provider.
6. Decode the content according to `format`. Format 0 is a self-contained CAR file and is handed to the existing site loader.

If a provider is unreachable, or any check in steps 4 or 5 fails, the client moves on to the next provider from step 2.

Capacity lets an authorized party challenge a provider to prove it still holds a chunk.
A successful challenge slashes a provider that lost the data, but it does not deliver the content to the client, for that, it's necessary to connect to a replica.
The User Agents may offer the user the option to challenge a provider that failed to serve, but never start one automatically, because a challenge costs the user money.

Capacity providers send permissive CORS headers by default, so Polkadot Web can read their responses from the browser.
A provider that tightens its CORS policy breaks fetches from Polkadot Web while the other User Agents keep working.

### Publishing

`bulletin-deploy` (potentially renamed) gains a Capacity target.
Publishing creates or reuses a bucket, uploads the CAR file, checkpoints the bucket and waits for that checkpoint to be finalized, then writes the DotNS record.
Publishing latency doesn't increase as chain finality is still the bottleneck.

Updating a site uploads the new CAR file to the same bucket and writes a new record with the new `data_root`.
Capacity plans content-defined chunking, so successive versions of a site share most of their chunks and an update costs little extra storage.

### Transition

During the transition period `bulletin-deploy` publishes to both systems and the User Agents keep the CID resolution path.
Existing sites stay on Levity unless their owners republish them.
How long dual publishing lasts and when the Levity path is removed are out of scope for this design.

### Bucket visibility

Sites are published to public buckets. Private buckets, once Capacity supports them, are not relevant here.

## Drawbacks

- Publishing to Capacity costs money, while publishing to Levity stays free and supported. There is no free Capacity path until the Humanity Free Tier lands.
- The User Agents carry two resolution paths during the transition.
- The new `protoCode` is unknown to ENS tooling outside Trinity until it is registered.
- Fetching from Polkadot Web depends on providers keeping permissive CORS headers.
- A site cannot render until the whole CAR file is downloaded and verified. This is unchanged from Levity, but the record format locks it in. A Capacity-native format (`format = 1`) could allow fetching individual files and lift this limitation.

## Testing, Security, and Privacy

### Testing

- End-to-end test that the same CAR file can be published to and retrieved from both Levity and Capacity, and loads identically.
- Unit tests for encoding and decoding the new record.
- Unit tests for rebuilding the Merkle root from downloaded chunks, including content exactly at a chunk boundary, one byte past it, and the zero-padding cases.

### Security

When fetching from Capacity, the client performs two checks: the MMR inclusion proof against the on-chain bucket commitment, and the rebuilt Merkle root against `data_root` from the DotNS record.
A failure in either check is treated the same as an unreachable provider: the client falls back to the next provider, whether primary or replica.
Challenges remain available to the user as described in the fetch flow, but are never issued automatically.

### Privacy

Sites are public by nature, so no new privacy concerns are introduced.

## Performance, Ergonomics, and Compatibility

### Performance

Fetching from Capacity is one HTTPS session to a known provider, instead of bitswap peer discovery.
Before the first byte, the client performs the runtime API calls in step 2 through the light client, which adds some latency.
The whole CAR file is downloaded before the site renders, as it is today.

During the transition, `bulletin-deploy` chunks the same bundle twice: 1 MiB blocks for Levity and 256 KiB chunks for Capacity.

### Ergonomics

`bulletin-deploy` gains a Capacity target and publishers pick the target they want.

### Compatibility

DotNS gains a new record kind. Remaining compatible with ENS tooling outside Trinity would require registering a new EIP-1577 `protoCode`.

Capacity does not change. Fetching from Polkadot Web relies on the providers' default CORS policy.

## Alternatives Considered

### 1. Keep `.dot` site hosting on Levity indefinitely

Rejected for the reasons in Background: renewal and lack of scalability.

### 2. Change Capacity's hashing to match IPFS CIDs

Matching the hash function is not enough.
A CID also fixes the codec and the chunking, so Capacity would have to implement UnixFS dag-pb and change a large part of its design.

### 3. Serve IPFS CIDs over bitswap from Capacity providers

The appeal is that DotNS and the User Agents would not change.
That does not hold: a `data_root` alone does not say which providers hold the data, so the record has to carry the `bucket_id` regardless of transport, and the format changes anyway.
On top of that, Capacity providers only run an HTTP server, so serving bitswap means adding libp2p for this one use case.

## Prior Art and References

- [Levity's design](https://github.com/paritytech/polkadot-bulletin-chain/blob/9f09ea4c9b18ed2e7e8db7ddffbcf0fd6e6e1ff2/docs/book/src/concepts/README.md)
- [Capacity's design](https://github.com/paritytech/web3-storage/blob/192c6223467b965dada2857f75ba8aab34570f92/docs/design/scalable-web3-storage.md)
- [Capacity's implementation details](https://github.com/paritytech/web3-storage/blob/dev/docs/design/scalable-web3-storage-implementation.md): provider HTTP API, MMR layout and challenge mechanism.
- [EIP-1577: contenthash field for ENS](https://eips.ethereum.org/EIPS/eip-1577)
- [DotNS](https://github.com/paritytech/dotns/blob/ac912c7187e07f352347510e7b54e8bbc3f982aa/README.md)

## Unresolved Questions

- Should we register an EIP-1577 `protoCode` for Capacity to remain compliant with ENS tooling?
- What is the exact user experience for offering a challenge after a failed fetch?

## Future Directions and Related Material

- Humanity Free Tier: free `.dot` sites for users with proven Personhood, important for adoption. Covered in a separate document.
- `format = 1` is reserved for a Capacity-native filesystem format.
