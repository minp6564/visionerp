import streamlit as st
import datetime
import os
import uuid
import random
import openai

# 🔐 API Key 설정
openai.api_key = st.secrets["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"]

# 폴더 생성
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

current_user = "이사원"
gpt_bots = ["박과장", "김대리", "정부장"]
group_room = "GPT 단체방"

# 역할 프롬프트
bot_system_prompts = {
    "박과장": "당신은 전략적인 사고와 명확한 지시를 중시하는, 경험 있는 과장입니다.",
    "김대리": "당신은 상사의 지시를 이해하고 실무적으로 반응하는 예의 바른 대리입니다.",
    "정부장": "당신은 책임감 있고 권위 있는 부장입니다. 부드럽지만 단호하게 말하세요.",
}

# GPT 응답 생성 함수
def generate_gpt_reply(bot_name, user_input):
    system_prompt = bot_system_prompts.get(bot_name, "당신은 회사의 사내 직원입니다.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"(GPT 오류: {e})"

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "1:1 채팅"

if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = gpt_bots[0]

# UI 시작
st.title("💬 사내 GPT 채팅 시스템")

chat_mode = st.radio("채팅 모드 선택", ["1:1 채팅", "단체방"], index=0)
st.session_state.chat_mode = chat_mode

# 대상 선택
if chat_mode == "1:1 채팅":
    selected_bot = st.selectbox("대화할 GPT 챗봇 선택", gpt_bots)
    st.session_state.selected_bot = selected_bot
    chat_title = f"🗨️ {selected_bot} 님과의 대화"
    chat_filter = lambda c: c.get("mode") == "private" and c.get("pair") == frozenset([current_user, selected_bot])
else:
    chat_title = f"📢 [{group_room}] 단체방"
    chat_filter = lambda c: c.get("mode") == "group" and c.get("room") == group_room

# 대화 제목
st.subheader(chat_title)

# 대화 내역 출력
for chat in st.session_state.chat_history:
    if chat_filter(chat):
        with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
            st.markdown(f"**{chat['sender']}**: {chat['message']}")
            st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

# 입력창
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("메시지를 입력하세요", key="message_input")
with col2:
    if st.button("전송"):
        if user_input.strip():
            now = datetime.datetime.now()
            chat_log = {
                "sender": current_user,
                "message": user_input.strip(),
                "timestamp": now,
            }

            # 사용자 메시지 저장
            if chat_mode == "1:1 채팅":
                selected_bot = st.session_state.selected_bot
                chat_log.update({
                    "mode": "private",
                    "receiver": selected_bot,
                    "pair": frozenset([current_user, selected_bot])
                })
                st.session_state.chat_history.append(chat_log)

                # GPT 응답
                reply = generate_gpt_reply(selected_bot, user_input)
                st.session_state.chat_history.append({
                    "sender": selected_bot,
                    "message": reply,
                    "timestamp": datetime.datetime.now(),
                    "mode": "private",
                    "receiver": current_user,
                    "pair": frozenset([current_user, selected_bot])
                })

            else:
                chat_log.update({
                    "mode": "group",
                    "room": group_room
                })
                st.session_state.chat_history.append(chat_log)

                for bot in gpt_bots:
                    reply = generate_gpt_reply(bot, user_input)
                    st.session_state.chat_history.append({
                        "sender": bot,
                        "message": reply,
                        "timestamp": datetime.datetime.now(),
                        "mode": "group",
                        "room": group_room
                    })

            st.rerun()
        else:
            st.warning("메시지를 입력하세요.")
