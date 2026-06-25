# Theorem 1: Consistency

## Statement

If next-use predictions are accurate and confidence is high, trust-aware caching approaches prediction-augmented caching and can behave similarly to Belady-style eviction.

More informally:

When prediction error is small and confidence c is close to 1, the trust-aware policy makes eviction decisions close to the prediction-guided policy.

Since prediction-guided caching with exact next-use predictions matches the same intuition as Belady's offline optimal rule, trust-aware caching can approach Belady-like behavior under accurate predictions.

## Setting

Let:

* R = (r_1, r_2, ..., r_T) be the request sequence;
* k be the cache size;
* p_t(i) be the predicted next-use time of item i at time t;
* n_t(i) be the true next-use time of item i at time t;
* c in [0, 1] be the confidence value.

The trust-aware eviction score is:

eviction_score(i) =
c * predicted_next_use_rank(i)
+ (1 - c) * lru_rank(i)

The algorithm evicts the cached item with the largest score.

## Prediction Accuracy

Assume predictions are accurate:

p_t(i) is close to n_t(i)

for all cached items i at time t.

If predictions are exact:

p_t(i) = n_t(i)

then prediction-based eviction ranks items in the same order as Belady's next-use rule.

## Consistency Intuition

When c = 1, the trust-aware policy becomes fully prediction-guided.

In this case:

eviction_score(i) = predicted_next_use_rank(i)

So the algorithm evicts the item with the farthest predicted next use.

If predictions are exact, this is the same eviction principle used by Belady's algorithm.

When c is close to 1, the LRU component has only small weight:

(1 - c)

Therefore, the trust-aware score is dominated by the prediction rank.

This means trust-aware caching behaves close to prediction-augmented caching when confidence is high.

## Proof Sketch

At each eviction step, compare the item chosen by prediction-augmented caching and the item chosen by trust-aware caching.

Prediction-augmented caching chooses the item with the largest predicted next-use rank.

Trust-aware caching chooses the item maximizing:

c * predicted_next_use_rank(i)

* (1 - c) * lru_rank(i)

As c approaches 1, the second term becomes small.

Therefore, unless two items have very close prediction ranks, the same item will be selected by both policies.

If predictions are exact, the prediction ranks match true next-use ranks. Thus, prediction-guided eviction follows the same ranking principle as Belady.

Hence, under accurate predictions and high confidence, trust-aware caching approaches prediction-augmented and Belady-like behavior.

## Connection to Experiments

This theorem sketch is supported by Day 7 and Day 8.

In Day 7, prediction-augmented caching with exact predictions closely matches Belady.

In Day 8, trust-aware caching with high confidence and exact predictions approaches the prediction-guided result.

## Conclusion

Trust-aware caching is consistent in the sense that, when predictions are accurate and confidence is high, it can exploit predictions and approach Belady-like eviction behavior.
