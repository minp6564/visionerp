import streamlit as st
import datetime
import os

# 📁 파일 저장 폴더 만들기
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 👤 예시 사용자 목록 (연습용)
users = ["김대리", "박과장", "이사원"]

# 📌 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🏷️ 타이틀
st.title("💬 사내 채팅 (1:1 + 파일 공유)")

# 👥 현재 사용자 (로그인 흉내)
current_user = st.selectbox("내 이름을 선택하세요:", users, index=0)

# 🎯 대화 상대 선택
receiver_candidates = [u for u in users if u != current_user]
receiver = st.selectbox("채팅할 상대를 선택하세요:", receiver_candidates)

st.subheader(f"📨 {receiver} 님과의 대화")

# 💬 이전 채팅 내역 보여주기
for chat in st.session_state.chat_history:
    if {chat["sender"], chat["receiver"]} == {current_user, receiver}:
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

    # 파일 저장
    if uploaded_file:
        file_name = uploaded_file.name
        saved_file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(saved_file_path, "wb") as f:
            f.write(uploaded_file.read())

    if message.strip() or saved_file_path:
        st.session_state.chat_history.append({
            "sender": current_user,
            "receiver": receiver,
            "message": message if message.strip() else None,
            "file_path": saved_file_path,
            "timestamp": datetime.datetime.now()
        })
        st.experimental_rerun()
    else:
        st.warning("메시지나 파일 중 하나는 입력해 주세요.")
