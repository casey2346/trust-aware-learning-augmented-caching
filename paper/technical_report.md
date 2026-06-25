# Trust-Aware Learning-Augmented Caching under Unreliable Predictions

## Abstract

Prediction-augmented caching can reduce miss ratios when predictions are accurate, but can degrade under corrupted, shifted, or adversarial predictions. This project studies a confidence-aware fallback mechanism that interpolates between prediction-guided eviction and LRU fallback.

The project implements classical caching baselines, including LRU and FIFO, an offline optimal Belady benchmark, prediction-augmented caching based on predicted next-use time, and a trust-aware caching policy controlled by a confidence value. Experiments are conducted on synthetic request traces, Zipf-distributed traces, video/CDN-style traces, prediction noise sweeps, and adversarial burst sequences.

The results show that prediction-augmented caching can approach Belady-like behavior when predictions are accurate, but can fail badly when predictions are stale or adversarial. Trust-aware caching provides a more stable trade-off by using predictions when confidence is high and falling back toward LRU when confidence is low.

---

## 1. Introduction

Caching is a fundamental online decision-making problem. It appears in CPU caches, CDN systems, cloud storage, database buffer management, and video streaming platforms. A caching algorithm must decide which items to keep in a limited cache before knowing the full future request sequence.

Classical online caching policies such as LRU and FIFO are robust but prediction-free. They do not use machine-learned information about future requests. Learning-augmented caching introduces predictions into the online decision process, with the goal of improving performance when predictions are useful.

However, predictions can be unreliable. A prediction model may be noisy, systematically shifted, corrupted, or stale. In streaming and CDN-style workloads, request hotspots may change suddenly, while predictions may still reflect an old popularity pattern. In such cases, pure prediction-guided caching may evict useful items and suffer high miss ratios.

This project studies trust-aware learning-augmented caching. The main idea is to use predictions when they are reliable, but fall back toward LRU when confidence is low. This creates a controlled trade-off between prediction use and robustness.

---

## 2. Caching Problem Definition

Let the request sequence be:

R = (r_1, r_2, ..., r_T)

where each r_t is the item requested at time t.

The cache has capacity:

k

At each time step, the requested item is either already in the cache or not.

A cache hit occurs when the requested item is already in cache.

A cache miss occurs when the requested item is not in cache. If the cache is full during a miss, the algorithm must evict one cached item before inserting the requested item.

The main empirical metric is cache miss ratio:

miss ratio = number of misses / total number of requests

Lower miss ratio indicates better caching performance.

---

## 3. Algorithms

### 3.1 LRU

Least Recently Used evicts the item that was requested least recently.

LRU uses recency information and is a strong practical online baseline for workloads with temporal locality. It does not use predictions.

### 3.2 FIFO

First In First Out evicts the item that entered the cache earliest.

FIFO is simple, but it does not update item priority after cache hits. It only uses insertion order, not recency.

### 3.3 Belady Offline Optimal

Belady's algorithm is the classical offline optimal caching algorithm.

When the cache is full and an eviction is required, Belady evicts the cached item whose next future request is farthest away. If an item is never requested again, it is evicted first.

Belady is not an online algorithm because it uses future information. In this project, it is used as the offline lower-bound benchmark for cache misses.

### 3.4 Prediction-Augmented Caching

Prediction-augmented caching uses predicted next-use times.

At time t, for each cached item i, the prediction is:

p_t(i) = predicted next request time of item i after time t

On a cache miss, if the cache is full, the algorithm evicts the item with the farthest predicted next use.

If predictions are exact, prediction-augmented caching can approach Belady-style behavior. If predictions are wrong, it may evict useful items and perform worse than LRU.

---

## 4. Trust-Aware Fallback Design

The trust-aware algorithm introduces a confidence value:

c in [0, 1]

The confidence value controls how much the algorithm trusts predictions.

When c = 1, the algorithm fully trusts prediction-guided eviction.

When c = 0, the algorithm falls back to LRU.

When 0 < c < 1, the algorithm interpolates between prediction-guided eviction and LRU fallback.

For each cached item, the algorithm computes:

eviction_score(item) =
c * predicted_next_use_rank(item)
+ (1 - c) * lru_rank(item)

The algorithm evicts the item with the largest eviction score.

The predicted next-use rank gives higher score to items predicted to be needed farther in the future. The LRU rank gives higher score to items used less recently.

This design creates a simple trust-aware mechanism: confidence controls the trade-off between prediction use and LRU fallback.

---

## 5. Theoretical Analysis

### Theorem 1: Consistency

If next-use predictions are accurate and confidence is high, trust-aware caching approaches prediction-augmented caching and can behave similarly to Belady-style eviction.

When c = 1, the trust-aware score becomes the prediction rank. If predictions are exact, this follows the same next-use principle as Belady's algorithm.

When c is close to 1, the LRU term has small weight, so the eviction decision is dominated by the prediction rank.

Thus, under accurate predictions and high confidence, trust-aware caching is consistent with prediction-guided behavior.

### Theorem 2: Robustness

If confidence is low or fallback is active, trust-aware caching is bounded relative to LRU behavior.

When c = 0, the trust-aware score becomes the LRU rank. Therefore, the trust-aware policy is exactly LRU.

When c is small, prediction-based ranking only partially affects the eviction decision. This prevents the algorithm from being fully controlled by unreliable predictions.

Thus, low confidence provides a safe fallback mechanism.

### Theorem 3: Adversarial Separation

There exist corrupted or stale prediction sequences where prediction-augmented caching suffers many misses, while trust-aware caching with low confidence avoids the same degradation.

Consider a burst sequence where the active hot set suddenly changes. Suppose the prediction model remains stale and still trusts the old hot set. Prediction-augmented caching may repeatedly evict the new hot items because it predicts them to be far away.

LRU adapts to the new hot set through recency. Trust-aware caching with low confidence behaves close to LRU and avoids the same miss explosion.

This separates pure prediction-guided caching from trust-aware fallback.

---

## 6. Experiments

The project evaluates caching algorithms across several controlled settings.

### 6.1 Baseline Experiments

The project first implements and evaluates LRU and FIFO. LRU uses recency information, while FIFO only uses insertion order.

### 6.2 Belady Benchmark

Belady optimal offline caching is implemented as a lower-bound benchmark. Experiments compare Belady with LRU and FIFO across cache sizes.

### 6.3 Synthetic Trace Generation

Five trace generators are implemented:

1. uniform random trace;
2. Zipf-distributed trace;
3. burst trace;
4. video/CDN-style trace;
5. adversarial trace.

These traces allow evaluation under different workload patterns.

### 6.4 Prediction Quality

The project defines several prediction models:

1. exact prediction;
2. Gaussian noisy prediction;
3. shifted prediction;
4. corrupted prediction;
5. adversarial prediction.

Prediction error is measured using mean absolute error.

### 6.5 Prediction-Augmented Caching

Prediction-augmented caching is compared against Belady and LRU under exact, noisy, corrupted, and adversarial predictions.

### 6.6 Confidence Ablation

Trust-aware caching is evaluated across confidence values:

c = 0, 0.25, 0.5, 0.75, 1

The experiment shows how confidence controls the transition between LRU fallback and prediction-guided behavior.

### 6.7 Prediction Noise Sweep

Prediction noise is varied from 0% to 100%.

The experiment compares:

* Belady;
* LRU;
* FIFO;
* prediction-augmented caching;
* trust-aware caching with c = 0.25;
* trust-aware caching with c = 0.50;
* trust-aware caching with c = 0.75.

### 6.8 Zipf Distribution Experiment

Zipf-distributed traces are tested with:

alpha = 0.6, 0.8, 1.0, 1.2

and cache sizes:

k = 10, 20, 50

This connects the project to CDN, video, web, and storage workloads with long-tail popularity.

### 6.9 Adversarial Burst Experiment

The adversarial burst experiment creates sudden hot-item shifts while the prediction model remains stale.

The main metric is rolling cache miss ratio over time.

This experiment directly tests whether trust-aware fallback prevents severe miss explosions.

---

## 7. Results

The experiments show several clear patterns.

First, LRU is a stronger practical baseline than FIFO on traces with temporal locality because it uses recency information.

Second, Belady provides the offline lower bound and consistently achieves the lowest or near-lowest miss ratio.

Third, prediction-augmented caching with exact predictions can closely approach Belady. This supports the consistency claim.

Fourth, corrupted or adversarial predictions can make prediction-augmented caching much worse than LRU. This demonstrates the risk of blindly trusting predictions.

Fifth, trust-aware caching provides a controllable middle ground. Low confidence gives behavior close to LRU. High confidence gives behavior close to prediction-guided eviction.

Sixth, the prediction noise sweep shows that prediction-augmented caching degrades as prediction noise increases, while trust-aware caching changes more smoothly.

Seventh, the Zipf experiments show that prediction-aware caching can help under realistic skewed popularity, but robustness still depends on prediction reliability.

Eighth, the adversarial burst experiment shows the strongest evidence for the proposed idea. When request hotspots shift and predictions remain stale, prediction-augmented caching suffers a large miss ratio, while low-confidence trust-aware caching falls back toward LRU and avoids the same failure.

---

## 8. Limitations

This project is a research-style prototype and has several limitations.

First, the confidence value c is manually specified rather than learned from data.

Second, the experiments use synthetic traces rather than real CDN or production request logs.

Third, the theoretical analysis is currently written as proof sketches, not fully formal competitive-ratio proofs.

Fourth, the trust-aware rule uses a simple linear interpolation between prediction rank and LRU rank. Other score functions may produce better trade-offs.

Fifth, the adversarial prediction model is intentionally constructed to expose failure cases. Real prediction failures may be more subtle.

---

## 9. Future Work

Future work includes several directions.

First, confidence could be learned automatically from historical prediction error.

Second, the theoretical analysis could be formalized into precise competitive-ratio bounds.

Third, the method could be tested on real CDN, storage, or video request traces.

Fourth, the trust-aware scoring rule could be extended to randomized caching policies.

Fifth, the method could be compared against additional caching baselines such as LFU, ARC, or learned eviction policies.

Sixth, the same trust-aware fallback idea could be applied to scheduling, resource allocation, database buffer management, and cloud storage systems.

---

## References

[1] A. R. Karlin, M. S. Manasse, L. Rudolph, and D. D. Sleator. Competitive snoopy caching. Algorithmica, 1988.

[2] A. Borodin and R. El-Yaniv. Online Computation and Competitive Analysis. Cambridge University Press, 1998.

[3] T. Lykouris and S. Vassilvitskii. Competitive caching with machine learned advice. International Conference on Machine Learning, 2018.

[4] M. Purohit, Z. Svitkina, and R. Kumar. Improving online algorithms via ML predictions. Advances in Neural Information Processing Systems, 2018.

[5] M. Mitzenmacher. Scheduling with predictions and the price of misprediction. ITCS, 2020.

[6] S. Angelopoulos, C. Dürr, S. Jin, S. Kamali, and M. Renault. Online computation with untrusted advice. ITCS, 2020.

[7] L. A. Belady. A study of replacement algorithms for a virtual-storage computer. IBM Systems Journal, 1966.

[8] G. D. Zipf. Human Behavior and the Principle of Least Effort. Addison-Wesley, 1949.
