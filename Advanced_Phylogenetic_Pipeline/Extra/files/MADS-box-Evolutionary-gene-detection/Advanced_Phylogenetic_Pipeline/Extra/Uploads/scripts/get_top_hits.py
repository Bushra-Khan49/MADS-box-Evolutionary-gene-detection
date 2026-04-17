#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: get_top_hits.py <blast_out> <output_txt>")
        sys.exit(1)

    blast_file = sys.argv[1]
    out_file = sys.argv[2]

    # Map: query -> best hit (first line encountered for each query)
    best_hits = {}
    
    try:
        with open(blast_file, 'r') as f:
            for line in f:
                parts = line.split('\t')
                if len(parts) >= 12:
                    query = parts[0]
                    subject = parts[1]
                    evalue = float(parts[10])
                    score = float(parts[11])
                    if query not in best_hits:
                        best_hits[query] = (subject, evalue, score)
    except FileNotFoundError:
        print(f"Error: {blast_file} not found.")

    with open(out_file, 'w') as f:
        f.write("Medicago_Gene_ID\tTop_AT_Hit\tE-value\tBit-score\n")
        for q, (s, e, sc) in sorted(best_hits.items()):
            f.write(f"{q}\t{s}\t{e}\t{sc}\n")

    print(f"Processed {len(best_hits)} unique queries to {out_file}")

if __name__ == "__main__":
    main()
