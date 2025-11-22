#!/usr/bin/env python3
"""
PDF Token Calculator

Estimates token counts for PDF files using rough word-based heuristics.
Useful for estimating context window usage for LLM processing.

Usage:
    python calculate-pdf-tokens.py <path_pattern> [<path_pattern2> ...]

Examples:
    python calculate-pdf-tokens.py "scenarios/*.pdf"
    python calculate-pdf-tokens.py "theory/*.pdf" "scenarios/*.pdf"
    python calculate-pdf-tokens.py "**/*.pdf"
"""

import PyPDF2
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
        text: Extracted text from PDF

    Returns:
        Estimated token count
    """
    words = text.split()
    return int(len(words) * 1.3)


def process_pdfs(patterns):
    """
    Process PDF files matching given glob patterns.

    Args:
        patterns: List of glob patterns for PDF files

    Returns:
        List of tuples (filename, token_count, page_count)
    """
    all_files = []
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        all_files.extend(files)

    # Remove duplicates and sort
    all_files = sorted(set(all_files))

    results = []
    for pdf_path in all_files:
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                tokens = count_tokens_rough(text)
                results.append((pdf_path, tokens, len(reader.pages)))
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}", file=sys.stderr)

    return results


def print_results(results):
    """Print formatted results table."""
    if not results:
        print("No PDF files found.")
        return

    print("\n=== PDF Token Counts (Estimated) ===")
    print(f"{'File':<50} {'Pages':>6} {'Tokens':>10}")
    print("-" * 68)

    total_tokens = 0
    total_pages = 0

    for filepath, tokens, pages in results:
        filename = os.path.basename(filepath)
        print(f"{filename:<50} {pages:>6} {tokens:>10,}")
        total_tokens += tokens
        total_pages += pages

    print("-" * 68)
    print(f"{'TOTAL':<50} {total_pages:>6} {total_tokens:>10,}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    patterns = sys.argv[1:]
    results = process_pdfs(patterns)
    print_results(results)
