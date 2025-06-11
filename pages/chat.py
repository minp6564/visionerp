import streamlit as st
import datetime
import os
import pickle
import uuid

# 📁 파일 저장 경로
UPLOAD_DIR = "data/uploads"
SAVE_FILE = "data/chat_history.pkl"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 사용자 목록
users = [
    {"name": "김대리", "department": "물류팀"},
    {"name": "이사원", "department": "물류팀"},
    {"name": "박과장", "department": "회계팀"},
    {"name": "정부장", "department": "영업팀"},
]

# 채팅 기록 복원
if "chat_history" not in st.session_state:
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            st.session_state.chat_history = pickle.load(f)
    else:
        st.session_state.chat_history = []

if "chat_rooms" not in st.session_state:
    st.session_state.chat_rooms = []

st.title("💬 사내 채팅")

# 사용자 선택
if "current_user" not in st.session_state:
    st.session_state.current_user = users[0]["name"]
st.session_state.current_user = st.selectbox(
    "내 이름을 선택하세요:",
    [u["name"] for u in users],
    index=[u["name"] for u in users].index(st.session_state.current_user),
    key="user_select"
)
current_user = st.session_state.current_user

# 채팅 모드
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "1:1 채팅"
st.session_state.chat_mode = st.radio(
    "채팅 모드", ["1:1 채팅", "단체방 (자신 생성)"],
    index=["1:1 채팅", "단체방 (자신 생성)"].index(st.session_state.chat_mode)
)
chat_mode = st.session_state.chat_mode

# 1:1 또는 단체방 선택
if chat_mode == "1:1 채팅":
    receiver_candidates = [u["name"] for u in users if u["name"] != current_user]
    if "receiver" not in st.session_state:
        st.session_state.receiver = receiver_candidates[0]
    st.session_state.receiver = st.selectbox("채팅할 상대:", receiver_candidates)
    receiver = st.session_state.receiver
    chat_title = f"📨 {receiver} 님과의 1:1 대화"
    chat_pair = frozenset([current_user, receiver])
    chat_filter = lambda chat: (
        chat.get("mode") == "private" and chat.get("pair") == chat_pair
    )
else:
    with st.expander("➕ 단체방 만들기"):
        new_room_name = st.text_input("채팅방 이름", key="room_name_input")
        new_room_members = st.multiselect("참가자 선택", [u["name"] for u in users if u["name"] != current_user])
        if st.button("채팅방 생성"):
            if new_room_name.strip() and new_room_members:
                st.session_state.chat_rooms.append({
                    "name": new_room_name.strip(),
                    "members": [current_user] + new_room_members
                })
                st.success(f"'{new_room_name}' 채팅방이 생성되었습니다.")
            else:
                st.warning("방 이름과 참가자를 모두 입력하세요.")

    my_rooms = [r for r in st.session_state.chat_rooms if current_user in r["members"]]
    if not my_rooms:
        st.info("➕ 먼저 단체방을 만들고 입장하세요.")
        st.stop()

    if "selected_room" not in st.session_state:
        st.session_state.selected_room = my_rooms[0]["name"]
    st.session_state.selected_room = st.selectbox(
        "입장할 단체방", [r["name"] for r in my_rooms]
    )
    selected_room = st.session_state.selected_room
    chat_title = f"📢 [{selected_room}] 단체방"
    chat_filter = lambda chat: (
        chat.get("mode") == "custom_group" and chat.get("room") == selected_room
    )

# 채팅 표시 함수
chat_container = st.empty()

def render_chat():
    with chat_container:
        st.subheader(chat_title)
        for chat in st.session_state.chat_history:
            if chat_filter(chat):
                with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
                    if chat["message"]:
                        st.markdown(f"**{chat['sender']}**: {chat['message']}")
                    if chat["file_path"] and os.path.exists(chat["file_path"]):
                        file_name = os.path.basename(chat["file_path"])
                        with open(chat["file_path"], "rb") as f:
