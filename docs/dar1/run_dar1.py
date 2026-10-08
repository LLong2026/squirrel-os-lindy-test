#!/usr/bin/env python3
"""DAR-1 determinism harness: reduce each sample twice in separate processes,
compare SHA-256, prove byte-identical output."""
import hashlib, subprocess, sys, glob, os

def run(path):
    r = subprocess.run([sys.executable, 'dar1_reducer.py', path],
                       capture_output=True, text=True)
    return r.stdout

print(f"{'sample':<24} {'input_sha256 (first 12)':<18} {'output_sha256 (first 12)':<20} runs1==2")
print('-' * 80)
all_ok = True
rows = []
for f in sorted(glob.glob('tests/*.js')):
    src = open(f, encoding='utf-8').read()
    o1, o2 = run(f), run(f)
    isha = hashlib.sha256(src.encode()).hexdigest()
    os1 = hashlib.sha256(o1.encode()).hexdigest()
    os2 = hashlib.sha256(o2.encode()).hexdigest()
    identical = os1 == os2
    all_ok &= identical
    name = os.path.basename(f)
    print(f"{name:<24} {isha[:12]:<18} {os1[:12]:<20} {'IDENTICAL' if identical else 'DRIFT!'}")
    rows.append((name, isha, os1, identical, o1))

with open('outputs/last_run.txt', 'w', encoding='utf-8') as fh:
    for name, isha, osha, ident, block in rows:
        fh.write(f"===== {name} =====\n")
        fh.write(f"input_sha256:  {isha}\n")
        fh.write(f"output_sha256: {osha}\n")
        fh.write(f"byte-identical across runs: {ident}\n\n")
        fh.write(block + "\n\n")

print()
print("ALL DETERMINISTIC" if all_ok else "DRIFT DETECTED")
sys.exit(0 if all_ok else 1)
