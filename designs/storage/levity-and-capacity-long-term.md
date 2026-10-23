# Levity and Capacity long-term

|                 |                   |
| --------------- | ----------------- |
| **Start Date**  | 2026-10-21        |
| **Description** | Long-term plan for both Levity and Capacity: Levity serves users through allowances, Capacity serves developers who pay, and both stay |
| **Authors**     | Francisco Aguirre |
| **Relates to**  | [Storage umbrella design issue](https://github.com/paritytech/technical-design/issues/13), [Personhood Free Tier](./capacity/personhood-free-tier.md), [TrUAPI Host Functions](./capacity/truapi-host-functions.md), [Serving `.dot` sites from Capacity](./capacity/serving-dot-sites.md) |

## Summary

**Keep both Levity and Capacity long-term until usage data suggests otherwise. Levity is the free store for users, most of whom will only ever need an allowance. Capacity is the paid store for developers and power users who want more. Capacity is proposed as pallets on Bulletin Chain, priced in dotUSD, and gets no free tier until usage shows one is needed. The only thing that migrates is `.dot` sites. How a user upgrades beyond an allowance is left open.**

Everything this design says about Bulletin Chain, Asset Hub or the treasury is a proposal.

The Polkadot Products Platform has two storage systems.
Levity (Bulletin Chain) is a free, personhood-gated, on-chain store with a 14-day retention window and renewals on top.
Capacity (Web3 Storage) is a paid, mostly off-chain, challenge-based store with stake-backed guarantees and agreements of any duration.
Each gets an audience:

- **Users** mostly store little, within an allowance. Levity serves them: free, personhood-gated, persistent through auto-renew that the App keeps alive by making the next People Chain claim each time it opens. A person who does not open the App for about two weeks makes no claim and risks losing that data, which is accepted for now.
- **Developers and power users** store far more and pay for it. Capacity serves them: paid agreements, reached through extrinsics and SDKs first and through paid host functions once integrated into Trinity.

Capacity could take over users' persistent storage too if it had a free tier, leaving Levity only as ephemeral storage.
The [Personhood Free Tier](./capacity/personhood-free-tier.md) design holds initial ideas for it.
Since the addition is so complex, it's advised to keep Levity renewals for now.

The order of releases: Levity's auto-renew host functions come first, Capacity opens to providers before it integrates with the platform, and sites move last.

## Motivation

Levity was built for ephemeral storage and cannot scale.
Renewals were added because Products needed persistence and nothing else offered it.
They added considerable complexity to the chain and still have rough UX limits.

Capacity is the long-term solution for large persistent data.
It scales with the number of providers and agreements have whatever duration the owner buys.
But it has no concept of a free tier, and giving it one increases the complexity considerably.

Most users store a little, so splitting the audiences lets each system do what it was built for and defers the free tier machinery until real usage says it is worth building.

### Goals

- Users get free persistent storage on Levity.
- Developers and power users get storage that scales on Capacity, and pay for it.
- Capacity ships and integrates without the free tier.
- Nothing users store today has to move.

### Non-goals

- Designing Capacity's paid host functions or the DotNS record. These sub-designs are linked.
- Designing the move of Capacity to smart contracts. See [Future Directions](#future-directions-and-related-material).

## Stakeholders

- Storage team (Levity, Capacity)
- TrUAPI team
- Mobile team (Polkadot App)
- Platform team (Polkadot Web, Polkadot Desktop)
- Owners of DotNS and the `bulletin-deploy` tool

## Explanation

### Terminology

- **Levity**: the storage service running on Bulletin Chain, including its renewal features (see the [data renewal design](https://github.com/paritytech/polkadot-bulletin-chain/blob/main/docs/data-renewal.md)).
- **Capacity**: the storage service implemented in `paritytech/web3-storage`.
- **User Agent**: the Polkadot App, Polkadot Web or Polkadot Desktop.
- **App**: the Polkadot App, which RFC-0010 calls the Account Holder.
- **User**: a person with personhood or devicehood using Products through a User Agent.
- **Developer**: someone who builds Products or deploys `.dot` sites.
- **Power user**: a user who needs more than an allowance and pays for it.
- **Allowance**: the bytes and transactions an account holds on Levity for a window, the sum of the claims assigned to it.
- **Allowance account**: the per-Product account that holds the allowance on Levity and owns the Product's bucket on Capacity. Products never see its key. Defined in [RFC-0010](https://github.com/paritytech/truapi/blob/main/docs/rfcs/0010-allowance.md).
- **Temporary store**: the TrUAPI `preimage_submit` host function from RFC-0010. It stores on Levity and returns the content hash.
- **Window**: a 14-day People Chain period.
- **Claim**: one unit of allowance a person obtains from People Chain in a window and assigns to an account. A person has a fixed number per window and can assign several to one account.
- **Forward claim**: a claim in the next window, made while the current window is still active.
- **Authorization slot**: a position on an account's Levity authorization that holds one window's allowance. An account has a few, so it can hold the current window and a forward-claimed one at once. Not the same thing as a claim.

### Users on Levity, developers on Capacity

| | Users (Levity) | Developers (Capacity) |
| --- | --- | --- |
| How much | A few megabytes per Product | Gigabytes and up |
| Pays | Nobody; the treasury funds Levity collators | The developer or power user, per agreement |
| Access | A People Chain claim per window | Stake-backed provider agreements |
| Through | Temporary store plus auto-renew host functions | Extrinsics and SDKs, later the paid TrUAPI functions |
| Persistence | Auto-renew, kept alive by forward claims | Agreement duration, extended by paying more |
| Holds | Product user data | `.dot` sites and anything a Product team stores beyond allowances |

### The App keeps renewals alive by forward claiming

Opening the App is what claims: each time it opens, it makes a forward claim for each Product ([how claims work today](./capacity/personhood-free-tier.md#how-claims-work-today-people-chain-to-levity)), so the authorization never lapses as long as the App is opened at least once per window.
Auto-renew lapses when the allowance account's authorization lapses, so renewals depend on those claims.
RFC-0010 assigns the claims to the Account Holder, which is the App, so Web and Desktop rely on the App having claimed: a person who only uses Web or Desktop has no persistent storage.

The trade-off is a person who does not open the App for about two weeks risks data loss.
No forward claim is made, so once the windows already claimed run out the authorization lapses, auto-renew lands without an active authorization and the data is lost.
That is a reasonable trade-off for now since most users won't land in this scenario.
The experience for this kind of user can be improved later. See [Future Directions](#future-directions-and-related-material).

For Products to use this, the TrUAPI gains enable and disable auto-renew host functions, which need their own sub-design.
Products register the data they want kept.
This assumes the renewal pallet is live on Bulletin Chain, and it needs the authorization slots code merged on both sides, [People Chain](https://github.com/paritytech/individuality/pull/931) and [Bulletin Chain](https://github.com/paritytech/polkadot-bulletin-chain/pull/509), since forward claiming depends on it.

### Capacity is proposed as pallets on Bulletin Chain

Adding Capacity's pallets to the Bulletin Chain runtime is a governance decision; this design is the proposal.
Pallets are the only form that fits the work already done and the security audit that is already underway, and the pallets are audited before they are added to the runtime.
Running them on Bulletin Chain keeps Capacity's runtime code out of Asset Hub, so a vulnerability in it cannot affect other parts of the system.
The costs are under [Drawbacks](#drawbacks).

Capacity opens to providers before it integrates with the platform: early users are developers driving the pallets through regular extrinsics and the existing SDKs, and that is where provider prices are first observed.

Long-term the goal is to reduce the attack surface by moving Capacity out of pallets.
That move is follow-up work that deserves its own design. See [Future Directions](#future-directions-and-related-material).

### Providers are paid in dotUSD

Capacity agreements are priced and paid in dotUSD instead of DOT.
The proposal adds `pallet-assets` to Bulletin Chain so that dotUSD can reach it from Asset Hub over XCM and every Capacity transaction on Bulletin Chain can pay its fees in dotUSD, so nobody needs PGAS, the fee asset people claim with personhood.
A purchase through the TrUAPI pays in RFC-0006's payment asset, which is dotUSD, so nothing is converted and nobody carries rate risk.

### Products reach Capacity through the paid host functions

Once providers are live, the paid half of the [host functions design](./capacity/truapi-host-functions.md#the-paid-flow) and the [new DotNS record](./capacity/serving-dot-sites.md) ship, and Products can create a bucket and pay for a storage agreement through the TrUAPI.
The sponsored half and the free tier are deferred; see [What happens to each sub-design](#what-happens-to-each-sub-design).

### Only sites move

`.dot` sites move from Levity, referenced by CID from DotNS, to Capacity, referenced by the [new DotNS record](./capacity/serving-dot-sites.md).
Everything else on Levity is unchanged.

The move follows the [publishing](./capacity/serving-dot-sites.md#publishing) section of the dot-sites design, with one change to its [transition](./capacity/serving-dot-sites.md#transition): there is no dual-publishing period.
The deploy tool gains a way to pay for a site's agreement in dotUSD directly, without going through a User Agent, and drops its Levity target in the same release.
Owners re-publish the sites to the new target.
DotNS keeps resolving both record types; a site that is never re-published expires with its last renewal and its CID record dangles.

### What happens to each sub-design

All of the following are updated for the proposed Capacity on Bulletin Chain and agreements in dotUSD:

- [Serving `.dot` sites from Capacity](./capacity/serving-dot-sites.md) proceeds, with the deploy tool's direct payment path and no dual-publishing period.
- [TrUAPI Host Functions](./capacity/truapi-host-functions.md) proceeds with its paid half, whose payment path now ends on Bulletin Chain rather than Asset Hub; the sponsored half is deferred with the free tier.
- [Personhood Free Tier](./capacity/personhood-free-tier.md) stays unmerged as initial ideas until usage shows a free tier is needed.
- The canonical [Capacity design](https://github.com/paritytech/web3-storage/blob/dev/docs/design/scalable-web3-storage.md) is updated in its own repository.
- Two sub-designs are still to be written: the auto-renew host functions, and the move of Capacity to smart contracts.

### Upgrading beyond an allowance (open)

The split leaves one path undefined: a Product whose user needs more than an allowance.
The pieces that exist today are RFC-0010's extra claims on Levity and the paid [Capacity host functions](./capacity/truapi-host-functions.md).
Levity identifies bytes by their content hash and Capacity by a Merkle root over their chunks (see [content addressing in the two systems](./capacity/serving-dot-sites.md#content-addressing-in-the-two-systems)), and the options below differ in who carries that difference.
This design does not pick one; the Storage team reviews the options internally.

#### Option A: two namespaces, the Product decides

Keep the [two namespaces of the host functions design](./capacity/truapi-host-functions.md#1-route-submit_preimage-to-capacity) as they are: temporary store plus auto-renew for free data, the Capacity namespace for paid data, chosen per piece of data by the Product.
Moving data from one to the other is the Product's own work, using the hashes it kept.

- Pros: no new User Agent work; matches the host functions design as written; each API is simple on its own.
- Cons: a Product that wants to grow must be written against both APIs from the start; a free user hits Capacity's quota-exhausted error until they buy, so the first paid byte is a cliff; nothing surfaces to the user that Levity can no longer keep their data.

#### Option B: one namespace, the User Agent places and migrates

A single persistent namespace keyed by the hash of the full bytes.
The User Agent stores to Levity while the allowance has room and to Capacity once the user has purchased, keeps a per-Product map from key to backend, and moves a blob from Levity to Capacity when a renewal would fail.
`purchase` is the only user-facing step.

- Pros: one API and one identifier for Products; the cliff becomes a prompt; data drifts to Capacity only when Levity cannot keep it.
- Cons: the User Agent gains a storage index, a placement policy, a background migration worker and the problem of keeping that index durable across reinstalls.

#### Option C: one namespace, no migration

The same single namespace, but `store` returns which backend holds the bytes, and `read` takes that locator back.
The User Agent routes each store to Levity or Capacity by quota and keeps no index.
Nothing ever moves.

- Pros: one API for Products and no User Agent bookkeeping; the cliff becomes a prompt for new data.
- Cons: the Product still holds two kinds of identifier, just wrapped; data already on Levity stays bounded by the allowance and expires if the allowance cannot renew it.

## Drawbacks

- Users' persistent data is bounded by Levity's allowance and renewal caps, per person and chain-wide.
- A person who does not open the App for about two weeks makes no forward claim and risks losing auto-renewed data, and a person who only uses Web or Desktop has no persistent storage. See [The App keeps renewals alive by forward claiming](#the-app-keeps-renewals-alive-by-forward-claiming).
- Bulletin Chain would gain assets when it was built without them. Capacity's checkpoints and challenge responses also compete with Levity's blobs for blockspace.
- Moving Capacity to smart contracts later means moving funds under hold and state across chains.
- Old `.dot` CID records become dangling pointers once their Levity data is no longer renewed.

## Testing, Security, and Privacy

- Capacity's pallets are audited before they are added to the Bulletin Chain runtime. See [Capacity is proposed as pallets on Bulletin Chain](#capacity-is-proposed-as-pallets-on-bulletin-chain).
- Payment consent for Capacity purchases is specified in the [host functions design](./capacity/truapi-host-functions.md#security).

## Performance, Ergonomics, and Compatibility

- Users see no change beyond their data persisting; the auto-renew functions are additions.
- Developers get a store that scales, at the cost of holding dotUSD and managing agreements.
- Nothing is removed from Levity, see [Only sites move](#only-sites-move).

## Prior Art and References

- [Bulletin Chain](https://github.com/paritytech/polkadot-bulletin-chain).
- [Web3 Storage design](https://github.com/paritytech/web3-storage/blob/dev/docs/design/scalable-web3-storage.md) and [implementation details](https://github.com/paritytech/web3-storage/blob/dev/docs/design/scalable-web3-storage-implementation.md).
- [TrUAPI RFC-0010: Allowance](https://github.com/paritytech/truapi/blob/main/docs/rfcs/0010-allowance.md).
- [Bulletin data renewal design](https://github.com/paritytech/polkadot-bulletin-chain/blob/main/docs/data-renewal.md).
- [`bulletin-deploy`](https://github.com/paritytech/bulletin-deploy).

## Future Directions and Related Material

- **Sponsored storage.** A Product or organization funding storage for its users or clients; the free tier design already [supports a sponsor other than the pot](./capacity/personhood-free-tier.md#future-directions-and-related-material), what is missing is the platform path.
- **Moving Capacity to smart contracts.** Whether it becomes smart contracts on Asset Hub or a hybrid of a light pallet and heavier contracts.
- A better experience for people who do not open the App for weeks, for example a longer People Chain period or claiming more than one window ahead.
- An IPFS-compatible read path for Capacity, a [rejected alternative](./capacity/serving-dot-sites.md#3-serve-ipfs-cids-over-bitswap-from-capacity-providers) in the dot-sites design, if it were ever revisited.
- JAM DA may supersede Levity as the ephemeral store. That is expected but not certain, and would be its own design.
