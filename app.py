import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CHẠY HOẶC BỊ BẮT - AoT Escape", page_icon="⚠️", layout="centered"
)

st.title("🎵 🏃‍♂️‍➡️🏃‍♀️‍➡️🏃‍➡️🕺💃CHẠY LẸ LÊN!!!")
st.subheader("Akuma no Ko - Attack on Titan ED 7")

# Thanh phát nhạc chính chủ Streamlit (ổn định tuyệt đối, không lo lỗi trình duyệt)
music_url = "https://actions.google.com/sounds/v1/ambiences/epic_battle.ogg"
st.audio(music_url, format="audio/ogg")

st.sidebar.title("🎮 Hướng dẫn chơi")
st.sidebar.info(
    "1. Bấm thanh phát nhạc bên trên để nghe nhạc.\n2. Chọn cấp độ và bấm Bắt"
    " Đầu.\n3. Dùng nút bấm Trái/Phải hoặc phím A/D để né Đá (🪨) và Cây (🌳).\n4."
    " Nhặt Kiếm (🗡️) để tăng điểm!"
)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { background: #0e1117; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 0; }
        #box { position: relative; width: 450px; height: 400px; margin: 10px auto; }
        canvas { background: linear-gradient(to bottom, #1f2937, #111827); border: 3px solid #ff4b4b; border-radius: 12px; display: block; }
        #menu, #popup { position: absolute; top: 0; left: 0; width: 450px; height: 400px; background: rgba(17, 24, 39, 0.95); border: 3px solid #ff4b4b; border-radius: 12px; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
        #popup { display: none; background: rgba(0, 0, 0, 0.92); }
        h1 { color: #ff4b4b; font-size: 22px; margin: 0 0 5px 0; }
        .s-btn { background: #374151; color: white; border: 2px solid #4b5563; padding: 5px 12px; font-weight: bold; border-radius: 6px; cursor: pointer; margin: 0 3px; }
        .s-btn.active { background: #ff4b4b; border-color: #ff2222; }
        .play-btn, .restart-btn { background: #22c55e; color: white; border: none; padding: 10px 25px; font-size: 15px; font-weight: bold; border-radius: 25px; cursor: pointer; margin-top: 12px; }
        .restart-btn { background: #ff4b4b; }
        .ctrl { margin-top: 10px; display: flex; justify-content: center; gap: 20px; }
        .c-btn { background-color: #ff4b4b; color: white; border: none; padding: 12px 40px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <div id="box">
        <!-- Menu chính -->
        <div id="menu">
            <h1>🏃 CHẠY HOẶC BỊ BẮT</h1>
            <p style="font-size: 12px; color: #d1d5db; margin-bottom: 8px;">Né Đá (🪨) & Cây (🌳). Nhặt Kiếm (🗡️) tăng điểm!</p>
            <div style="margin-bottom: 10px;">
                <div style="font-size: 12px; margin-bottom: 4px; color: #fbbf24; font-weight: bold;">CHỌN CẤP ĐỘ:</div>
<button class="s-btn" onclick="setLevel(2.0, 2500, this)">🐢 Chậm</button>
                <button class="s-btn active" onclick="setLevel(3.6, 1500, this)">🏃 Vừa</button>
                <button class="s-btn" onclick="setLevel(6.5, 750, this)">⚡ Nhanh</button>
            </div>
            <button class="play-btn" onclick="start()">🎮 BẮT ĐẦU CHƠI</button>
        </div>

        <!-- Bảng thông báo khi kết thúc game (Dùng được cho cả điện thoại & máy tính) -->
        <div id="popup">
            <h2 id="popup-title" style="color: #ff4b4b; margin-bottom: 5px;">💀 BẠN ĐÃ BỊ BẮT!</h2>
            <p id="popup-desc" style="font-size: 14px; color: #d1d5db; margin-bottom: 15px;">Bầy titan đã vây kín bạn!</p>
            <button class="restart-btn" onclick="resetGame()">🔄 CHƠI LẠI NGAY</button>
        </div>

        <canvas id="cvs" width="450" height="400"></canvas>
    </div>

    <div class="ctrl">
        <button class="c-btn" onclick="move(-1)">⬅️ Trái</button>
        <button class="c-btn" onclick="move(1)">Phải ➡️</button>
    </div>

    <script>
        const cvs = document.getElementById("cvs"), ctx = cvs.getContext("2d");
        const menu = document.getElementById("menu"), popup = document.getElementById("popup");
        let lane = 1, score = 0, wall = 5000, active = false;
        
        let spd = 3.6;
        let spawnRate = 1500;

        let obs = [], items = [], titans = [{x:70, y:50, e:"👹"}, {x:220, y:40, e:"👺"}, {x:370, y:50, e:"🗿"}];
        let t1, t2;

        function setLevel(speed, rate, btn) {
            spd = speed;
            spawnRate = rate;
            document.querySelectorAll('.s-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }

        function start() {
            menu.style.display = "none";
            popup.style.display = "none";
            active = true; score = 0; wall = 5000; obs = []; items = []; lane = 1;
            
            clearInterval(t1);
            clearInterval(t2);

            t1 = setInterval(() => {
                if(active) {
                    obs.push({
                        l: Math.floor(Math.random() * 3), 
                        y: 70, 
                        t: Math.random() < 0.5 ? "🪨" : "🌳"
                    });
                }
            }, spawnRate);

            t2 = setInterval(() => {
                if(active) {
                    items.push({
                        l: Math.floor(Math.random() * 3),
                        y: 70
                    });
                }
            }, 3000);
        }

        function resetGame() {
            popup.style.display = "none";
            start();
        }

        function move(dir) {
            if(active) lane = Math.max(0, Math.min(2, lane + dir));
        }

        window.addEventListener('keydown', e => {
if(e.key === "ArrowLeft" || e.key === "a") move(-1);
            if(e.key === "ArrowRight" || e.key === "d") move(1);
        });

        function loop() {
            ctx.clearRect(0, 0, 450, 400);
            ctx.strokeStyle = "#444"; ctx.lineWidth = 2; ctx.setLineDash([12,12]);
            ctx.beginPath(); ctx.moveTo(150,60); ctx.lineTo(150,365); ctx.moveTo(300,60); ctx.lineTo(300,365); ctx.stroke(); ctx.setLineDash([]);

            // Titan phía sau
            ctx.fillStyle = "rgba(255, 75, 75, 0.25)"; ctx.fillRect(0,0,450,65);
            ctx.font = "26px sans-serif";
            titans.forEach((t, i) => {
                t.y = 45 + Math.sin(Date.now()/150 + i)*5;
                ctx.fillText(t.e, t.x, t.y + 15);
            });
            ctx.fillStyle = "#ff4b4b"; ctx.font = "bold 11px sans-serif"; ctx.fillText("⚠️ BẦY TITAN ĐANG ĐUỔI SÁT PHÍA SAU!", 110, 22);

            if(active) {
                wall -= (spd * 0.3);

                obs.forEach((o, i) => {
                    o.y += spd;
                    if(o.y > 310 && o.y < 360 && o.l === lane) {
                        active = false; 
                        clearInterval(t1); clearInterval(t2);
                        document.getElementById("popup-title").innerText = "💀 BẠN ĐÃ BỊ BẮT!";
                        document.getElementById("popup-title").style.color = "#ff4b4b";
                        document.getElementById("popup-desc").innerText = "Bầy titan đã vây quanh và bắt bạn đi!";
                        popup.style.display = "flex";
                    } else if(o.y > 400) {
                        obs.splice(i, 1); score += 50;
                    }
                });

                items.forEach((it, i) => {
                    it.y += spd;
                    if(it.y > 310 && it.y < 360 && it.l === lane) {
                        score += 200;
                        items.splice(i, 1);
                    } else if(it.y > 400) {
                        items.splice(i, 1);
                    }
                });

                if(wall <= 0) { 
                    active = false; 
                    clearInterval(t1); clearInterval(t2);
                    document.getElementById("popup-title").innerText = "🎉 VỀ ĐẾN TƯỜNG THÀNH!";
                    document.getElementById("popup-title").style.color = "#22c55e";
                    document.getElementById("popup-desc").innerText = "Bạn đã sống sót và trốn thoát thành công!";
                    popup.style.display = "flex";
                }
            }

            obs.forEach(o => { ctx.font = "32px sans-serif"; ctx.fillText(o.t, o.l * 150 + 55, o.y); });
            items.forEach(it => { ctx.font = "32px sans-serif"; ctx.fillText("🗡️", it.l * 150 + 55, it.y); });

            let px = lane * 150 + 45, py = 345;
ctx.font = "40px sans-serif"; ctx.fillText("🦽", px, py + (active ? Math.sin(Date.now()/100)*3 : 0));

            // HUD
            ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; ctx.fillRect(0, 365, 450, 35);
            ctx.fillStyle = "white"; ctx.font = "14px sans-serif";
            ctx.fillText(`🏆 Điểm: ${Math.floor(score)}`, 15, 387);
            ctx.fillText(`🏰 Tường: ${Math.max(0, Math.floor(wall))}m`, 280, 387);

            requestAnimationFrame(loop);
        }
        loop();
    </script>
</body>
</html>
"""

components.html(game_html, height=520)
