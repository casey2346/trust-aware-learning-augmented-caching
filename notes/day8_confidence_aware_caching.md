# Day 8: Confidence-Aware Trust-Aware Caching

## Goal

Day 8 implements the main trust-aware caching idea.

The project now has online baselines, an offline optimal benchmark, trace generators, prediction models, and prediction-augmented caching. Day 8 adds the confidence mechanism that controls how much the algorithm should trust predictions.

## Motivation

Prediction-augmented caching can approach Belady when predictions are accurate.

However, Day 7 showed that unreliable or adversarial predictions can make prediction-guided eviction much worse than LRU.

This motivates a trust-aware policy that uses predictions when confidence is high and falls back toward LRU when confidence is low.

## Confidence Parameter

The trust-aware policy uses a confidence value:

c in [0, 1]

The meaning is:

c = 1 means fully trust prediction-guided eviction.

c = 0 means fall back to LRU eviction.

0 < c < 1 means interpolate between prediction-guided eviction and LRU fallback.

## Eviction Score

For each cached item, the algorithm computes:

eviction_score(item) =
c * predicted_next_use_rank(item)
+ (1 - c) * lru_rank(item)

The algorithm evicts the item with the largest eviction score.

## Prediction Rank

The prediction rank is based on predicted next-use time.

An item with a farther predicted next use receives a larger prediction-based eviction rank.

This follows the same intuition as Belady: items needed farthest in the future are better eviction candidates.

## LRU Rank

The LRU rank is based on recency.

An item that was used less recently receives a larger LRU-based eviction rank.

This creates a fallback toward the classical LRU baseline.

## Algorithm

For each request:

1. If the requested item is in cache, count a hit and update LRU recency.
2. If the requested item is not in cache, count a miss.
3. If the cache is full, compute the trust-aware eviction score for each cached item.
4. Evict the item with the largest score.
5. Insert the requested item as most recently used.

## Implementation

Implemented file:

src/caching/trust_aware.py

The implementation combines predicted next-use ranks with LRU ranks using the confidence value.

## Experiment

Implemented file:

experiments/day8_confidence_aware_caching.py

The experiment evaluates trust-aware caching under exact, corrupted, and adversarial predictions across confidence values:

c = 0, 0.25, 0.5, 0.75, 1

Generated figure:

figures/day8_confidence_ablation.png

## Expected Result

When predictions are accurate, higher confidence should move the algorithm closer to prediction-guided eviction and closer to Belady-like behavior.

When predictions are adversarial, higher confidence may hurt performance because the algorithm trusts misleading predictions.

When confidence is low, the algorithm falls back toward LRU and avoids severe prediction-driven failure.

## Research Significance

Day 8 is the main innovation point of the project.

It shows that confidence can control the trade-off between using predictions and preserving robustness.

This directly addresses the weakness observed in Day 7: prediction-augmented caching can fail when predictions are unreliable.

## Core Conclusion

Confidence controls the trade-off between prediction use and LRU fallback.

A trust-aware caching policy can use predictions when they are reliable while reducing dependence on predictions when confidence is low.

## Day 8 Output

Completed:

* implemented confidence-aware caching;
* combined predicted next-use rank with LRU rank;
* tested confidence values between 0 and 1;
* compared exact, corrupted, and adversarial prediction settings;
* generated a confidence-ablation figure;
* documented how confidence controls prediction use and fallback behavior.

Files produced:

* src/caching/trust_aware.py
* experiments/day8_confidence_aware_caching.py
* figures/day8_confidence_ablation.png
* notes/day8_confidence_aware_caching.md
