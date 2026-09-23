# Coinage load paths

This document records the verified implementation paths through which profile-generated Coinage operations place load on the system. It is the source for identifying test artifacts, bounded resources and the Wallet policies that can amplify them.

Only paths confirmed from Android Community, iOS Community, the Coinage runtime and the test harness belong here. Brevity may be recorded as supporting evidence but is not authoritative production behaviour.

## Scope

Trace the business operations represented by the profile schema:

- top-up;
- payment;
- recycling;
- offboarding.

A **component** is an implementation unit, such as a wallet planner, RPC client or runtime pallet. An **artifact** is the specific function, queue, call, collection or bounded resource stimulated and measured by a test. Scenarios target artifacts rather than components in the abstract.

## Component and artifact catalogue

| ID | Layer | Artifact | Responsibility | Authoritative implementation |
| -- | ----- | -------- | -------------- | ---------------------------- |

## Operation paths

Each path must identify its ordered artifacts, the applicable production-policy variants and the runtime calls it reaches.

### Top-up / Onboarding

_To be traced._

### Payment
#### Send

_To be traced._

#### Claim

_To be traced._

### Recycling

_To be traced._

### Offboarding

_To be traced._

## Stress surfaces

A stress surface is a resource that can grow, saturate or reach an implementation or runtime bound along a verified path.

| Artifact | Resource under load | Known bound | Influencing Wallet policies |
| -------- | ------------------- | ----------- | --------------------------- |

## Policy-to-artifact mapping

Concrete adversarial overrides are defined only after this mapping identifies the artifact and resource they are intended to stress.

| Wallet-policy key | Influenced artifacts | Stress objective | Applicable constraints |
| ----------------- | -------------------- | ---------------- | ---------------------- |
