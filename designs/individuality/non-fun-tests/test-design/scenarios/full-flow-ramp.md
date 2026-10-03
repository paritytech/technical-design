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
