import streamlit as st
import datetime
import os
import pickle
import uuid

# 파일 건설
UPLOAD_DIR = "data/uploads"
SAVE_FILE = "data/chat_history.pkl"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 사운드 사용자 목록 (사번 포함)
users = [
    {"id": "1001", "name": "김대리", "department": "물류팀"},
    {"id": "1002", "name": "이사원", "department": "물류팀"},
    {"id": "1003", "name": "박과장", "department": "회계팀"},
    {"id": "1004", "name": "정부장", "department": "영업팀"},
]

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            st.session_state.chat_history = pickle.load(f)
    else:
        st.session_state.chat_history = []

if "chat_rooms" not in st.session_state:
    st.session_state.chat_rooms = []

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# 로그인 처리
if st.session_state.logged_in_user is None:
    st.title("🔐 사용자 로그인")
    user_id = st.text_input("사번 입력")
    user_name = st.text_input("이름 입력")
    if st.button("로그인"):
        matched = next((u for u in users if u["id"] == user_id and u["name"] == user_name), None)
        if matched:
            st.session_state.logged_in_user = matched
            st.success(f"{matched['name']}님 로그인 완료")
            st.experimental_rerun()
        else:
            st.error("사용자 정보를 확인하세요.")
    st.stop()

user = st.session_state.logged_in_user
current_user = user["name"]

st.title(f"💬 사내 채팅 - {current_user}님")

# 채팅 모드
st.session_state.chat_mode = st.radio("채팅 모드", ["1:1 채팅", "단체방"])
chat_mode = st.session_state.chat_mode

# 대상 설정
if chat_mode == "1:1 채팅":
    receiver_candidates = [u["name"] for u in users if u["name"] != current_user]
    receiver = st.selectbox("채팅할 상대:", receiver_candidates)
    chat_title = f"📨 {receiver} 님과의 1:1 대화"
    chat_filter = lambda c: c.get("mode") == "private" and c.get("pair") == frozenset([current_user, receiver])
else:
    with st.expander("➕ 단체방 만들기"):
        room_name = st.text_input("방 이름")
        room_members = st.multiselect("참가자 선택", [u["name"] for u in users if u["name"] != current_user])
        if st.button("단체방 생성"):
            if room_name and room_members:
                st.session_state.chat_rooms.append({
                    "name": room_name,
                    "members": [current_user] + room_members
                })
                st.success(f"'{room_name}' 단체방 생성 완료")
            else:
                st.warning("방 이름과 참가자를 입력하세요.")

    my_rooms = [r for r in st.session_state.chat_rooms if current_user in r["members"]]
    if not my_rooms:
        st.info("먼저 단체방을 생성하고 입장하세요.")
        st.stop()

    selected_room = st.selectbox("입장할 단체방", [r["name"] for r in my_rooms])
    chat_title = f"📢 [{selected_room}] 단체방"
    chat_filter = lambda c: c.get("mode") == "group" and c.get("room") == selected_room

# 채팅 이력 표시
st.subheader(chat_title)
for chat in st.session_state.chat_history:
    if chat_filter(chat):
        with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
            if chat["message"]:
                st.markdown(f"**{chat['sender']}**: {chat['message']}")
            if chat["file_path"] and os.path.exists(chat["file_path"]):
                file_name = os.path.basename(chat["file_path"])
                with open(chat["file_path"], "rb") as f:
                    st.download_button(
                        f"📎 {file_name} 다운로드", data=f, file_name=file_name, key=str(uuid.uuid4())
                    )
            st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

# 메시지 입력 및 전송
col1, col2 = st.columns([3, 1])
with col1:
    message = st.text_input("메시지를 입력하세요", key="message_input")
with col2:
    uploaded_file = st.file_uploader("파일", label_visibility="collapsed")

if st.button("전송"):
    saved_path = None
    if uploaded_file:
        file_name = uploaded_file.name
        saved_path = os.path.join(UPLOAD_DIR, file_name)
        with open(saved_path, "wb") as f:
            f.write(uploaded_file.read())

    if message.strip() or saved_path:
        chat = {
            "sender": current_user,
            "message": message.strip() or None,
            "file_path": saved_path,
            "timestamp": datetime.datetime.now(),
        }
        if chat_mode == "1:1 채팅":
            chat.update({"mode": "private", "receiver": receiver, "pair": frozenset([current_user, receiver])})
        else:
            chat.update({"mode": "group", "room": selected_room})

        st.session_state.chat_history.append(chat)
        with open(SAVE_FILE, "wb") as f:
            pickle.dump(st.session_state.chat_history, f)

        st.session_state.message_input = ""
        st.rerun()
    else:
        st.warning("메시지나 파일을 입력하세요.")
