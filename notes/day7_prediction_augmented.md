# Day 7: Prediction-Augmented Caching

## Goal

Day 7 implements a prediction-augmented caching algorithm.

The project now has classical online baselines, an offline optimal benchmark, synthetic trace generators, and prediction models. Day 7 connects these components by using predicted next-use times to make eviction decisions.

## Main Idea

Belady's offline optimal algorithm evicts the cached item whose true next future request is farthest away.

An online algorithm cannot know the true future. However, a prediction-augmented algorithm can use predicted next-use times instead.

The prediction-augmented rule is:

On a cache miss, if the cache is full, evict the cached item with the farthest predicted next use.

## Prediction Used

At time t, for each cached item i, the prediction is:

p_t(i) = predicted next request time of item i after time t

The algorithm evicts the item with the largest p_t(i).

## Algorithm

For each request:

1. If the requested item is already in cache, count a cache hit.
2. If the requested item is not in cache, count a cache miss.
3. If the cache is full, use predictions to choose an item to evict.
4. Evict the cached item whose predicted next use is farthest away.
5. Insert the requested item.

## Why This Approaches Belady

If the prediction is exact, then predicted next-use time equals true next-use time.

In that case, prediction-augmented caching makes the same type of eviction decision as Belady.

Therefore, with accurate predictions, prediction-augmented caching can approach Belady-style behavior.

## Why This Can Fail

If predictions are wrong, the algorithm may evict useful items.

For example, if an item will be needed soon but the prediction says it is far away, prediction-augmented caching may evict it and suffer extra misses.

This creates the robustness problem that motivates trust-aware fallback in later days.

## Implementation

Implemented file:

src/caching/prediction_augmented.py

The implementation uses:

* request sequence;
* cache size;
* prediction sequence;
* predicted next-use maps.

## Experiment

Implemented file:

experiments/day7_prediction_augmented.py

The experiment compares:

1. Belady optimal offline caching;
2. LRU online caching;
3. prediction-augmented caching with exact predictions;
4. prediction-augmented caching with noisy predictions;
5. prediction-augmented caching with corrupted predictions;
6. prediction-augmented caching with adversarial predictions.

Generated figure:

figures/day7_prediction_augmented_vs_lru.png

## Expected Result

Prediction-augmented caching with exact predictions should be close to Belady.

LRU should provide a stable online baseline.

Prediction-augmented caching with noisy, corrupted, or adversarial predictions may perform worse than exact prediction and may sometimes perform worse than LRU.

## Research Significance

Day 7 demonstrates both the promise and risk of learning-augmented caching.

Accurate predictions can help online caching approach offline-optimal behavior.

Unreliable predictions can harm performance.

This creates the need for a confidence-aware or trust-aware algorithm that can use predictions when they are reliable and fall back toward LRU when they are not.

## Core Conclusion

Prediction-augmented caching can approach Belady when predictions are accurate.

However, unreliable predictions can make prediction-guided eviction worse than robust online baselines.

## Day 7 Output

Completed:

* implemented prediction-augmented caching;
* used predicted next-use time for eviction;
* compared prediction-augmented caching with Belady and LRU;
* tested exact, noisy, corrupted, and adversarial prediction settings;
* generated a prediction-augmented caching comparison figure;
* documented why prediction-augmented caching motivates trust-aware fallback.

Files produced:

* src/caching/prediction_augmented.py
* experiments/day7_prediction_augmented.py
* figures/day7_prediction_augmented_vs_lru.png
* notes/day7_prediction_augmented.md
