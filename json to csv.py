#!/usr/bin/env python3
"""
Convert JSON Lines (JSONL) files to CSV format.

Usage:
    python jsonl_to_csv.py input_file.jsonl
    python jsonl_to_csv.py input_file.jsonl -o output_file.csv
    python jsonl_to_csv.py input_file.jsonl --preview 5
"""

import json
import csv
import argparse
from pathlib import Path


def convert_jsonl_to_csv(input_path, output_path=None, preview=0):
    """
    Convert a JSONL file to CSV format.

    Args:
        input_path: Path to the input JSONL file
        output_path: Path for the output CSV file (optional, defaults to input name + .csv)
        preview: Number of rows to preview (0 = no preview, just convert)
    """
    input_path = Path(input_path)

    if output_path is None:
        output_path = input_path.with_suffix(".csv")
    else:
        output_path = Path(output_path)

    # First pass: collect all unique keys (in case records have different fields)
    all_keys = []
    seen_keys = set()
    record_count = 0

    print(f"Reading {input_path}...")

    skipped_lines = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                record_count += 1
                for key in record.keys():
                    if key not in seen_keys:
                        all_keys.append(key)
                        seen_keys.add(key)
            except json.JSONDecodeError:
                skipped_lines.append(line_num)

    print(f"Found {record_count:,} records with {len(all_keys)} columns")
    print(f"Columns: {', '.join(all_keys)}")

    # Second pass: write CSV
    print(f"Writing to {output_path}...")

    rows_written = 0
    preview_rows = []

    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", newline="", encoding="utf-8") as outfile,
    ):
        writer = csv.DictWriter(outfile, fieldnames=all_keys, extrasaction="ignore")
        writer.writeheader()

        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                writer.writerow(record)
                rows_written += 1

                if preview > 0 and len(preview_rows) < preview:
                    preview_rows.append(record)

                if rows_written % 100000 == 0:
                    print(f"  Processed {rows_written:,} rows...")
            except json.JSONDecodeError:
                pass  # Skip malformed lines

    print(f"Done! Wrote {rows_written:,} rows to {output_path}")

    if skipped_lines:
        print(
            f"Warning: Skipped {len(skipped_lines)} malformed line(s): {skipped_lines[:10]}{'...' if len(skipped_lines) > 10 else ''}"
        )

    # Show preview if requested
    if preview > 0 and preview_rows:
        print(f"\nPreview (first {len(preview_rows)} rows):")
        print("-" * 80)
        for i, row in enumerate(preview_rows, 1):
            print(f"Row {i}: {json.dumps(row, indent=2)}")

    return rows_written, all_keys


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON Lines (JSONL) files to CSV format"
    )
    parser.add_argument("input", help="Input JSONL file path")
    parser.add_argument(
        "-o",
        "--output",
        help="Output CSV file path (default: input name with .csv extension)",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=0,
        help="Number of rows to preview after conversion",
    )

    args = parser.parse_args()

    try:
        convert_jsonl_to_csv(args.input, args.output, args.preview)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
