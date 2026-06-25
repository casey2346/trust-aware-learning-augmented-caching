# Day 2: LRU Baseline

## Goal

Day 2 implements the Least Recently Used caching baseline.

LRU is one of the most important classical online caching algorithms. It does not use future information or machine-learned predictions. Instead, it relies only on recency: when the cache is full, it evicts the item that was requested least recently.

## Problem Setting

The input is a request sequence:

R = (r_1, r_2, ..., r_T)

and a cache size:

k

At each request, the algorithm checks whether the requested item is already in the cache.

If the item is in the cache, the request is a cache hit.

If the item is not in the cache, the request is a cache miss. If the cache is already full, one item must be evicted before inserting the requested item.

## LRU Policy

The LRU policy evicts the least recently used cached item.

The intuition is that recently requested items are more likely to be requested again soon. This makes LRU a strong practical baseline for workloads with locality.

## Implementation

The implementation uses an ordered dictionary to maintain cache recency.

When an item is requested:

1. If the item is already in cache, it is a hit and is moved to the most recently used position.
2. If the item is not in cache, it is a miss.
3. If the cache is full, the least recently used item is evicted.
4. The requested item is inserted as the most recently used item.

Implemented file:

src/caching/lru.py

## Experiment

The Day 2 experiment evaluates LRU across different cache sizes.

Implemented file:

experiments/day2_lru_baseline.py

The experiment generates a repeated synthetic request trace and measures cache miss ratio for cache sizes from 1 to 10.

The generated figure is:

figures/day2_lru_cache_size_sweep.png

## Expected Result

As cache size increases, the cache can store more of the working set. Therefore, the miss ratio should generally decrease.

This result confirms that the LRU implementation behaves correctly and provides a meaningful baseline for later experiments.

## Why This Matters

LRU will serve as the main fallback policy in the trust-aware caching algorithm.

The later trust-aware policy will compare prediction-guided eviction against LRU-style fallback. Therefore, a correct and clean LRU implementation is essential before adding prediction-based algorithms.

## Day 2 Output

Completed:

* implemented LRU cache;
* tested LRU on a small example request sequence;
* ran a cache-size sweep experiment;
* generated a figure showing miss ratio versus cache size;
* documented why LRU is the classical robust online baseline.

Files produced:

* src/caching/lru.py
* experiments/day2_lru_baseline.py
* figures/day2_lru_cache_size_sweep.png
* notes/day2_lru_baseline.md
