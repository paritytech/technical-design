# Coinage components

A **component** has a responsibility, inputs, outputs and dependencies. A **flow** shows how components interact during one operation. A **scenario** defines the load and measures the response.

The load generator uses four wallet-side components. These are test boundaries across native modules, not four existing packages or a shared mobile library. The [load paths](load-paths.md) use the same names and IDs.

## Responsibilities and dependencies

| ID | Component | Input → output | Responsibility | Dependencies |
| -- | --------- | -------------- | -------------- | ------------ |
| C1 | Wallet state | Chain observations and operation results → inventory, eligibility and balances | Track coins, vouchers, derivation indices, reservations and operation progress. Retain partial results. | Persistent store, chain reads, time and resolved readiness/recycling policy. |
| C2 | Planner | Intent, inventory and policy → selected inputs, outputs and required calls, or no valid plan | Choose denominations, construct payments and select recycling candidates. | C1 snapshots, runtime bounds, allowance, time and the selected policy variant. |
| C3 | Transaction builder | Plan, keys and chain context → calls, proofs, signed transactions and payment memo | Allocate output keys through C1; construct signatures, recycler proofs and transaction extensions. Encode the memo for the selected payment coins. | C1 index allocation, key derivation, cryptography, runtime metadata, ring revisions and unload-token state. |
| C4 | Submitter | Transaction requests → registration, submission and chain outcomes | Register work before broadcast. Submit transactions, watch results and supply observations to C1. | C1 operation records, RPC, transaction pool, chain heads and dispatch results. |

Transaction building can run inside background submission. The boundary separates responsibilities; it does not require every transaction to be signed before registration.

The **chain is the system under test**: the Coinage pallet and its extensions, member-ring construction, cleanup operations, and node RPC/transaction pool. It is outside the four wallet components. The test driver supplies intents and records results. Memo delivery is another external dependency: native apps use chat; a chain-focused harness can use controlled delivery between agents.

## Native implementation map

The traces use Android Community `f875be3` and iOS Community `b960f77`, also cited in [production policies](production-policies.md). These are source snapshots, not deployment claims.

| Component | iOS Community | Android Community |
| --------- | ------------- | ----------------- |
| C1 Wallet state | [Balance service][ios-state]; [transaction engine][ios-submit] for reservations and progress | [Asset selector][android-state]; [transaction service][android-submit] for reservations and progress |
| C2 Planner | [Coin selector][ios-planner]; [recycling evaluator][ios-recycling-policy] | [Transfer planner][android-planner]; [recycling strategy provider][android-recycling-policy] |
| C3 Transaction builder | [Split strategy][ios-builder]; [voucher unload strategy][ios-unload] | [Split strategy][android-builder]; [voucher unload strategy][android-unload] |
| C4 Submitter | [CoinageTxService][ios-submit] | [CoinageTransactionService contract][android-submit] |

Onboarding and claim entry points are linked beside their diagrams in [load paths](load-paths.md). Platform policy differences remain in [production policies](production-policies.md).

[ios-state]: https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Services/CoinageBalanceService.swift
[ios-submit]: https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/CoinageTx/Engine/CoinageTxService.swift
[ios-planner]: https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/CoinSelection/CoinSelector.swift
[ios-recycling-policy]: https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Recycling/CoinRecyclingEvaluator.swift
[ios-builder]: https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/Plan/Strategies/SplitCoinStrategy.swift
[ios-unload]: https://github.com/paritytech/polkadot-ios-community/blob/b960f771049c07819de1f201b901b037613d42e9/Packages/Coinage/Sources/Transfer/Plan/Strategies/UnloadIntoCoinsStrategy.swift
[android-state]: https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/CoinageAssetSelector.kt
[android-submit]: https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/api/src/main/java/io/paritytech/polkadotapp/feature_coinage_api/domain/transaction/CoinageTransactionService.kt
[android-planner]: https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/TransferPlanner.kt
[android-recycling-policy]: https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/recycling/RecyclingStrategyProvider.kt
[android-builder]: https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/strategies/SplitCoinStrategy.kt
[android-unload]: https://github.com/paritytech/polkadot-android-community/blob/f875be37451f5282a92dec2aa9bf764ac5e64f43/feature/coinage/impl/src/main/java/io/paritytech/polkadotapp/feature_coinage_impl/domain/planner/strategies/UnloadAndSplitVouchersStrategy.kt
