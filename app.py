import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="HÃY CẨN THẬN!! - AoT Escape", page_icon="⚠️", layout="centered"
)

# 1. Thanh Sidebar: Tải nhạc nền tùy chỉnh
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
    "⚔️ **Hướng dẫn sinh tồn:**\n"
    "- Né ngay các viên **Đá (🪨)** và **Cành cây (🪵)** khi chúng rơi xuống!\n"
    "- Nhặt **Kiếm (🗡️)** để hồi thể lực.\n"
    "- Đừng để bầy Titan phía sau tóm được bạn!"
)

# Giao diện chính game
st.title("⚠️ HÃY CẨN THẬN!!")
st.subheader("🏰 BẦY TITAN ĐANG RƯỢT ĐUỔI PHÍA SAU!")
st.write("🏃 Né chướng ngại vật xuất hiện trên đường và sinh tồn đến cùng!")

# 2. Khung Game HTML/JS Canvas với nhân vật 🦽
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
            background: linear-gradient(to bottom, #1f2937, #111827);
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
            padding: 12px 35px;
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
        let wallDist = 5000;

        let obstacles = [];
        let items = [];
        // Bầy Titan ở phía sau (phía trên)
        let titans = [
            { x: 70, y: 50, emoji: "👹" },
            { x: 220, y: 40, emoji: "👺" },
            { x: 370, y: 50, emoji: "🗿" }
        ];
        let gameActive = true;

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

        setInterval(spawnObstacle, 2000);
        setInterval(spawnItem, 4000);

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
            stamina -= 0.03;

            titans.forEach(t => {
                t.y = 45 + Math.sin(Date.now() / 200) * 5;
            });

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].y += 2.8;
                if (obstacles[i].y > 310 && obstacles[i].y < 360 && obstacles[i].lane === playerLane) {
                    stamina -= 25;
                    obstacles.splice(i, 1);
                } else if (obstacles[i].y > 400) {
                    obstacles.splice(i, 1);
                    score += 50;
                }
            }

            for (let i = items.length - 1; i >= 0; i--) {
                items[i].y += 2.8;
                if (items[i].y > 310 && items[i].y < 360 && items[i].lane === playerLane) {
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

            // Vẽ làn đường
            ctx.strokeStyle = "#444";
            ctx.lineWidth = 2;
            ctx.setLineDash([10, 10]);
            ctx.beginPath();
            ctx.moveTo(150, 60); ctx.lineTo(150, 365);
            ctx.moveTo(300, 60); ctx.lineTo(300, 365);
            ctx.stroke();
ctx.setLineDash([]);

            // 1. Vẽ bầy Titan ở phía sau (vùng trên)
            ctx.fillStyle = "rgba(255, 75, 75, 0.2)";
            ctx.fillRect(0, 0, 450, 65);
            ctx.font = "26px sans-serif";
            for (let t of titans) {
                ctx.fillText(t.emoji, t.x, t.y + 15);
            }
            ctx.fillStyle = "#ff4b4b";
            ctx.font = "bold 11px sans-serif";
            ctx.fillText("⚠️ BẦY TITAN ĐANG ĐUỔI SÁT PHÍA SAU!", 110, 25);

            // 2. Vẽ chướng ngại vật (🪨 / 🪵)
            for (let obs of obstacles) {
                let x = obs.lane * laneWidth + 55;
                ctx.font = "32px sans-serif";
                ctx.fillText(obs.type, x, obs.y);
            }

            // 3. Vẽ vật phẩm kiếm (🗡️)
            for (let item of items) {
                let x = item.lane * laneWidth + 55;
                ctx.font = "32px sans-serif";
                ctx.fillText("🗡️", x, item.y);
            }

            // 4. Vẽ nhân vật chính với emoji 🦽 ở phía dưới
            let playerX = playerLane * laneWidth + 45;
            ctx.font = "40px sans-serif";
            ctx.fillText("🦽", playerX, 345);

            // Bảng HUD thông tin
            ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
            ctx.fillRect(0, 365, 450, 35);
            ctx.fillStyle = "white";
            ctx.font = "14px sans-serif";
            ctx.fillText(`🏆 Điểm: ${Math.floor(score)}`, 15, 387);
            ctx.fillText(`❤️ Thể lực: ${Math.floor(stamina)}%`, 155, 387);
            ctx.fillText(`🏰 Tường: ${Math.floor(wallDist)}m`, 315, 387);

            if (!gameActive) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.9)";
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
