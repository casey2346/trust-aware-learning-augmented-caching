# Day 10: Zipf Distribution Experiment

## Goal

Day 10 evaluates caching algorithms under Zipf-distributed request traces.

This is important because real CDN, video streaming, web, and storage request workloads often show long-tail popularity patterns. A small number of popular items receive many requests, while many other items are requested rarely.

## Motivation

Earlier experiments used controlled synthetic traces and prediction noise sweeps.

Day 10 moves the project closer to realistic systems by testing caching policies under skewed popularity distributions.

Zipf-distributed traces are useful because they approximate workloads where some content is globally popular while most content belongs to a long tail.

## Experimental Setup

The experiment uses Zipf request traces with:

Zipf alpha = 0.6, 0.8, 1.0, 1.2

Cache sizes:

k = 10, 20, 50

The Zipf alpha controls popularity skew.

A smaller alpha means popularity is more spread out.

A larger alpha means a smaller number of items dominate the request sequence.

## Algorithms Compared

The experiment compares:

1. Belady optimal offline caching;
2. LRU;
3. FIFO;
4. prediction-augmented caching with exact predictions;
5. prediction-augmented caching with corrupted predictions;
6. trust-aware caching with confidence c = 0.50.

## Prediction Setting

The exact prediction model uses true next-use information.

The corrupted prediction model randomly corrupts a fraction of next-use predictions.

Trust-aware caching uses corrupted predictions but interpolates between prediction-guided eviction and LRU fallback.

## Evaluation Metric

The main metric is cache miss ratio:

miss ratio = number of misses / total number of requests

Lower miss ratio means better caching performance.

## Expected Result

Belady should provide the offline lower bound.

Prediction-augmented caching with exact predictions should approach Belady-style behavior.

LRU should remain a stable online baseline.

Prediction-augmented caching with corrupted predictions may degrade when predictions are unreliable.

Trust-aware caching should provide a more robust middle ground between prediction use and LRU fallback.

## Why Zipf Matters

Zipf traces are closer to realistic content request patterns than uniform random traces.

In CDN and video streaming systems, a few videos or files may receive many requests, while many long-tail items receive only occasional requests.

This makes Zipf-distributed traces useful for connecting the theoretical caching project to real systems.

## Core Conclusion

Under realistic skewed popularity, prediction-aware caching can help, but robustness still depends on prediction reliability.

Accurate predictions can move online caching closer to Belady-like behavior.

Corrupted predictions can reduce the benefit of prediction-guided eviction.

Trust-aware fallback helps control this risk.

## Day 10 Output

Completed:

* generated Zipf-distributed request traces;
* tested Zipf alpha values 0.6, 0.8, 1.0, and 1.2;
* tested cache sizes 10, 20, and 50;
* compared Belady, LRU, FIFO, prediction-augmented caching, and trust-aware caching;
* generated a Zipf cache miss ratio figure;
* documented why Zipf traces matter for CDN and video-style workloads.

Files produced:

* experiments/day10_zipf_experiment.py
* figures/day10_zipf_cache_miss_ratio.png
* notes/day10_zipf_experiment.md
