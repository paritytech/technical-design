# Parity internal tech-design repo

**For:** engineering across Node, Runtime, Platform, Product Prototypes.  
**Purpose:** one place where all teams contribute technical designs for the Polkadot Products Platform.  
**Organisated by area,** mirroring the Polkadot Products Platform's own layered architecture. Developer surface, access layer, capability suite, infrastructure services, operator layer are generic layers that outlive project names, team names or internal org.

## Structure

```
tech-designs/
├── README.md                      what this repo is, what goes elsewhere
├── CONTRIBUTING.md                how to add a design, how review works
├── TEMPLATE.md                    required template
├── INDEX.md                       all designs, status, owner, area
│
├── decisions/                     cross-team decisions
│   └── 2026-08-18-products-test-platform.md
│
└── designs/
    ├── 00-platform/               whole-platform, cross-layer
    ├── 10-developer-surface/      SDK, playground, docs, AI dev tooling
    ├── 20-access/                 TrUAPI, triangle hosts, light client
    ├── 30-capabilities/           the capability suite
    │   ├── humanity/              personhood, DIMs
    │   ├── privity/               aliases, unlinkability
    │   ├── celerity/              statement store, messaging
    │   ├── levity/                Bulletin, ephemeral storage, HOP
    │   ├── capacity/              durable Web3 storage
    │   ├── fungibility/           coinage, payments, dotUSD
    │   └── ...
    ├── 40-infrastructure/         consensus, collation, networking, storage nodes,
    │                              light-client serving, JAM compute
    ├── 50-operators/              metanode, QoS, rewards, deployment, autoupdate
    └── 90-cross-cutting/          security, privacy, economics, testing, observability
```

**Number prefixes** keep the folders in stack order, so a new joiner can read 10 → 50 top-down and understand the platform.

**Two levels maximum under `designs/`.**

### Programmes: hub and spoke

Some work is not one design in one layer. A programme like Metanode touches access, capabilities, infrastructure, operators and economics at once.

Do **not** put a whole programme in one layer folder, also do **not** scatter it with no hub.

**Hub and spoke:**

- The **programme doc is the hub**, in `00-platform/<programme>/`.
- **Component designs live in their true layers.**
- The hub links them. `affected:` makes them findable from both directions.

```
designs/00-platform/metanode/PPP-0001-metanode-programme.md   hub
designs/00-platform/metanode/STATUS.md                        live state
designs/20-access/PPP-0005-user-agent-metering-and-hopping.md spoke
designs/30-capabilities/fungibility/PPP-0004-allowances.md    spoke
designs/40-infrastructure/PPP-0003-sizing-and-capacity.md     spoke
designs/50-operators/PPP-0002-node-architecture.md            spoke
```

## Rules

### 1. Status is mandatory metadata

One needs to **find** the doc but also know its **status.**

Every design starts with required frontmatter:

```yaml
---
id: PPP-0042
title: Bulletin data renewal
type: design | programme | decision
area: 30-capabilities/levity
status: draft | in-review | accepted | implemented | superseded | abandoned
owner: <name>
affected: [levity, access, capabilities/humanity]   # discovery and filtering
sign-off: [levity, access]                          # who must approve, a subset
blocked-on: [PPP-0038, measurement:lc-serving-capacity]   # optional
supersedes: PPP-0031
last-reviewed: 2026-08-20
review-cadence: 6 months                            # shorten for volatile areas
---
```

- **Status lives in the file, not in the folder path.** Moving files to reflect status breaks every link and every PR reference.
- **`INDEX.md` is the single view** of what exists, its status and its owner. Generate it if you can, maintain it by hand if you cannot.
- **`last-reviewed` is the anti-rot field.** Anything untouched for 6 months gets swept and either re-confirmed or marked superseded.
- **Stable IDs (`PPP-0042`)** give people something to cite in PRs and chat that survives a title change.
- **`review-cadence` defaults to 6 months, and the owner can shorten it.** Six months is too slow for volatile areas. Metanode's direction changed materially twice in three months; a six-month sweep would have let a stale design sit for half a year.

### 1a. `type` is mandatory too

- **`design`** - how one thing works or should work. Lives in a layer folder. Uses the design template.
- **`programme`** - cross-layer work with phases, gates and its own ownership map. Lives in `00-platform/`. Uses the programme template.
- **`decision`** - a choice, its alternatives, and why. Lives in `decisions/`. Short, dated, never revised.

### 1b. `blocked-on` and unproven inputs

`accepted` reads as settled. A design can be `accepted` while resting entirely on numbers nobody has measured.

- Use **`blocked-on:`** for a hard dependency, whether another design or a pending measurement.
- **`INDEX.md` must surface `blocked-on` and a flag for a non-empty `Unproven assumptions` section.**

### 2. Quickly filter cross-team/cross-stack/cross-functional topics/designs

**`affected:`** - the list of areas and teams a design touches. Use keywords e.g. `affected: [economics]`. For **discovery and filtering**.

**`sign-off:`** - the subset of those areas that must actually approve. For **review**.

**Both mandatory. Reviewers should check both.**

**Why two fields.** "One reviewer per affected area" does not scale with breadth. A cross-layer programme is affected across most of the stack, so that rule turns into a six-person veto pool. Keep `affected` wide so people can find the work. Keep `sign-off` narrow so the work can move.

### 3. Designs and decisions are different documents

- A **design** says how something works or should work. It is long-lived and gets revised.
- A **decision** captures a choice, the alternatives, and why. It is short, dated, and never revised, you supersede it instead.

Keeping them apart stops design docs from becoming archaeology. It also gives leads a single place to read "what did we actually commit to" without reading twenty designs.

- *Design-internal decisions* go in a `Decision log` section **inside** the design or programme doc. One row each: decision, one-line reasoning, date.
- **`decisions/` is reserved for cross-team commitments** - things another team has to plan around.

**Rule of thumb:** if only your own doc changes as a result, log it in the doc. If someone else has to change their plan, it is a `decisions/` file.

## Template formats

### Design template

Minimum sections:

1. **Problem** - what's not working today, for whom
2. **Non-goals** - what this deliberately does not do
3. **Design** - the actual proposal
4. **Alternatives considered** - and why not
5. **Dependencies and affected areas** - who/what else must change
6. **Open questions** - with owners
7. **Unproven assumptions** - anything load-bearing and unmeasured
8. **Decision log** - design-internal calls, dated, with one-line reasoning

### Programme template

Minimum sections:

1. **Problem** - what's not working today, for whom
2. **Non-goals** - what this deliberately does not do
3. **End state** - what it looks like when done, and what we get
4. **Why phased** - why this cannot ship as one change
5. **Phases** - each with deliverables and **a named, measurable gate**
6. **Component designs** - the spokes, with IDs and status
7. **Ownership** - per area, with **unowned areas named explicitly**
8. **Risks** - accepted risks we are carrying, distinct from assumptions
9. **Open questions** - with owners
10. **Unproven assumptions** - anything load-bearing and unmeasured
11. **Decision log** - or a link to the programme's `STATUS.md`

Gates are what make a programme reviewable.

Name the owned *and* the unowned areas.

### Programmes get a `STATUS.md`

`INDEX.md` says what exists. It does not say what changed this week, what is decided, or what is owed. For a programme that is the most-read artifact.

`00-platform/<programme>/STATUS.md`: current phase, decisions owed with owners, decision log, recent changes. Revised constantly - unlike the programme doc, which should stay stable.

## Review - keep it light or it dies

- **One named owner per top-level area.** Not a team, a person. They keep their area's index honest.
- **To move `draft` → `accepted`:** owner approval, plus one reviewer from each area listed in **`sign-off`**.
- **Anyone can open a draft.** No gate on contributing.
- **No review SLA, but a visible queue.** Our review capacity is already the known bottleneck across the org; pretending otherwise won't help anyone.

## What goes here, and what does not

**This is the part most likely to fail.** We already have several places designs live. Without a clear boundary this becomes a fifth place nobody reads.

| Venue | What belongs there |
|---|---|
| **This repo** | Internal designs for the Polkadot Products Platform, and cross-team decisions |
| **Fellowship RFCs** | Public protocol changes needing ecosystem or governance buy-in |
| **Rust docs in polkadot-sdk** | API and component reference docs that ship with the code |
| **Component repos** (e.g. chat-spec) | Specs tightly coupled to one codebase |
| **Google Docs** | Drafting and live collaboration - but the accepted version lands here |

**Suggested rule:** *if two teams need to agree on it, it belongs here. If one team owns it and it ships with the code, it belongs next to the code. If the ecosystem must accept it, it becomes an RFC.*

## How this tech-design source-of-truth dies (and how to prevent it)

- **It becomes a graveyard.** Mitigation: `last-reviewed` plus a scheduled sweep, and named area owners.
- **Nobody uses it because Google Docs is easier to write in.** Mitigation: allow drafting anywhere, require the accepted version to land here.
- **Review becomes the bottleneck.** Already our known constraint. Keep the _formal mandatory_ bar at one reviewer per affected area, no more.
- **The structure fights reality.** If designs keep landing awkwardly in one folder, the structure is wrong; change it at the 3-month sweep.
