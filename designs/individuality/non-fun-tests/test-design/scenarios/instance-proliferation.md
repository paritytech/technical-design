# Instance proliferation (Draft)

Many Coinage instances exist at once. Any signed account can currently create a sponsored instance, and each instance creates one recycler collection per denomination. The offchain workers walk this state, so their work grows with the number of instances even if payment volume does not.

**User flow:** none directly. Instance creation is setup, but in this runtime anyone can do it.

**Runtime path:** [Instances and sponsored deposits](../../coinage/pallet-components.md#instances-and-sponsored-deposits). `create_sponsored_instance` requires `EnablePermissionless`, which is `true` in this runtime, and holds a creation deposit ([config][permissionless]). Each instance creates collections for exponents 0 to 14: 15 collections ([creation][create-instance]). One asset can back several instances.

| Part | This scenario |
| ---- | ------------- |
| **Source** | Many signed accounts, each creating instances. |
| **Stimulus** | The number of instances grows, while a fixed reference workload runs on one instance. |
| **Environment** | Performance: the instance count expected in production. Stress: ramp the instance count. |
| **Artifacts** | R5.instances, R3.rings, R4.cleanup, N1.pool, N2.execution, N3.storage. IDs are defined in the [artifact catalogue](../../coinage/user-flows.md#component-and-artifact-catalogue). |
| **Response** | Instance creation stays bounded by its deposit. The reference workload keeps its latency and ring readiness. |
| **Response measure** | Creation calls per block and their weight; state size; OCW maintenance delay; reference workload finality and ring readiness, against the no-extra-instance baseline. |

**Still to decide:** scale, budgets and the actor profiles, which follow the [profile schema](../profile-schema.md). These wait on the [open questions](../../README.md#open-questions).

## Pilot: reference workload at rising instance counts

**Question:** Does the number of instances slow ring readiness or user transactions on an unrelated instance?

| Setting | Pilot |
| ------- | ----- |
| Network | Same as the top-up burst, with real Members and Coinage OCWs and the default pool. |
| Instances | Steps of 0, 100, 1,000 and 10,000 extra sponsored instances, each on fresh state, created from funded accounts before the reference workload. Read the creation deposit at the starting block and fund each account for it. |
| Reference workload | 1,000 top-ups on one sufficient instance, then wait for ring readiness. Use the same workload at every step. |
| Creation burst | Separately, at the 1,000 step, submit all creations at once and measure their own inclusion and finality. |

**Required evidence and checks:**

- Instances and recycler collections present after each creation stage: 15 collections per instance.
- Creation call weight, calls per block and finality during the creation burst.
- State size before and after creation, from the node database.
- For the reference workload: load finality and ring readiness at p50, p95 and max, compared with the 0-instance step.
- Members and Coinage OCW behaviour: maintenance calls per block and how long each call waited for inclusion. Note any step where ring builds for the reference instance slow down.
- The creation deposit held per creator. If creation is stopped by the deposit rather than by the chain, say so.

Empty instances may not cost the workers anything, if the workers skip collections with no members. In that case, add a variant where each extra instance has one voucher loaded, and report both.

[permissionless]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/runtimes/next-people-paseo/src/people.rs#L1640
[create-instance]: https://github.com/paritytech/individuality-community/blob/fce93ef38a15c673a8b0b208362bc46ae755c7d7/pallets/coinage/src/lib.rs#L4278-L4340
