import sys
from bip_utils import Bip39SeedGenerator, Bip39MnemonicGenerator
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from BIP39Colors import BIP39Colors
from pywavefront import visualization, Wavefront
from pywavefront import Obj

# Get the hex string from command line arguments
if len(sys.argv) != 2 or len(sys.argv[1]) != 64:
    print("Usage: python script.py <64-char hex string>")
    exit(1)

hex_string = sys.argv[1]

# Convert hex string into a BIP39 seed
entropy_bytes = bytes.fromhex(hex_string)
seed_bytes = Bip39SeedGenerator.FromEntropy(entropy_bytes)
seed = Bip39MnemonicGenerator.FromEntropy(entropy_bytes)

# Use BIP39Colors to convert the seed into colors
BIP39Colors.fromSeed(seed)
colors = BIP39Colors.colors

# Create the color wheel
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.set_yticklabels([])
ax.set_xticklabels([])

# Plot each color
theta = np.linspace(0.0, 2 * np.pi, len(colors), endpoint=False)
bars = ax.bar(theta, [1]*len(colors), width=(2*np.pi)/len(colors), bottom=0.0, color=colors)
plt.savefig('color_wheel.png')

# Generate .obj file for color column
obj = Obj()
with open('color_column.obj', 'w') as f:
    for i, color in enumerate(colors):
        obj.vertex((i, 0, 0))
        obj.vertex((i, 1, 0))
        obj.vertex((i, 1, 1))
        obj.vertex((i, 0, 1))
        obj.face([str(j+1) for j in range(i*4, i*4+4)], color)
    f.write(str(obj))

print(f"Color wheel saved to 'color_wheel.png'")
print(f"Color column saved to 'color_column.obj'")
