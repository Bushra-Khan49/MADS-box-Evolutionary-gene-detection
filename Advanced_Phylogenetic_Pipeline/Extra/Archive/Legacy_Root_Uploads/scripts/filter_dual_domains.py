#!/usr/bin/env python3
import sys

def parse_domtbl(file_path):
    ids = set()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) > 0:
                    ids.add(parts[0])
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return ids

def parse_fasta(file_path):
    headers = []
    seqs = []
    with open(file_path, 'r') as f:
        current_seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    seqs.append("".join(current_seq))
                headers.append(line[1:]) # Remove '>'
                current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            seqs.append("".join(current_seq))
    return headers, seqs

def main():
    if len(sys.argv) < 5:
        print("Usage: filter_dual_domains.py <domtbl1> <domtbl2> <input_fasta> <output_fasta>")
        sys.exit(1)

    domtbl1 = sys.argv[1]
    domtbl2 = sys.argv[2]
    input_fasta = sys.argv[3]
    output_fasta = sys.argv[4]

    ids1 = parse_domtbl(domtbl1)
    ids2 = parse_domtbl(domtbl2)

    common_ids = ids1.intersection(ids2)
    print(f"Found {len(ids1)} hits in {domtbl1}")
    print(f"Found {len(ids2)} hits in {domtbl2}")
    print(f"Found {len(common_ids)} common hits.")

    headers, seqs = parse_fasta(input_fasta)
    
    count = 0
    with open(output_fasta, 'w') as out_f:
        for h, s in zip(headers, seqs):
            # FASTA header might be "ID description", we only need the first part
            seq_id = h.split()[0]
            if seq_id in common_ids:
                out_f.write(f">{h}\n{s}\n")
                count += 1

    print(f"Saved {count} sequences to {output_fasta}")

if __name__ == "__main__":
    main()
