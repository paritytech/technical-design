# Technical design docs

This is where we keep the technical design docs for the Polkadot Products Platform.

Only finished designs go in here. While a design still changes every week, keep it in its PR. Once merged, it can still be corrected later or replaced by a new design.

Designs are grouped into topics, one folder per topic. A design that touches several parts of the stack still lives under a single topic.

```
designs/
├── jam/        JAM
├── storage/    Everything storage related: Capacity, Bulletin, and so on
└── ...
```

If your design doesn't fit any of the existing topics, add a folder for it.

Keep a design in a single file when that is enough. If it needs diagrams or other extra files, give it a folder inside the topic. The `README.md` in that folder is then the design itself, and everything it references sits next to it.

```
designs/storage/
├── bulletin-data-renewal.md    a single file is enough
└── capacity/                   needs more
    ├── README.md               the design
    ├── encoding.md
    └── lifecycle.svg
```

If a design covers several topics, put it under the one it changes most and mention the others in the document. A topic may also have its own `README.md` listing what the folder contains, but keep status updates out of it.

## What a design looks like

Copy [`TEMPLATE.md`](TEMPLATE.md) to `designs/<topic>/<name>.md`, or to `README.md` inside the design's own folder, and fill it in.

The template follows the Fellowship RFC structure. It is a proposed structure, not a strict requirement: drop the headings you don't need, and reorder or add others where that suits the design better.

A design is final once merged, so record what you are still unsure about, unverified numbers, for example, under Unresolved Questions rather than leaving it out.

When a new design replaces an old one, add a **Superseded by** row to the old design's header table pointing at the new one. That is usually all the old document needs.

## Review

Open a PR, keep updating the design until it is ready, get it approved, and merge it. Merging makes a design final, so don't merge one you expect to rewrite next week.

## Publishing elsewhere

A design can also be published elsewhere, for example as a Fellowship RFC. The design stays here and links out to wherever it was published.

Two kinds of documents don't belong in this repository. Reference docs describe the code as it is today and belong in the code's own repository; plans and progress reports belong in issues and PRs.
