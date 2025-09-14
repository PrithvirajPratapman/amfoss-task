# Lost Villager's Treasure Map
You've heard whispers of a legendary treasure, its location lost to time and the failing memory of an ancient Villager. This wise, but forgetful, Villager has scattered pieces of their treasure map across various biomes. But these aren't ordinary map fragments; they're "Biome Scans" – cryptic images, each depicting a single, prominent Minecraft block type.

Your mission, should you choose to accept it, is to reassemble this fragmented map using clever image recognition and manipulation techniques. By doing so, you'll uncover the hidden path to the Villager's long-lost treasure!

## Overview
The assets folder contains numerous 128x128 pixel images. Each image showcases a distinct Minecraft block (like Dirt, Oak Log, or even rare Diamond Ore) against a plain background. The filenames are numbered, indicating their sequence in the overall map, alongside the block type (e.g., 001_dirt.png). You'll also find some completely blank images – these act as "teleportation" points, signifying a break in the treasure path.

## Instructions
Your Python script will need to:

* Sort the Biome Scans: Arrange the images in their correct numerical order.
* Identify the Key Block: For each "Biome Scan," use OpenCV to detect the main Minecraft block, calculate its average color, and pinpoint its central coordinates.
* Construct the Treasure Path: Using Pillow, create a larger output image. On this image, you'll:
  * Plot the Blocks: Represent each identified block at its calculated coordinates using its average color.
  * Connect the Biomes: Draw lines between the central coordinates of consecutive blocks in the sequence.
  * Color the Path: The connecting lines should be colored based on the average color of the starting block for that segment.
  * Handle Teleportation: Recognize the blank images as breaks in the path – no lines should be drawn to or from these "teleportation" points.

## What You'll Learn
This project will give you hands-on experience with:

* Image Loading and Manipulation with OpenCV and Pillow.
* Object Detection using various OpenCV techniques (e.g., color thresholding, contour detection).
* Color Analysis and extracting meaningful information from pixel data.
* Geometric Transformations and drawing primitives to construct a new image.
* Algorithmic Thinking to piece together fragmented data.

## Resources
* [OpenCV](https://docs.opencv.org/4.x/index.html)
* [Pillow](https://pillow.readthedocs.io/en/stable/)

Let the Adventure Begin!
Clone this repository, dive into the assets folder, and start crafting your solution. May your code be bug-free and your treasure map clear!
