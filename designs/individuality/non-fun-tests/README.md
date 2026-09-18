# Non-Functional Tests

|                 |                   |
| --------------- | ----------------- |
| **Start Date**  | 2026-09-18        |
| **Description** | _To be filled._   |
| **Authors**     | Andrzej Sulkowski |

## Summary

_To be filled._

## Motivation

_To be filled._

## Stakeholders

_To be filled._

## Explanation

### Prelude

We have tests which run via `cargo test`, some e2e tests and runtime upgrade tests. All of them cover correctness. With this PRD we do the initial step towards coverage of non-functional tests. We want to map out which components break under which load? What kind of breakage do we see? Is it graceful, hard or silent? 

Other quality attributes like availability under faults, privacy or modifiability are deferred


### Test Types

We will be focusing on two test types: _Performance Tests_ and _Stress Tests_.

|                 | Performance Test                                     | Stress Test                                                                                  |
| --------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Question**    | Does the response measure hold at planned load?      | At what load is it first violated, how, and what happens after?                              |
| **Environment** | The tier's normal and peak load from the scale model | Load ramped past peak until the measure is violated or the artifact fails                    |
| **Pass**        | Measure within budget                                | Failure is graceful and diagnosed, recovery within budget, nothing silent                    |
| **Done when**   | The run completes                                    | The artifact fails; that is the point                                                        |
| **Deliverable** | A number against a budget, and a regression gate<br> | 1) Breaking point (with component location)<br>2) Detect failure mode<br>3) Measure recovery |

> [!WARNING]
> A stress test that ends without failure is a performance test with a generous budget


Failure modes from acceptable to unacceptable: 

1) graceful - bounded and reported
2) hard  - an error, the operation terminal
3) silent - a wrong result or lost data with no signal

The silent class is what stress testing exists to find.

**Performance Test Sub-Type: Endurance Test**
One year of planned load compressed into hours, included where it matters.

Endurance runs at *planned* load, not ramped load. It finds what accumulates
rather than what spikes: state that grows without bound, resources that leak,
and costs that only appear once the system has a history.

Measured over the run, per profile:
- Storage growth, memory, CPU, latency
- Coin inventory: count, denomination spread, age distribution
- Forced recycling and offboarding rate

After the load, once the system settles:
- Idle state and operations, compared to before

#### Scenario

Every scenario, of either kind, has six parts.

| Part                 | Meaning                              | Example                                                       |
| -------------------- | ------------------------------------ | ------------------------------------------------------------- |
| **Source**           | Who or what produces the stimulus    | Customers of a busy venue                                     |
| **Stimulus**         | The event the system must respond to | A day of deposits arrives in one catch-up sync                |
| **Environment**      | The condition the system is in       | Normal operation, Launch tier, UI consuming at 1 ms per event |
| **Artifact**         | The part of the system stimulated    | `CoinageEventBus`, capacity 256                               |
| **Response**         | What the system does                 | Every subscriber converges to the store's terminal status     |
| **Response measure** | How we know                          | 100% convergence, drain under 2 s, lag count reported         |

A performance and a stress scenario for the same artifact share five parts. They differ only in the **Environment** (planned load versus a ramp) and the **Response measure** (a budget versus a breaking point).

### Profiles

The input into every test scenario is a scale of consumption profiles: who pays, how often, what
amounts, and how regular is their purchasing profile. 
With power-of-two denominations, a payment may cost one coin or several, and splitting grinds large coins into small ones over time.

> [!NOTE]
> Hypothesis: variance may matter more than focus. A tight cluster lets the wallet hold a few well-fitted denominations. A wide spread forces splits in both directions and grinds the inventory faster. 

Profile parameters to vary:
- param_1: Payment frequency - how often someone pays
- param_2: Value focus - low, mid or high value goods
- param_3: Variance - how tightly amounts cluster around that focus
- param_4: Top-Up amount - the amount to top up
- param_5: Top-Up split - the runtime lets us pick the split
- param_6: Top-Up threshold - when the top-up amount get triggered
- param_7: Offboard threshold - when offboarding coins triggers
- param_8: Offboard selection - which coin denominations to offboard
- param_9: Recycle age threshold - the coin age at which you recycle (1 = maximum privacy, 16 = only when forced)
- param_10: Privacy budget - what the actor will pay per recycle beyond free (0 = never pay, X = pay up to X, ∞ = always recycle)
- param_11: Recycle return split - the denominations returned after recycling
- param_12: Personhood status - sets free quota (none, lite, person)
- param_13: Initial coins held - starting balance of coins and split _(will be for sake of simplicity 1x top-up amount&split)_

One rule to follow up: recycle takes precedence. offboard is the fallback when quota is exhausted and budget won't cover the fee.

The deliverable is a set of curves per profile, plus which profile degrades worst. That profile sets k for S8

> [!NOTE]
> personhood = none + budget = 0 is a combination which renders the recycler unusable

#### Profile Axes

The 13 parameters group into five axes. An actor profile is a point in this
space.

| Axis                | Params    | What it varies                                | Orthogonal?                             |
| ------------------- | --------- | --------------------------------------------- | --------------------------------------- |
| **Volume**          | 1, 4, 13  | How much traffic the actor generates          | yes                                     |
| **Privacy**         | 9, 10, 12 | Recycle vs offboard, and who pays for it      | yes                                     |
| **Spend shape**     | 2, 3      | Value focus and the variance around it        | yes                                     |
| **Wallet strategy** | 5, 6, 11  | Which denominations the actor chooses to hold | correlated with Spend shape in practice |
| **Exit policy**     | 7, 8      | When and what gets offboarded                 | conditional on Privacy                  |

**Exit policy is conditional.** Recycle takes precedence over offboard, so
`param_7` and `param_8` only fire once the free quota is exhausted and the privacy
budget will not cover the fee. At maximum privacy with an unbounded budget this
axis is inert.

**Wallet strategy and Spend shape are independent dials but correlated in the
real world.** An actor buying high-value goods will hold large denominations.
They stay separate so the mismatch can be tested deliberately an actor holding
small change while spending large, grinds through `MaximumAge` fastest.

#### Scale Model
This defines "planned load" for performance tests and the starting point of every stress ramp. Coinage has no server of its own in this repository. Users load three things: a payer's device, with that user's history; a merchant's device, with how many customers pay it; the chain and its RPC endpoints, with the whole population.

To determine the mix of our profiles we need to orientate ourselves to the real world and heuristically determine types of profiles:
We have two parties involved in a transaction. A sender and a recipient. Either one of them can be a Payer or a Merchant. However, the merchant will in the majority of cases be the recipient.
#### Payer Profile
see [[concrete-profiles]]
#### Merchant Profile
see [[concrete-profiles]]

## Scale Model

## Drawbacks

_To be filled._

## Testing, Security, and Privacy

_To be filled._

## Performance, Ergonomics, and Compatibility

### Performance

_To be filled._

### Ergonomics

_To be filled._

### Compatibility

_To be filled._

## Prior Art and References

_To be filled._

## Unresolved Questions

_To be filled._

## Future Directions and Related Material

_To be filled._
