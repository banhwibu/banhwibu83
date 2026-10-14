import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AoT: Levi's Wall Escape", page_icon="🏰", layout="centered"
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
    "⚔️ **Cách chơi:** Dùng phím mũi tên `⬅️` `➡️` hoặc bấm các nút phía dưới"
    " để điều khiển Binh trưởng Levi né Đá (🪨) và Cành cây (🪵), nhặt Kiếm"
    " (🗡️) hồi thể lực!"
)

# Giao diện chính game
st.title("🏰 ATTACK ON TITAN: BINH TRƯỞNG LEVI VƯỢT ẢI")
st.write(
    "🏃 Chạy thật nhanh về phía trước, né chướng ngại vật và sinh tồn trước bầy"
    " Titan!"
)

# 2. Khung Game HTML/JS Canvas chuẩn xác không bị lỗi kết thúc sớm
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
            padding: 12px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 10px;
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
        let wallDist = 1000;

        let obstacles = [];
        let items = [];
        let titans = [
            { x: 70, y: 90, emoji: "👹" },
            { x: 220, y: 120, emoji: "👺" },
            { x: 370, y: 100, emoji: "🗿" }
        ];
        let gameActive = true;

        // Sinh chướng ngại vật
        function spawnObstacle() {
            if (!gameActive) return;
            let lane = Math.floor(Math.random() * 3);
            let type = Math.random() < 0.5 ? "🪨" : "🪵";
            obstacles.push({ lane: lane, y: -40, type: type });
        }

        // Sinh vật phẩm kiếm
        function spawnItem() {
            if (!gameActive) return;
            let lane = Math.floor(Math.random() * 3);
            items.push({ lane: lane, y: -40 });
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

            wallDist -= 0.4;
            stamina -= 0.03;

            // Hiệu ứng bầy Titan nhấp nhô đuổi theo
            titans.forEach(t => {
                t.y += Math.sin(Date.now() / 200) * 0.3;
            });

            // Di chuyển chướng ngại vật
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].y += 2.5;
                // Va chạm
                if (obstacles[i].y > 310 && obstacles[i].y < 360 && obstacles[i].lane === playerLane) {
                    stamina -= 25;
                    obstacles.splice(i, 1);
                } else if (obstacles[i].y > 400) {
                    obstacles.splice(i, 1);
                    score += 50;
                }
            }

            // Di chuyển vật phẩm
            for (let i = items.length - 1; i >= 0; i--) {
                items[i].y += 2.5;
                if (items[i].y > 310 && items[i].y < 360 && items[i].lane === playerLane) {
                    stamina = Math.min(100, stamina + 30);
                    items.splice(i, 1);
                } else if (items[i].y > 400) {
                    items.splice(i, 1);
                }
            }

            if (stamina <= 0) {
                gameActive = false;
            } else if (wallDist <= 0) {
                gameActive = false;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ làn đường
ctx.strokeStyle = "#555";
            ctx.lineWidth = 2;
            ctx.setLineDash([10, 10]);
            ctx.beginPath();
            ctx.moveTo(150, 0); ctx.lineTo(150, 400);
            ctx.moveTo(300, 0); ctx.lineTo(300, 400);
            ctx.stroke();
            ctx.setLineDash([]);

            // Vẽ Titan phía sau
            ctx.font = "28px sans-serif";
            for (let t of titans) {
                ctx.fillText(t.emoji, t.x, t.y);
            }
            ctx.fillStyle = "#ff4b4b";
            ctx.font = "bold 12px sans-serif";
            ctx.fillText("⚠️ BẦY TITAN ĐANG GẦM GỪ PHÍA SAU!", 110, 70);

            // Vẽ chướng ngại vật
            for (let obs of obstacles) {
                let x = obs.lane * laneWidth + 55;
                ctx.font = "32px sans-serif";
                ctx.fillText(obs.type, x, obs.y);
            }

            // Vẽ vật phẩm kiếm
            for (let item of items) {
                let x = item.lane * laneWidth + 55;
                ctx.font = "32px sans-serif";
                ctx.fillText("🗡️", x, item.y);
            }

            // Vẽ nhân vật Binh trưởng Levi (Sử dụng icon chiến binh áo choàng ngầu)
            let playerX = playerLane * laneWidth + 50;
            ctx.font = "38px sans-serif";
            ctx.fillText("🪖", playerX - 2, 335);
            ctx.font = "24px sans-serif";
            ctx.fillText("🧥", playerX + 2, 355);

            // Bảng HUD thông tin
            ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
            ctx.fillRect(0, 365, 450, 35);
            ctx.fillStyle = "white";
            ctx.font = "14px sans-serif";
            ctx.fillText(`🏆 Điểm: ${Math.floor(score)}`, 20, 387);
            ctx.fillText(`❤️ Thể lực: ${Math.floor(stamina)}%`, 160, 387);
            ctx.fillText(`🏰 Tường: ${Math.floor(wallDist)}m`, 320, 387);

            if (!gameActive) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = stamina <= 0 ? "#ff4b4b" : "#00cc66";
                ctx.font = "bold 22px sans-serif";
                ctx.fillText(stamina <= 0 ? "💀 BẠN ĐÃ BỊ BẦY TITAN TÓM!" : "🎉 VỀ ĐẾN TƯỜNG THÀNH AN TOÀN!", 30, 200);
                ctx.font = "14px sans-serif";
                ctx.fillStyle = "white";
                ctx.fillText("Tải lại trang (F5) để chơi lại!", 130, 240);
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
