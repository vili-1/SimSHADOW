#!/usr/bin/env python3
from Documentation.visualization import FingerprintVisualizer

def main() -> int:
    viz = FingerprintVisualizer()
    viz.generate_figure2_4_combined("figures/figure2_fingerprints.pdf")
    viz.generate_figure5_scaling("figures/figure3_scaling.pdf")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
