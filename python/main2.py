import sys
from bip_utils import Bip39SeedGenerator, Bip39MnemonicGenerator
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from BIP39Colors import BIP39Colors
import trimesh

def get_mnemonic_from_hex(hex_value):
    from bip_utils import Bip39MnemonicGenerator
    entropy_bytes = bytes.fromhex(hex_value)
    mnemonic = Bip39MnemonicGenerator.FromEntropy(entropy_bytes)
    return mnemonic

def get_color_wheel_png_and_obj(hex_value, filename_prefix):
    mnemonic = get_mnemonic_from_hex(hex_value)
    colors = BIP39Colors.from_mnemonic(mnemonic)
    # create and save color wheel image
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    theta = np.linspace(0.0, 2 * np.pi, len(colors), endpoint=False)
    bars = ax.bar(theta, [1]*len(colors), width=(2*np.pi)/len(colors), bottom=0.0, color=colors)
    plt.savefig(f"{filename_prefix}_color_wheel.png")

    # create square column segments using trimesh
    meshes = []
    size = 1.0  # size of each block
    for i, color in enumerate(colors):
        vertices = [
            [-size / 2, -size / 2, i * size],
            [size / 2, -size / 2, i * size],
            [size / 2, size / 2, i * size],
            [-size / 2, size / 2, i * size],
            [-size / 2, -size / 2, (i + 1) * size],
            [size / 2, -size / 2, (i + 1) * size],
            [size / 2, size / 2, (i + 1) * size],
            [-size / 2, size / 2, (i + 1) * size],
        ]
        faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 4, 5, 1],
            [2, 6, 7, 3],
            [0, 4, 7, 3],
            [1, 5, 6, 2],
        ]
        vertex_colors = [color] * 8
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_colors=vertex_colors)
        meshes.append(mesh)

    final_mesh = trimesh.util.concatenate(meshes)
    final_mesh.export(f"{filename_prefix}_color_column.obj")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [64 char hex string]")
        exit(1)
    
    hex_value = sys.argv[1]
    get_color_wheel_png_and_obj(hex_value, "output")
