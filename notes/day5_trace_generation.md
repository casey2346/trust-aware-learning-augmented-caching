# Day 5: Synthetic Trace Generation

## Goal

Day 5 implements synthetic request trace generators for later caching experiments.

The project now has classical online baselines and an offline optimal benchmark. The next step is to generate request sequences with different workload patterns so that caching policies can be tested under controlled conditions.

## Why Trace Generation Matters

Caching performance depends heavily on the structure of the request sequence.

A policy that performs well on uniform random requests may behave differently on skewed, bursty, or adversarial requests. Therefore, a strong caching project needs multiple workload types rather than a single fixed trace.

The trace generators in this project create controlled request sequences for evaluating LRU, FIFO, Belady, prediction-augmented caching, and trust-aware fallback.

## Trace Types

### 1. Uniform Random Trace

In the uniform trace, each item has approximately equal probability of being requested.

This is a simple baseline workload. It has weak locality and limited popularity skew.

### 2. Zipf Trace

In the Zipf trace, a small number of popular items receive many requests, while many long-tail items are requested rarely.

This is important because many real systems, including CDN, web, storage, and video platforms, often show long-tail popularity patterns.

### 3. Burst Trace

In the burst trace, requests concentrate on a small hot set for a period of time before switching to another hot set.

This models temporary popularity spikes and changing workload phases.

### 4. Video/CDN-Style Trace

The video/CDN-style trace combines:

1. globally popular videos;
2. long-tail video requests;
3. occasional trending bursts.

This connects the project to realistic streaming and content-delivery settings.

### 5. Adversarial Trace

The adversarial trace repeatedly changes the active working set.

It is designed to be difficult for policies that over-trust stale or shifted predictions. This trace will be useful later when testing prediction-augmented and trust-aware caching policies.

## Implementation

Implemented file:

src/caching/trace_generators.py

The file includes:

* generate_uniform_trace
* generate_zipf_trace
* generate_burst_trace
* generate_video_cdn_trace
* generate_adversarial_trace
* summarize_trace

Each generator uses a fixed random seed where appropriate so that experiments are reproducible.

## Experiment

Implemented file:

experiments/day5_trace_examples.py

The experiment generates all five trace types and plots their top-item frequency distributions.

Generated figure:

figures/day5_trace_distributions.png

## Expected Result

The generated figure should show visibly different workload patterns.

Uniform should look relatively flat.

Zipf should show strong popularity skew.

Burst should show concentrated repeated requests.

Video/CDN should show a mixture of hot content, long-tail content, and trending bursts.

Adversarial should show a structured request pattern designed for later robustness tests.

## Research Significance

Day 5 turns the project into a controlled experimental framework.

Instead of testing caching algorithms on one hand-written trace, the project can now evaluate algorithms across multiple workload regimes:

1. random;
2. skewed;
3. bursty;
4. realistic video/CDN-style;
5. adversarial.

This is important for studying robustness under unreliable predictions.

## Core Conclusion

Different request traces expose different caching behaviors.

Synthetic trace generators make it possible to test whether prediction-augmented and trust-aware caching policies are robust across diverse workload patterns.

## Day 5 Output

Completed:

* implemented uniform random trace generation;
* implemented Zipf trace generation;
* implemented burst trace generation;
* implemented video/CDN-style trace generation;
* implemented adversarial trace generation;
* generated a trace-distribution figure;
* documented why different workload types matter for caching research.

Files produced:

* src/caching/trace_generators.py
* experiments/day5_trace_examples.py
* figures/day5_trace_distributions.png
* notes/day5_trace_generation.md
