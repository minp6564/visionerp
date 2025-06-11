import streamlit as st
import datetime

# 세션 상태 초기화
if 'username' not in st.session_state:
    st.session_state.username = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 사용자 로그인 (단순화)
def login():
    st.session_state.username = st.text_input("사용자 이름을 입력하세요", key='username_input')
    if st.session_state.username:
        st.experimental_rerun()

# 채팅 메시지 추가
def add_message():
    msg = st.session_state.message_input
    if msg:
        st.session_state.messages.append({
            "user": st.session_state.username,
            "text": msg,
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        })
        st.session_state.message_input = ""

# 로그인 인터페이스
if st.session_state.username is None:
    login()
else:
    st.title("💬 사내 채팅 시스템")

    # 메시지 출력
    for msg in st.session_state.messages:
        st.markdown(f"**[{msg['time']}] {msg['user']}**: {msg['text']}")

    # 메시지 입력
    st.text_input("메시지를 입력하세요", key="message_input", on_change=add_message)

    # 파일 업로드
    uploaded_file = st.file_uploader("파일 업로드", type=['png', 'jpg', 'pdf', 'docx'])
    if uploaded_file is not None:
        st.success(f"파일 '{uploaded_file.name}' 업로드 완료됨.")

    # 로그아웃
    if st.button("로그아웃"):
        del st.session_state.username
        st.experimental_rerun()
