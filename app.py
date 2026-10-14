import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AoT: Wall Escape 3D Style", page_icon="🏰", layout="centered"
)

# 1. Thanh Sidebar: Tải nhạc nền tùy chỉnh (MP3, WAV, OGG)
st.sidebar.title("🎵 Âm Thanh Trận Chiến")
uploaded_music = st.sidebar.file_uploader(
    "Tải lên bài hát yêu thích của bạn (MP3, WAV, OGG):",
    type=["mp3", "wav", "ogg"],
)
if uploaded_music is not None:
  st.sidebar.audio(uploaded_music, format="audio/mp3", loop=True)
  st.sidebar.success("🎉 Đang phát nhạc tùy chỉnh của bạn!")
else:
  st.sidebar.info("💡 Mẹo: Tải file nhạc `.mp3` của bạn lên ở trên.")
  st.sidebar.markdown("---")
  st.sidebar.write("Hoặc nghe nhạc mặc định:")
  st.sidebar.audio(
      "https://actions.google.com/sounds/v1/ambiences/epic_battle.ogg",
      format="audio/ogg",
      loop=True,
  )

st.sidebar.markdown("---")
st.sidebar.info(
    "⚔️ **Cách chơi:** Dùng phím `⬅️` `➡️` hoặc nút bấm trên màn hình để né Đá"
    " (🪨) và Cành cây (🪵), nhặt Kiếm (🗡️) hồi thể lực và chạy về Tường thành"
    " (🏰) trước khi bị Titan bắt!"
)

# Giao diện chính game
st.title("🏰 ATTACK ON TITAN: CHẠY VỀ BỨC TƯỜNG")
st.write(
    "🎮 **Bản đồ họa chuyển động:** Né chướng ngại vật ngẫu nhiên rơi xuống và"
    " sinh tồn!"
)

# 2. Khung Game HTML/JS Canvas trực quan
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            background-color: #0e1117;
            color: white;
            font-family: sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        canvas {
            background: linear-gradient(to bottom, #2b3e50, #1a252f);
            border: 3px solid #ff4b4b;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(255, 75, 75, 0.4);
            display: block;
            margin: 10px auto;
        }
        .btn-container {
            margin-top: 10px;
        }
        button {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 5px;
            transition: 0.2s;
        }
        button:hover {
            background-color: #ff2222;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="450" height="400"></canvas>
    <div class="btn-container">
        <button onclick="moveLeft()">⬅️ Trái</button>
        <button onclick="moveRight()">Phải ➡️</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let laneWidth = 150;
let playerLane = 1; // 0: Trái, 1: Giữa, 2: Phải
        let score = 0;
        let stamina = 100;
        let titanDist = 80;
        let wallDist = 400;

        let obstacles = [];
        let items = [];
        let gameActive = true;

        // Sinh ngẫu nhiên chướng ngại vật ở các làn
        function spawnObstacle() {
            if (!gameActive) return;
            let lane = Math.floor(Math.random() * 3);
            let type = Math.random() < 0.5 ? "🪨" : "🪵";
            obstacles.push({ lane: lane, y: -50, type: type });
        }

        // Sinh ngẫu nhiên vật phẩm kiếm (🗡️)
        function spawnItem() {
            if (!gameActive) return;
            let lane = Math.floor(Math.random() * 3);
            items.push({ lane: lane, y: -50 });
        }

        setInterval(spawnObstacle, 2000);
        setInterval(spawnItem, 3500);

        function moveLeft() {
            if (playerLane > 0) playerLane--;
        }

        function moveRight() {
            if (playerLane < 2) playerLane++;
        }

        window.addEventListener('keydown', function(e) {
            if (e.key === "ArrowLeft" || e.key === "a") moveLeft();
            if (e.key === "ArrowRight" || e.key === "d") moveRight();
        });

        function update() {
            if (!gameActive) return;

            wallDist -= 1;
            stamina -= 0.05;

            // Di chuyển và kiểm tra chướng ngại vật
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].y += 3;
                if (obstacles[i].y > 320 && obstacles[i].y < 370 && obstacles[i].lane === playerLane) {
                    stamina -= 25;
                    titanDist = Math.max(10, titanDist - 15);
                    obstacles.splice(i, 1);
                } else if (obstacles[i].y > 400) {
                    obstacles.splice(i, 1);
                    score += 50;
                }
            }

            // Di chuyển và kiểm tra vật phẩm hồi thể lực
            for (let i = items.length - 1; i >= 0; i--) {
                items[i].y += 3;
                if (items[i].y > 320 && items[i].y < 370 && items[i].lane === playerLane) {
                    stamina = Math.min(100, stamina + 30);
                    items.splice(i, 1);
                } else if (items[i].y > 400) {
                    items.splice(i, 1);
                }
            }

            if (stamina <= 0 || wallDist <= 0) {
                gameActive = false;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ 3 làn đường
            ctx.strokeStyle = "#555";
            ctx.lineWidth = 2;
            ctx.setLineDash([10, 10]);
            ctx.beginPath();
            ctx.moveTo(150, 0); ctx.lineTo(150, 400);
            ctx.moveTo(300, 0); ctx.lineTo(300, 400);
            ctx.stroke();
            ctx.setLineDash([]);
// Vẽ Titan phía sau
            ctx.fillStyle = "#ff4b4b";
            ctx.font = "24px sans-serif";
            ctx.fillText("👹 TITAN ĐANG Đuổi", 150, 40);

            // Vẽ chướng ngại vật ngẫu nhiên
            for (let obs of obstacles) {
                let x = obs.lane * laneWidth + 50;
                ctx.font = "32px sans-serif";
                ctx.fillText(obs.type, x, obs.y);
            }

            // Vẽ vật phẩm
            for (let item of items) {
                let x = item.lane * laneWidth + 50;
                ctx.font = "32px sans-serif";
                ctx.fillText("🗡️", x, item.y);
            }

            // Vẽ nhân vật người chơi
            let playerX = playerLane * laneWidth + 50;
            ctx.font = "36px sans-serif";
            ctx.fillText("🏃", playerX, 350);

            // Bảng thông tin HUD trên canvas
            ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
            ctx.fillRect(0, 365, 450, 35);
            ctx.fillStyle = "white";
            ctx.font = "14px sans-serif";
            ctx.fillText(`🏆 Điểm: ${Math.floor(score)}`, 20, 387);
            ctx.fillText(`❤️ Thể lực: ${Math.floor(stamina)}%`, 160, 387);
            ctx.fillText(`🏰 Tường: ${wallDist}m`, 320, 387);

            if (!gameActive) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = stamina <= 0 ? "#ff4b4b" : "#00cc66";
                ctx.font = "bold 24px sans-serif";
                ctx.fillText(stamina <= 0 ? "💀 BẠN ĐÃ BỊ TITAN TÓM!" : "🎉 THẮNG RỒI!", 90, 200);
                ctx.font = "16px sans-serif";
                ctx.fillStyle = "white";
                ctx.fillText("Tải lại trang (F5) để chơi lại!", 120, 240);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

components.html(game_html, height=500)
