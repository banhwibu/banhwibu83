box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
            transition: 0.2s;
        }
        .start-btn:hover {
            transform: scale(1.08);
            background: linear-gradient(135deg, #16a34a, #15803d);
        }
        .btn-container {
            margin-top: 10px;
        }
        .ctrl-btn {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 12px 35px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            margin: 0 10px;
            transition: 0.2s;
        }
        .ctrl-btn:hover {
            background-color: #ff2222;
            transform: scale(1.05);
        }
    </style>
</head>
<body>

    <!-- Nhạc nền trận chiến -->
    <audio id="bgMusic" loop preload="auto">
        <source src="https://actions.google.com/sounds/v1/ambiences/epic_battle.ogg" type="audio/ogg">
    </audio>

    <div id="game-container">
        <!-- Màn hình Menu Bắt đầu -->
        <div id="menu-screen">
            <h1 class="title">🏃 CHẠY HOẶC BỊ BẮT</h1>
            <p class="subtitle">🏰 BẦY TITAN ĐANG RƯỢT ĐUỔI PHÍA SAU!</p>
            
            <div style="font-size: 13px; color: #9ca3af; margin-bottom: 15px; text-align: left; padding: 0 30px;">
                • <b>Né tránh:</b> Đá (🪨) và Cành cây (🪵)<br>
                • <b>Nhặt:</b> Kiếm (🗡️) để hồi sinh lực<br>
                • <b>Điều khiển:</b> Nút Trái/Phải hoặc Phím mũi tên
            </div>

            <div class="speed-selector">
                <div style="font-size: 14px; margin-bottom: 8px; font-weight: bold; color: #fbbf24;">CHỌN TỐC ĐỘ:</div>
                <button class="speed-btn" onclick="setSpeed('slow', this)">🐢 Chậm</button>
                <button class="speed-btn active" onclick="setSpeed('medium', this)">🏃 Vừa</button>
                <button class="speed-btn" onclick="setSpeed('fast', this)">⚡ Nhanh</button>
            </div>

            <button class="start-btn" onclick="startGame()">🎮 BẮT ĐẦU CHƠI</button>
        </div>

        <canvas id="gameCanvas" width="450" height="400"></canvas>
    </div>

    <div class="btn-container">
        <button class="ctrl-btn" onclick="moveLeft()">⬅️ Trái</button>
        <button class="ctrl-btn" onclick="moveRight()">Phải ➡️</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const bgMusic = document.getElementById("bgMusic");
        const menuScreen = document.getElementById("menu-screen");

        let laneWidth = 150;
        let playerLane = 1;
        let score = 0;
        let stamina = 100;
        let wallDist = 5000;

        let selectedSpeed = 'medium';
        let gameSpeed = 3.2;
        let spawnIntervalObs = 1800;
let spawnIntervalItem = 3500;

        let obstacles = [];
        let items = [];
        let titans = [
            { x: 70, y: 50, emoji: "👹" },
            { x: 220, y: 40, emoji: "👺" },
            { x: 370, y: 50, emoji: "🗿" }
        ];

        let gameActive = false;
        let obsTimer = null;
        let itemTimer = null;

        function setSpeed(speed, btn) {
            selectedSpeed = speed;
            document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            if (speed === 'slow') {
                gameSpeed = 2.0;
                spawnIntervalObs = 2400;
                spawnIntervalItem = 4000;
            } else if (speed === 'medium') {
                gameSpeed = 3.2;
                spawnIntervalObs = 1800;
                spawnIntervalItem = 3500;
            } else if (speed === 'fast') {
                gameSpeed = 4.8;
                spawnIntervalObs = 1300;
                spawnIntervalItem = 3000;
            }
        }

        function startGame() {
            menuScreen.style.display = "none";
            gameActive = true;
            stamina = 100;
            score = 0;
            wallDist = 5000;
            obstacles = [];
            items = [];
            playerLane = 1;

            bgMusic.play().catch(e => console.log("Audio play error:", e));

            if (obsTimer) clearInterval(obsTimer);
            if (itemTimer) clearInterval(itemTimer);

            obsTimer = setInterval(spawnObstacle, spawnIntervalObs);
            itemTimer = setInterval(spawnItem, spawnIntervalItem);
        }

        function spawnObstacle() {
            if (!gameActive) return;
            let lane = Math.floor(Math.random() * 3);
            let type = Math.random() < 0.5 ? "🪨" : "🪵";
            obstacles.push({ lane: lane, y: 70, type: type });
        }

        function spawnItem() {
            if (!gameActive) return;
            let lane = Math.floor(Math.random() * 3);
            items.push({ lane: lane, y: 70 });
        }

        function moveLeft() {
            if (playerLane > 0 && gameActive) playerLane--;
        }

        function moveRight() {
            if (playerLane < 2 && gameActive) playerLane++;
        }

        window.addEventListener('keydown', function(e) {
            if (e.key === "ArrowLeft" || e.key === "a") moveLeft();
            if (e.key === "ArrowRight" || e.key === "d") moveRight();
        });

        function update() {
            if (!gameActive) return;

            wallDist -= (gameSpeed * 0.4);
            stamina -= 0.03;

            titans.forEach(t => {
                t.y = 45 + Math.sin(Date.now() / 150) * 6;
            });

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].y += gameSpeed;
                if (obstacles[i].y > 310 && obstacles[i].y < 360 && obstacles[i].lane === playerLane) {
stamina -= 25;
                    obstacles.splice(i, 1);
                } else if (obstacles[i].y > 400) {
                    obstacles.splice(i, 1);
                    score += 50;
                }
            }

            for (let i = items.length - 1; i >= 0; i--) {
                items[i].y += gameSpeed;
                if (items[i].y > 310 && items[i].y < 360 && items[i].lane === playerLane) {
                    stamina = Math.min(100, stamina + 30);
                    items.splice(i, 1);
                } else if (items[i].y > 400) {
                    items.splice(i, 1);
                }
            }

            if (stamina <= 0 || wallDist <= 0) {
                gameActive = false;
                clearInterval(obsTimer);
                clearInterval(itemTimer);
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.strokeStyle = "#444";
            ctx.lineWidth = 2;
            ctx.setLineDash([12, 12]);
            ctx.beginPath();
            ctx.moveTo(150, 60); ctx.lineTo(150, 365);
            ctx.moveTo(300, 60); ctx.lineTo(300, 365);
            ctx.stroke();
            ctx.setLineDash([]);

            // 1. Bầy Titan đuổi ph
