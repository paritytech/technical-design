# Technical design docs

Every technical design for the Polkadot Products Platform lives here, in one place.

This holds designs that have settled. A doc lands here once it has stopped moving - if it's still changing week to week, keep it in the PR. Corrections and superseding are fine, but a doc that needs constant editing is tracking work rather than recording a design, and belongs somewhere else.

One folder per topic - the thing you'd name if someone asked what you're working on. Topic names outlast the teams that own them, and the designs that matter usually cut across the stack, so filing by topic keeps everything about one thing in one place.

## Where things go

```
designs/
├── jam/            JAM
├── storage/        Everything storage related, e.g. Web3 storage, Bulletin etc.
└── etc..
```

That's what exists today, not a fixed taxonomy. Add a folder when your design doesn't fit one.

A design is one file when one file is enough. When it needs diagrams, sub-documents or worked examples, give it its own folder inside the topic. The `README.md` there is the design, carrying the header table and the sections below, and the supporting files sit beside it.

```
designs/storage/
├── bulletin-data-renewal.md      one file is enough
└── web3-storage/                 needs more
    ├── README.md                 the design
    ├── encoding.md
    └── lifecycle.svg
```

A design that spans topics goes in the one it changes most and names the others in the doc.

A topic can also have a `README.md` of its own, listing what's in the folder - keep live state out of it.

## What a design looks like

Copy [`TEMPLATE.md`](TEMPLATE.md) to `designs/<topic>/<name>.md`, or to `README.md` inside the design's own folder, and fill it in.

It's the same shape as a Fellowship RFC, so a design can be promoted to one without a rewrite. Keep the headings even when a section has nothing in it and say so, rather than deleting it.

Unresolved Questions carries the most weight here. Merging reads as settled, so if the design rests on numbers nobody has checked, name them.

When a later design replaces this one, add a **Superseded by** row to the header table pointing at it. That's the only edit an old doc should normally need.

## Review

Open a PR. Iterate there as long as you need, that's what the PR is for. An approval and a merge is the whole process.

Merging means it's settled, so don't merge something you expect to rewrite next week.

## Publishing elsewhere

A design often gets published somewhere else as well: a Fellowship RFC when the ecosystem has to accept it, a spec in the repo of the codebase it describes like chat-spec, reference docs that ship with the code. That's publication, not a second home. The design still lands here and links out to wherever it went.

Because the structure matches, promoting a design to a Fellowship RFC is a copy into that repo's `text/` folder plus a PR, not a rewrite. The Fellowship numbers an RFC after its PR, so designs here stay unnumbered.

Two things aren't designs and don't belong here at all. Reference documentation describing the code as it currently stands belongs next to the code, so it moves with it. Plans and progress belong in issues and PRs.
