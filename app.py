<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Levi: Cuộc Tháo Chạy Khỏi Rừng Titan</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body {
            background-color: #1a1a1a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: #fff;
        }

        #game-container {
            position: relative;
            width: 450px;
            height: 700px;
            background: linear-gradient(#2d3e50, #1b2631);
            overflow: hidden;
            border: 4px solid #4a5568;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }

        /* Giao diện điểm số & Tiến trình */
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            padding: 15px;
            z-index: 10;
            background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent);
        }

        .hud-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .score-box {
            font-size: 20px;
            font-weight: bold;
            color: #f6e05e;
            text-shadow: 2px 2px 4px #000;
        }

        .progress-container {
            width: 100%;
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            padding: 3px;
            border: 1px solid #718096;
        }

        .progress-bar {
            height: 12px;
            width: 0%;
            background: linear-gradient(90deg, #3182ce, #63b3ed);
            border-radius: 8px;
            transition: width 0.1s linear;
        }

        .progress-labels {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #cbd5e0;
            margin-top: 4px;
            font-weight: bold;
        }

        /* Khung cảnh game / Đường chạy */
        #track {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
        }

        .lane-line {
            position: absolute;
            top: 0;
            width: 2px;
            height: 100%;
            background: dashed rgba(255, 255, 255, 0.15);
        }

        .lane-line.left { left: 33.33%; }
        .lane-line.right { left: 66.66%; }

        /* Các Entity trong Game */
        .entity {
            position: absolute;
            transform: translate(-50%, -50%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            border-radius: 8px;
            transition: left 0.1s ease-out;
        }

        /* Levi (Nhân vật chính) */
        #player {
            width: 50px;
            height: 60px;
            background-color: #2b6cb0;
            border: 3px solid #63b3ed;
            color: #fff;
            border-radius: 50% 50% 10px 10px;
            z-index: 5;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }

        /* Titan Đuổi Theo Phía Sau */
        #chaser-titan {
            width: 90px;
            height: 90px;
            background-color: #c53030;
            border: 3px solid #feb2b2;
            color: #fff;
            border-radius: 20px;
            z-index: 4;
            transition: bottom 0.3s ease, left 0.2s ease;
            box-shadow: 0 0 20px rgba(229, 62, 62, 0.6);
            display: flex;
            flex-direction: column;
            font-size: 11px;
            text-align: center;
        }

        /* Chướng ngại vật & Lưỡi kiếm */
        .obstacle-rock {
            width: 55px;
            height: 55px;
            background-color: #4a5568;
            border: 3px solid #a0aec0;
            border-radius: 40%;
            color: #e2e8f0;
            font-size: 12px;
        }

        .obstacle-tree {
            width: 110px;
            height: 35px;
            background-color: #744210;
            border: 2px solid #d69e2e;
            border-radius: 5px;
            color: #fefcbf;
            font-size: 11px;
        }

        .item-blade {
            width: 35px;
            height: 35px;
            background-color: #319795;
            border: 2px solid #81e6d9;
            transform: translate(-50%, -50%) rotate(45deg);
            box-shadow: 0 0 10px #81e6d9;
        }

        /* Màn hình Bắt đầu & Kết thúc */
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.85);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 20;
            padding: 20px;
            text-align: center;
        }

        .overlay h1 {
            font-size: 26px;
            color: #e53e3e;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .overlay p {
            font-size: 14px;
            color: #cbd5e0;
            margin-bottom: 25px;
            line-height: 1.6;
        }

        .btn {
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            background: #e53e3e;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(229, 62, 62, 0.4);
            transition: transform 0.1s, background 0.2s;
        }

        .btn:hover {
            background: #c53030;
            transform: scale(1.05);
        }

        .controls-hint {
            margin-top: 15px;
            font-size: 12px;
            color: #a0aec0;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <!-- UI Layer -->
        <div id="ui-layer">
            <div class="hud-row">
                <div class="score-box" id="score-text">ĐIỂM: 0</div>
            </div>
            <div class="progress-container">
                <div class="progress-bar" id="progress-bar"></div>
            </div>
            <div class="progress-labels">
                <span>🌲 KHU RỪNG</span>
                <span>🏰 BỨC TƯỜNG</span>
            </div>
        </div>

        <!-- Track / Lanes -->
        <div id="track">
            <div class="lane-line left"></div>
            <div class="lane-line right"></div>
        </div>

        <!-- Player (Levi) -->
        <div id="player" class="entity">LEVI</div>

        <!-- Chaser Titan -->
        <div id="chaser-titan" class="entity">
            <span>TITAN</span>
            <span>ĐUỔI THEO</span>
        </div>

        <!-- Start Overlay -->
        <div id="start-overlay" class="overlay">
            <h1>Chạy Trốn Titan</h1>
            <p>
                <b>Nhạc nền Attack on Titan (Akuma no Ko) 🎵</b><br><br>
                Dùng phím <b>Mũi tên Trái / Phải</b> hoặc <b>A / D</b> để chuyển làn.<br><br>
                • Nhặt <b>Lưỡi Kiếm ⚔️</b> để tăng điểm.<br>
                • Tránh <b>Đá 🪨</b> và <b>Cành Cây 🪵</b>.<br>
                • Va vấp sẽ khiến Titan phía sau áp sát và bắt bạn!<br>
                • Chạy về tới <b>Bức Tường</b> an toàn để chiến thắng!
            </p>
            <button class="btn" onclick="startGame()">BẮT ĐẦU CHẠY</button>
            <div class="controls-hint">Hỗ trợ cả vuốt màn hình trên điện thoại</div>
        </div>

        <!-- Game Over Overlay -->
        <div id="gameover-overlay" class="overlay" style="display: none;">
            <h1 id="gameover-title">BẠN ĐÃ THẤT BẠI</h1>
            <p id="gameover-desc">Titan đã bắt được Levi!</p>
            <div class="score-box" id="final-score" style="margin-bottom: 20px;">ĐIỂM: 0</div>
            <button class="btn" onclick="startGame()">CHẠY LẠI</button>
        </div>
    </div>

    <!-- Nhạc nền tích hợp -->
    <audio id="bgm" loop preload="auto">
        <source src="https://assets.mixkit.co/music/preview/mixkit-epic-heroic-cinematic-1145.mp3" type="audio/mpeg">
    </audio>

    <script>
        const container = document.getElementById('game-container');
        const player = document.getElementById('player');
        const chaserTitan = document.getElementById('chaser-titan');
        const scoreText = document.getElementById('score-text');
        const progressBar = document.getElementById('progress-bar');
        const startOverlay = document.getElementById('start-overlay');
        const gameoverOverlay = document.getElementById('gameover-overlay');
        const bgm = document.getElementById('bgm');

        // Tạo hiệu ứng âm thanh hệ thống (Web Audio API)
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playSound(type) {
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            if (type === 'blade') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(600, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.15);
            } else if (type === 'hit') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(150, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.3);
                gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.3);
            }
        }

        const lanePositions = [75, 225, 375];
        const TARGET_DISTANCE = 1000;
        
        let currentLane = 1;
        let score = 0;
        let distanceTraveled = 0;
        let speed = 4;
        let isGaming = false;
        let titanCloser = false;
        let items = [];
        let gameLoopId;
        let spawnTimer;

        // Xử lý điều khiển bàn phím
        document.addEventListener('keydown', (e) => {
            if (!isGaming) return;
            if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && currentLane > 0) {
                currentLane--;
            } else if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && currentLane < 2) {
                currentLane++;
            }
            updatePlayerPosition();
        });

        // Xử lý điều khiển cảm ứng vuốt
        let touchStartX = 0;
        container.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
        });
        container.addEventListener('touchend', (e) => {
            if (!isGaming) return;
            let touchEndX = e.changedTouches[0].clientX;
            let diff = touchEndX - touchStartX;
            if (diff > 30 && currentLane < 2) {
                currentLane++;
            } else if (diff < -30 && currentLane > 0) {
                currentLane--;
            }
            updatePlayerPosition();
        });

        function updatePlayerPosition() {
            player.style.left = lanePositions[currentLane] + 'px';
            chaserTitan.style.left = lanePositions[currentLane] + 'px';
        }

        function startGame() {
            bgm.currentTime = 0;
            bgm.volume = 0.5;
            bgm.play().catch(e => console.log("Trình duyệt yêu cầu tương tác để phát nhạc"));

            currentLane = 1;
            score = 0;
            distanceTraveled = 0;
            titanCloser = false;
            speed = 4.5;
            
            items.forEach(item => item.element.remove());
            items = [];

            startOverlay.style.display = 'none';
            gameoverOverlay.style.display = 'none';
            scoreText.innerText = `ĐIỂM: 0`;
            progressBar.style.width = '0%';
            
            player.style.bottom = '100px';
            chaserTitan.style.bottom = '-120px';
            updatePlayerPosition();

            isGaming = true;
            clearInterval(spawnTimer);
            cancelAnimationFrame(gameLoopId);

            spawnTimer = setInterval(spawnObject, 1200);
            gameLoop();
        }

        function spawnObject() {
            if (!isGaming) return;

            const lane = Math.floor(Math.random() * 3);
            const rand = Math.random();

            let type = 'blade';
            if (rand < 0.5) {
                type = 'rock';
            } else if (rand < 0.75) {
                type = 'tree';
            } else {
                type = 'blade';
            }

            const element = document.createElement('div');
            element.classList.add('entity');

            if (type === 'rock') {
                element.classList.add('obstacle-rock');
                element.innerText = '🪨';
            } else if (type === 'tree') {
                element.classList.add('obstacle-tree');
                element.innerText = '🪵 CÀNH CÂY';
            } else {
                element.classList.add('item-blade');
                element.innerText = '⚔️';
            }

            element.style.left = lanePositions[lane] + 'px';
            element.style.top = '-50px';

            container.appendChild(element);

            items.push({
                element: element,
                lane: lane,
                y: -50,
                type: type
            });
        }

        function gameLoop() {
            if (!isGaming) return;

            distanceTraveled += speed * 0.1;
            let progress = Math.min((distanceTraveled / TARGET_DISTANCE) * 100, 100);
            progressBar.style.width = progress + '%';

            if (distanceTraveled >= TARGET_DISTANCE) {
                endGame(true);
                return;
            }

            for (let i = items.length - 1; i >= 0; i--) {
                let item = items[i];
                item.y += speed;
                item.element.style.top = item.y + 'px';

                const playerY = 600;

                if (item.lane === currentLane && Math.abs(item.y - playerY) < 35) {
                    if (item.type === 'blade') {
                        playSound('blade');
                        score += 100;
                        scoreText.innerText = `ĐIỂM: ${score}`;
                        item.element.remove();
                        items.splice(i, 1);
                        continue;
                    } else {
                        playSound('hit');
                        item.element.remove();
                        items.splice(i, 1);
                        handleObstacleHit();
                        continue;
                    }
                }

                if (item.y > 750) {
                    item.element.remove();
                    items.splice(i, 1);
                }
            }

            gameLoopId = requestAnimationFrame(gameLoop);
        }

        function handleObstacleHit() {
            if (titanCloser) {
                endGame(false);
            } else {
                titanCloser = true;
                chaserTitan.style.bottom = '15px';
                
                setTimeout(() => {
                    if (isGaming && titanCloser) {
                        titanCloser = false;
                        chaserTitan.style.bottom = '-120px';
                    }
                }, 4000);
            }
        }

        function endGame(isWin) {
            isGaming = false;
            clearInterval(spawnTimer);
            cancelAnimationFrame(gameLoopId);
            bgm.pause();

            gameoverOverlay.style.display = 'flex';
            document.getElementById('final-score').innerText = `TỔNG ĐIỂM: ${score}`;

            if (isWin) {
                document.getElementById('gameover-title').innerText = "BẠN ĐÃ THÀNH CÔNG!";
                document.getElementById('gameover-title').style.color = "#48bb78";
                document.getElementById('gameover-desc').innerText = "Levi đã an toàn rút lui vào bên trong Bức Tường!";
            } else {
                document.getElementById('gameover-title').innerText = "BẠN ĐÃ BỊ BẮT!";
                document.getElementById('gameover-title').style.color = "#e53e3e";
                document.getElementById('gameover-desc').innerText = "Lũ Titan đã bắt kịp Levi do vấp phải chướng ngại vật!";
            }
        }
    </script>
</body>
</html>
