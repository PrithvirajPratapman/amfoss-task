Draw a Perfect Circle Game
A web-based game that challenges users to draw the most perfect circle possible with their mouse. This project is built from scratch using vanilla HTML, CSS, and JavaScript, inspired by the popular online game from Neal Fun.

Features
Interactive Canvas Drawing: A smooth drawing experience using the HTML Canvas API.

Scoring Algorithm: Your drawing is evaluated for "circularity" based on the variance of the radius from the center.

Center Point Validation: The score is only calculated if your drawn path successfully encloses the central red dot.

Session-Based High Score: Your best score is saved using sessionStorage and displayed until you close the tab.

Difficulty Modes:

Easy: Large center dot, forgiving scoring.

Medium: Standard challenge (default).

Hardcore: Tiny center dot and no visual drawing line for the ultimate test of muscle memory.

Time Bonus: Finish your circle faster to earn extra points!

Audio Feedback: An immersive pencil-drawing sound plays while you draw.

Dark/Light Mode: A theme toggle for comfortable viewing in any lighting.

Responsive Design: The layout is centered and functional on various screen sizes.

Tech Stack
HTML5: For the basic structure and elements of the game.

CSS3: For all styling, layout, and the dark/light mode theme.
--   Vanilla JavaScript: For all game logic, including drawing, event handling, and score calculation.

HTML Canvas API: Used for rendering the drawing path and center dot.

Web Audio API: For integrating the drawing sound effect.

Web Storage API (sessionStorage): For persisting the user's best score during their session.

Code Overview
index.html: Contains the structural markup for the canvas, control buttons, mode selector, and score displays. It also includes the <audio> tag for the sound effect.

style.css: Defines the visual appearance of the game. It uses CSS variables for easy theming (dark/light mode) and Flexbox for layout.

script.js: The core of the project. This file handles:

Setting up the canvas and event listeners (mousedown, mousemove, mouseup).

The drawing logic to capture points and render lines.

The scoring algorithm calculates the average radius and standard deviation of all points from the center.

The point-in-polygon check to ensure the center dot is enclosed.

Managing game state, including difficulty, scores, and theme.
