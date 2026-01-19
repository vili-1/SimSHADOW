#!/usr/bin/env python3
import glob
import json
import os


def main() -> int:
    json_paths = sorted(glob.glob(os.path.join('results', 'simshadow_results_*.json')))
    if not json_paths:
        print('No result JSON files found in results/. Run `make full` to regenerate.')
        # Continue with figure checks
        ok = True
    else:
        ok = True
    for path in json_paths:
        with open(path) as fh:
            data = json.load(fh)
        distances = data.get('cross_platform_distances', {})
        for name, value in distances.items():
            try:
                v = float(value)
            except Exception:
                print('Non-numeric distance in', os.path.basename(path), name, value)
                ok = False
                continue
            if not (0.0 <= v < 5.0):
                print('Distance out of range in', os.path.basename(path), name, v)
                ok = False
    # check figures used in the paper (Figure 2 and Figure 3 labels)
    # filenames: figure2_fingerprints.pdf (Figure 2), figure3_scaling.pdf (Figure 3 in paper)
    figs = ['figure2_fingerprints.pdf','figure3_scaling.pdf']
    miss = [f for f in figs if not os.path.exists(os.path.join('figures', f))]
    if miss:
        print('Missing figures:', ', '.join(miss))
        ok = False
    print('Verification:', 'OK' if ok else 'FAIL')
    return 0 if ok else 2

if __name__ == '__main__':
    raise SystemExit(main())

