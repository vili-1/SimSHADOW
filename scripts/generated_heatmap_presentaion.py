import numpy as np
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt


def plot_results(arr,title,_vmax=2.0,_vmin=-2.0,colour="coolwarm"):
  # 15 observables
  observables = ["XX","XY","XZ","YX","YY","YZ","ZX","ZY","ZZ","XI","IX","YI","IY","ZI","IZ"]
  # 9 states
  states = ["|00⟩","|01⟩","|10⟩","|11⟩","|+0⟩","|-0⟩","|0+⟩","|0-⟩","|Φ⁺⟩"]
  
  fig, ax = plt.subplots(figsize=(6, 3))
  im = ax.imshow(
    arr,
    cmap=colour,
    aspect="auto",
    interpolation="nearest",
    vmin=_vmax,
    vmax=_vmin
  )

  # Axes
  ax.set_xticks(np.arange(len(observables)))
  ax.set_yticks(np.arange(len(states)))
  ax.set_xticklabels(observables, rotation=45, ha="right", fontsize=9)
  ax.set_yticklabels(states, fontsize=10)

  # Labels
  ax.set_xlabel("Observable", fontsize=12)
  ax.set_ylabel("State", fontsize=12)
  ax.set_title(title, fontsize=14, weight='bold')

  # Colorbar
  cbar = fig.colorbar(im, ax=ax)
  cbar.set_label("E_noisy - E_ideal", rotation=270, labelpad=15)

  # Uncomment if you want to see the actual values:
  #fmt="{:.5f}"
  #for i in range(arr.shape[0]):
  #  for j in range(arr.shape[1]):
  #      val = arr[i, j]
  #      ax.text(
  #          j, i,
  #          fmt.format(val),
  #          ha="center",
  #          va="center",
  #          fontsize=7,
  #          color="black"
  #      )

  plt.tight_layout()
  plt.show()

path = 'results/' # Main folder/results
fingerprints = {}
fingerprintstypes = []

for json_filename in glob.glob(os.path.join(path, '*.json')):
  # Fixed JSON file name (from inspection)
  #json_filename = "simshadow_results_20251215_181631.json"
  #id="20251215_181631"
  id = Path(json_filename).stem.replace("simshadow_results_", "", 1)
  with open(json_filename, 'r') as file:
      data = json.load(file)

  # Extract fingerprint_data section
  fingerprint_data = data["fingerprint_data"]
  # Convert each [platform][noise_type] matrix into a numpy array
  for platform, noises in fingerprint_data.items():
      for noise_type, matrix in noises.items():
          key = f"{platform}/{noise_type}/{id}"
          fingerprints[key] = np.array(matrix)
          item = f"{platform}/{noise_type}"
          if item not in fingerprintstypes:
            fingerprintstypes.append(item)

debug = False
if (debug):
  # Just to test
  for key in fingerprintstypes:
    print(key)
  for inner_key, arr in fingerprints.items():
    print(f"{inner_key}: shape={arr.shape}")
    print(arr, "\n")

# --- Group matrices by type ---
grouped = {ftype: [] for ftype in fingerprintstypes}
for key_full, arr in fingerprints.items():
    key_type = "/".join(key_full.split("/")[:2])  # strip the run_id
    grouped[key_type].append(arr)
# --- Compute elementwise mean and std for each type ---
mean_std = {}
for ftype, matrices in grouped.items():
    stack = np.stack(matrices, axis=0)   # shape (N, 9, 15)
    mean_std[ftype] = {
        "mean": np.mean(stack, axis=0),
        "std": np.std(stack, axis=0),
        "n": stack.shape[0]
    }
# --- Get the global min/max to set it for the graphs uniqely
mean_min = min(np.min(stats["mean"]) for stats in mean_std.values())
mean_max = max(np.max(stats["mean"]) for stats in mean_std.values())
if mean_min < 0:
    abs_mean_max = max(mean_max, -mean_min)
else:
    abs_mean_max = max(mean_max, 0.0)

std_min  = min(np.min(stats["std"])  for stats in mean_std.values())
std_max  = max(np.max(stats["std"])  for stats in mean_std.values())
if std_min < 0:
    abs_std_max = max(std_max, -std_min)
else:
    abs_std_max = max(std_max, 0.0)

# --- Display results ---
for ftype, stats in mean_std.items():
    if (debug):
      print(f"\n=== {ftype} === (N={stats['n']})")
      print("Elementwise mean (9x15):")
      print(stats["mean"])
      print("\nElementwise std (9x15):")
      print(stats["std"])
    plot_results(stats["mean"],ftype+": MEAN",abs_mean_max,-abs_mean_max,"twilight_shifted")
    plot_results(stats["std"],ftype+": STDV",abs_std_max*1.008,-abs_std_max*1.008,"PiYG")
