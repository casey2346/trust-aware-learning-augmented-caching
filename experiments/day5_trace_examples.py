"""
Day 5 experiment: visualize synthetic request trace generators.

This experiment generates five types of traces:

1. uniform random trace;
2. Zipf trace;
3. burst trace;
4. video/CDN-style trace;
5. adversarial trace.

The output figure shows the item-frequency distribution of each trace.
This helps verify that the trace generators produce meaningfully different
workload patterns for later caching experiments.

Output:
    figures/day5_trace_distributions.png
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from src.caching.trace_generators import (
    generate_adversarial_trace,
    generate_burst_trace,
    generate_uniform_trace,
    generate_video_cdn_trace,
    generate_zipf_trace,
    summarize_trace,
)


FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)


def top_item_frequencies(requests: list[int], top_k: int = 20) -> tuple[list[int], list[int]]:
    """
    Return the top item IDs and frequencies.

    Args:
        requests: Request sequence.
        top_k: Number of most frequent items to keep.

    Returns:
        Tuple of item IDs and corresponding counts.
    """

    counts = Counter(requests)
    most_common = counts.most_common(top_k)

    item_ids = [item for item, _ in most_common]
    frequencies = [count for _, count in most_common]

    return item_ids, frequencies


def plot_trace_distributions() -> None:
    """
    Generate traces and plot their top-item frequency distributions.
    """

    traces = {
        "Uniform": generate_uniform_trace(
            num_requests=1000,
            num_items=100,
            seed=7,
        ),
        "Zipf": generate_zipf_trace(
            num_requests=1000,
            num_items=100,
            alpha=1.1,
            seed=7,
        ),
        "Burst": generate_burst_trace(
            num_requests=1000,
            num_items=100,
            burst_length=40,
            hot_set_size=6,
            seed=7,
        ),
        "Video/CDN": generate_video_cdn_trace(
            num_requests=1000,
            num_videos=150,
            hot_video_count=12,
            burst_probability=0.18,
            seed=7,
        ),
        "Adversarial": generate_adversarial_trace(
            num_blocks=80,
            cache_size=5,
        ),
    }

    for trace_name, requests in traces.items():
        summary = summarize_trace(requests)
        print(
            f"{trace_name}: "
            f"total_requests={int(summary['total_requests'])}, "
            f"unique_items={int(summary['unique_items'])}, "
            f"repetition_rate={summary['repetition_rate']:.4f}"
        )

    fig, axes = plt.subplots(3, 2, figsize=(11, 9))
    axes = axes.flatten()

    for index, (trace_name, requests) in enumerate(traces.items()):
        item_ids, frequencies = top_item_frequencies(requests, top_k=20)

        axes[index].bar(range(len(item_ids)), frequencies)
        axes[index].set_title(trace_name)
        axes[index].set_xlabel("Top requested items")
        axes[index].set_ylabel("Frequency")
        axes[index].grid(True, alpha=0.25)

    axes[-1].axis("off")

    fig.suptitle("Day 5: Synthetic request trace distributions", fontsize=14)
    fig.tight_layout()

    output_path = FIGURE_DIR / "day5_trace_distributions.png"
    fig.savefig(output_path, dpi=200)
    plt.close(fig)

    print(f"Saved figure to {output_path}")


if __name__ == "__main__":
    plot_trace_distributions()