import streamlit as st
import datetime

# 초기 상태 설정
if 'username' not in st.session_state:
    st.session_state.username = None
if 'all_users' not in st.session_state:
    st.session_state.all_users = set()
if 'chats' not in st.session_state:
    st.session_state.chats = {}  # 키: frozenset({user1, user2}), 값: 메시지 리스트

# 로그인 기능
def login():
    username = st.text_input("사용자 이름을 입력하세요", key='username_input')
    if username:
        st.session_state.username = username
        st.session_state.all_users.add(username)
        st.experimental_rerun()

# 메시지 전송 함수
def send_message():
    sender = st.session_state.username
    receiver = st.session_state.receiver
    msg = st.session_state.message_input.strip()

    if not msg:
        return

    chat_key = frozenset({sender, receiver})
    st.session_state.chats.setdefault(chat_key, []).append({
        "sender": sender,
        "text": msg,
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.message_input = ""

# 로그인 화면
if st.session_state.username is None:
    login()
else:
    st.title(f"💬 환영합니다, {st.session_state.username}님!")

    # 사용자 선택
    candidates = sorted(u for u in st.session_state.all_users if u != st.session_state.username)
    if not candidates:
        st.info("다른 사용자가 아직 없습니다. 채팅하려면 다른 사용자가 로그인해야 합니다.")
        st.stop()

    receiver = st.selectbox("메시지를 보낼 사용자 선택", candidates, key="receiver")

    # 메시지 표시
    chat_key = frozenset({st.session_state.username, receiver})
    messages = st.session_state.chats.get(chat_key, [])

    st.subheader(f"📨 {receiver}님과의 대화")
    for msg in messages:
        is_sender = msg["sender"] == st.session_state.username
        prefix = "🟦나" if is_sender else f"🟥{msg['sender']}"
        st.markdown(f"**[{msg['time']}] {prefix}**: {msg['text']}")

    # 메시지 입력창
    st.text_input("메시지를 입력하세요", key="message_input", on_change=send_message)

    # 로그아웃
    if st.button("로그아웃"):
        del st.session_state.username
        st.experimental_rerun()
