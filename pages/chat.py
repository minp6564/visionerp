import streamlit as st
import datetime

# 예시용 사용자 목록 (추후 DB로 대체 가능)
users = ["김대리", "박과장", "이사원"]

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 제목
st.title("💬 사내 채팅")

# 1. 대화 상대 선택
receiver = st.selectbox("채팅할 상대를 선택하세요:", users)

# 2. 채팅 내용 보여주기
st.subheader(f"📨 {receiver} 님과의 대화")

for chat in st.session_state.chat_history:
    if chat["receiver"] == receiver:
        with st.chat_message("user" if chat["sender"] == "나" else "assistant"):
            st.markdown(f"**{chat['sender']}**: {chat['message']}")
            st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

st.divider()

# 3. 메시지 입력 및 전송
message = st.text_input("메시지를 입력하세요", key="message_input")

if st.button("📤 전송"):
    if message.strip():
        st.session_state.chat_history.append({
            "sender": "나",
            "receiver": receiver,
            "message": message,
            "timestamp": datetime.datetime.now()
        })
        st.experimental_rerun()  # 메시지 새로고침
    else:
        st.warning("메시지를 입력해 주세요.")
