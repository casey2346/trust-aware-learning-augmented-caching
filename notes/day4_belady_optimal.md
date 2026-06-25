# Day 4: Belady Optimal Offline Benchmark

## Goal

Day 4 implements Belady's optimal offline caching algorithm and compares it with the online baselines LRU and FIFO.

This is an important step because Belady provides the offline optimal lower bound for cache misses. It allows the project to compare online algorithms not only against each other, but also against the best possible caching policy with full future knowledge.

## Belady's Algorithm

Belady's algorithm assumes that the entire future request sequence is known.

When the cache is full and a new item must be inserted, Belady evicts the cached item whose next future request is farthest away.

If a cached item is never requested again, that item is evicted first.

## Why Belady Is Offline

Belady is not an online algorithm because it uses future information.

An online caching algorithm only sees requests as they arrive. It cannot know exactly when cached items will be requested again in the future.

Therefore, Belady is used only as a benchmark, not as a deployable online policy.

## Problem Setting

The input is a request sequence:

R = (r_1, r_2, ..., r_T)

and a cache size:

k

At each request, the algorithm gets either a cache hit or a cache miss.

If the request is a miss and the cache is full, the algorithm must evict one cached item.

## Implementation

The implementation first builds a map from each item to the future positions where it appears.

At each request time t:

1. remove the current request position from the future-position map;
2. if the requested item is already in cache, count a hit;
3. otherwise, count a miss;
4. if the cache is full, evict the item with the farthest next future use;
5. if an item has no future use, treat its next use as infinity and evict it first;
6. insert the requested item.

Implemented file:

src/caching/belady.py

## Experiment

The Day 4 experiment compares:

1. Belady optimal offline caching;
2. LRU online caching;
3. FIFO online caching.

Implemented file:

experiments/day4_belady_optimal.py

Generated figure:

figures/day4_belady_vs_lru_fifo.png

## Expected Result

Belady should have the lowest miss ratio or tie for the lowest miss ratio across cache sizes.

This is because Belady has access to future requests and can make the best eviction decision at each cache miss.

LRU and FIFO are online policies. They do not know the future, so their miss ratios are usually higher.

## Research Significance

Belady gives the offline optimal lower bound for cache misses.

This matters because later prediction-augmented caching algorithms will try to approximate Belady-like behavior using predictions.

If predictions are accurate, prediction-augmented caching may move closer to Belady.

If predictions are unreliable, prediction-augmented caching may perform worse than robust online baselines such as LRU.

Therefore, Belady is the correct benchmark for measuring the value and risk of using predictions.

## Core Conclusion

Belady gives the offline optimal lower bound for cache misses.

It is not an online algorithm, but it is essential for evaluating how close online and prediction-augmented caching policies come to the best possible offline performance.

## Day 4 Output

Completed:

* implemented Belady optimal offline caching;
* tested Belady on a small example request sequence;
* compared Belady, LRU, and FIFO across cache sizes;
* generated a Belady-vs-LRU-vs-FIFO miss-ratio figure;
* documented why Belady is an offline benchmark and not an online policy.

Files produced:

* src/caching/belady.py
* experiments/day4_belady_optimal.py
* figures/day4_belady_vs_lru_fifo.png
* notes/day4_belady_optimal.md
