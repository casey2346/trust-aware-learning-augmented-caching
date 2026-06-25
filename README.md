# Trust-Aware Learning-Augmented Caching under Unreliable Predictions

## Main Message

Prediction-augmented caching can fail under corrupted request predictions, while trust-aware fallback to LRU preserves robustness.

This project studies how online caching algorithms can use learned predictions without becoming fragile when those predictions are noisy, shifted, corrupted, stale, or adversarial.

---

## Research Question

Can a learning-augmented caching algorithm improve cache performance when predictions are accurate while remaining robust when predictions are unreliable?

---

## Why Caching Matters

Caching is a fundamental online decision-making problem. It appears in CPU caches, CDN systems, cloud storage, database buffer management, and video streaming platforms.

A caching algorithm must decide which items to keep in a limited cache before knowing the full future request sequence.

Classical online policies such as LRU and FIFO are robust but prediction-free. Prediction-augmented caching can reduce cache misses when future request predictions are accurate, but it can also fail when predictions are corrupted or stale.

This project studies a trust-aware fallback mechanism that interpolates between prediction-guided eviction and LRU fallback.

---

## Problem Setting

Given a request sequence:

R = (r_1, r_2, ..., r_T)

and cache size:

k

each request is either a cache hit or a cache miss.

A cache hit occurs when the requested item is already in cache.

A cache miss occurs when the requested item is not in cache. If the cache is full, the algorithm must evict one cached item before inserting the requested item.

The main metric is:

cache miss ratio = number of misses / total number of requests

Lower miss ratio means better caching performance.

---

## Algorithms Implemented

### LRU

Least Recently Used evicts the item that was requested least recently. It uses recency and does not require predictions.

### FIFO

First In First Out evicts the item that entered the cache earliest. It uses insertion order and does not update priority after cache hits.

### Belady Optimal Offline Benchmark

Belady's algorithm evicts the cached item whose next future request is farthest away. If an item is never requested again, it is evicted first.

Belady is not an online algorithm because it uses future information. It is used as the offline lower-bound benchmark.

### Prediction-Augmented Caching

Prediction-augmented caching uses predicted next-use time:

p_t(i) = predicted next request time of item i after time t

On a cache miss, if the cache is full, it evicts the cached item with the farthest predicted next use.

When predictions are accurate, this can approach Belady-like behavior. When predictions are wrong, it can perform worse than LRU.

### Trust-Aware Caching

Trust-aware caching introduces a confidence value:

c ∈ [0, 1]

The eviction score is:

eviction_score(item) =
    c * predicted_next_use_rank(item)
    + (1 - c) * lru_rank(item)

The algorithm evicts the item with the largest score.

When `c = 1`, the policy fully trusts predictions.

When `c = 0`, the policy falls back to LRU.

When `0 < c < 1`, the policy interpolates between prediction-guided eviction and LRU fallback.

---

## Theoretical Claims

### Theorem 1: Consistency

If predictions are accurate and confidence is high, trust-aware caching approaches prediction-augmented caching and can behave similarly to Belady-style eviction.

### Theorem 2: Robustness

If confidence is low or fallback is active, trust-aware caching remains bounded relative to LRU behavior.

### Theorem 3: Adversarial Separation

There exist corrupted or stale prediction sequences where prediction-augmented caching suffers many misses, while trust-aware fallback avoids the same degradation.

---

## Experiments

This project includes the following experiments:

Day 2:  LRU baseline
Day 3:  FIFO vs LRU
Day 4:  Belady offline optimum
Day 5:  Synthetic trace generators
Day 6:  Prediction model and prediction error
Day 7:  Prediction-augmented caching
Day 8:  Confidence-aware trust-aware caching
Day 9:  Prediction noise sweep
Day 10: Zipf-distributed request traces
Day 11: Adversarial burst sequences
Day 12: Theorem proof sketches
Day 13: Technical report

---

## Main Results

### 1. Belady provides the offline lower bound

Belady optimal caching consistently gives the lowest or near-lowest miss ratio because it uses future request information.

### 2. Prediction-augmented caching can approach Belady

When predictions are exact, prediction-augmented caching closely matches Belady-style behavior.

### 3. Prediction-augmented caching can fail under bad predictions

When predictions are corrupted, shifted, stale, or adversarial, prediction-guided eviction can evict useful items and suffer many cache misses.

### 4. Trust-aware caching provides a controlled trade-off

Confidence controls how much the algorithm trusts predictions.

Low confidence behaves closer to LRU.

High confidence behaves closer to prediction-guided eviction.

### 5. Adversarial burst sequences show the strongest failure case

When request hotspots suddenly shift but predictions remain focused on old hot items, prediction-augmented caching suffers a large miss ratio. Trust-aware fallback with low confidence avoids the same miss explosion.

---

## Main Figures

### LRU Cache Size Sweep

figures/day2_lru_cache_size_sweep.png

Shows that cache miss ratio decreases as cache size increases.

### FIFO vs LRU

figures/day3_fifo_vs_lru.png

Shows that LRU uses recency information while FIFO only uses insertion order.

### Belady vs Online Baselines

figures/day4_belady_vs_lru_fifo.png

Shows Belady as the offline optimal lower-bound benchmark.

### Trace Distributions

figures/day5_trace_distributions.png

Shows uniform, Zipf, burst, video/CDN-style, and adversarial request traces.

### Prediction Error Models

figures/day6_prediction_noise.png

Shows exact, Gaussian, shifted, corrupted, and adversarial prediction errors.

### Prediction-Augmented Caching

figures/day7_prediction_augmented_vs_lru.png

Shows that exact predictions approach Belady, while adversarial predictions can fail badly.

### Confidence Ablation

figures/day8_confidence_ablation.png

Shows how confidence controls the trade-off between prediction use and LRU fallback.

### Prediction Noise Sweep

figures/day9_prediction_noise_sweep.png

Shows that prediction-augmented caching becomes less reliable as prediction noise increases.

### Zipf Request Traces

figures/day10_zipf_cache_miss_ratio.png

Shows caching behavior under long-tail request distributions similar to CDN and video workloads.

### Adversarial Burst Failure

figures/day11_adversarial_burst_failure.png

Shows that stale predictions can cause prediction-augmented caching to fail, while trust-aware fallback avoids severe miss explosions.

---

## How to Reproduce

### 1. Clone the repository

```bash
git clone https://github.com/casey2346/trust-aware-learning-augmented-caching.git
cd trust-aware-learning-augmented-caching
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run individual experiments

```bash
PYTHONPATH=. python3 experiments/day2_lru_baseline.py
PYTHONPATH=. python3 experiments/day3_fifo_vs_lru.py
PYTHONPATH=. python3 experiments/day4_belady_optimal.py
PYTHONPATH=. python3 experiments/day5_trace_examples.py
PYTHONPATH=. python3 experiments/day6_prediction_quality.py
PYTHONPATH=. python3 experiments/day7_prediction_augmented.py
PYTHONPATH=. python3 experiments/day8_confidence_aware_caching.py
PYTHONPATH=. python3 experiments/day9_prediction_noise_sweep.py
PYTHONPATH=. python3 experiments/day10_zipf_experiment.py
PYTHONPATH=. python3 experiments/day11_adversarial_bursts.py
```

### 4. Open generated figures

```bash
open figures/day11_adversarial_burst_failure.png
```

---

## Repository Structure

trust-aware-learning-augmented-caching/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── caching/
│       ├── __init__.py
│       ├── problem.py
│       ├── lru.py
│       ├── fifo.py
│       ├── belady.py
│       ├── trace_generators.py
│       ├── prediction_models.py
│       ├── prediction_augmented.py
│       └── trust_aware.py
├── experiments/
│   ├── day2_lru_baseline.py
│   ├── day3_fifo_vs_lru.py
│   ├── day4_belady_optimal.py
│   ├── day5_trace_examples.py
│   ├── day6_prediction_quality.py
│   ├── day7_prediction_augmented.py
│   ├── day8_confidence_aware_caching.py
│   ├── day9_prediction_noise_sweep.py
│   ├── day10_zipf_experiment.py
│   └── day11_adversarial_bursts.py
├── figures/
├── notes/
├── traces/
└── paper/
    └── technical_report.md

---

## Limitations

This project is a research-style prototype.

The confidence value is manually specified rather than learned.

The experiments use synthetic traces rather than real production CDN logs.

The theoretical analysis is currently written as proof sketches, not full competitive-ratio proofs.

The trust-aware score uses a simple linear interpolation between prediction rank and LRU rank.

---

## Future Work

Future work could learn confidence automatically from historical prediction error.

The proof sketches could be extended into formal competitive-ratio bounds.

The experiments could be tested on real CDN, storage, or video request traces.

Additional baselines such as LFU, ARC, or learned eviction policies could be included.

The trust-aware fallback idea could also be applied to scheduling, resource allocation, database buffer management, and cloud storage.

---

## Technical Report

The full technical report is available at:

paper/technical_report.md

---

## Summary

This project shows that prediction-augmented caching can be powerful but fragile. Accurate predictions can move caching behavior closer to Belady, but corrupted or stale predictions can cause severe failures.

Trust-aware fallback provides a simple and effective mechanism for balancing prediction use with LRU robustness.
