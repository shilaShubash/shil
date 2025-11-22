#!/usr/bin/env python3
"""
Scenario Markdown Token Calculator

Estimates token counts for scenario markdown files using word-based heuristics.
Useful for estimating embedding costs and context window usage.

Usage:
    python calculate-scenario-tokens.py <path_pattern> [<path_pattern2> ...]

Examples:
    python calculate-scenario-tokens.py "scenarios/*.md"
    python calculate-scenario-tokens.py "scenarios/scenario-*.md"
"""

import glob
import os
import sys


def count_tokens_rough(text):
    """
    Rough token estimation based on word count.

    Approximation:
    - English: ~4 chars per token, ~1 token per word
    - Hebrew: ~2 chars per token, ~1.5 tokens per word
    - Mixed content: using 1.3 multiplier as average

    Args:
        text: Text content from markdown file

    Returns:
        Estimated token count
    """
    words = text.split()
    return int(len(words) * 1.3)


def process_markdown_files(patterns):
    """
    Process markdown files matching given glob patterns.

    Args:
        patterns: List of glob patterns for markdown files

    Returns:
        List of tuples (filename, token_count, char_count)
    """
    all_files = []
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        all_files.extend(files)

    # Remove duplicates and sort
    all_files = sorted(set(all_files))

    results = []
    for md_path in all_files:
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                text = f.read()
                tokens = count_tokens_rough(text)
                char_count = len(text)
                results.append((md_path, tokens, char_count))
        except Exception as e:
            print(f"Error processing {md_path}: {e}", file=sys.stderr)

    return results


def print_results(results):
    """Print formatted results table with statistics."""
    if not results:
        print("No markdown files found.")
        return

    print("\n=== Scenario Token Counts (Estimated) ===")
    print(f"{'File':<30} {'Characters':>12} {'Tokens':>10}")
    print("-" * 54)

    total_tokens = 0
    total_chars = 0

    for filepath, tokens, chars in results:
        filename = os.path.basename(filepath)
        print(f"{filename:<30} {chars:>12,} {tokens:>10,}")
        total_tokens += tokens
        total_chars += chars

    print("-" * 54)
    print(f"{'TOTAL':<30} {total_chars:>12,} {total_tokens:>10,}")

    # Calculate statistics
    count = len(results)
    if count > 0:
        avg_tokens = total_tokens / count
        avg_chars = total_chars / count
        min_tokens = min(tokens for _, tokens, _ in results)
        max_tokens = max(tokens for _, tokens, _ in results)

        print()
        print("=== Statistics ===")
        print(f"Number of scenarios: {count}")
        print(f"Average tokens per scenario: {avg_tokens:,.1f}")
        print(f"Average characters per scenario: {avg_chars:,.1f}")
        print(f"Min tokens: {min_tokens:,}")
        print(f"Max tokens: {max_tokens:,}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    patterns = sys.argv[1:]
    results = process_markdown_files(patterns)
    print_results(results)
