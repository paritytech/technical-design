# Named runtime conditions

A named runtime condition is a boolean fact derived from profile inputs, wallet state and runtime state. A condition does not prescribe how the wallet responds.

## Preferred Recycling Unavailable

This condition is satisfied for a coin when:

- the coin has reached the actor's preferred recycle age;
- the actor has no remaining free-recycling allowance; and
- the wallet implementation has no currently executable paid-unload method whose quoted fee is at or below the actor's paid recycling fee limit.

A wallet implementation with no supported paid-unload method satisfies the third clause without assigning a numeric fee to that unavailable method. When a paid method exists, its fee must be quoted in the asset used by `privacy.recycling.paid_fee_limit` before comparison.

The condition does not prescribe an action. The [`wallet.recycling.unavailable_handling`](profile-schema.md#recycling-unavailable-handling) policy determines the wallet's response.
