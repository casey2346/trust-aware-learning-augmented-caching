# Day 11: Adversarial Burst Sequences

## Goal

Day 11 evaluates caching algorithms on adversarial burst sequences.

This is one of the most important experiments in the project because it directly tests the weakness of prediction-augmented caching under stale or misleading predictions.

## Motivation

In CDN and video streaming systems, request patterns can shift suddenly. A video, file, or content group may become popular for a short period of time, and then a different group may become popular.

A prediction model may lag behind this change. It may continue to believe that the old hot items are important while the new hot items are actually being requested.

This creates a failure case for pure prediction-guided caching.

## Adversarial Burst Design

The experiment creates multiple phases.

In each phase, a hot set of items receives most of the requests.

At the phase boundary, the active hot set suddenly changes.

The adversarial prediction model is stale:

* it still treats the previous hot set as important;
* it predicts the new hot set as far away;
* therefore prediction-augmented caching may evict the new useful items.

## Algorithms Compared

The experiment compares:

1. LRU;
2. prediction-augmented caching;
3. trust-aware caching with confidence c = 0.25;
4. trust-aware caching with confidence c = 0.50;
5. trust-aware caching with confidence c = 0.75.

## Evaluation Metric

The main metric is rolling cache miss ratio.

The x-axis is time.

The y-axis is rolling cache miss ratio.

A rolling metric is useful because it shows when algorithms fail during burst transitions rather than only reporting one final average.

## Expected Result

Prediction-augmented caching should suffer when predictions are stale or adversarial.

LRU should adapt to the new hot set through recency.

Trust-aware caching should reduce severe miss spikes by mixing prediction-guided eviction with LRU fallback.

Lower confidence should behave closer to LRU.

Higher confidence should depend more on stale predictions and may suffer larger miss spikes.

## Why This Matters

This experiment connects the project to realistic streaming and CDN behavior.

Real systems often experience sudden popularity shifts. A robust learning-augmented caching policy should not collapse when predictions lag behind the workload.

This experiment demonstrates why confidence-aware fallback is useful.

## Core Conclusion

Adversarial burst sequences expose the risk of blindly trusting predictions.

When request hotspots shift and predictions remain stale, prediction-augmented caching can evict the wrong items and suffer high miss ratios.

Trust-aware fallback helps avoid severe miss explosions by retaining LRU-style adaptation.

## Day 11 Output

Completed:

* generated adversarial burst request sequences;
* simulated stale predictions that lag behind hot-set changes;
* compared LRU, prediction-augmented caching, and trust-aware caching;
* measured rolling cache miss ratio over time;
* generated an adversarial burst failure figure.

Files produced:

* experiments/day11_adversarial_bursts.py
* figures/day11_adversarial_burst_failure.png
* notes/day11_adversarial_burst.md
