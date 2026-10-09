# Full-flow ramp (Draft)

A population runs every user flow while the load is ramped. This finds which artifact breaks first under realistic mixed load.

**User flow:** [All user flows](../../coinage/user-flows.md#user-flows)

**Runtime path:** Use the [flow-to-runtime map](../../coinage/user-flows.md#flow-to-runtime-and-scenario-map) to record which components the chosen inventory reaches. All submitted calls share [pool and execution capacity](../../coinage/pallet-components.md#one-coin-transaction-client-to-runtime-and-back). [Cleanup](../../coinage/pallet-components.md#ocw-cleanup-and-archive-recovery) needs eligible state and enough elapsed time; instance creation is normally setup.

| Part | This scenario |
| ---- | ------------- |
| **Source** | A population built from the scale model. |
| **Stimulus** | The population runs onboarding, payments, recycling and offboarding while the load is ramped. |
| **Environment** | Stress only: ramp the population's load from planned peak until the first response measure fails. Every policy resolves to one platform variant. |
| **Artifacts** | Artifacts reached by the configured flows. Instance creation and expired-state cleanup are included only when configured. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | Each artifact holds its response measure until its breaking point. |
| **Response measure** | The first artifact to violate its response measure, how it fails and whether it recovers. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).

## Pilot: mixed flows on one network

**Question:** When every flow runs together and the load keeps rising, which artifact fails first, how does it fail, and does it recover?

**Before this runs:** each flow's own pilot must pass at 1,000 actors or more: [top-up](top-up-burst.md), [claim](claim-burst.md), [payment burst](payment-burst.md) including the unload pilot, [merchant fan-in](merchant-fan-in.md), [synchronised recycling](synchronised-recycling.md), [free-quota exhaustion](free-quota-exhaustion.md) and [offboarding](offboarding-burst.md). Otherwise a failure here cannot be traced to one flow.

| Setting | Pilot |
| ------- | ----- |
| Network | Same network as the flow pilots, with real Members and Coinage OCWs, default pool, People from the [shared unload fixture](../unload-fixture.md) and one sufficient instance. Record every node and runtime revision. |
| Population | Provisional until the [scale model](../../README.md#scale-model) is agreed: 10% of operations are top-ups, 60% payments, 20% recycling evaluations and 10% offboards. Payments use the selected platform's planner, so each payment becomes an exact, split or unload plan. Each payment's recipient claims it. Replace this mix with the agreed one when it exists. |
| Policies | Select one platform for every wallet-policy key where Android and iOS differ. |
| Ramp | Start at 10 operations per second for 10 minutes. Double the rate each 10-minute step. Arrivals are randomised within each step. |
| Stop | End the ramp at the first step where any response measure below fails, then stop arrivals and observe recovery for 30 minutes. |

**Response measures per step.** A step passes only if all of these hold:

| Artifact | Measure | Provisional limit |
| -------- | ------- | ----------------- |
| N1.pool | Rejections and evictions | None |
| Each flow | p95 time from intent to completion | At most twice that flow's own pilot p95 at a similar size |
| R3.rings | Time from load finality to ring readiness | No growth over the step |
| N2.execution | Why block authoring stopped; claims or calls per block | Report only |
| R2.origins | Free-token limit from `get_free_unload_token_info` | Report changes |
| OCW calls | Inclusion delay for maintenance calls | Report only |
| Relay | Finality lag and PVF execution time | Report only |
| All | Silent results: a client told "ready" with no final outcome, or wrong state | None |

The provisional limits are placeholders for the budgets in the [open questions](../../README.md#open-questions). Replace them when budgets are agreed, and say which limit stopped the ramp.

**At the stopping step, report:**

- the first artifact to break, and the exact measure and value;
- whether the failure was graceful, hard or silent, using the [overview's classes](../../README.md#test-types);
- what was still pending when arrivals stopped, per flow;
- recovery: time until the pool is empty, ring readiness is caught up and finality is back to its pre-run lag. If something does not recover within 30 minutes, report what remains.

Cleanup and instance creation only take part if their state is set up for them. Their own scenarios are [cleanup backlog](cleanup-backlog.md) and [instance proliferation](instance-proliferation.md).

## Requested burst campaign

The [remaining-flow campaign](../remaining-flow-campaign.md) specifies six sequential cases for this scenario, from 100 to 20,000 actors, including default-pool, paced and enlarged-pool comparisons. It also defines evidence for recycling-unavailable handling and distinguishes the fixed-plan pilot from the broader scenario above.
