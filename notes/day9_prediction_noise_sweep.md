# Day 9: Prediction Noise Sweep

## Goal

Day 9 evaluates how caching algorithms behave as prediction quality gets worse.

The goal is to show that prediction-augmented caching can perform well when predictions are accurate, but can degrade as predictions become noisy or corrupted. Trust-aware caching should be more stable because it can fall back toward LRU.

## Experimental Setup

The experiment uses a video/CDN-style synthetic request trace.

The cache size is fixed.

Prediction noise is varied from:

0% to 100%

The noise level represents the probability that a next-use prediction is corrupted.

## Algorithms Compared

The experiment compares:

1. Belady optimal offline caching;
2. LRU;
3. FIFO;
4. prediction-augmented caching;
5. trust-aware caching with confidence c = 0.25;
6. trust-aware caching with confidence c = 0.50;
7. trust-aware caching with confidence c = 0.75.

## Prediction Noise

The base prediction is exact next-use prediction:

p_t(i) = true next request time of item i after time t

To create noisy predictions, a fraction of predictions is corrupted.

At 0% noise, the prediction is exact.

At 100% noise, all predictions are corrupted.

## Evaluation Metric

The main metric is cache miss ratio:

miss ratio = number of misses / total number of requests

Lower miss ratio means better caching performance.

## Expected Result

Belady should remain the best or near-best benchmark because it uses true future information.

LRU and FIFO are prediction-free, so their performance should remain constant across prediction noise levels.

Prediction-augmented caching should perform well when noise is low, but degrade as prediction noise increases.

Trust-aware caching should be more stable than pure prediction-augmented caching because it mixes prediction-guided eviction with LRU fallback.

## Why This Matters

Day 7 showed that accurate predictions can help prediction-augmented caching approach Belady.

Day 8 introduced confidence-aware fallback.

Day 9 tests the robustness story directly by sweeping prediction noise from low to high.

This is important because real prediction systems are rarely perfectly accurate. A useful learning-augmented algorithm should not collapse when predictions become unreliable.

## Core Conclusion

Prediction quality strongly affects prediction-augmented caching.

As prediction noise increases, pure prediction-guided eviction becomes less reliable.

Trust-aware caching provides a smoother trade-off between prediction use and LRU fallback.

## Day 9 Output

Completed:

* ran prediction noise sweep from 0% to 100%;
* compared Belady, LRU, FIFO, prediction-augmented caching, and trust-aware caching;
* tested trust-aware confidence values c = 0.25, c = 0.50, and c = 0.75;
* generated a cache miss ratio figure across prediction noise levels;
* documented how prediction noise affects caching robustness.

Files produced:

* experiments/day9_prediction_noise_sweep.py
* figures/day9_prediction_noise_sweep.png
* notes/day9_prediction_noise_sweep.md
