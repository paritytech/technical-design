---
created: 2026-09-16
edit: 2026-09-16
Scope: Coinage
---

# Non-Functional Tests

|                 |                                                   |
| --------------- | ------------------------------------------------- |
| **Start Date**  | 2026-09-18                                        |
| **Description** | Performance and stress testing for Coinage        |
| **Authors**     | Agustinus Theodorus, Maxim Skorikov, Andrzej Sułkowski |

This proposal describes how we will measure Coinage performance at planned load and find its limits under stress. It explains the wallet components and transaction paths that generate load, then defines the profiles, policies and runtime conditions needed to build test scenarios; the scenario catalogue and execution setup are still being developed.

## Reading Order

1. **[This overview](#purpose)** — purpose, test types and open decisions.
2. **[Components](components.md)** — responsibilities, dependencies and isolation boundaries.
3. **[Load paths](load-paths.md)** — sequence diagrams from onboarding through payment, recycling and offboarding.
4. **[Profile schema](profile-schema.md)** — inputs that describe each test actor.
5. **[Production policies](production-policies.md)** — how Android and iOS turn those inputs into operations.
6. **[Runtime conditions](runtime-conditions.md) and [constants](constants.md)** — supporting definitions and constraints.

## Purpose

Existing `cargo test`, end-to-end tests and runtime-upgrade tests cover correctness. This document defines the initial approach to non-functional testing: determining which components break under which load, how they fail and whether they recover.

Availability under faults, privacy, modifiability and other quality attributes are deferred.

### Runtime and node failure hypotheses

Coinage executes as a state transition function in a Substrate runtime. Kian Paimani's feedback identifies three areas to investigate alongside the [wallet load paths](load-paths.md). These are hypotheses, not confirmed bottlenecks or an exhaustive list.

- **Weights and block production.** Underestimated weights can admit more work than fits the execution budget; overestimated weights can leave capacity unused. Block authoring also has a wall-clock deadline. Compare declared weight, actual execution time, block utilisation and why authoring stopped. See the [SDK proposer](https://docs.rs/sc-basic-authorship/latest/src/sc_basic_authorship/basic_authorship.rs.html).
- **Parachain validation.** Relay-chain validators re-execute candidates through the parachain validation function (PVF). Record execution times, validation failures and disputes under load. Use the tested network's deadlines for each validation stage; do not assume a universal 500 ms limit or that every timeout causes a dispute. This needs a parachain/relay-chain environment; a standalone runtime test cannot establish it. See [approval checking](https://paritytech.github.io/polkadot-sdk/book/node/approval/approval-voting.html) and [disputes](https://paritytech.github.io/polkadot-sdk/book/node/disputes/dispute-coordinator.html).
- **Transaction-pool saturation and recovery.** Even with accurate weights and successful validation, arrivals can exceed throughput. Check whether a finite burst queues and drains after arrivals fall below capacity. Record queue size, inclusion/finality latency, rejected or dropped transactions and time to drain. If forks occur, inspect revalidation and re-inclusion. A bounded pool cannot absorb sustained overload indefinitely.

Successful buffering is a result to demonstrate, not an assumption. Agree the load target, budgets and responsible teams through the [open questions](#open-questions) before turning these hypotheses into scenarios.

## Test Types

This work uses two test types: **performance tests** and **stress tests**.

|                 | Performance Test                                     | Stress Test                                                               |
| --------------- | ---------------------------------------------------- | ------------------------------------------------------------------------- |
| **Question**    | Does the response measure hold at planned load?      | At what load is it first violated, how, and what happens after?           |
| **Environment** | The tier's normal and peak load from the scale model | Load ramped past peak until the measure is violated or the artifact fails |
| **Pass**        | Measure within budget                                | Failure is graceful and diagnosed, recovery within budget, nothing silent |
| **Done when**   | The run completes                                    | The artifact fails; that is the point                                     |
| **Deliverable** | A number against a budget and a regression gate      | Breaking point, failure mode, recovery and component location             |

> [!warning]
> A stress test that ends without failure is a performance test with a generous budget.

Failure modes, from acceptable to unacceptable, are:

1. **Graceful** — bounded and reported.
2. **Hard** — an error makes the operation terminal.
3. **Silent** — a wrong result or lost data has no signal.

The silent class is what stress testing exists to find.

### Endurance Tests

An endurance test is a performance test over time: one year of planned load compressed into hours, included where it matters. It runs at planned load rather than ramped load and detects state that grows without bound, resources that leak and costs that appear only after the system has accumulated history.

During the run it measures, per profile:

- storage growth, memory, CPU and latency;
- coin count, denomination spread and age distribution;
- forced-recycling and offboarding rates.

After the load settles, it compares idle state and operations with their pre-run values.

## Scenario Form

Every performance or stress scenario has six parts.

| Part                 | Meaning                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------- |
| **Source**           | Who or what produces the stimulus                                                           |
| **Stimulus**         | The event the system must respond to                                                        |
| **Environment**      | The load, runtime configuration and applicable wallet-policy implementation or override    |
| **Artifact**         | The part of the system stimulated                                                           |
| **Response**         | What the system does                                                                        |
| **Response measure** | How the result is evaluated                                                                 |

Performance and stress scenarios for the same artifact share the source, stimulus, artifact and response. They differ in environment—planned load versus a ramp—and response measure—a budget versus a breaking point.

## Scale Model

The scale model defines planned load for performance tests and the starting point of every stress ramp. It combines actor profiles into a population. Population shares, arrival rates, concurrency, topology and simulated-time compression belong here rather than in individual parameter definitions.

### Profiles

A profile describes one actor's demand, preferences and provisioned state. Every profile uses the same 16 parameters, grouped into five areas:

- **Payment demand** — how often the actor pays, when and what values;
- **Inventory and wallet strategy** — when and how much the wallet tops up, and how it constructs payments;
- **Privacy preferences** — preferred recycling, acceptable fees, recycled output and unavailable handling;
- **Exit preferences** — when and how much the actor offboards, and which inventory it uses;
- **Initial inventory** — the coins held at the start of the test.

Each parameter is a profile input, a wallet policy or provisioned state. Definitions and the complete parameter index are in [[profile-schema]].

Payer and merchant are longer-lived business archetypes, not fixed transaction roles. Either can be a sender or recipient. A concrete profile assigns schema values, ranges and relationships without introducing new parameters; concrete payer and merchant work is in [[concrete-profiles]]. Population shares belong to the scale model.

## Behaviour Policies

A behaviour policy is wallet decision logic that translates profile inputs, wallet state, runtime state and named runtime conditions into Coinage operations, or into a decision to perform no operation.

### Policy Resolution

Every parameter classified as a Wallet policy must resolve to exactly one implementation. Production implementations are Android Community and iOS Community. Where they differ, a scenario must select one explicitly; there is no implicit platform default.

Performance and endurance tests use production policies. A stress test also uses production policies unless it explicitly replaces an individual policy with a named adversarial implementation. Invalid or malformed input belongs to robustness or security testing rather than to a wallet-policy override.

### Production Policies

Detailed behaviour, platform differences and commit-pinned evidence are in [[production-policies]].

| Policy key                               | Android versus iOS                                                                  | Scenario must select a variant                                             |
| ---------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `inventory.top_up.composition`           | Same                                                                                | No                                                                         |
| `wallet.payment_construction`            | Differ in split-coin and voucher selection                                          | Yes                                                                        |
| `wallet.recycling.output_composition`    | Differ when a composition exceeds `MaxSplitOutputs`                                 | When recycler output composition is exercised                              |
| `wallet.recycling.unavailable_handling`  | Differ in allowance-read failure, allowance periods and forced-recycling threshold  | Yes                                                                        |
| `wallet.offboarding.inventory_selection` | Same selection; differ above `MaxConsolidation` vouchers from one recycler           | When one recycler contributes more than `MaxConsolidation` vouchers        |

### Named Runtime Conditions

A named runtime condition is a boolean fact derived from profile inputs, wallet state and runtime state. It does not prescribe a response; the resolved wallet policy determines that response. Definitions are in [[runtime-conditions]].

### Adversarial Policy Overrides

An adversarial override is a test-owned implementation that replaces one production policy decision. It creates valid but inefficient behaviour, such as maximising splits, holding excessive inventory or selecting many small inputs.

Each override must state:

- which Wallet-policy key it replaces;
- what pathological behaviour it creates;
- whether it remains protocol-valid;
- which system limit it is intended to exercise.

An override does not affect other policy keys unless it says so. It is scenario configuration, not a separate test type.

## Deriving Scenarios

Derive scenarios by walking one verified operation from its source to completion and listing every artifact through which its load passes. Each artifact receives a performance scenario at planned load and a stress scenario that ramps the relevant environment until its response measure is violated or the artifact fails.

Verified operation paths, their component and artifact catalogue, stress surfaces and policy-to-artifact mapping are maintained in [[load-paths]].

Wallet responsibilities, native source references and dependency replacements for isolated tests are in [components](components.md).

A system-level scenario may ramp the complete path and report which verified artifact breaks first. Coinage paths, artifacts and limits must be established from the current implementations before scenarios are added.

## Utility Tree [TODO]

The utility tree organises scenario candidates under one quality attribute, **Performance**, with two refinements:

- holds at planned load;
- breaking point known.

Its leaves are scenarios rated for business importance and difficulty to achieve as high, medium or low. Coinage-specific leaves are added only after their paths and artifacts have been verified.

## Scenarios [TODO]

A scenario resolves the source profile or population, behaviour policies, test type, scale, artifact, response and response measure using the six-part form above. No scenario is added until its Coinage path and assumptions have been verified.

## Means [TODO]

Execution environments and test levels must be assigned after the scenario artifacts and dependencies are verified.

## Rules Every Test Follows

- Name its scenario and test type.
- Take planned load and the start of any stress ramp from the checked-in scale model.
- Resolve every applicable Wallet-policy key and explicitly select a platform wherever production implementations differ.
- Use seeded generators, fixed inventories and controlled time where applicable.
- Keep budgets and breaking points in version control and fail on regressions beyond an agreed tolerance.
- Measure the failure mode and recovery after stress stops.
- Run chain or RPC stress only against infrastructure we own; public networks receive planned load only.

## Expected Outcomes

- Performance budgets with regression gates.
- Known breaking points, including the first component to violate its response measure.
- Failure modes classified as graceful, hard or silent.
- Recovery measurements after stress stops.

## Later

Availability under faults, recoverability, privacy, energy use and modifiability are deferred and can be added later using the same scenario form.

Kian also suggested a separate exercise for chat with image uploads, covering SSS and BC. That needs its own owners and load paths; their relative fragility is not an established finding of this Coinage work.

## Open Questions

- Which population and workload are we targeting: 10k users, 1M users, or another tier? Specify active users, operation mix, arrival rates and burst concurrency; a user count alone does not define load.
- Which throughput, latency and post-burst recovery budgets should we agree with the runtime, transaction-pool and parachain-validation leads?
- Which owned test environment and instrumentation can exercise block production and relay-chain validation together, and who owns the resulting findings?
