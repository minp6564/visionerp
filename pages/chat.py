import streamlit as st
import datetime
import os
import uuid
import random

# 기본 설정
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

current_user = "이사원"
gpt_bots = ["박과장", "김대리", "정부장"]
group_room = "GPT 단체방"

# 프롬프트 (내부용)
bot_prompts = {
    "박과장": "전략적인 사고와 명확한 지시를 중시하는, 경험 있는 과장답게 응답하시오.",
    "김대리": "상사의 지시를 이해하고 실무적으로 응답하는 대리답게 응답하시오. 공손하면서도 실질적인 대화로 이어가시오.",
    "정부장": "업무 전반을 관리하는 부장답게 책임감 있고 신중하며 권위 있는 말투로 응답하시오.",
}

# 예시 응답
bot_replies = {
    "박과장": [
        "좋습니다. 일단 그 방향으로 추진해보죠.",
        "이번 건은 일정이 중요하니, 계획대로 밀고 가도록 하세요.",
        "성과를 낼 수 있도록 팀원들과 조율 바랍니다.",
    ],
    "김대리": [
        "네, 곧 처리해서 보고드리겠습니다!",
        "방금 말씀하신 내용은 확인 후 바로 공유드릴게요.",
        "최대한 꼼꼼히 준비하겠습니다.",
    ],
    "정부장": [
        "그 사안은 조직 전체에 영향을 줄 수 있으니 신중히 접근해야 합니다.",
        "관련 부서와 협의 후 최종 결정하겠습니다.",
        "리스크를 감안하여 대안을 마련해 두는 것이 좋겠습니다.",
    ],
}

# 응답 생성
def generate_gpt_reply(bot_name, user_input):
    return random.choice(bot_replies.get(bot_name, ["네, 확인했습니다."]))

# 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "1:1 채팅"

if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = gpt_bots[0]

# UI
st.title("💼 사내 GPT 채팅")

chat_mode = st.radio("채팅 모드 선택", ["1:1 채팅", "단체방"], index=0)
st.session_state.chat_mode = chat_mode

# 1:1 채팅 대상
if chat_mode == "1:1 채팅":
    selected_bot = st.selectbox("대화 상대 선택", gpt_bots)
    st.session_state.selected_bot = selected_bot
    chat_title = f"🗨️ {selected_bot} 님과의 대화"
    chat_filter = lambda c: c.get("mode") == "private" and c.get("pair") == frozenset([current_user, selected_bot])
else:
    chat_title = f"📢 [{group_room}] 단체방"
    chat_filter = lambda c: c.get("mode") == "group" and c.get("room") == group_room

st.subheader(chat_title)

# 채팅 출력
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

            if chat_mode == "1:1 채팅":
                selected_bot = st.session_state.selected_bot
                chat_log.update({
                    "mode": "private",
                    "receiver": selected_bot,
                    "pair": frozenset([current_user, selected_bot])
                })
                st.session_state.chat_history.append(chat_log)

                reply = generate_gpt_reply(selected_bot, user_input)
                st.session_state.chat_history.append({
                    "sender": selected_bot,
                    "message": reply,
                    "timestamp": datetime.datetime.now(),
                    "mode": "private",
                    "receiver": current_user,
                    "pair": frozenset([current_user, selected_bot])
                })

            else:  # 단체방
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
