import streamlit as st
import datetime
import os

# 📁 파일 저장 폴더
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 👥 사용자 목록
users = [
    {"name": "김대리", "department": "물류팀"},
    {"name": "이사원", "department": "물류팀"},
    {"name": "박과장", "department": "회계팀"},
    {"name": "정부장", "department": "영업팀"},
]

# 부서 목록 추출
departments = sorted(list(set(u["department"] for u in users)))

# 🧠 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🧑 내 사용자 이름 선택
current_user = st.selectbox("내 이름을 선택하세요:", [u["name"] for u in users])
user_info = next(u for u in users if u["name"] == current_user)

# 💬 모드 선택
chat_mode = st.radio("채팅 모드를 선택하세요:", ["1:1 채팅", "부서 단체방"])

# 📌 채팅 대상 정하기
if chat_mode == "1:1 채팅":
    receiver_candidates = [u["name"] for u in users if u["name"] != current_user]
    receiver = st.selectbox("대화할 상대를 선택하세요:", receiver_candidates)
    chat_title = f"📨 {receiver} 님과의 1:1 대화"
    chat_filter = lambda chat: (
        chat.get("mode") == "private"
        and {chat["sender"], chat["receiver"]} == {current_user, receiver}
    )
else:
    dept = user_info["department"]
    chat_title = f"📢 [{dept}] 부서 단체방"
    chat_filter = lambda chat: (
        chat.get("mode") == "group" and chat["room"] == dept
    )

st.subheader(chat_title)

# 📜 채팅 내역 보여주기
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

# ✍️ 메시지 입력 + 📎 파일 업로드
col1, col2 = st.columns([3, 1])
with col1:
    message = st.text_input("메시지를 입력하세요", key="message_input")
with col2:
    uploaded_file = st.file_uploader("파일", key="file_input", label_visibility="collapsed")

# 📤 전송 버튼
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
                "mode": "group",
                "room": user_info["department"]
            })

        st.session_state.chat_history.append(new_chat)
        st.experimental_rerun()
    else:
        st.warning("메시지나 파일 중 하나는 입력해 주세요.")
