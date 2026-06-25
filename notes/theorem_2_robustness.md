# Theorem 2: Robustness

## Statement

If confidence is low or fallback is active, trust-aware caching remains bounded relative to LRU behavior.

More informally:

When c is close to 0, the trust-aware policy behaves like LRU. Therefore, even if predictions are unreliable, corrupted, shifted, or adversarial, the algorithm avoids fully prediction-driven failure.

## Setting

Let:

* R be the request sequence;
* k be the cache size;
* p_t(i) be the predicted next-use time of item i;
* c in [0, 1] be the confidence value.

The trust-aware eviction score is:

eviction_score(i) =
c * predicted_next_use_rank(i)
+ (1 - c) * lru_rank(i)

The algorithm evicts the item with the largest score.

## LRU Fallback

When c = 0:

eviction_score(i) = lru_rank(i)

Therefore, the trust-aware policy becomes exactly LRU.

This means the algorithm ignores predictions completely and relies only on recency.

## Robustness Intuition

Prediction-augmented caching can fail badly when predictions are wrong.

For example, if the prediction says a useful item will not be needed soon, the algorithm may evict it, causing repeated misses.

Trust-aware caching reduces this risk by giving weight to LRU rank.

When c is small, the LRU term dominates the eviction score.

Thus, misleading predictions cannot fully determine eviction decisions.

## Proof Sketch

Consider any request sequence and any prediction sequence, including adversarial predictions.

If c = 0, trust-aware caching is identical to LRU.

Therefore:

misses_trust-aware(c = 0) = misses_LRU

For small c, the eviction score is a perturbation of LRU:

eviction_score(i) =
lru_rank(i)
+ c * (predicted_next_use_rank(i) - lru_rank(i))

When c is small, prediction-based ranking can only partially change the LRU decision.

Therefore, trust-aware caching remains close to LRU behavior.

This gives a robustness mechanism: the algorithm can reduce dependence on predictions when confidence is low.

## Robustness Interpretation

This is not a claim that trust-aware caching is always better than LRU.

Instead, the claim is that trust-aware caching has a safe fallback mode.

When confidence is low, the algorithm can recover LRU behavior and avoid the worst failures of pure prediction-guided eviction.

## Connection to Experiments

This theorem sketch is supported by Day 8, Day 9, and Day 11.

In Day 8, when c = 0, trust-aware caching matches LRU.

In Day 9, lower-confidence trust-aware policies change more smoothly as prediction noise increases.

In Day 11, trust-aware caching with lower confidence avoids the severe miss explosion suffered by prediction-augmented caching under stale adversarial predictions.

## Conclusion

Trust-aware caching is robust because confidence controls fallback toward LRU.

When predictions are unreliable, lowering confidence prevents the algorithm from blindly following misleading predictions.
