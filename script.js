document.addEventListener("DOMContentLoaded", () => {
    // ---- DOM Elements ----
    const boardContainer = document.getElementById('board-container');
    const puzzleGrid = document.getElementById('puzzle-grid');
    const difficultySelect = document.getElementById('difficulty-select');
    const themeSelect = document.getElementById('theme-select');
    const startBtn = document.getElementById('start-btn');
    const shuffleBtn = document.getElementById('shuffle-btn');
    const imageUpload = document.getElementById('image-upload');
    const targetImage = document.getElementById('target-image');
    
    // Stats
    const movesCounter = document.getElementById('moves-counter');
    const timerDisplay = document.getElementById('timer-display');
    const bestScoreDisplay = document.getElementById('best-score');
    const progressText = document.getElementById('progress-text');
    const progressFill = document.getElementById('progress-fill');
    
    // Theme info
    const currentThemeName = document.getElementById('current-theme-name');
    const currentGridSize = document.getElementById('current-grid-size');

    // ---- Game State ----
    let gridSize = parseInt(difficultySelect.value);
    let tiles = [];
    let isPlaying = false;
    let moves = 0;
    let timer = null;
    let secondsElapsed = 0;
    let bestScores = JSON.parse(localStorage.getItem('slidingPuzzleBestScores')) || {};
    let currentImageUrl = targetImage.src;

    const GRID_SIZE_PX = 500; // Fixed visual size of the board

    // Initialize
    initGame();
    updateBestScoreDisplay();

    // ---- Event Listeners ----
    difficultySelect.addEventListener('change', (e) => {
        gridSize = parseInt(e.target.value);
        currentGridSize.innerHTML = `${gridSize} &times; ${gridSize} Grid`;
        initGame();
        updateBestScoreDisplay();
    });

    themeSelect.addEventListener('change', (e) => {
        const val = e.target.value;
        const text = e.target.options[e.target.selectedIndex].text;
        currentThemeName.innerHTML = text;
        
        // Use a placeholder or change image based on selection if not custom
        if(val === 'forest') currentImageUrl = 'assets/forest.png';
        else if(val === 'cyber') currentImageUrl = 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80';
        else if(val === 'space') currentImageUrl = 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80';
        
        targetImage.src = currentImageUrl;
        initGame();
    });

    imageUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                currentImageUrl = event.target.result;
                targetImage.src = currentImageUrl;
                currentThemeName.innerHTML = '✨ Custom Image';
                themeSelect.value = 'forest'; // reset select visual
                initGame();
            };
            reader.readAsDataURL(file);
        }
    });

    startBtn.addEventListener('click', () => {
        if(!isPlaying) {
            startGame();
        } else {
            initGame(); // Reset
            startBtn.innerHTML = '<i class="fa-solid fa-play"></i> START GAME';
            startBtn.classList.remove('secondary-btn');
            startBtn.classList.add('primary-btn');
        }
    });

    shuffleBtn.addEventListener('click', () => {
        if(isPlaying) {
            shuffleBoard();
            moves = 0;
            updateMoves();
        }
    });

    // ---- Core Game Logic ----
    function initGame() {
        stopTimer();
        isPlaying = false;
        moves = 0;
        secondsElapsed = 0;
        updateMoves();
        updateTimerDisplay();
        updateProgress(100); // Solved state visually
        
        startBtn.innerHTML = '<i class="fa-solid fa-play"></i> START GAME';
        startBtn.classList.remove('secondary-btn');
        startBtn.classList.add('primary-btn');

        createBoard();
    }

    function startGame() {
        isPlaying = true;
        moves = 0;
        secondsElapsed = 0;
        updateMoves();
        
        startBtn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> RESET';
        startBtn.classList.remove('primary-btn');
        startBtn.classList.add('secondary-btn');
        
        shuffleBoard();
        startTimer();
    }

    function createBoard() {
        puzzleGrid.innerHTML = '';
        puzzleGrid.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`;
        puzzleGrid.style.gridTemplateRows = `repeat(${gridSize}, 1fr)`;
        
        tiles = [];
        const tileSize = GRID_SIZE_PX / gridSize;
        const totalTiles = gridSize * gridSize;

        for (let i = 0; i < totalTiles; i++) {
            const tile = document.createElement('div');
            tile.classList.add('puzzle-tile');
            
            const isLast = i === totalTiles - 1;
            
            // Calculate exact position based on index
            const row = Math.floor(i / gridSize);
            const col = i % gridSize;
            
            // Positioning for absolute smooth sliding
            tile.style.width = `${tileSize - 4}px`; // accounting for gap visually if using absolute
            tile.style.height = `${tileSize - 4}px`;
            
            // Setup target position mapping
            const tileObj = {
                element: tile,
                correctPos: i,
                currentPos: i,
                isEmpty: isLast
            };

            if (isLast) {
                tile.classList.add('empty');
            } else {
                // Background image mapping
                tile.style.backgroundImage = `url(${currentImageUrl})`;
                
                // Calculate background position
                const bgX = (col * 100) / (gridSize - 1);
                const bgY = (row * 100) / (gridSize - 1);
                tile.style.backgroundPosition = `${bgX}% ${bgY}%`;
                
                // Number hint (optional, but looks cool in cyberpunk)
                // tile.innerText = i + 1;
            }

            // Click event
            tile.addEventListener('click', () => handleTileClick(tileObj));

            puzzleGrid.appendChild(tile);
            tiles.push(tileObj);
        }
        
        renderBoard();
    }

    function renderBoard() {
        const tileSize = GRID_SIZE_PX / gridSize;
        tiles.forEach(tile => {
            const row = Math.floor(tile.currentPos / gridSize);
            const col = tile.currentPos % gridSize;
            // +2px offset for the gap centering
            tile.element.style.transform = `translate(${col * tileSize + 2}px, ${row * tileSize + 2}px)`;
        });
        
        // Calculate progress
        if(isPlaying) {
            let correctCount = 0;
            tiles.forEach(t => {
                if(t.currentPos === t.correctPos) correctCount++;
            });
            const percent = Math.floor((correctCount / tiles.length) * 100);
            updateProgress(percent);
            
            if(correctCount === tiles.length && moves > 0) {
                handleWin();
            }
        }
    }

    function handleTileClick(tile) {
        if (!isPlaying) return;

        const emptyTile = tiles.find(t => t.isEmpty);
        
        // Check if adjacent
        const tileRow = Math.floor(tile.currentPos / gridSize);
        const tileCol = tile.currentPos % gridSize;
        const emptyRow = Math.floor(emptyTile.currentPos / gridSize);
        const emptyCol = emptyTile.currentPos % gridSize;

        const isAdjacent = Math.abs(tileRow - emptyRow) + Math.abs(tileCol - emptyCol) === 1;

        if (isAdjacent) {
            // Swap
            const tempPos = tile.currentPos;
            tile.currentPos = emptyTile.currentPos;
            emptyTile.currentPos = tempPos;
            
            moves++;
            updateMoves();
            renderBoard();
            playSlideSound();
        }
    }

    function shuffleBoard() {
        // Random moves to ensure solvability
        let emptyTile = tiles.find(t => t.isEmpty);
        let previousMove = null;
        
        const shuffleSteps = gridSize * gridSize * 10;
        
        for (let i = 0; i < shuffleSteps; i++) {
            const emptyRow = Math.floor(emptyTile.currentPos / gridSize);
            const emptyCol = emptyTile.currentPos % gridSize;
            
            const neighbors = [];
            
            tiles.forEach(t => {
                const tRow = Math.floor(t.currentPos / gridSize);
                const tCol = t.currentPos % gridSize;
                if (Math.abs(tRow - emptyRow) + Math.abs(tCol - emptyCol) === 1) {
                    neighbors.push(t);
                }
            });
            
            // Filter out the reverse move to prevent backtracking immediately
            const validNeighbors = neighbors.filter(n => n.currentPos !== previousMove);
            const targetNeighbor = validNeighbors.length > 0 
                ? validNeighbors[Math.floor(Math.random() * validNeighbors.length)] 
                : neighbors[0];
                
            previousMove = emptyTile.currentPos;
            
            // Swap
            const temp = targetNeighbor.currentPos;
            targetNeighbor.currentPos = emptyTile.currentPos;
            emptyTile.currentPos = temp;
        }
        renderBoard();
    }

    // ---- UI Updates & Helpers ----
    function updateMoves() {
        movesCounter.innerText = moves;
    }

    function updateTimerDisplay() {
        const m = Math.floor(secondsElapsed / 60).toString().padStart(2, '0');
        const s = (secondsElapsed % 60).toString().padStart(2, '0');
        timerDisplay.innerText = `${m}:${s}`;
    }

    function startTimer() {
        stopTimer();
        timer = setInterval(() => {
            secondsElapsed++;
            updateTimerDisplay();
        }, 1000);
    }

    function stopTimer() {
        if(timer) {
            clearInterval(timer);
            timer = null;
        }
    }

    function updateProgress(percent) {
        progressText.innerText = `${percent}%`;
        progressFill.style.width = `${percent}%`;
    }

    function updateBestScoreDisplay() {
        const key = `size_${gridSize}`;
        if(bestScores[key]) {
            bestScoreDisplay.innerText = bestScores[key];
        } else {
            bestScoreDisplay.innerText = '-';
        }
    }

    function handleWin() {
        isPlaying = false;
        stopTimer();
        updateProgress(100);
        
        // Restore missing piece visual
        const emptyTile = tiles.find(t => t.isEmpty);
        emptyTile.classList.remove('empty');
        emptyTile.style.backgroundImage = `url(${currentImageUrl})`;
        const row = Math.floor(emptyTile.correctPos / gridSize);
        const col = emptyTile.correctPos % gridSize;
        emptyTile.style.backgroundPosition = `${(col * 100) / (gridSize - 1)}% ${(row * 100) / (gridSize - 1)}%`;

        // Update High Score
        const key = `size_${gridSize}`;
        if(!bestScores[key] || moves < bestScores[key]) {
            bestScores[key] = moves;
            localStorage.setItem('slidingPuzzleBestScores', JSON.stringify(bestScores));
            updateBestScoreDisplay();
        }
        
        // Show Win Overlay
        showWinOverlay();
    }
    
    function playSlideSound() {
        // Minimal synth slide sound (using Web Audio API for a futuristic effect)
        try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            oscillator.type = 'sine';
            oscillator.frequency.setValueAtTime(300, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(150, audioCtx.currentTime + 0.1);
            
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            oscillator.start();
            oscillator.stop(audioCtx.currentTime + 0.1);
        } catch(e) {
            // Ignore if audio fails
        }
    }

    function showWinOverlay() {
        // Create an overlay dynamically
        let overlay = document.querySelector('.win-overlay');
        if(!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'win-overlay';
            overlay.innerHTML = `
                <h2 class="win-title">SYSTEM RESTORED</h2>
                <div class="win-stats">
                    Moves: <span id="win-moves">0</span> | Time: <span id="win-time">00:00</span>
                </div>
                <button class="btn primary-btn glow-hover" onclick="document.querySelector('.win-overlay').classList.remove('active')">
                    CONTINUE
                </button>
            `;
            boardContainer.appendChild(overlay);
        }
        
        document.getElementById('win-moves').innerText = moves;
        document.getElementById('win-time').innerText = timerDisplay.innerText;
        
        setTimeout(() => {
            overlay.classList.add('active');
            createParticles(200); // Burst of particles
        }, 500);
    }

    // ---- Particle System (Background Effects) ----
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let particlesArray = [];
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2;
            this.speedX = Math.random() * 1 - 0.5;
            this.speedY = Math.random() * 1 - 0.5;
            this.color = Math.random() > 0.5 ? 'rgba(181, 43, 255, 0.5)' : 'rgba(0, 240, 255, 0.5)';
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x > canvas.width || this.x < 0) this.speedX = -this.speedX;
            if (this.y > canvas.height || this.y < 0) this.speedY = -this.speedY;
        }
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            
            // Add subtle glow
            ctx.shadowBlur = 10;
            ctx.shadowColor = this.color;
        }
    }

    function initParticles() {
        for (let i = 0; i < 100; i++) {
            particlesArray.push(new Particle());
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
            particlesArray[i].draw();
        }
        requestAnimationFrame(animateParticles);
    }

    function createParticles(amount) {
        for(let i=0; i<amount; i++) {
            particlesArray.push(new Particle());
            if(particlesArray.length > 200) particlesArray.shift();
        }
    }

    initParticles();
    animateParticles();
});
