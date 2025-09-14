import cv2
import numpy as np
import os
import math

folder = "assets"
tile_size = 64  # Resize tiles to fixed size

# Collect files in order
files = sorted([f for f in os.listdir(folder) if f.endswith(".png")])

tiles = []
for filename in files:
    img = cv2.imread(os.path.join(folder, filename))
    if img is None:
        raise ValueError(f"Missing or corrupted tile: {filename}")
    img = cv2.resize(img, (tile_size, tile_size))
    tiles.append(img)

num_tiles = len(tiles)
cols = int(math.ceil(math.sqrt(num_tiles)))  # Estimate columns
rows = math.ceil(num_tiles / cols)

print(f"Tiles count: {num_tiles}, Grid: {rows}x{cols}")

# Pad missing tiles with blanks so the grid is complete
total_needed = rows * cols
if len(tiles) < total_needed:
    blanks_needed = total_needed - len(tiles)
    blank_tile = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)
    tiles.extend([blank_tile] * blanks_needed)

# Build grid row by row
grid_rows = []
for r in range(rows):
    row_tiles = tiles[r * cols:(r + 1) * cols]
    row_img = np.hstack(row_tiles)
    grid_rows.append(row_img)

# Now all rows have the same width, stack vertically
final_img = np.vstack(grid_rows)

# Show the final full image grid
cv2.imshow("AMFOSS Map", final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
