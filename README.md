# Technical design docs

This is where we keep the technical design docs for the Polkadot Products Platform.

Only finished designs go in here. If one is still changing every week, keep it in the PR. You can fix a design later or replace it with a new one.

One folder per topic, named after the topic. Even designs that affect several parts of the stack go under one topic.

```
designs/
├── jam/            JAM
├── storage/        Everything storage related, e.g. Web3 storage, Bulletin etc.
└── etc..
```

These are the current topics. If your design doesn't fit, add a folder.

Keep a design in one file when one file is enough. With diagrams, extra files, or examples, give it a folder inside the topic. The `README.md` in that folder is then the design, with the header table and the template sections; the other files go in the same folder.

```
designs/storage/
├── bulletin-data-renewal.md      one file is enough
└── web3-storage/                 needs more
    ├── README.md                 the design
    ├── encoding.md
    └── lifecycle.svg
```

If a design covers several topics, put it under the topic it changes most and mention the rest in the document. A topic can also have its own `README.md` that lists the folder contents; just don't put status updates in it.

## What a design looks like

Copy [`TEMPLATE.md`](TEMPLATE.md) to `designs/<topic>/<name>.md`, or to `README.md` inside the design's own folder, and fill it in.

The template follows the Fellowship RFC structure, so you don't have to rewrite a design to make it an RFC. Keep every heading even when a section stays empty, and mark it as empty instead of removing it.

Unresolved Questions is the most important section, because a design is final once merged. Anything you're still unsure about — unverified numbers, for example — has to go in that section.

When a new design replaces an old one, add a **Superseded by** row to the header table pointing at the new design. That's usually all the old document needs afterwards.

## Review

Open a PR, keep updating the design until it's ready, get it approved, and merge it. Once merged, a design is final, so don't merge something you expect to rewrite next week.

## Publishing elsewhere

A design may also be published elsewhere — as a Fellowship RFC, as a spec in the code's own repo, or as reference docs. The design stays here and links out to them.

To publish a design as a Fellowship RFC, copy it into that repo's `text/` folder and open a PR. The RFC is numbered after the PR, so the designs here don't have an RFC number.

Two kinds of files don't go in this repo. Reference docs describe the code as it is now, so they go in the code's own repository; plans and progress reports go in issues and PRs.
