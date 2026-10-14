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
                Dùng phím <b>Mũi tên Trái / Phải</b> hoặc <b>A / D</b> để chuyển làn đường.<br><br>
                • Nhặt <b>Lưỡi Kiếm ⚔️</b> để tăng điểm.<br>
                • Tránh <b>Đá 🪨</b> và <b>Cành Cây 🪵</b>.<br>
                • Nếu va phải vật cản, Titan phía sau sẽ áp sát!<br>
                • Chạy thoát về <b>Bức Tường</b> trước khi bị bắt!
            </p>
            <button class="btn" onclick="startGame()">BẮT ĐẦU CHẠY</button>
            <div class="controls-hint">Hỗ trợ cả Vuốt Màn Hình trên Điện Thoại</div>
        </div>

        <!-- Game Over Overlay -->
        <div id="gameover-overlay" class="overlay" style="display: none;">
            <h1 id="gameover-title">BẠN ĐÃ THẤT BẠI</h1>
            <p id="gameover-desc">Titan đã bắt được Levi!</p>
            <div class="score-box" id="final-score" style="margin-bottom: 20px;">ĐIỂM: 0</div>
            <button class="btn" onclick="startGame()">CHẠY LẠI</button>
        </div>
    </div>

    <script>
        const container = document.getElementById('game-container');
        const player = document.getElementById('player');
        const chaserTitan = document.getElementById('chaser-titan');
        const scoreText = document.getElementById('score-text');
        const progressBar = document.getElementById('progress-bar');
        const startOverlay = document.getElementById('start-overlay');
        const gameoverOverlay = document.getElementById('gameover-overlay');

        // Thông số cấu hình Game
        const lanePositions = [75, 225, 375]; // Tương ứng 3 làn: Trái (0), Giữa (1), Phải (2)
        const TARGET_DISTANCE = 1000; // Khoảng cách tới Bức Tường
        
        let currentLane = 1; // Mặc định làn giữa
        let score = 0;
        let distanceTraveled = 0;
        let speed = 4;
        let isGaming = false;
        let titanCloser = false; // Trạng thái Titan áp sát
        let items = [];
        let gameLoopId;
        let spawnTimer;

        // Xử lý Phím Bàn phím
        document.addEventListener('keydown', (e) => {
            if (!isGaming) return;
            if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && currentLane > 0) {
                currentLane--;
            } else if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && currentLane < 2) {
                currentLane++;
            }
            updatePlayerPosition();
        });

        // Xử lý vuốt trên Điện thoại
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
            // Titan luôn đuổi theo ở làn của Levi
            chaserTitan.style.left = lanePositions[currentLane] + 'px';
        }

        function startGame() {
            // Reset các chỉ số
            currentLane = 1;
            score = 0;
            distanceTraveled = 0;
            titanCloser = false;
            speed = 4.5;
            
            // Dọn dẹp đồ vật cũ
            items.forEach(item => item.element.remove());
            items = [];

            // Cập nhật giao diện
            startOverlay.style.display = 'none';
            gameoverOverlay.style.display = 'none';
            scoreText.innerText = `ĐIỂM: 0`;
            progressBar.style.width = '0%';
            
            player.style.bottom = '100px';
            chaserTitan.style.bottom = '-120px'; // Titan ở khoảng cách xa ban đầu
            updatePlayerPosition();

            isGaming = true;
            clearInterval(spawnTimer);
            cancelAnimationFrame(gameLoopId);

            // Bắt đầu vòng lặp tạo vật cản
            spawnTimer = setInterval(spawnObject, 1200);
            
            // Vòng lặp cập nhật Game
            gameLoop();
        }

        function spawnObject() {
            if (!isGaming) return;

            const lane = Math.floor(Math.random() * 3);
            const rand = Math.random();

            let type = 'blade';
            if (rand < 0.5) {
                type = 'rock'; // Đá
            } else if (rand < 0.75) {
                type = 'tree'; // Cành cây ngã
            } else {
                type = 'blade'; // Lưỡi kiếm
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

            // Cập nhật quãng đường
            distanceTraveled += speed * 0.1;
            let progress = Math.min((distanceTraveled / TARGET_DISTANCE) * 100, 100);
            progressBar.style.width = progress + '%';

            // Kiểm tra chiến thắng khi về Bức Tường
            if (distanceTraveled >= TARGET_DISTANCE) {
                endGame(true);
                return;
            }

            // Di chuyển và xử lý va chạm đồ vật
            for (let i = items.length - 1; i >= 0; i--) {
                let item = items[i];
                item.y += speed;
                item.element.style.top = item.y + 'px';

                // Khoảng cách Y của Levi là khoảng 600px (khi bottom = 100px)
                const playerY = 600;

                // Kiểm tra va chạm (cùng làn đường và độ cao)
                if (item.lane === currentLane && Math.abs(item.y - playerY) < 35) {
                    if (item.type === 'blade') {
                        // Nhặt lưỡi kiếm
                        score += 100;
                        scoreText.innerText = `ĐIỂM: ${score}`;
                        item.element.remove();
                        items.splice(i, 1);
                        continue;
                    } else {
                        // Va phải chướng ngại vật
                        item.element.remove();
                        items.splice(i, 1);
                        handleObstacleHit();
                        continue;
                    }
                }

                // Xóa vật thể khi chạy ra khỏi màn hình
                if (item.y > 750) {
                    item.element.remove();
                    items.splice(i, 1);
                }
            }

            gameLoopId = requestAnimationFrame(gameLoop);
        }

        function handleObstacleHit() {
            if (titanCloser) {
                // Đã bị áp sát mà va chạm tiếp -> Titan bắt thành công
                endGame(false);
            } else {
                // Titan tiến sát lại gần phía sau Levi
                titanCloser = true;
                chaserTitan.style.bottom = '15px'; // Titan áp sát ngay sau lưng
                
                // Tự động lùi Titan ra xa sau 4 giây nếu giữ an toàn
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
