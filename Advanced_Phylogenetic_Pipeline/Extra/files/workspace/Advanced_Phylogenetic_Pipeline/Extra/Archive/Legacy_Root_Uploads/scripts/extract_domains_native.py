#!/usr/bin/env python3
import sys

def parse_domtbl(file_path):
    # Map: seq_id -> list of (domain, start, end)
    # domtblout columns (1-based):
    # 1: target name
    # 4: query name (domain name)
    # 18: ali-from (seq space)
    # 19: ali-to (seq space)
    coords = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) >= 19:
                    seq_id = parts[0]
                    domain = parts[3]
                    start = int(parts[17])
                    end = int(parts[18])
                    if seq_id not in coords:
                        coords[seq_id] = []
                    coords[seq_id].append((domain, start, end))
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return coords

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
                headers.append(line[1:])
                current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            seqs.append("".join(current_seq))
    return headers, seqs

def extract_aligned_domain(aligned_seq, start, end):
    # start, end are 1-based indices in the original (ungapped) sequence
    # returns the substring of aligned_seq that corresponds to these positions
    current_pos = 0
    msa_start = -1
    msa_end = -1
    for i, char in enumerate(aligned_seq):
        if char != '-':
            current_pos += 1
        if current_pos == start and msa_start == -1:
            msa_start = i
        if current_pos == end:
            msa_end = i
            break
    if msa_start != -1 and msa_end != -1:
        return aligned_seq[msa_start:msa_end+1]
    return None

def main():
    if len(sys.argv) < 4:
        print("Usage: extract_domains_native.py <msa_fasta> <domtblfile> <output_fasta>")
        sys.exit(1)

    msa_file = sys.argv[1]
    domtbl_file = sys.argv[2]
    out_file = sys.argv[3]

    coords = parse_domtbl(domtbl_file)
    headers, seqs = parse_fasta(msa_file)

    count = 0
    with open(out_file, 'w') as f:
        for h, s in zip(headers, seqs):
            seq_id = h.split()[0]
            if seq_id in coords:
                for domain, start, end in coords[seq_id]:
                    domain_seq = extract_aligned_domain(s, start, end)
                    if domain_seq:
                        f.write(f">{seq_id}_{domain}_{start}_{end}\n{domain_seq}\n")
                        count += 1
    
    print(f"Extracted {count} domain sequences to {out_file}")

if __name__ == "__main__":
    main()
