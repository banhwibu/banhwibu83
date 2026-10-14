import random
import streamlit as st

st.set_page_config(
    page_title="AoT: Wall Escape", page_icon="🏰", layout="centered"
)

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
    "⚔️ **Cách chơi:** Né Đá (🪨) và Cành cây (🪵), nhặt Kiếm (🗡️) hồi thể lực"
    " và chạy về Tường thành (🏰) trước khi bị Titan bắt!"
)

if "game_over" not in st.session_state:
  st.session_state.game_over = False
if "game_win" not in st.session_state:
  st.session_state.game_win = False
if "score" not in st.session_state:
  st.session_state.score = 0
if "stamina" not in st.session_state:
  st.session_state.stamina = 100
if "titan_distance" not in st.session_state:
  st.session_state.titan_distance = 8
if "wall_distance" not in st.session_state:
  st.session_state.wall_distance = 40
if "lane" not in st.session_state:
  st.session_state.lane = 1
if "obstacle_lane" not in st.session_state:
  st.session_state.obstacle_lane = random.randint(0, 2)
if "obstacle_type" not in st.session_state:
  st.session_state.obstacle_type = random.choice(["🪨", "🪵"])
if "item_lane" not in st.session_state:
  st.session_state.item_lane = random.randint(0, 2)

st.title("🏰 ATTACK ON TITAN: CHẠY VỀ BỨC TƯỜNG")
st.write(
    "Né **Đá (🪨)** và **Cành cây (🪵)**, nhặt **Kiếm (🗡️)** và chạy về"
    " **Tường thành** trước khi Titan bắt!"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
  st.metric(label="🏆 Điểm", value=st.session_state.score)
with col2:
  st.metric(label="❤️ Thể lực", value=f"{st.session_state.stamina}%")
with col3:
  st.metric(label="👹 Titan cách", value=f"{st.session_state.titan_distance}m")
with col4:
  st.metric(label="🏰 Còn cách Tường", value=f"{st.session_state.wall_distance}m")

if st.session_state.obstacle_lane == st.session_state.item_lane:
  st.session_state.item_lane = (st.session_state.obstacle_lane + 1) % 3

lane_symbols = ["  🌿  ", "  🌿  ", "  🌿  "]
lane_symbols[st.session_state.obstacle_lane] = (
    f"  {st.session_state.obstacle_type}  "
)
lane_symbols[st.session_state.item_lane] = "  🗡️  "
lane_symbols[st.session_state.lane] = "  🏃💨 "

st.markdown("### 🌲 Đường Mòn Hướng Về Cổng Thành")
st.code(
    f"""
[Làn Trái]    [Làn Giữa]    [Làn Phải]
     {lane_symbols[0]}     {lane_symbols[1]}     {lane_symbols[2]}
    -----------------------------------
                  👹 TITAN ĐANG GẦM GỪ PHÍA SAU!
    """,
    language="text",
)

if st.session_state.game_win:
  st.success("🎉 XUẤT SẮC! Bạn đã chạy vào bên trong Tường thành an toàn!")
  if st.button("🔄 Chơi lại màn mới"):
    st.session_state.game_win = False
    st.session_state.score = 0
    st.session_state.stamina = 100
    st.session_state.titan_distance = 8
    st.session_state.wall_distance = 40
    st.session_state.lane = 1
    st.rerun()
elif st.session_state.game_over:
  st.error("💀 BẠN ĐÃ BỊ TITAN TÓM HOẶC KIỆT SỨC!")
  if st.button("🔄 Thử lại"):
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.stamina = 100
    st.session_state.titan_distance = 8
    st.session_state.wall_distance = 40
    st.session_state.lane = 1
    st.rerun()
else:
  c1, c2, c3 = st.columns(3)


  def run_game(direction):
    if direction == "left" and st.session_state.lane > 0:
      st.session_state.lane -= 1
    elif direction == "right" and st.session_state.lane < 2:
      st.session_state.lane += 1

    st.session_state.stamina -= 5
    st.session_state.wall_distance = max(
        0, st.session_state.wall_distance - 4
    )

    if st.session_state.lane == st.session_state.obstacle_lane:
      st.session_state.titan_distance -= 3
      st.session_state.wall_distance += 3
      st.toast("💥 Bạn vấp chướng ngại vật! Titan áp sát!", icon="⚠️")
    else:
      st.session_state.score += 20
      st.session_state.titan_distance = min(
          10, st.session_state.titan_distance + 1
      )

    if st.session_state.lane == st.session_state.item_lane:
      st.session_state.stamina = min(100, st.session_state.stamina + 30)
      st.toast("✨ Nhặt được Lưỡi kiếm! Phục hồi thể lực.", icon="🗡️")

    st.session_state.obstacle_lane = random.randint(0, 2)
    st.session_state.obstacle_type = random.choice(["🪨", "🪵"])
    st.session_state.item_lane = random.randint(0, 2)

    if st.session_state.wall_distance <= 0:
      st.session_state.game_win = True
    elif (
        st.session_state.titan_distance <= 0
        or st.session_state.stamina <= 0
    ):
      st.session_state.game_over = True


  with c1:
    if st.button("⬅️ Tránh Trái"):
      run_game("left")
      st.rerun()
  with c2:
    if st.button("⬆️ Chạy Thẳng"):
      run_game("straight")
      st.rerun()
  with c3:
    if st.button("➡️ Tránh Phải"):
      run_game("right")
      st.rerun()
