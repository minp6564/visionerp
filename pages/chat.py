import streamlit as st

st.title("💬 사내 채팅")
import datetime
import os
import pickle

# 파일 저장 경로
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

# 채팅 기록 불러오기
if "chat_history" not in st.session_state:
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            st.session_state.chat_history = pickle.load(f)
    else:
        st.session_state.chat_history = []

if "chat_rooms" not in st.session_state:
    st.session_state.chat_rooms = []

# 타이틀
st.title("💬 사내 채팅")

# 현재 사용자 선택
current_user = st.selectbox("내 이름을 선택하세요:", [u["name"] for u in users])
user_info = next(u for u in users if u["name"] == current_user)

# 모드 선택
chat_mode = st.radio("채팅 모드에서 선택:", ["1:1 채팅", "단체방 (자신 생성)"])

# 채팅 상대/방 설정
if chat_mode == "1:1 채팅":
    receiver_candidates = [u["name"] for u in users if u["name"] != current_user]
    receiver = st.selectbox("채팅할 상대를 선택하세요:", receiver_candidates)
    chat_title = f"📨 {receiver} 님과의 1:1 대화"
    chat_filter = lambda chat: (
        chat.get("mode") == "private" and {chat["sender"], chat["receiver"]} == {current_user, receiver}
    )
else:
    st.markdown("---")
    with st.expander("➕ 새로운 단체방 만들기"):
        new_room_name = st.text_input("채팅방 이름")
        new_room_members = st.multiselect("참가자 선택", [u["name"] for u in users if u["name"] != current_user])
        if st.button("채팅방 생성"):
            if new_room_name.strip() and new_room_members:
                st.session_state.chat_rooms.append({
                    "name": new_room_name.strip(),
                    "members": [current_user] + new_room_members
                })
                st.success(f"'{new_room_name}' 채팅방이 생성되었습니다.")
            else:
                st.warning("방 이름과 참가자를 모두 입력해주세요.")

    my_rooms = [r for r in st.session_state.chat_rooms if current_user in r["members"]]
    if my_rooms:
        selected_room = st.selectbox("입장할 단체방 선택", [r["name"] for r in my_rooms])
        chat_title = f"📢 [{selected_room}] 단체방"
        chat_filter = lambda chat: (
            chat.get("mode") == "custom_group" and chat["room"] == selected_room
        )
    else:
        st.info("➕ 먼저 채팅방을 만들고 입장하세요.")
        st.stop()

# 🪄 채팅창 placeholder 만들기
chat_container = st.empty()

def render_chat():
    with chat_container:
        st.subheader(chat_title)
        for i, chat in enumerate(st.session_state.chat_history):
            if chat_filter(chat):
                with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
                    if chat["message"]:
                        st.markdown(f"**{chat['sender']}**: {chat['message']}")

                    if chat["file_path"]:
                        file_name = os.path.basename(chat["file_path"])
                        with open(chat["file_path"], "rb") as f:
                            st.download_button(
                                label=f"📎 {file_name} 다운로드",
                                data=f,
                                file_name=file_name,
                                key=f"download_{i}_{chat['sender']}_{file_name}"
                            )

                    st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

# 초기 채팅 표시
render_chat()

st.divider()

# 입력창 + 업로더
col1, col2 = st.columns([3, 1])
with col1:
    message = st.text_input("메시지를 입력하세요", key="message_input")
with col2:
    uploaded_file = st.file_uploader("파일", key="file_input", label_visibility="collapsed")

# 전송 버튼
if st.button("전송"):
    saved_file_path = None

    if uploaded_file:
        file_name = uploaded_file.name
        saved_file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(saved_file_path, "wb") as f:
            f.write(uploaded_file.read())

    if message.strip() or saved_file_path:
        new_chat = {
            "sender": current_user,
            "message": message if message.strip() else None,
            "file_path": saved_file_path,
            "timestamp": datetime.datetime.now(),
        }

        if chat_mode == "1:1 채팅":
            new_chat.update({"mode": "private", "receiver": receiver})
        else:
            new_chat.update({"mode": "custom_group", "room": selected_room})

        st.session_state.chat_history.append(new_chat)

        with open(SAVE_FILE, "wb") as f:
            pickle.dump(st.session_state.chat_history, f)

        message = ""  # 입력창 초기화
        render_chat()  # 채팅창만 다시 그림
    else:
        st.warning("메시지나 파일을 입력해주세요.")
