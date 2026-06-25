# Day 1: Problem Definition

## Project Title

Trust-Aware Learning-Augmented Caching under Unreliable Predictions

## Motivation

Caching is a fundamental online decision-making problem. It appears in CPU caches, CDN systems, cloud storage, database buffer management, and video streaming platforms. A caching algorithm must decide which items to keep in a limited cache before knowing the full future request sequence.

Classical online caching algorithms such as LRU and FIFO do not use predictions. Learning-augmented caching uses predictions about future requests to improve cache performance when predictions are accurate. However, prediction-guided caching can fail when predictions are noisy, shifted, corrupted, or adversarial.

This project studies whether a trust-aware caching algorithm can use predictions when they are reliable while falling back toward a robust classical policy when they are unreliable.

## Problem Setting

Let the request sequence be:

R = (r_1, r_2, ..., r_T)

where each r_t is the item requested at time t.

The cache has capacity:

k

At each time step, the requested item is either already in the cache or not.

## Cache Hit

A cache hit occurs when the requested item is already in the cache.

If r_t is in the cache, the algorithm serves the request without loading a new item.

## Cache Miss

A cache miss occurs when the requested item is not in the cache.

If the cache is not full, the item can be inserted directly.

If the cache is full, the algorithm must evict one cached item before inserting the requested item.

## Cache Miss Ratio

The main empirical metric is cache miss ratio:

miss ratio = number of misses / total number of requests

Lower miss ratio means better caching performance.

## Offline Optimal Benchmark

The offline optimal caching algorithm knows the entire future request sequence.

The classical offline optimal policy is Belady's algorithm:

When the cache is full and an eviction is needed, evict the item whose next future request is farthest away. If an item is never requested again, evict it first.

Belady's algorithm is not an online algorithm because it uses future information. In this project, it is used only as an offline benchmark.

## Online Baselines

This project will compare against two classical online baselines.

### LRU

Least Recently Used evicts the item that was requested least recently.

LRU adapts to recent access patterns and is commonly used in practical caching systems.

### FIFO

First In First Out evicts the item that entered the cache earliest.

FIFO is simple but does not adapt to recency.

## Prediction Model

A prediction estimates future request behavior.

In this project, the main prediction type is next-use prediction:

p_t(i) = predicted next request time of item i after time t

A prediction-guided caching policy can evict the item with the farthest predicted next use.

If predictions are accurate, this can approximate Belady-style behavior.

If predictions are wrong, prediction-guided eviction may remove useful items and increase cache misses.

## Prediction Error

For an item i at time t, prediction error is defined as:

error_t(i) = |true_next_use_t(i) - predicted_next_use_t(i)|

Prediction errors may be:

1. small and random;
2. systematically shifted;
3. corrupted for some items;
4. adversarially chosen to mislead the caching policy.

## Trust-Aware Idea

The trust-aware policy will use a confidence value:

c in [0, 1]

When c is high, the policy relies more on predictions.

When c is low, the policy falls back toward LRU.

The goal is to obtain strong performance under accurate predictions without suffering severe degradation under unreliable predictions.

## Research Question

Can we design a learning-augmented caching algorithm that improves cache performance when predictions are accurate while remaining robust when predictions are noisy, shifted, corrupted, or adversarial?

## Day 1 Output

Day 1 defines the caching problem, the evaluation metric, the offline benchmark, the prediction model, and the trust-aware research direction.

Implemented files:

* src/caching/problem.py
* notes/day1_problem_definition.md
* README.md initial version
