document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d');
    const resetButton = document.getElementById('reset-button');
    const difficultySelect = document.getElementById('difficulty');
    const themeToggle = document.getElementById('theme-toggle');
    const currentScoreEl = document.getElementById('current-score');
    const bestScoreEl = document.getElementById('best-score');
    const scoreFeedbackEl = document.getElementById('score-feedback');
    const drawingSound = document.getElementById('drawing-sound');

    // Game State
    let isDrawing = false;
    let points = [];
    let bestScore = sessionStorage.getItem('bestCircleScore') || 0;
    let startTime;

    // Game Configuration
    const center = { x: canvas.width / 2, y: canvas.height / 2 };
    const difficultySettings = {
        easy: { dotSize: 10, tolerance: 0.3 },
        medium: { dotSize: 6, tolerance: 0.2 },
        hardcore: { dotSize: 2, tolerance: 0.1 }
    };
    let currentDifficulty = difficultySettings[difficultySelect.value];

    // --- INITIALIZATION ---
    function init() {
        updateBestScoreDisplay();
        resetCanvas();
        setupEventListeners();
        // Set initial theme based on user preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.classList.add('dark-mode');
            themeToggle.textContent = '☀️';
        }
    }

    // --- EVENT LISTENERS ---
    function setupEventListeners() {
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseleave', stopDrawing); // Stop if mouse leaves canvas

        // Touch events for mobile
        canvas.addEventListener('touchstart', (e) => { e.preventDefault(); startDrawing(e.touches[0]); });
        canvas.addEventListener('touchmove', (e) => { e.preventDefault(); draw(e.touches[0]); });
        canvas.addEventListener('touchend', stopDrawing);

        resetButton.addEventListener('click', resetCanvas);
        difficultySelect.addEventListener('change', handleDifficultyChange);
        themeToggle.addEventListener('click', toggleTheme);
    }

    // --- DRAWING LOGIC ---
    function startDrawing(e) {
        if (isDrawing) return;
        isDrawing = true;
        resetCanvas(); // Clear canvas for new drawing
        startTime = Date.now();
        drawingSound.currentTime = 0;
        drawingSound.play();
        
        const { x, y } = getMousePos(e);
        points.push({ x, y });

        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    function draw(e) {
        if (!isDrawing) return;
        
        const { x, y } = getMousePos(e);
        points.push({ x, y });

        // On hardcore mode, don't show the drawing line
        if (difficultySelect.value !== 'hardcore') {
            ctx.lineTo(x, y);
            ctx.strokeStyle = document.body.classList.contains('dark-mode') ? '#fff' : '#000';
            ctx.lineWidth = 3;
            ctx.stroke();
        }
    }

    function stopDrawing() {
        if (!isDrawing) return;
        isDrawing = false;
        drawingSound.pause();
        
        if (points.length > 10) { // Require a minimum number of points
            calculateScore();
        } else {
            resetCanvas(); // Not enough points, just reset
        }
    }

    // --- SCORING ALGORITHM ---
    function calculateScore() {
        if (!isCenterInside(points, center)) {
            showFeedback('The red dot is not inside your circle!');
            currentScoreEl.textContent = '0%';
            return;
        }

        const distances = points.map(p => Math.sqrt((p.x - center.x) ** 2 + (p.y - center.y) ** 2));
        const avgRadius = distances.reduce((sum, d) => sum + d, 0) / distances.length;
        
        // Calculate the variance of the distances from the average radius
        const variance = distances.reduce((sum, d) => sum + (d - avgRadius) ** 2, 0) / distances.length;
        const stdDeviation = Math.sqrt(variance);

        // Roundness score is based on how much the standard deviation varies from the average radius
        const roundness = Math.max(0, 100 * (1 - stdDeviation / avgRadius));
        
        // Time bonus: faster is better
        const duration = (Date.now() - startTime) / 1000; // in seconds
        const timeBonus = Math.max(0, 10 - duration * 2); // Bonus points for finishing under 5s
        
        let finalScore = roundness + timeBonus;

        // Apply difficulty tolerance
        const toleranceFactor = (100 - finalScore) * currentDifficulty.tolerance;
        finalScore = Math.min(100, finalScore + toleranceFactor);

        displayScore(finalScore);
    }

    /**
     * Point-in-Polygon Test (Ray-Casting Algorithm)
     * Checks if the center point is inside the user-drawn path.
     */
    function isCenterInside(path, point) {
        let crossings = 0;
        for (let i = 0, j = path.length - 1; i < path.length; j = i++) {
            const p1 = path[i];
            const p2 = path[j];
            const isBetweenY = (p1.y > point.y) !== (p2.y > point.y);
            if (isBetweenY) {
                const xIntersection = (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x;
                if (xIntersection > point.x) {
                    crossings++;
                }
            }
        }
        return crossings % 2 === 1; // Odd number of crossings means the point is inside
    }

    // --- UI & STATE MANAGEMENT ---
    function displayScore(score) {
        const roundedScore = score.toFixed(2);
        currentScoreEl.textContent = `${roundedScore}%`;
        showFeedback(`${roundedScore}%`);

        if (roundedScore > bestScore) {
            bestScore = roundedScore;
            sessionStorage.setItem('bestCircleScore', bestScore);
            updateBestScoreDisplay();
        }
    }

    function showFeedback(message) {
        scoreFeedbackEl.textContent = message;
        scoreFeedbackEl.classList.add('show');
        setTimeout(() => {
            scoreFeedbackEl.classList.remove('show');
        }, 2000);
    }

    function resetCanvas() {
        points = [];
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawCenterDot();
        currentScoreEl.textContent = '--';
    }

    function drawCenterDot() {
        ctx.beginPath();
        ctx.arc(center.x, center.y, currentDifficulty.dotSize, 0, 2 * Math.PI);
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--dot-color');
        ctx.fill();
    }
    
    function updateBestScoreDisplay() {
        bestScoreEl.textContent = bestScore > 0 ? `${parseFloat(bestScore).toFixed(2)}%` : '--';
    }
    
    function handleDifficultyChange() {
        currentDifficulty = difficultySettings[difficultySelect.value];
        resetCanvas();
    }
    
    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        themeToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
        // Redraw canvas elements to match new theme
        resetCanvas();
    }

    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    // --- START THE GAME ---
    init();
});