# Theorem 3: Adversarial Separation

## Statement

There exist corrupted or stale prediction sequences where prediction-augmented caching suffers many misses, while trust-aware caching with fallback avoids the same degradation.

More informally:

Prediction-augmented caching can be much worse than LRU when predictions are adversarial. Trust-aware caching can avoid this failure when confidence is low enough.

## Setting

Consider a cache of size k.

There are two hot sets:

Old hot set:

A = {a_1, a_2, ..., a_k}

New hot set:

B = {b_1, b_2, ..., b_k}

The request sequence has phases.

In one phase, items from A are repeatedly requested.

Then the workload suddenly switches, and items from B are repeatedly requested.

This models a CDN or video streaming workload where the popular content changes suddenly.

## Stale Prediction Model

Assume the prediction model is stale.

After the workload switches from A to B, the prediction model still believes that A is important.

It predicts:

* old hot items in A will be requested soon;
* new hot items in B will be requested far in the future.

This is the opposite of the true request pattern.

## Failure of Prediction-Augmented Caching

Prediction-augmented caching evicts the item with the farthest predicted next use.

Because the stale prediction model says new hot items are far away, prediction-augmented caching tends to evict items from B.

But B is exactly the current hot set.

Therefore, the algorithm repeatedly evicts useful items and suffers many cache misses.

This creates a large gap between prediction-augmented caching and robust recency-based policies.

## Trust-Aware Fallback

Trust-aware caching uses:

eviction_score(i) =
c * predicted_next_use_rank(i)
+ (1 - c) * lru_rank(i)

When c is low, the LRU rank dominates.

LRU adapts to the new hot set because items in B are requested recently and repeatedly.

Therefore, trust-aware caching with low confidence keeps the new hot items in cache and avoids the same repeated miss pattern.

## Proof Sketch

Construct a request sequence with repeated phase changes.

At each phase boundary:

1. the true hot set changes from A to B;
2. the prediction model remains focused on A;
3. prediction-augmented caching treats B as unimportant;
4. prediction-augmented caching evicts B items even though they will be requested soon.

This causes repeated misses for prediction-augmented caching during the new phase.

In contrast, LRU quickly adapts because items in B become recently used.

Trust-aware caching with low confidence behaves close to LRU, so it also adapts to B.

Therefore, there exists a request sequence and prediction sequence where prediction-augmented caching has many more misses than trust-aware caching.

## Connection to Experiments

This theorem sketch is directly supported by Day 11.

The adversarial burst experiment creates sudden hot-item shifts and stale predictions.

The result shows:

* prediction-augmented caching suffers a high miss ratio;
* LRU adapts through recency;
* trust-aware caching with low confidence matches the robust fallback behavior;
* trust-aware caching with high confidence can also fail because it still over-trusts predictions.

## Conclusion

The adversarial separation shows why trust-aware fallback is necessary.

Prediction-augmented caching can perform extremely well under accurate predictions, but it can fail under corrupted or stale predictions.

Trust-aware caching avoids this failure by controlling how much the algorithm trusts predictions.
