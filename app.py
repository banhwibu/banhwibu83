import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CHẠY HOẶC BỊ BẮT - AoT Escape", page_icon="⚠️", layout="centered"
)

# --- PHẦN TRÌNH PHÁT NHẠC AKUMA NO KO & TẢI NHẠC ---
st.title("🎵 Akuma no Ko - Attack on Titan ED 7")
st.subheader("Trình phát nhạc Streamlit")

# Link audio bài hát Akuma no Ko hoặc file tải lên tùy chỉnh
akuma_no_ko_url = "https://archive.org/download/akuma-no-ko-attack-on-titan/Akuma%20no%20Ko.mp3"

uploaded_music = st.sidebar.file_uploader(
    "Tải lên file nhạc MP3/WAV của bạn:", type=["mp3", "wav", "ogg"]
)

if uploaded_music is not None:
  st.sidebar.audio(uploaded_music, format="audio/mp3")
  st.sidebar.success("🎉 Đang phát nhạc bạn tải lên!")
else:
  st.sidebar.info("💡 Đang phát nhạc mặc định Akuma no Ko.")
  st.sidebar.audio(akuma_no_ko_url, format="audio/mp3")

st.sidebar.markdown("---")

# --- PHẦN GAME "CHẠY HOẶC BỊ BẮT" ---
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body { background: #0e1117; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 0; }
        #box { position: relative; width: 450px; height: 400px; margin: 10px auto; }
        canvas { background: linear-gradient(to bottom, #1f2937, #111827); border: 3px solid #ff4b4b; border-radius: 12px; display: block; }
        #menu { position: absolute; top: 0; left: 0; width: 450px; height: 400px; background: rgba(17, 24, 39, 0.96); border: 3px solid #ff4b4b; border-radius: 12px; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
        h1 { color: #ff4b4b; font-size: 26px; margin: 0 0 5px 0; }
        .s-btn { background: #374151; color: white; border: 2px solid #4b5563; padding: 6px 14px; font-weight: bold; border-radius: 8px; cursor: pointer; margin: 0 4px; }
        .s-btn.active { background: #ff4b4b; border-color: #ff2222; }
        .play-btn { background: #22c55e; color: white; border: none; padding: 10px 30px; font-size: 16px; font-weight: bold; border-radius: 30px; cursor: pointer; margin-top: 15px; }
        .ctrl { margin-top: 10px; }
        .c-btn { background-color: #ff4b4b; color: white; border: none; padding: 12px 35px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; margin: 0 10px; }
    </style>
</head>
<body>
    <audio id="music" loop><source src="https://archive.org/download/akuma-no-ko-attack-on-titan/Akuma%20no%20Ko.mp3" type="audio/mpeg"></audio>
    <div id="box">
        <div id="menu">
            <h1>🏃 CHẠY HOẶC BỊ BẮT</h1>
            <p style="font-size: 13px; color: #d1d5db; margin-bottom: 15px;">Né Đá (🪨) & Cây (🌳). Đụng là bị bắt ngay!</p>
            <div style="margin-bottom: 15px;">
                <div style="font-size: 13px; margin-bottom: 6px; color: #fbbf24; font-weight: bold;">TỐC ĐỘ:</div>
<button class="s-btn" onclick="setSpd(2.0, this)">Chậm</button>
                <button class="s-btn active" onclick="setSpd(3.2, this)">Vừa</button>
                <button class="s-btn" onclick="setSpd(4.8, this)">Nhanh</button>
            </div>
            <button class="play-btn" onclick="start()">🎮 BẮT ĐẦU CHƠI</button>
        </div>
        <canvas id="cvs" width="450" height="400"></canvas>
    </div>
    <div class="ctrl">
        <button class="c-btn" onclick="move(-1)">⬅️ Trái</button>
        <button class="c-btn" onclick="move(1)">Phải ➡️</button>
    </div>
    <script>
        const cvs = document.getElementById("cvs"), ctx = cvs.getContext("2d");
        const music = document.getElementById("music"), menu = document.getElementById("menu");
        let lane = 1, score = 0, wall = 5000, spd = 3.2, active = false, caught = false;
        let obs = [], titans = [{x:70, y:50, e:"👹"}, {x:220, y:40, e:"👺"}, {x:370, y:50, e:"🗿"}];
        let t1;

        function setSpd(s, btn) {
            spd = s;
            document.querySelectorAll('.s-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }

        function start() {
            menu.style.display = "none";
            active = true; caught = false; score = 0; wall = 5000; obs = []; lane = 1;
            music.play().catch(e => {});
            clearInterval(t1);
            t1 = setInterval(() => { if(active) obs.push({l: Math.floor(Math.random()*3), y: 70, t: Math.random()<0.5?"🪨":"🌳"}); }, 1800 - spd*120);
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
                wall -= spd * 0.4;
                obs.forEach((o, i) => {
                    o.y += spd;
                    // Đụng đá (🪨) hoặc cây (🌳) là thua và bị bắt ngay lập tức
                    if(o.y > 310 && o.y < 360 && o.l === lane) {
active = false; caught = true; clearInterval(t1);
                    } else if(o.y > 400) {
                        obs.splice(i, 1); score += 50;
                    }
                });
                if(wall <= 0) { active = false; caught = false; clearInterval(t1); }
            }

            obs.forEach(o => { ctx.font = "32px sans-serif"; ctx.fillText(o.t, o.l * 150 + 55, o.y); });

            let px = lane * 150 + 45, py = 345;
            ctx.font = "40px sans-serif"; ctx.fillText("🦽", px, py + (active ? Math.sin(Date.now()/100)*3 : 0));

            // HUD
            ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; ctx.fillRect(0, 365, 450, 35);
            ctx.fillStyle = "white"; ctx.font = "14px sans-serif";
            ctx.fillText(`🏆 Điểm: ${Math.floor(score)}`, 15, 387);
            ctx.fillText(`🏰 Tường: ${Math.max(0, Math.floor(wall))}m`, 280, 387);

            if(!active && menu.style.display === "none") {
                ctx.fillStyle = "rgba(0, 0, 0, 0.88)"; ctx.fillRect(0, 0, 450, 400);
                if(caught) {
                    ctx.font = "38px sans-serif";
                    ctx.fillText("👹", px-45, py-35); ctx.fillText("👺", px+45, py-35);
                    ctx.fillText("🗿", px-50, py+10); ctx.fillText("🧟", px+50, py+10); ctx.fillText("👿", px, py-50);
                    ctx.font = "40px sans-serif"; ctx.fillText("🦽", px, py);
                    ctx.fillStyle = "#ff4b4b"; ctx.font = "bold 22px sans-serif"; ctx.fillText("💀 ĐÃ ĐỤNG VẬT CẢN, BỊ TITAN BẮT!", 30, 160);
                } else {
                    ctx.fillStyle = "#00cc66"; ctx.font = "bold 22px sans-serif"; ctx.fillText("🎉 VỀ ĐẾN TƯỜNG THÀNH AN TOÀN!", 30, 160);
                }
                ctx.font = "14px sans-serif"; ctx.fillStyle = "white"; ctx.fillText("Bấm F5 để chơi lại!", 150, 210);
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
</body>
</html>
"""

components.html(game_html, height=520)
