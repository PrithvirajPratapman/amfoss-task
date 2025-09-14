import csv
import cv2
import numpy as np
import os

# --- Configuration ---
CSV_FILE = 'treasure_map.csv'
WINDOW_TITLE = 'AMFOSS Map'
TEXT_TO_DISPLAY = 'amFOSS'

# --- Visual Settings ---
CELL_SIZE = 80  # Increased cell size for better text visibility
GRID_LINE_COLOR = (80, 80, 80)
BACKGROUND_COLOR = (20, 30, 40)
PATH_COLOR = (60, 90, 130)
TEXT_COLOR = (220, 220, 220)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_THICKNESS = 2


def show_map_with_text():
    """
    Reads the CSV grid and displays the map with custom text marking
    the path in an interactive window.
    """
    # --- 1. Check for the required CSV file ---
    if not os.path.exists(CSV_FILE):
        print(f"--- ERROR: '{CSV_FILE}' not found. ---")
        print("Please run the 'solve_map_to_csv.py' script first.")
        return

    # --- 2. Read CSV and create canvas ---
    print(f"Reading grid data from '{CSV_FILE}'...")
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        grid_data = list(reader)

    rows, cols = len(grid_data), len(grid_data[0])
    canvas_height = rows * CELL_SIZE
    canvas_width = cols * CELL_SIZE
    canvas = np.full((canvas_height, canvas_width, 3), BACKGROUND_COLOR, dtype=np.uint8)

    # --- 3. Draw path and the text ---
    print(f"Drawing the treasure path with the text: '{TEXT_TO_DISPLAY}'...")
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is part of the path
            if grid_data[r][c].strip() != '--':
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                
                # Draw the colored rectangle for the path cell
                cv2.rectangle(canvas, (x1, y1), (x2, y2), PATH_COLOR, -1)

                # Calculate text size to perfectly center it
                (text_width, text_height), _ = cv2.getTextSize(TEXT_TO_DISPLAY, FONT, FONT_SCALE, FONT_THICKNESS)
                text_x = x1 + (CELL_SIZE - text_width) // 2
                text_y = y1 + (CELL_SIZE + text_height) // 2
                
                # Draw the "amFOSS" text in the center of the cell
                cv2.putText(canvas, TEXT_TO_DISPLAY, (text_x, text_y), FONT, FONT_SCALE, TEXT_COLOR, FONT_THICKNESS)

    # --- 4. Draw grid lines on top ---
    for i in range(1, cols): # Vertical lines
        cv2.line(canvas, (i * CELL_SIZE, 0), (i * CELL_SIZE, canvas_height), GRID_LINE_COLOR, 1)
    for i in range(1, rows): # Horizontal lines
        cv2.line(canvas, (0, i * CELL_SIZE), (canvas_width, i * CELL_SIZE), GRID_LINE_COLOR, 1)

    # --- 5. Display the final map in a window ---
    print(f"\n--- Quest Complete! Displaying '{WINDOW_TITLE}'. ---")
    print("Press any key to close the window.")
    cv2.imshow(WINDOW_TITLE, canvas)
    
    # Wait until the user presses a key, then clean up
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Window closed.")


if __name__ == "__main__":
    show_map_with_text()
