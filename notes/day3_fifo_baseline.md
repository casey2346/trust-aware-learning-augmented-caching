# Day 3: FIFO Baseline and Comparison with LRU

## Goal

Day 3 implements the First In First Out caching baseline and compares it with the Least Recently Used baseline from Day 2.

The purpose is to move from a single baseline to a baseline comparison. This makes the project stronger because later prediction-augmented and trust-aware caching algorithms can be evaluated against multiple classical online policies.

## FIFO Policy

FIFO evicts the item that entered the cache earliest.

Unlike LRU, FIFO does not update item priority when an item is requested again. Once an item is inserted, its position in the FIFO order remains fixed until it is evicted.

## LRU vs FIFO

LRU uses recency information.

FIFO only uses insertion order.

This difference matters in request sequences with temporal locality. If recently requested items are likely to appear again soon, LRU can preserve useful items more effectively than FIFO.

## Implementation

The FIFO implementation maintains:

1. a set of cached items for fast membership checks;
2. a queue recording insertion order.

When a request arrives:

1. if the item is already in cache, FIFO counts a hit and does not change the order;
2. if the item is not in cache, FIFO counts a miss;
3. if the cache is full, FIFO evicts the item at the front of the queue;
4. the requested item is inserted at the back of the queue.

Implemented file:

src/caching/fifo.py

## Experiment

The Day 3 experiment compares FIFO and LRU across cache sizes from 1 to 10.

Implemented file:

experiments/day3_fifo_vs_lru.py

The experiment uses a synthetic request trace with temporal locality. Some items appear repeatedly as hot items, while other items appear occasionally. This creates a setting where recency information can be useful.

Generated figure:

figures/day3_fifo_vs_lru.png

## Expected Result

As cache size increases, both FIFO and LRU should generally have lower miss ratios.

LRU is expected to perform at least as well as FIFO in traces with strong temporal locality because it keeps recently requested items. FIFO may evict useful items simply because they entered the cache earlier.

## Research Significance

FIFO provides a second classical online baseline.

Together, LRU and FIFO establish a stronger experimental foundation before adding:

1. Belady optimal offline caching;
2. prediction-augmented caching;
3. confidence-aware caching;
4. trust-aware fallback-to-LRU caching.

This matters because the later trust-aware algorithm will use LRU as a robust fallback, while FIFO shows how a simpler insertion-order baseline behaves without recency adaptation.

## Core Conclusion

LRU uses recency information, while FIFO only uses insertion order.

This makes LRU a more natural robust fallback policy for request sequences with locality.

## Day 3 Output

Completed:

- implemented FIFO caching;
- tested FIFO on a small example request sequence;
- compared FIFO and LRU across cache sizes;
- generated a FIFO-vs-LRU miss-ratio figure;
- documented the difference between recency-based and insertion-order caching.

Files produced:

- src/caching/fifo.py
- experiments/day3_fifo_vs_lru.py
- figures/day3_fifo_vs_lru.png
- notes/day3_fifo_baseline.md