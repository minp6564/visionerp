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

# 채팅 기록 복원 (pickle 열기)
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "rb") as f:
        st.session_state.chat_history = pickle.load(f)
else:
    st.session_state.chat_history = []

if "chat_rooms" not in st.session_state:
    st.session_state.chat_rooms = []  # [{"name": "신제품 TF", "members": ["김대리", "박과장"]}]

# 현재 사용자 선택
current_user = st.selectbox("내 이름을 선택하세요:", [u["name"] for u in users])

# 모드 선택
chat_mode = st.radio("채팅 모드에서 선택:", ["1:1 채팅", "단체방 (자신 생성)"])

# 1:1 채팅명 및 호환 값 설정
if chat_mode == "1:1 채팅":
    receiver_candidates = [u["name"] for u in users if u["name"] != current_user]
    receiver = st.selectbox("채팅할 상당을 선택하세요:", receiver_candidates)
    chat_title = f"📨 {receiver} 님과의 1:1 대화"
    chat_filter = lambda chat: (
        chat.get("mode") == "private"
        and {chat["sender"], chat["receiver"]} == {current_user, receiver}
    )

else:
    # 단체방 생성명
    st.markdown("---")
    with st.expander("➕ 새로운 단체방 만들기"):
        new_room_name = st.text_input("채팅방 이름")
        new_room_members = st.multiselect("채팅방 참가자 선택", [u["name"] for u in users if u["name"] != current_user])
        if st.button("채팅방 생성"):
            if new_room_name.strip() and new_room_members:
                st.session_state.chat_rooms.append({
                    "name": new_room_name.strip(),
                    "members": [current_user] + new_room_members
                })
                st.success(f"'{new_room_name}' 채팅방이 생성되었습니다.")
            else:
                st.warning("방 이름과 참가자를 모두 입력해주세요.")

    # 사용자가 포함된 방 목록
    my_rooms = [r for r in st.session_state.chat_rooms if current_user in r["members"]]
    if my_rooms:
        selected_room = st.selectbox("입장할 방 선택:", [r["name"] for r in my_rooms])
        chat_title = f"📢 [{selected_room}] 단체방"
        chat_filter = lambda chat: (
            chat.get("mode") == "custom_group" and chat["room"] == selected_room
        )
    else:
        st.info("➕ 채팅방을 만들고 입장하세요.")
        st.stop()

# 채팅 보기
st.subheader(chat_title)
for chat in st.session_state.chat_history:
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
                        file_name=file_name
                    )
            st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

st.divider()

# 메시지 + 파일 입력
col1, col2 = st.columns([3, 1])
with col1:
    message = st.text_input("메시지를 입력하세요", key="message_input")
with col2:
    uploaded_file = st.file_uploader("파일", key="file_input", label_visibility="collapsed")

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
            new_chat.update({
                "mode": "private",
                "receiver": receiver
            })
        else:
            new_chat.update({
                "mode": "custom_group",
                "room": selected_room
            })

        st.session_state.chat_history.append(new_chat)

        # pickle에 저장
        with open(SAVE_FILE, "wb") as f:
            pickle.dump(st.session_state.chat_history, f)

        st.experimental_rerun()
    else:
        st.warning("메시지나 파일을 입력해주세요.")
